"""Série S4 — Le second degré : parabole et forme factorisée. Fil rouge E : le festival."""

import random
from fractions import Fraction

import streamlit as st
import sympy as sp

from moteur import Etape, Exercice, executer

st.set_page_config(page_title="S4 | Second degré", page_icon="🎪", layout="wide")

x, p_ = sp.symbols("x p")

st.title("🎪 S4 — Le second degré : parabole et forme factorisée")

with st.expander("📖 Contexte & objectifs", expanded=True):
    st.markdown(
        """
### 🎯 Ce que cette série entraîne
Reconnaître une fonction du second degré, lire l'**orientation** de sa parabole,
trouver ses **racines** à partir de la forme factorisée, et localiser son **sommet**.

### 🧠 Pourquoi on quitte l'affine
Une recette n'est pas proportionnelle au prix : augmenter le prix rapporte plus par
billet, mais fait fuir des spectateurs. Le produit de ces deux effets contraires n'est
plus une droite — c'est une parabole, et son sommet est précisément le point qu'on
cherche.

### 🎪 Fil rouge E — Le festival de Villeneuve
Au prix $p$ (en euros), le nombre de spectateurs est $N(p) = 9\\,000 - 60p$.
La recette de billetterie vaut donc $R(p) = p\\,(9\\,000 - 60p)$.
"""
    )

with st.sidebar:
    st.header("📝 Aide-mémoire — Séance 4")
    st.latex(r"f(x) = ax^2 + bx + c \quad (a \neq 0)")
    st.markdown("**Orientation**")
    st.markdown(
        "$a > 0$ : parabole tournée vers le **haut**, sommet = **minimum**\n\n"
        "$a < 0$ : tournée vers le **bas**, sommet = **maximum**"
    )
    st.markdown("**Forme factorisée**")
    st.latex(r"f(x) = a(x - x_1)(x - x_2)")
    st.markdown("Les racines $x_1$ et $x_2$ se lisent directement.")
    st.markdown("**Le sommet est au milieu des racines**")
    st.latex(r"x_S = \frac{x_1 + x_2}{2} \qquad x_S = -\frac{b}{2a}")
    st.info(
        "**Pourquoi la forme factorisée est précieuse**\n\n"
        "Elle livre les racines sans calcul, et le signe se lit immédiatement — "
        "exactement comme en pré-rentrée 3."
    )


def _fr(v, n=2):
    return f"{v:,.{n}f}".replace(",", "\u202f").replace(".", ",")


# --- 1. Orientation de la parabole (QCM) -----------------------------------


def gen_orientation() -> Exercice:
    a = random.choice([-3, -2, -0.5, 0.5, 2, 4])
    b = random.choice([-12, -5, 6, 18])
    c = random.choice([-8, 0, 15])
    f = a * x**2 + b * x + c

    if a > 0:
        bonne = "Tournée vers le haut : le sommet est un minimum"
    else:
        bonne = "Tournée vers le bas : le sommet est un maximum"
    options = [
        "Tournée vers le haut : le sommet est un minimum",
        "Tournée vers le bas : le sommet est un maximum",
        "L'orientation dépend du signe de c",
    ]

    enonce = f"""
> Soit la fonction du second degré
>
> $$ f(x) = {sp.latex(f)} $$
>
> Comment sa parabole est-elle orientée, et que représente son sommet ?
"""

    etapes = [
        Etape(
            "Identifier — seul le coefficient de $x^2$ compte",
            f"Le coefficient dominant vaut ${a}$. C'est **lui seul** qui décide de "
            "l'orientation : ni $b$ ni $c$ n'y changent quoi que ce soit. Ils "
            "déplacent la parabole, ils ne la retournent pas.",
        ),
        Etape(
            "Appliquer la règle",
            f"${a}$ est **{'positif' if a > 0 else 'négatif'}**, donc la parabole est "
            f"tournée vers le **{'haut' if a > 0 else 'bas'}** et son sommet est un "
            f"**{'minimum' if a > 0 else 'maximum'}**.",
        ),
        Etape(
            "Vérifier — le comportement aux extrêmes",
            f"Pour $x$ très grand, le terme ${sp.latex(a*x**2)}$ écrase tous les "
            f"autres : $f$ part donc vers "
            f"{'$+\\infty$' if a > 0 else '$-\\infty$'} des deux côtés. "
            "C'est cohérent avec l'orientation annoncée. ✓",
        ),
        Etape(
            "Interpréter — pourquoi le signe de $a$ est décisif en pratique",
            "Une recette ou un profit a presque toujours $a < 0$ : il existe donc un "
            "**maximum**, et la question « quel prix choisir ? » a une réponse. "
            "Avec $a > 0$, on cherche au contraire un minimum — un coût moyen, par "
            "exemple. Le signe de $a$ dit quel type de question on peut poser.",
        ),
    ]

    return Exercice(
        enonce=enonce,
        reponse=bonne,
        etapes=etapes,
        type_reponse="qcm",
        options=options,
        libelle="Orientation",
        indice="Regardez uniquement le coefficient de $x^2$.",
        pieges=[
            ("Tournée vers le bas : le sommet est un maximum" if a > 0
             else "Tournée vers le haut : le sommet est un minimum",
             f"Le coefficient de $x^2$ vaut ${a}$, donc "
             f"**{'positif' if a > 0 else 'négatif'}** : la parabole est tournée vers "
             f"le {'haut' if a > 0 else 'bas'}."),
            ("L'orientation dépend du signe de c",
             "$c$ est l'ordonnée à l'origine : il translate la parabole "
             "verticalement, sans jamais la retourner."),
        ],
    )


