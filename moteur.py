"""
moteur.py — Noyau commun de la plateforme d'exercices de mathématiques appliquées.

Principe de conception
----------------------
Un exercice = un générateur aléatoire qui renvoie un objet `Exercice` contenant :
  - un énoncé instancié sur des paramètres tirés au hasard ;
  - LA réponse attendue (numérique ou symbolique) ;
  - la liste ORDONNÉE des étapes de la méthode, reconstruites sur ces mêmes
    paramètres (jamais un corrigé statique) ;
  - une liste de « pièges » : les valeurs qu'obtient un étudiant qui commet
    une erreur classique, associées au diagnostic correspondant.

À la validation, la plateforme affiche TOUJOURS la méthode complète, que la
réponse soit juste ou fausse. Si la réponse correspond à un piège, le
diagnostic de l'erreur est affiché en premier.

Convention des étapes : Identifier → Calculer → Vérifier → Interpréter.
"""

import random
import re

from dataclasses import dataclass, field
from typing import Any, Callable, List, Optional, Tuple

import streamlit as st
import sympy as sp
from sympy.parsing.sympy_parser import (
    parse_expr,
    standard_transformations,
    implicit_multiplication_application,
    convert_xor,
)

TRANSFORMATIONS = standard_transformations + (
    implicit_multiplication_application,
    convert_xor,
)

# --------------------------------------------------------------------------
# Structures de données
# --------------------------------------------------------------------------


@dataclass
class Etape:
    """Une étape de la méthode. `titre` suit le gabarit Identifier/Calculer/…"""

    titre: str
    contenu: str = ""
    latex: Optional[str] = None


@dataclass
class Exercice:
    enonce: str
    reponse: Any
    etapes: List[Etape]
    type_reponse: str = "num"  # "num" | "sym" | "qcm"
    forme: str = ""  # "factorisee" : exige une réponse effectivement factorisée
    options: List[str] = field(default_factory=list)  # pour les QCM
    libelle: str = "Votre réponse"
    unite: str = ""
    tolerance: float = 0.005  # tolérance RELATIVE
    tolerance_abs: float = 0.0  # tolérance ABSOLUE (prioritaire si > 0)
    pieges: List[Tuple[Any, str]] = field(default_factory=list)
    indice: str = ""
    symboles: List[str] = field(default_factory=list)
    reponse_affichee: str = ""  # rendu LaTeX de la réponse (facultatif)


# --------------------------------------------------------------------------
# Comparaison des réponses
# --------------------------------------------------------------------------


def _marge(ex: "Exercice") -> float:
    """Demi-largeur de la fenêtre d'acceptation autour de la bonne réponse."""
    if ex.tolerance_abs > 0:
        return ex.tolerance_abs
    return max(ex.tolerance * abs(float(ex.reponse)), 1e-9)


def analyser_numerique(ex: Exercice, valeur: float) -> Tuple[bool, str]:
    """Renvoie (juste, diagnostic)."""
    marge = _marge(ex)
    if abs(valeur - float(ex.reponse)) <= marge:
        return True, ""
    for val_piege, message in ex.pieges:
        # Garde-fou : on ne diagnostique un piège que s'il est nettement
        # distinct de la bonne réponse, sinon le message serait trompeur.
        if abs(float(val_piege) - float(ex.reponse)) < 2 * marge:
            continue
        if abs(valeur - float(val_piege)) <= marge:
            return False, message
    return False, ""


