"""Série S8 — Optimisation : maximiser un profit, minimiser un coût moyen."""

import random

import streamlit as st
import sympy as sp

from moteur import Etape, Exercice, executer

st.set_page_config(page_title="S8 | Optimisation", page_icon="🎯", layout="wide")

q = sp.Symbol("q")

st.title("🎯 S8 — Optimisation")

with st.expander("📖 Contexte & objectifs", expanded=True):
    st.markdown(
        """
### 🎯 Ce que cette série entraîne
Construire une fonction objectif à partir d'un énoncé, la **maximiser** ou la
**minimiser**, vérifier qu'on a bien affaire à l'extremum attendu, et interpréter le
résultat en termes de décision.

### 🧠 La méthode, en quatre temps
1. Écrire la fonction à optimiser. 2. La dériver et annuler la dérivée.
3. **Vérifier** la nature de l'extremum, par le signe de $f''$ ou par le sens de
variation. 4. Revenir à la question posée — qui demande parfois la quantité, parfois
la valeur optimale, parfois les deux.

L'étape 3 est celle qu'on saute, et c'est celle qui coûte des points.
"""
    )

with st.sidebar:
    st.header("📝 Aide-mémoire — Séance 8")
    st.markdown("**Profit**")
    st.latex(r"B(q) = R(q) - C(q) = p\,q - C(q)")
    st.markdown("**Condition du premier ordre**")
    st.latex(r"B'(q) = 0 \iff R'(q) = C'(q)")
    st.markdown("Recette marginale = coût marginal.")
    st.markdown("**Condition du second ordre**")
    st.latex(r"B''(q) < 0 \;\Rightarrow\; \text{maximum}")
    st.latex(r"B''(q) > 0 \;\Rightarrow\; \text{minimum}")
    st.error(
        "**L'erreur interdite**\n\n"
        "Conclure « maximum » sans vérifier le second ordre ni le changement "
        "de signe de la dérivée."
    )

ATELIERS = [
    ("l'atelier de réparation", "réparations"),
    ("le service de restauration", "repas"),
    ("le centre de tri", "lots traités"),
]


def _fr(v, n=2):
    return f"{v:,.{n}f}".replace(",", "\u202f").replace(".", ",")


# --- 1. Quantité qui maximise le profit ------------------------------------


def gen_quantite_optimale() -> Exercice:
    atelier, unite = random.choice(ATELIERS)
    prix = random.choice([100, 120, 150])
    alpha = random.choice([1, 2])  # coefficient quadratique du coût
    beta = random.choice([20, 30, 40])
    fixe = random.choice([500, 800, 1200])
    # C(q) = alpha q^2 + beta q + fixe ; B(q) = prix q - C(q)
    C = alpha * q**2 + beta * q + fixe
    B = sp.expand(prix * q - C)
    Bp = sp.diff(B, q)
    sol = sp.solve(Bp, q)[0]
    reponse = float(sol)

    enonce = f"""
> Pour **{atelier}**, le coût total de production de $q$ {unite} est
>
> $$ C(q) = {sp.latex(C)} \\qquad \\text{{(en euros)}} $$
>
> Chaque unité est facturée **{prix} €**.
>
> Quelle quantité $q$ **maximise le bénéfice** ?
"""

    etapes = [
        Etape(
            "Identifier — écrire la fonction à optimiser",
            "Le bénéfice est la recette moins le coût. La recette vaut le prix "
            "multiplié par la quantité. C'est cette construction, et non le calcul "
            "de dérivée, qui est le vrai travail de l'exercice.",
            rf"B(q) = {prix}q - ({sp.latex(C)}) = {sp.latex(B)}",
        ),
        Etape(
            "Calculer — annuler la dérivée",
            "La condition du premier ordre s'écrit $B'(q) = 0$, ce qui revient à "
            "égaliser la recette marginale et le coût marginal.",
            rf"B'(q) = {sp.latex(Bp)} = 0 \iff q = {sp.latex(sol)} "
            rf"\approx {reponse:.2f}",
        ),
        Etape(
            "Vérifier — est-ce bien un maximum ?",
            f"$B''(q) = {sp.latex(sp.diff(B, q, 2))}$, strictement **négatif** : la "
            "fonction est concave partout, donc le point critique est bien un "
            "maximum — et il est global, pas seulement local. "
            "Sans cette vérification, la réponse est incomplète.",
        ),
        Etape(
            "Interpréter — la lecture marginale",
            f"Produire au-delà de {reponse:.1f} {unite} reste possible, mais chaque "
            f"unité supplémentaire coûte alors plus de {prix} € à produire : elle "
            "détruit du bénéfice. La décision ne se lit pas sur le coût total, qui "
            "augmente toujours, mais sur le **coût marginal** comparé au prix.",
        ),
    ]

    return Exercice(
        enonce=enonce,
        reponse=reponse,
        etapes=etapes,
        libelle=f"Quantité optimale ({unite})",
        tolerance=0.005,
        indice="Écrivez le bénéfice, dérivez-le, annulez la dérivée.",
        pieges=[
            (float(sp.solve(sp.diff(C, q), q)[0]) if sp.solve(sp.diff(C, q), q) else 0.0,
             "Vous avez annulé la dérivée du **coût**, pas celle du bénéfice. "
             "Minimiser le coût n'est pas maximiser le profit — sauf à ne rien "
             "produire du tout."),
            (float(prix),
             "Vous avez donné le prix unitaire, pas une quantité. "
             "Vérifiez toujours l'unité de votre réponse."),
        ],
    )


