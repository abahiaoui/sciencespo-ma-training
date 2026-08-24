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
    type_reponse: str = "num"  # "num" | "sym"
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


def parser(texte: str, symboles: List[str]):
    """Parse une saisie étudiante en expression SymPy. Renvoie None si invalide."""
    local = {s: sp.Symbol(s) for s in symboles}
    texte = texte.strip().replace(",", ".").replace("÷", "/").replace("×", "*")
    if not texte:
        return None
    try:
        return parse_expr(texte, local_dict=local, transformations=TRANSFORMATIONS)
    except Exception:
        return None


def analyser_symbolique(ex: Exercice, texte: str) -> Tuple[Optional[bool], str]:
    """Renvoie (juste, diagnostic). `juste = None` si la saisie est illisible."""
    expr = parser(texte, ex.symboles)
    if expr is None:
        return None, ""
    try:
        if sp.simplify(sp.together(expr - ex.reponse)) == 0:
            return True, ""
    except Exception:
        return None, ""
    for expr_piege, message in ex.pieges:
        try:
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
            saisie = st.number_input(
                f"{ex.libelle} {('(' + ex.unite + ')') if ex.unite else ''}",
                value=None,
                step=None,
                format="%.4f",
                key=f"{cle}_input",
                disabled=st.session_state[k_fait],
                placeholder="Saisissez un nombre",
            )
        else:
            saisie = st.text_input(
                ex.libelle,
                key=f"{cle}_input",
                disabled=st.session_state[k_fait],
                placeholder="Par exemple : 5x/6",
            )
            st.caption(
                "Syntaxe : `5x/6`, `(a+b)/c`, `x^2` ou `x**2`. "
                "Les écritures équivalentes sont acceptées."
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
    elif ex.type_reponse == "num":
        juste, diagnostic = analyser_numerique(ex, float(saisie))
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