def parser_nombre(texte) -> Optional[float]:
    """Lit un nombre saisi par un étudiant. Renvoie None si illisible.

    `st.number_input` délègue la lecture au navigateur, dont la locale décide
    du séparateur décimal : sur un poste réglé en français, un « 12.5 » tapé
    avec un point était rejeté. On lit donc un champ texte et l'on accepte
    indifféremment la virgule et le point, les espaces de milliers, un signe
    moins typographique, et une unité collée à la fin (« 12,5 % », « 85 M€ »).
    """
    if texte is None:
        return None
    texte = str(texte).strip()
    for espace in ("\u202f", "\u00a0", " "):
        texte = texte.replace(espace, "")
    texte = texte.replace("\u2212", "-").replace("\u2013", "-")
    correspondance = re.match(r"^[+-]?(?:[0-9][0-9.,]*|[.,][0-9]+)", texte)
    if not correspondance:
        return None
    nombre = correspondance.group(0)
    # Ce qui suit le nombre ne peut être qu'une unité (« % », « M€ », « ans ») :
    # un chiffre ou un opérateur signale une expression, pas un nombre.
    if re.search(r"[0-9+*/^=()-]", texte[correspondance.end():]):
        return None
    if "," in nombre and "." in nombre:
        # Les deux présents : le dernier est la décimale, l'autre sépare les
        # milliers (« 1.234,5 » ou « 1,234.5 »).
        decimale = "," if nombre.rfind(",") > nombre.rfind(".") else "."
        milliers = "." if decimale == "," else ","
        nombre = nombre.replace(milliers, "").replace(decimale, ".")
    elif nombre.count(",") > 1:
        nombre = nombre.replace(",", "")  # « 1,234,567 » : milliers
    elif nombre.count(".") > 1:
        nombre = nombre.replace(".", "")  # « 1.234.567 » : milliers
    else:
        nombre = nombre.replace(",", ".")
    try:
        return float(nombre)
    except ValueError:
        return None


def parser(texte: str, symboles: List[str]):
    """Parse une saisie étudiante en expression SymPy. Renvoie None si invalide.

    `e` et `ln` sont ajoutés au dictionnaire local : un étudiant qui écrit
    `e^x` ou `ln(x)` écrit ce que le cours lui a appris, et sa réponse doit
    être acceptée au même titre que `exp(x)` ou `log(x)`.
    """
    local = {s: sp.Symbol(s) for s in symboles}
    local.setdefault("e", sp.E)
    local.setdefault("ln", sp.log)
    texte = texte.strip().replace(",", ".").replace("÷", "/").replace("×", "*")
    if not texte:
        return None
    try:
        return parse_expr(texte, local_dict=local, transformations=TRANSFORMATIONS)
    except Exception:
        return None


def _est_factorisee(expr) -> bool:
    """Une expression factorisée est un produit ou une puissance au niveau le plus haut."""
    return bool(expr.is_Mul or expr.is_Pow)


def analyser_symbolique(ex: Exercice, texte: str) -> Tuple[Optional[bool], str]:
    """Renvoie (juste, diagnostic). `juste = None` si la saisie est illisible."""
    expr = parser(texte, ex.symboles)
    if expr is None:
        return None, ""
    try:
        if sp.simplify(sp.together(expr - ex.reponse)) == 0:
            if ex.forme == "factorisee" and not _est_factorisee(expr):
                return False, (
                    "Votre expression est **mathématiquement juste**, mais elle n'est "
                    "pas **factorisée** : elle est encore écrite comme une somme. "
                    "Factoriser, c'est écrire l'expression sous forme de **produit**."
                )
            return True, ""
    except Exception:
        return None, ""
    for expr_piege, message in ex.pieges:
        try:
            # Garde-fou : un piège équivalent à la bonne réponse n'est jamais
            # diagnostiqué (le test de justesse a déjà tranché au-dessus).
            if sp.simplify(sp.together(expr_piege - ex.reponse)) == 0:
                continue
            if sp.simplify(sp.together(expr - expr_piege)) == 0:
                return False, message
        except Exception:
            continue
    return False, ""


# --------------------------------------------------------------------------
# Affichage
# --------------------------------------------------------------------------


def afficher_methode(ex: Exercice) -> None:
    """Affiche la méthode complète, étape par étape. Toujours appelée."""
    st.markdown("#### 🧭 La méthode, étape par étape")
    for i, etape in enumerate(ex.etapes, start=1):
        with st.container(border=True):
            st.markdown(f"**{i}. {etape.titre}**")
            if etape.contenu:
                st.markdown(etape.contenu)
            if etape.latex:
                st.latex(etape.latex)