# --- 2. Racines d'une forme factorisée -------------------------------------


def gen_racines() -> Exercice:
    a = random.choice([-2, -1, 1, 2, 3])
    x1 = random.choice([-6, -3, -1, 2, 4])
    x2 = x1 + random.choice([2, 3, 5, 7])
    reponse = float(max(x1, x2))

    enonce = f"""
> Soit la fonction du second degré donnée sous **forme factorisée** :
>
> $$ f(x) = {a}\\,(x - ({x1}))\\,(x - ({x2})) $$
>
> Quelle est la **plus grande** de ses deux racines ?
"""

    f = sp.expand(a * (x - x1) * (x - x2))

    etapes = [
        Etape(
            "Identifier — surtout ne pas développer",
            "La forme factorisée livre les racines **sans aucun calcul**. Développer "
            "reviendrait à détruire l'information qu'on cherche, pour devoir la "
            "reconstruire ensuite avec le discriminant.",
        ),
        Etape(
            "Appliquer l'équation produit nul",
            "Un produit est nul si l'un des facteurs est nul — règle de la "
            "pré-rentrée 3, appliquée telle quelle.",
            rf"f(x) = 0 \iff x - ({x1}) = 0 \ \text{{ou}}\ x - ({x2}) = 0 "
            rf"\iff x = {x1} \ \text{{ou}}\ x = {x2}",
        ),
        Etape(
            "Vérifier",
            f"$f({x2}) = {a} \\times ({x2 - x1}) \\times 0 = 0$ ✓. "
            f"Le facteur $a = {a}$ ne s'annule jamais : il ne crée donc aucune racine "
            "supplémentaire, il ne fait que régler l'ouverture de la parabole.",
        ),
        Etape(
            "Interpréter — ce que les racines représentent",
            f"Les racines sont les points où la courbe **coupe l'axe horizontal**, "
            "c'est-à-dire où la grandeur modélisée s'annule. Pour une recette, ce "
            "sont les prix qui ne rapportent rien : un prix nul, et un prix si élevé "
            f"que plus personne ne vient. La forme développée $f(x) = {sp.latex(f)}$ "
            "cache complètement cette information.",
        ),
    ]

    return Exercice(
        enonce=enonce,
        reponse=reponse,
        etapes=etapes,
        libelle="Plus grande racine",
        tolerance=1e-6,
        indice="Un produit est nul si l'un de ses facteurs est nul.",
        pieges=[
            (float(min(x1, x2)),
             "C'est la **plus petite** racine. L'énoncé demande la plus grande."),
            (float(-max(x1, x2)),
             f"Attention au signe : le facteur $(x - ({x2}))$ s'annule pour "
             f"$x = {x2}$, pas pour $x = {-x2}$."),
            (float(a),
             "Le coefficient $a$ ne s'annule jamais : il ne donne pas de racine."),
        ],
    )