# --- 2. Valeur du bénéfice maximal -----------------------------------------


def gen_benefice_maximal() -> Exercice:
    atelier, unite = random.choice(ATELIERS)
    prix = 100
    alpha = random.choice([1, 2])
    sol = random.choice([10, 15, 20, 25])
    beta = prix - 2 * alpha * sol
    fixe = random.choice([200, 400, 600])
    C = alpha * q**2 + beta * q + fixe
    B = sp.expand(prix * q - C)
    reponse = float(B.subs(q, sol))

    enonce = f"""
> Pour **{atelier}**, le coût total s'écrit
>
> $$ C(q) = {sp.latex(C)} $$
>
> et chaque unité est facturée **{prix} €**. On sait que le bénéfice est maximal
> pour $q = {sol}$ {unite}.
>
> Quel est le **montant du bénéfice maximal** ?
"""

    etapes = [
        Etape(
            "Identifier — deux questions distinctes",
            "La quantité optimale est donnée. On demande maintenant **combien** on "
            "gagne au mieux : il faut donc revenir à la fonction bénéfice et l'évaluer "
            "en ce point. C'est l'étape 4 de la méthode, celle qu'on oublie.",
        ),
        Etape(
            "Écrire le bénéfice",
            "",
            rf"B(q) = {prix}q - ({sp.latex(C)}) = {sp.latex(B)}",
        ),
        Etape(
            "Évaluer au point optimal",
            "",
            rf"B({sol}) = {sp.latex(B.subs(q, sol))} = {reponse:.0f}\ \text{{€}}",
        ),
        Etape(
            "Vérifier — comparer avec un voisin",
            f"$B({sol - 5}) = {float(B.subs(q, sol-5)):.0f}$ € et "
            f"$B({sol + 5}) = {float(B.subs(q, sol+5)):.0f}$ €, tous deux inférieurs "
            f"à {reponse:.0f} €. ✓ Le point est bien un maximum.",
        ),
        Etape(
            "Interpréter",
            f"Le bénéfice maximal atteint **{reponse:.0f} €**"
            + (
                ". Notez qu'il reste positif : l'activité est viable."
                if reponse > 0 else
                ". Il est **négatif** : même à l'optimum, l'activité ne couvre pas "
                "ses coûts. Optimiser ne garantit pas la rentabilité — cela garantit "
                "seulement qu'on fait au mieux avec les paramètres donnés, ce qui "
                "est une information utile pour un service public."
            ),
        ),
    ]

    return Exercice(
        enonce=enonce,
        reponse=reponse,
        etapes=etapes,
        libelle="Bénéfice maximal",
        unite="€",
        tolerance=1e-6,
        indice="Remplacez $q$ par la quantité optimale dans la fonction bénéfice.",
        pieges=[
            (float(sol),
             "Vous avez redonné la quantité optimale. La question porte sur le "
             "**montant** du bénéfice."),
            (float(prix * sol),
             "C'est la **recette**, pas le bénéfice : il reste à retrancher le coût."),
            (float(C.subs(q, sol)),
             "C'est le **coût** au point optimal, pas le bénéfice."),
        ],
    )