def _reponse_lisible(ex: Exercice) -> str:
    if ex.reponse_affichee:
        return ex.reponse_affichee
    if ex.type_reponse == "sym":
        return f"${sp.latex(ex.reponse)}$"
    valeur = float(ex.reponse)
    if abs(valeur - round(valeur)) < 1e-9:
        texte = f"{round(valeur):,}".replace(",", "\u202f")
    else:
        texte = f"{valeur:,.2f}".replace(",", "\u202f").replace(".", ",")
    if ex.unite:
        texte += f" {ex.unite}"
    return f"**{texte}**"


def executer(cle: str, generateur: Callable[[], Exercice]) -> None:
    """Cycle complet d'un exercice : énoncé → saisie → verdict → méthode."""
    k_ex, k_fait, k_saisie = f"{cle}_ex", f"{cle}_fait", f"{cle}_saisie"

    if k_ex not in st.session_state:
        st.session_state[k_ex] = generateur()
        st.session_state[k_fait] = False
        st.session_state[k_saisie] = None

    ex: Exercice = st.session_state[k_ex]

    st.markdown(ex.enonce)

    if ex.indice:
        with st.expander("💡 Un indice (sans la réponse)"):
            st.markdown(ex.indice)

    colonne_saisie, colonne_boutons = st.columns([2, 1])

    with colonne_saisie:
        if ex.type_reponse == "num":
            # Champ texte et non `number_input` : ce dernier laisse le navigateur
            # décider du séparateur décimal, et refuse le point sur un poste
            # réglé en français. Ici, virgule et point sont acceptés.
            saisie = st.text_input(
                f"{ex.libelle} {('(' + ex.unite + ')') if ex.unite else ''}",
                key=f"{cle}_input",
                disabled=st.session_state[k_fait],
                placeholder="Saisissez un nombre — virgule ou point, au choix",
            )
        elif ex.type_reponse == "qcm":
            saisie = st.radio(
                ex.libelle,
                ex.options,
                index=None,
                key=f"{cle}_input",
                disabled=st.session_state[k_fait],
            )
        else:
            saisie = st.text_input(
                ex.libelle,
                key=f"{cle}_input",
                disabled=st.session_state[k_fait],
                placeholder="Par exemple : 5x/6",
            )
            st.caption(
                "Syntaxe : `5x/6`, `(a+b)/c`, `x^2` ou `x**2`, `e^x` ou `exp(x)`, "
                "`ln(x)`. Les écritures équivalentes sont acceptées."
            )

    with colonne_boutons:
        st.write("")
        st.write("")
        if not st.session_state[k_fait]:
            if st.button("✅ Valider", key=f"{cle}_valider", type="primary"):
                st.session_state[k_saisie] = saisie
                st.session_state[k_fait] = True
                st.rerun()
        else:
            if st.button("🔄 Nouvel énoncé", key=f"{cle}_nouveau"):
                for k in (k_ex, k_fait, k_saisie, f"{cle}_input"):
                    st.session_state.pop(k, None)
                st.rerun()

    if not st.session_state[k_fait]:
        return

    saisie = st.session_state[k_saisie]
    st.markdown("---")

    if saisie is None or (isinstance(saisie, str) and not saisie.strip()):
        st.warning("Aucune réponse saisie. La méthode complète est ci-dessous.")
    elif ex.type_reponse == "qcm":
        if str(saisie).strip() == str(ex.reponse).strip():
            st.success("✅ Bonne réponse. Lisez la méthode : c'est elle qui est évaluée.")
        else:
            diag = ""
            for option, message in ex.pieges:
                if str(saisie).strip() == str(option).strip():
                    diag = message
            st.error(f"❌ Réponse attendue : **{ex.reponse}**")
            if diag:
                st.warning(f"🔍 **Diagnostic :** {diag}")
    elif ex.type_reponse == "num" and parser_nombre(saisie) is None:
        st.warning(
            "Nombre illisible (lettres, symbole inattendu ?). Écrivez par exemple "
            "`12,5` ou `12.5`. Ce n'est pas compté comme une erreur — voici la "
            "méthode."
        )
    elif ex.type_reponse == "num":
        juste, diagnostic = analyser_numerique(ex, parser_nombre(saisie))
        if juste:
            st.success(
                f"✅ Correct : {_reponse_lisible(ex)}. "
                "Lisez quand même la méthode : c'est elle qui est évaluée."
            )
        elif diagnostic:
            st.error(f"❌ Ce n'est pas la bonne valeur — et l'écart est instructif.")
            st.warning(f"🔍 **Diagnostic :** {diagnostic}")
        else:
            st.error(f"❌ Réponse attendue : {_reponse_lisible(ex)}")
    else:
        juste, diagnostic = analyser_symbolique(ex, str(saisie))
        if juste is None:
            st.warning(
                "Expression illisible (parenthèse manquante ? symbole inattendu ?). "
                "Ce n'est pas compté comme une erreur — voici la méthode."
            )
        elif juste:
            st.success(
                f"✅ Correct : {_reponse_lisible(ex)}. "
                "Lisez quand même la méthode : c'est elle qui est évaluée."
            )
        elif diagnostic:
            st.error("❌ Ce n'est pas l'expression attendue — et l'erreur est classique.")
            st.warning(f"🔍 **Diagnostic :** {diagnostic}")
        else:
            st.error(f"❌ Réponse attendue : {_reponse_lisible(ex)}")

    st.markdown("")
    afficher_methode(ex)