# --- 3. Le sommet -----------------------------------------------------------


def gen_sommet() -> Exercice:
    modele = random.choice(["racines", "coefficients"])

    if modele == "racines":
        a = random.choice([-2, -1, 1, 3])
        x1 = random.choice([-8, -4, 0, 2, 6])
        x2 = x1 + random.choice([4, 6, 10])
        reponse = float(Fraction(x1 + x2, 2))
        enonce = f"""
> Une parabole a pour racines $x_1 = {x1}$ et $x_2 = {x2}$.
>
> Quelle est l'**abscisse de son sommet** ?
"""
        etapes = [
            Etape(
                "Identifier — la parabole est symétrique",
                "Une parabole est symétrique par rapport à l'axe vertical qui passe "
                "par son sommet. Les deux racines, situées à la même hauteur (zéro), "
                "sont donc **symétriques** l'une de l'autre par rapport à cet axe.",
            ),
            Etape(
                "Prendre le milieu des racines",
                "L'abscisse du sommet est donc exactement au milieu.",
                rf"x_S = \frac{{{x1} + {x2}}}{{2}} = {reponse:.4g}",
            ),
            Etape(
                "Vérifier — l'écart aux deux racines",
                f"La distance du sommet à chaque racine vaut "
                f"${abs(reponse - x1):.4g}$ des deux côtés. ✓ C'est la définition "
                "même de la symétrie.",
            ),
            Etape(
                "Interpréter",
                "Ce raisonnement évite toute formule : dès qu'on connaît les deux "
                "racines, le sommet s'obtient de tête. C'est la méthode la plus "
                "rapide, et elle marche dans tous les cas où la forme factorisée "
                "est disponible.",
            ),
        ]
        pieges = [
            (float(x2 - x1),
             "C'est l'**écart** entre les racines, pas leur milieu. Il reste à le "
             "diviser par deux et à l'ajouter à la première racine."),
            (float(x1 * x2),
             "Le sommet est au milieu — donc une moyenne, pas un produit."),
        ]
    else:
        a = random.choice([-3, -2, 2, 4])
        xs = random.choice([-3, -1, 2, 5])
        b = -2 * a * xs
        c = random.choice([-6, 0, 12])
        f = a * x**2 + b * x + c
        reponse = float(xs)
        enonce = f"""
> Soit la fonction du second degré
>
> $$ f(x) = {sp.latex(f)} $$
>
> Quelle est l'**abscisse de son sommet** ?
"""
        etapes = [
            Etape(
                "Identifier — la formule du sommet",
                "Quand les racines ne sont pas connues, l'abscisse du sommet se lit "
                "directement sur les coefficients.",
                r"x_S = -\frac{b}{2a}",
            ),
            Etape(
                "Appliquer",
                f"Ici $a = {a}$ et $b = {b}$.",
                rf"x_S = -\frac{{{b}}}{{2 \times {a}}} = {reponse:.4g}",
            ),
            Etape(
                "Vérifier — la symétrie",
                f"$f({xs - 2}) = {float(f.subs(x, xs-2)):.0f}$ et "
                f"$f({xs + 2}) = {float(f.subs(x, xs+2)):.0f}$ : deux points "
                "symétriques ont bien la même image. ✓ C'est le meilleur contrôle "
                "d'une abscisse de sommet.",
            ),
            Etape(
                "Interpréter",
                f"Le sommet est le point où la grandeur atteint son "
                f"{'maximum' if a < 0 else 'minimum'}. Sa valeur s'obtient ensuite en "
                f"calculant $f({reponse:.4g})$ — c'est une seconde étape, souvent "
                "oubliée.",
            ),
        ]
        pieges = [
            (float(b) / (2 * a),
             "Erreur de signe : la formule est $-\\frac{b}{2a}$, avec un signe moins."),
            (float(-b / a),
             "Il manque le facteur 2 au dénominateur."),
        ]

    return Exercice(
        enonce=enonce,
        reponse=reponse,
        etapes=etapes,
        libelle="Abscisse du sommet",
        tolerance=1e-6,
        indice="Le sommet est au milieu des racines — ou se lit sur les coefficients.",
        pieges=pieges,
    )