# --- 3. Minimiser le coût moyen ---------------------------------------------


def gen_cout_moyen_minimal() -> Exercice:
    atelier, unite = random.choice(ATELIERS)
    alpha = random.choice([1, 2, 4])
    sol = random.choice([10, 15, 20, 30])
    fixe = alpha * sol**2  # CM(q) = alpha q + fixe/q + beta ; minimum en sqrt(fixe/alpha)
    beta = random.choice([10, 25, 40])
    reponse = float(sol)

    enonce = f"""
> Pour **{atelier}**, le coût total de $q$ {unite} vaut
>
> $$ C(q) = {alpha}q^2 + {beta}q + {fixe} $$
>
> Le coût **moyen** par unité est $CM(q) = \\dfrac{{C(q)}}{{q}}$.
>
> Pour quelle quantité le coût moyen est-il **minimal** ?
"""

    CM = alpha * q + beta + sp.Rational(fixe, 1) / q
    CMp = sp.diff(CM, q)

    etapes = [
        Etape(
            "Identifier — écrire le coût moyen sous forme exploitable",
            "On divise chaque terme par $q$. La forme obtenue met en évidence les deux "
            "forces en présence : un terme croissant et un terme décroissant.",
            rf"CM(q) = \frac{{{alpha}q^2 + {beta}q + {fixe}}}{{q}} = "
            rf"{alpha}q + {beta} + \frac{{{fixe}}}{{q}}",
        ),
        Etape(
            "Dériver et annuler",
            f"La dérivée de $\\frac{{{fixe}}}{{q}}$ est $-\\frac{{{fixe}}}{{q^2}}$. "
            "Le terme constant disparaît.",
            rf"CM'(q) = {alpha} - \frac{{{fixe}}}{{q^2}} = 0 "
            rf"\iff q^2 = \frac{{{fixe}}}{{{alpha}}} = {fixe//alpha} "
            rf"\iff q = {sol}",
        ),
        Etape(
            "Vérifier — minimum et non maximum",
            f"Pour $q < {sol}$, le terme $\\frac{{{fixe}}}{{q^2}}$ l'emporte et $CM'$ "
            f"est négative ; pour $q > {sol}$, elle devient positive. La dérivée passe "
            "du négatif au positif : c'est bien un **minimum**. "
            f"(On écarte la racine négative, une quantité ne pouvant l'être.)",
        ),
        Etape(
            "Interpréter — l'arbitrage qui produit l'optimum",
            f"Deux effets s'opposent : répartir le coût fixe pousse à produire "
            "davantage, mais le coût unitaire croissant pousse à produire moins. "
            f"Le minimum, à {sol} {unite}, est le point d'équilibre entre les deux. "
            "C'est la structure de tout problème d'optimisation appliqué : deux forces "
            "contraires, et un point où elles se compensent.",
        ),
    ]

    return Exercice(
        enonce=enonce,
        reponse=reponse,
        etapes=etapes,
        libelle=f"Quantité optimale ({unite})",
        tolerance=0.005,
        indice="Écrivez $CM(q)$ terme à terme avant de dériver.",
        pieges=[
            (float(fixe) / alpha,
             "Vous avez oublié la racine carrée : l'équation donne $q^2$, pas $q$."),
            (float(sp.solve(sp.diff(alpha*q**2 + beta*q + fixe, q), q)[0]),
             "Vous avez minimisé le coût **total**, qui est croissant et n'a pas de "
             "minimum pour $q > 0$. C'est le coût **moyen** qu'il fallait étudier."),
        ],
    )


# --- 4. La condition du second ordre (QCM) ---------------------------------