# --------------------------------------------------------------------------
# Famille « vrai ou faux + contre-exemple »
# --------------------------------------------------------------------------


def executer_vrai_faux(cle: str, regles: List[dict]) -> None:
    """Cycle complet d'un item « cette règle est-elle vraie ? ».

    `regles` est une liste de dictionnaires comportant les clés :
      - latex        : l'égalité à juger, en LaTeX ;
      - vraie        : True si la règle est valable pour tous les nombres ;
      - gauche/droite: deux fonctions (a, b) -> float évaluant chaque membre ;
      - explication  : le verdict argumenté, affiché dans la correction.

    Quand la règle est fausse, l'étudiant doit produire un contre-exemple :
    la plateforme évalue les deux membres sur ses valeurs et confirme — ou non
    — que la règle est bien mise en défaut.
    """
    k_regle, k_fait = f"{cle}_r", f"{cle}_fait"

    if k_regle not in st.session_state:
        st.session_state[k_regle] = random.choice(regles)
        st.session_state[k_fait] = False

    regle = st.session_state[k_regle]

    st.markdown(
        "> La règle suivante est-elle **vraie pour tous les nombres**, "
        "ou **fausse** ?\n>\n"
        f"> $$ {regle['latex']} $$\n>\n"
        "> Si vous la jugez fausse, il ne suffit pas de le dire : "
        "**produisez un contre-exemple**, c'est-à-dire deux nombres qui la "
        "mettent en défaut."
    )

    colonne_gauche, colonne_droite = st.columns([1, 1])

    with colonne_gauche:
        st.radio(
            "Cette règle est :",
            ["Vraie pour tous les nombres", "Fausse"],
            index=None,
            key=f"{cle}_verdict",
            disabled=st.session_state[k_fait],
        )
    with colonne_droite:
        st.caption("Si vous répondez « Fausse », proposez un contre-exemple :")
        st.text_input(
            "a =", value="1", key=f"{cle}_a",
            disabled=st.session_state[k_fait],
        )
        st.text_input(
            "b =", value="1", key=f"{cle}_b",
            disabled=st.session_state[k_fait],
        )

    if not st.session_state[k_fait]:
        if st.button("✅ Valider", key=f"{cle}_valider", type="primary"):
            st.session_state[k_fait] = True
            st.rerun()
        return

    if st.button("🔄 Nouvelle règle", key=f"{cle}_nouveau"):
        for k in [c for c in st.session_state.keys() if c.startswith(cle)]:
            st.session_state.pop(k, None)
        st.rerun()

    st.markdown("---")

    verdict = st.session_state.get(f"{cle}_verdict")
    val_a = parser_nombre(st.session_state.get(f"{cle}_a", "1"))
    val_b = parser_nombre(st.session_state.get(f"{cle}_b", "1"))
    dit_vraie = verdict == "Vraie pour tous les nombres"

    if verdict is None:
        st.warning("Aucun verdict donné. Voici la correction.")
    elif dit_vraie == regle["vraie"]:
        st.success(
            "✅ Verdict correct : cette règle est bien "
            f"**{'vraie' if regle['vraie'] else 'fausse'}**."
        )
    else:
        st.error(
            "❌ Verdict incorrect : cette règle est en réalité "
            f"**{'vraie' if regle['vraie'] else 'fausse'}**."
        )

    # Test du contre-exemple proposé
    if not regle["vraie"] and verdict == "Fausse" and (val_a is None or val_b is None):
        st.markdown("#### 🔬 Test de votre contre-exemple")
        st.warning(
            "Une des deux valeurs est illisible : écrivez un nombre, avec une "
            "virgule ou un point pour la décimale."
        )
    elif not regle["vraie"] and verdict == "Fausse":
        st.markdown("#### 🔬 Test de votre contre-exemple")
        try:
            g = regle["gauche"](val_a, val_b)
            d = regle["droite"](val_a, val_b)
            colonne_1, colonne_2 = st.columns(2)
            colonne_1.metric("Membre de gauche", f"{g:.4f}")
            colonne_2.metric("Membre de droite", f"{d:.4f}")
            if abs(g - d) > 1e-9:
                st.success(
                    f"✅ Contre-exemple **valide** : avec a = {val_a:g} et "
                    f"b = {val_b:g}, les deux membres diffèrent. Une seule "
                    "valeur suffit à démolir une règle prétendument générale — "
                    "c'est la méthode qu'il faut retenir."
                )
            else:
                st.warning(
                    "⚠️ Avec ces valeurs, les deux membres coïncident : ce n'est "
                    "donc **pas** un contre-exemple, même si la règle est fausse. "
                    "Essayez d'autres nombres — évitez 0, et méfiez-vous des cas "
                    "trop symétriques."
                )
        except (ZeroDivisionError, ValueError, TypeError):
            st.warning(
                "⚠️ Ces valeurs rendent l'expression indéfinie (division par zéro "
                "ou racine d'un négatif). Un contre-exemple doit rester **dans le "
                "domaine de validité**, sinon il ne prouve rien."
            )

    st.markdown("")
    st.markdown("#### 🧭 La méthode, étape par étape")
    for titre, contenu in [
        (
            "Identifier — de quel type d'énoncé s'agit-il ?",
            "Une règle du type « pour tous $a$, $b$ » est une affirmation "
            "**universelle**. Deux régimes de preuve, radicalement asymétriques :\n\n"
            "- pour la **réfuter** : un seul contre-exemple suffit ;\n"
            "- pour la **prouver** : aucun nombre d'exemples ne suffit, il faut "
            "une démonstration générale.",
        ),
        (
            "Calculer — tester les valeurs les plus simples",
            "Commencez par $a = b = 1$, puis $a = 1, b = 2$. Évitez $0$ (souvent "
            "hors domaine) et méfiez-vous des cas trop symétriques, qui peuvent "
            "coïncider par accident.",
        ),
        ("Vérifier — le verdict sur cette règle", regle["explication"]),
        (
            "Interpréter — ce que cela vous coûte à l'examen",
            "Ces erreurs ne sont pas des étourderies : elles reviennent parce "
            "qu'on suppose implicitement que toute opération « se distribue ». "
            "Le réflexe à installer est de **tester avant d'écrire**, en cinq "
            "secondes, dès qu'une règle paraît trop commode.",
        ),
    ]:
        with st.container(border=True):
            st.markdown(f"**{titre}**")
            st.markdown(contenu)