# --- 4. Fil rouge : les prix qui annulent la recette -----------------------


def gen_festival() -> Exercice:
    spectateurs = random.choice([7_500, 9_000, 10_800, 12_000])
    sensibilite = random.choice([50, 60, 75, 90])
    p_max = spectateurs / sensibilite
    reponse = float(p_max)
    p_sommet = p_max / 2

    enonce = f"""
> **Le festival de Villeneuve.** Au prix $p$ (en euros), le nombre de spectateurs est
>
> $$ N(p) = {spectateurs:,} - {sensibilite}\\,p $$
>
> La recette de billetterie vaut donc $R(p) = p \\times N(p)$.
>
> À partir de quel prix la recette devient-elle **nulle** (hors prix nul) ?
""".replace(",", "\u202f")

    etapes = [
        Etape(
            "Identifier — la recette est déjà sous forme factorisée",
            "$R(p) = p\\,(N(p))$ est un produit de deux facteurs affines. "
            "Il n'y a rien à développer : les racines se lisent directement.",
            rf"R(p) = p\,({spectateurs} - {sensibilite}p)",
        ),
        Etape(
            "Annuler chaque facteur",
            "Un produit est nul si l'un de ses facteurs l'est.",
            rf"p = 0 \quad \text{{ou}} \quad {spectateurs} - {sensibilite}p = 0 "
            rf"\iff p = \frac{{{spectateurs}}}{{{sensibilite}}} = {reponse:.0f}",
        ),
        Etape(
            "Vérifier — les deux racines ont un sens concret",
            f"À $p = 0$, l'entrée est gratuite : {spectateurs:,} spectateurs viennent "
            f"mais ne paient rien. À $p = {reponse:.0f}$ €, le prix est si élevé que "
            "plus personne ne vient : la recette est nulle pour la raison inverse. ✓"
            .replace(",", "\u202f"),
        ),
        Etape(
            "Interpréter — le sommet est déjà lisible",
            f"Les deux racines encadrent le maximum, qui se situe exactement à leur "
            f"milieu : $p = \\frac{{0 + {reponse:.0f}}}{{2}} = {p_sommet:.0f}$ €. "
            "Sans aucun calcul supplémentaire, on connaît donc déjà le prix qui "
            "maximise la recette. C'est exactement ce que la forme factorisée rend "
            "possible — et ce que la forme développée aurait caché.",
        ),
    ]

    return Exercice(
        enonce=enonce,
        reponse=reponse,
        etapes=etapes,
        libelle="Prix annulant la recette",
        unite="€",
        tolerance=0.002,
        indice="La recette est un produit : quand un produit est-il nul ?",
        pieges=[
            (float(p_sommet),
             "C'est le prix qui **maximise** la recette (le milieu des racines), pas "
             "celui qui l'annule."),
            (float(spectateurs),
             "C'est un nombre de spectateurs, pas un prix. Vérifiez l'unité de votre "
             "réponse."),
            (0.0,
             "L'énoncé écarte explicitement le prix nul : on cherche l'autre racine."),
        ],
    )


# ==========================================================================

st.markdown("---")

onglets = st.tabs(
    [
        "1️⃣ Orientation de la parabole",
        "2️⃣ Racines",
        "3️⃣ Le sommet",
        "4️⃣ Festival : recette nulle",
    ]
)

with onglets[0]:
    st.subheader("Vers le haut ou vers le bas ?")
    executer("s4_orientation", gen_orientation)

with onglets[1]:
    st.subheader("Lire les racines sur la forme factorisée")
    executer("s4_racines", gen_racines)

with onglets[2]:
    st.subheader("Localiser le sommet")
    executer("s4_sommet", gen_sommet)

with onglets[3]:
    st.subheader("Les prix qui annulent la recette")
    executer("s4_festival", gen_festival)

st.markdown("---")
st.caption(
    "Semestre — séance n°4 : Le second degré, parabole et forme factorisée · "
    "Fil rouge E : le festival de Villeneuve · Sciences Po."
)