def gen_second_ordre() -> Exercice:
    a = random.choice([-3, -2, -1, 1, 2, 3])
    q0 = random.choice([5, 10, 20])
    signe_seconde = 2 * a

    if signe_seconde < 0:
        bonne = f"Il s'agit d'un maximum, car f''({q0}) < 0"
    else:
        bonne = f"Il s'agit d'un minimum, car f''({q0}) > 0"

    options = [
        f"Il s'agit d'un maximum, car f''({q0}) < 0",
        f"Il s'agit d'un minimum, car f''({q0}) > 0",
        f"On ne peut pas conclure : f'({q0}) = 0 ne suffit jamais",
        f"Il s'agit d'un point d'inflexion",
    ]

    enonce = f"""
> Une fonction objectif $f$ vérifie
>
> $$ f'({q0}) = 0 \\qquad \\text{{et}} \\qquad f''(q) = {signe_seconde}
>    \\ \\text{{pour tout }} q $$
>
> Que peut-on conclure au point $q = {q0}$ ?
"""

    etapes = [
        Etape(
            "Identifier — deux conditions, deux rôles",
            "La condition du **premier ordre** ($f' = 0$) localise le point critique. "
            "La condition du **second ordre** (signe de $f''$) en détermine la nature. "
            "La première seule ne permet jamais de conclure.",
        ),
        Etape(
            "Lire le signe de la dérivée seconde",
            f"$f''(q) = {signe_seconde}$, constante et "
            f"**{'négative' if signe_seconde < 0 else 'positive'}** : la fonction est "
            f"{'concave' if signe_seconde < 0 else 'convexe'} sur tout son domaine.",
        ),
        Etape(
            "Vérifier — le caractère global",
            f"Comme $f''$ garde le même signe **partout**, l'extremum n'est pas "
            "seulement local : c'est un extremum **global**. C'est une information "
            "forte, et elle n'est disponible que grâce au second ordre.",
        ),
        Etape(
            "Interpréter — pourquoi on ne peut pas s'en dispenser",
            "Sans cette vérification, on ne distingue pas un maximum d'un minimum — "
            "ni de l'un ni de l'autre, comme pour $f(x) = x^3$ en $0$, où la dérivée "
            "s'annule sans qu'il y ait d'extremum. En décision publique, confondre un "
            "point de coût minimal avec un point de coût maximal n'est pas une nuance.",
        ),
    ]

    return Exercice(
        enonce=enonce,
        reponse=bonne,
        etapes=etapes,
        type_reponse="qcm",
        options=options,
        libelle="Conclusion",
        indice="Quel est le signe de la dérivée seconde ?",
        pieges=[
            (f"On ne peut pas conclure : f'({q0}) = 0 ne suffit jamais",
             "C'est vrai que $f'= 0$ ne suffit pas — mais ici on dispose **aussi** du "
             "signe de $f''$, qui permet précisément de trancher."),
            (f"Il s'agit d'un point d'inflexion",
             "Un point d'inflexion suppose que $f''$ **s'annule et change de signe**. "
             f"Ici $f''$ vaut ${signe_seconde}$ partout : elle ne s'annule jamais."),
            (f"Il s'agit d'un minimum, car f''({q0}) > 0" if signe_seconde < 0
             else f"Il s'agit d'un maximum, car f''({q0}) < 0",
             f"Relisez le signe : $f'' = {signe_seconde}$, donc "
             f"{'négative' if signe_seconde < 0 else 'positive'}."),
        ],
    )


# ==========================================================================

st.markdown("---")

onglets = st.tabs(
    [
        "1️⃣ Quantité optimale",
        "2️⃣ Valeur du maximum",
        "3️⃣ Minimiser le coût moyen",
        "4️⃣ Second ordre",
    ]
)

with onglets[0]:
    st.subheader("Maximiser le bénéfice")
    executer("s8_quantite", gen_quantite_optimale)

with onglets[1]:
    st.subheader("Combien gagne-t-on au mieux ?")
    executer("s8_benefice", gen_benefice_maximal)

with onglets[2]:
    st.subheader("L'arbitrage du coût moyen")
    executer("s8_cout_moyen", gen_cout_moyen_minimal)

with onglets[3]:
    st.subheader("Maximum ou minimum ?")
    executer("s8_second_ordre", gen_second_ordre)

st.markdown("---")
st.caption(
    "Semestre — séance n°8 : Optimisation · "
    "Mathématiques appliquées pour les sciences humaines et sociales, Sciences Po."
)
