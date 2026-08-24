"""
Série P1 — Fractions et puissances
Séance de pré-rentrée n°1 : nombres, fractions, puissances.
Fil rouge A : le budget de Villeneuve.
"""

import random
from fractions import Fraction

import streamlit as st
import sympy as sp

from moteur import Etape, Exercice, executer

st.set_page_config(
    page_title="P1 | Fractions et puissances", page_icon="➗", layout="wide"
)

URL_SLIDES = "https://moodle.sciencespo.fr/"  # à remplacer par le lien du dépôt

st.title("➗ P1 — Fractions et puissances")

with st.expander("📖 Contexte & objectifs", expanded=True):
    st.markdown(
        """
### 🎯 Ce que cette série entraîne
Écrire un nombre en **notation scientifique**, diviser deux ordres de grandeur,
manipuler des **fractions avec des lettres**, appliquer les **règles de puissances**,
et invalider une règle fausse par un **contre-exemple**.

### 🧠 Comment lire la correction
Chaque exercice ne demande qu'**un résultat**. Mais à la validation, la plateforme
affiche la **méthode complète étape par étape**, reconstruite sur les nombres de
*votre* énoncé — que votre réponse soit juste ou fausse.

C'est cette méthode qui compte : à l'examen comme en contrôle continu, un bon
résultat obtenu par une démarche fausse ne vaut rien, et une démarche juste
entachée d'une erreur de calcul vaut presque tout.

### 🔁 Les énoncés changent à chaque tentative
Refaites chaque famille jusqu'à ce que la démarche soit **fluide**, pas jusqu'à
ce que vous ayez « eu bon » une fois.
"""
    )

with st.sidebar:
    st.header("📝 Aide-mémoire — Séance 1")
    st.markdown("**Fractions** ($b \\neq 0$, $d \\neq 0$)")
    st.latex(
        r"\frac{a}{b}+\frac{c}{d}=\frac{ad+bc}{bd}\qquad"
        r"\frac{a}{b}\times\frac{c}{d}=\frac{ac}{bd}"
    )
    st.latex(r"\frac{a}{b}\div\frac{c}{d}=\frac{a}{b}\times\frac{d}{c}=\frac{ad}{bc}")
    st.markdown("**Puissances** ($a \\neq 0$)")
    st.latex(
        r"a^m a^n = a^{m+n}\qquad (a^m)^n = a^{mn}\qquad \frac{a^m}{a^n}=a^{m-n}"
    )
    st.latex(r"a^0 = 1\qquad a^{-n}=\frac{1}{a^n}\qquad a^{1/2}=\sqrt{a}")
    st.error(
        "**Les deux erreurs interdites**\n\n"
        r"$\frac{1}{a+b} \neq \frac{1}{a}+\frac{1}{b}$"
        "\n\n"
        r"$\sqrt{a+b} \neq \sqrt{a}+\sqrt{b}$"
    )
    st.info(
        "**Les deux réflexes**\n\n"
        "1. Face à une règle douteuse, **testez avec des nombres**.\n"
        "2. Avant de vérifier un calcul, demandez-vous si l'ordre de grandeur "
        "est **plausible**."
    )

# ==========================================================================
# GÉNÉRATEURS
# ==========================================================================

RUBRIQUES = [
    ("transports", "mobilités douces"),
    ("éducation", "activités périscolaires"),
    ("culture", "lecture publique"),
    ("sport", "équipements de quartier"),
    ("action sociale", "aide alimentaire"),
]


def _fmt(x: float, n: int = 2) -> str:
    """Formatage à la française."""
    return f"{x:,.{n}f}".replace(",", " ").replace(".", ",")


# --- Famille 1 : notation scientifique et ordre de grandeur ----------------


def gen_ordre_de_grandeur() -> Exercice:
    budget = random.choice([150, 180, 210, 240, 300, 360])  # en M€
    pop = random.choice([120_000, 150_000, 180_000, 200_000, 240_000, 250_000])

    a = budget / 100  # mantisse du budget en euros (x 10^8)
    b = pop / 100_000  # mantisse de la population (x 10^5)
    reponse = budget * 1e6 / pop

    pop_txt = f"{pop:,}".replace(",", " ")
    enonce = f"""
> **Villeneuve.** Le budget annuel de la ville s'élève à **{budget} millions d'euros**
> pour **{pop_txt} habitants**.
>
> Quelle est la **dépense annuelle par habitant** ? Répondez en euros, sans calculatrice.
"""

    etapes = [
        Etape(
            "Identifier — pourquoi la notation scientifique",
            "On divise une très grande quantité par une grande quantité. "
            "Poser la division telle quelle est pénible ; en notation scientifique, "
            "elle devient immédiate car les puissances de 10 se traitent séparément.",
        ),
        Etape(
            "Écrire les deux nombres en notation scientifique",
            f"Le budget est exprimé en **millions** d'euros : "
            f"{budget} M€ = {budget} × 10⁶ € = {_fmt(a, 1)} × 10⁸ €. "
            "C'est la conversion que l'on oublie le plus souvent.",
            rf"B = {a:g} \times 10^{{8}}\ \text{{€}}"
            rf"\qquad P = {b:g} \times 10^{{5}}\ \text{{hab.}}",
        ),
        Etape(
            "Calculer — séparer mantisses et puissances",
            "On applique $\\dfrac{a \\times 10^m}{b \\times 10^n} "
            "= \\dfrac{a}{b} \\times 10^{m-n}$ : les mantisses d'un côté, "
            "les puissances de 10 de l'autre.",
            rf"\frac{{{a:g} \times 10^{{8}}}}{{{b:g} \times 10^{{5}}}}"
            rf" = \frac{{{a:g}}}{{{b:g}}} \times 10^{{3}}"
            rf" \approx {a/b:.3f} \times 10^{{3}}"
            rf" \approx {reponse:.0f}\ \text{{€/habitant}}",
        ),
        Etape(
            "Vérifier — le résultat est-il plausible ?",
            "Une commune française dépense typiquement de l'ordre de **1 000 à "
            "2 000 € par habitant et par an**. Un résultat en centimes ou en "
            "millions signalerait une erreur de conversion, pas une erreur de calcul.",
        ),
        Etape(
            "Interpréter — revenir à la question sociale",
            f"Chaque habitant de Villeneuve « coûte » environ **{_fmt(reponse, 0)} €** "
            "de dépense publique locale par an. Ce nombre n'a de sens que **comparé** : "
            "à une autre ville, à une autre année, ou à la moyenne nationale. "
            "C'est tout l'objet de la séance 2.",
        ),
    ]

    return Exercice(
        enonce=enonce,
        reponse=reponse,
        etapes=etapes,
        libelle="Dépense par habitant",
        unite="€",
        tolerance=0.01,
        indice="Convertissez d'abord les millions d'euros en euros. "
        "Puis divisez les mantisses d'un côté, les puissances de 10 de l'autre.",
        pieges=[
            (
                budget / pop,
                "Vous avez divisé **des millions d'euros** par des habitants sans "
                "convertir : votre résultat est en millions d'euros par habitant. "
                "Il manque le facteur 10⁶.",
            ),
            (
                reponse / 1000,
                "Vous avez correctement divisé les mantisses mais **perdu la puissance "
                "de 10** : $10^8 / 10^5 = 10^3$, pas $10^0$.",
            ),
            (
                reponse * 1000,
                "Vous avez une puissance de 10 **en trop** : vérifiez le calcul "
                "$10^8 / 10^5$ — on **soustrait** les exposants.",
            ),
            (
                pop / (budget * 1e6),
                "Vous avez divisé dans le **mauvais sens** : la question demande "
                "des euros *par habitant*, donc le budget au numérateur.",
            ),
        ],
    )


# --- Famille 2 : fractions emboîtées ---------------------------------------


def gen_fractions_emboitees() -> Exercice:
    budget = random.choice([180, 200, 240, 250, 300])
    f1 = random.choice(
        [Fraction(1, 4), Fraction(1, 5), Fraction(1, 6), Fraction(1, 8), Fraction(1, 10)]
    )
    f2 = random.choice(
        [Fraction(1, 3), Fraction(1, 4), Fraction(1, 5), Fraction(2, 5), Fraction(3, 10)]
    )
    rubrique, sous_rubrique = random.choice(RUBRIQUES)

    part = f1 * f2
    reponse = budget * float(part)

    enonce = f"""
> **Villeneuve.** Le budget annuel est de **{budget} M€**.
> $\\dfrac{{{f1.numerator}}}{{{f1.denominator}}}$ de ce budget va à la rubrique
> **{rubrique}**, et $\\dfrac{{{f2.numerator}}}{{{f2.denominator}}}$ du budget
> {rubrique} va au poste **{sous_rubrique}**.
>
> Quel montant, en millions d'euros, est consacré au poste *{sous_rubrique}* ?
"""

    etapes = [
        Etape(
            "Identifier — « une part d'une part » se multiplie",
            "La seconde fraction ne porte pas sur le budget total mais sur la "
            "rubrique. Prendre une fraction **d'une** fraction, c'est **multiplier** "
            "les deux — jamais les additionner.",
        ),
        Etape(
            "Calculer la part du budget total",
            "On multiplie en ligne, numérateurs entre eux et dénominateurs entre eux.",
            rf"\frac{{{f1.numerator}}}{{{f1.denominator}}} \times "
            rf"\frac{{{f2.numerator}}}{{{f2.denominator}}} = "
            rf"\frac{{{f1.numerator * f2.numerator}}}{{{f1.denominator * f2.denominator}}} = "
            rf"\frac{{{part.numerator}}}{{{part.denominator}}}",
        ),
        Etape(
            "Appliquer cette part au budget",
            f"Il reste à prendre cette fraction de {budget} M€.",
            rf"\frac{{{part.numerator}}}{{{part.denominator}}} \times {budget} = "
            rf"{_fmt(reponse).replace(',','.')}\ \text{{M€}}",
        ),
        Etape(
            "Vérifier — encadrement rapide",
            f"Le poste *{sous_rubrique}* doit être plus petit que la rubrique "
            f"*{rubrique}* (soit {_fmt(budget * float(f1))} M€) et beaucoup plus petit "
            f"que le budget total ({budget} M€). "
            f"{_fmt(reponse)} M€ satisfait bien ce double encadrement.",
        ),
        Etape(
            "Interpréter — l'effet d'emboîtement",
            f"Deux fractions d'apparence modeste produisent une part très faible : "
            f"$\\frac{{{part.numerator}}}{{{part.denominator}}}$ du budget, soit "
            f"environ **{_fmt(100 * float(part), 1)} %** du total. C'est le mécanisme "
            "qui explique pourquoi un poste jugé « prioritaire » dans le discours "
            "politique peut peser très peu dans les comptes.",
        ),
    ]

    return Exercice(
        enonce=enonce,
        reponse=reponse,
        etapes=etapes,
        libelle=f"Budget du poste « {sous_rubrique} »",
        unite="M€",
        tolerance=0.01,
        indice="Une fraction d'une fraction : la question est de savoir si l'on "
        "additionne ou si l'on multiplie. Testez sur un cas simple : "
        "la moitié d'une moitié, est-ce un ou un quart ?",
        pieges=[
            (
                budget * float(f1 + f2),
                "Vous avez **additionné** les deux fractions. Or on cherche une part "
                "*d'une* part : la moitié d'une moitié fait un quart, pas un. "
                "On multiplie.",
            ),
            (
                budget * float(f2),
                f"Vous avez appliqué $\\frac{{{f2.numerator}}}{{{f2.denominator}}}$ au "
                "**budget total** alors qu'elle porte sur la rubrique "
                f"*{rubrique}* seulement.",
            ),
            (
                budget * float(f1),
                f"C'est le budget de la rubrique *{rubrique}* entière, pas celui du "
                f"poste *{sous_rubrique}*. Il reste une fraction à appliquer.",
            ),
        ],
    )


# --- Famille 3 : fractions avec des lettres --------------------------------


def gen_fractions_litterales() -> Exercice:
    modele = random.choice(["somme_x", "division", "inverses", "difference"])
    x, y, a, b, c, d = sp.symbols("x y a b c d")

    if modele == "somme_x":
        p, q = random.sample([2, 3, 4, 5, 6], 2)
        expression = sp.latex(x / p + x / q)
        reponse = sp.together(x / p + x / q)
        symboles = ["x"]
        etapes = [
            Etape(
                "Identifier — une somme de fractions",
                "Pour additionner, il faut un **dénominateur commun**. "
                "Le produit des deux dénominateurs convient toujours "
                f"(ici {p} × {q} = {p*q}), même s'il n'est pas le plus petit.",
            ),
            Etape(
                "Mettre au même dénominateur",
                "On multiplie chaque fraction par ce qui lui manque.",
                rf"\frac{{x}}{{{p}}} + \frac{{x}}{{{q}}} = "
                rf"\frac{{{q}x}}{{{p*q}}} + \frac{{{p}x}}{{{p*q}}}",
            ),
            Etape(
                "Additionner les numérateurs",
                "Le dénominateur ne change plus ; on factorise par $x$.",
                rf"= \frac{{{q}x + {p}x}}{{{p*q}}} = {sp.latex(sp.simplify(reponse))}",
            ),
            Etape(
                "Vérifier — le test numérique",
                f"Prenons $x = {p*q}$ : à gauche ${q} + {p} = {p+q}$, "
                f"à droite $\\frac{{{p+q}}}{{{p*q}}} \\times {p*q} = {p+q}$. "
                "Les deux coïncident. Ce test de 5 secondes détecte "
                "l'immense majorité des erreurs.",
            ),
            Etape(
                "Interpréter — pourquoi ça servira",
                "Regrouper deux termes en une seule fraction est ce qui permettra, "
                "au semestre, de factoriser une dérivée et d'en lire le signe.",
            ),
        ]
        pieges = [
            (x / (p + q), "Vous avez **additionné les dénominateurs**. "
             "Testez avec $x = 1$ : $\\frac{1}{2} + \\frac{1}{2} = 1$, "
             "et non $\\frac{1}{4}$."),
        ]

    elif modele == "division":
        expression = r"\frac{a+b}{c} \div \frac{a+b}{d}"
        reponse = d / c
        symboles = ["a", "b", "c", "d"]
        etapes = [
            Etape(
                "Identifier — une division de fractions",
                "Diviser par une fraction, c'est **multiplier par son inverse**. "
                "Rien d'autre n'est à faire pour l'instant.",
            ),
            Etape(
                "Transformer la division en multiplication",
                "On retourne la seconde fraction.",
                r"\frac{a+b}{c} \div \frac{a+b}{d} = "
                r"\frac{a+b}{c} \times \frac{d}{a+b}",
            ),
            Etape(
                "Simplifier",
                "Le facteur $(a+b)$ apparaît au numérateur **et** au dénominateur : "
                "on peut le simplifier, à condition que $a + b \\neq 0$.",
                r"= \frac{(a+b)\,d}{c\,(a+b)} = \frac{d}{c}",
            ),
            Etape(
                "Vérifier — attention à la condition",
                "La simplification n'est licite que si $a+b \\neq 0$. "
                "En sciences sociales, cette condition a souvent un sens concret "
                "(un effectif non nul, un budget non vide) : ne la traitez pas "
                "comme une formalité.",
            ),
            Etape(
                "Interpréter",
                "Le résultat ne dépend plus du tout de $a$ ni de $b$. "
                "Reconnaître qu'un bloc entier se simplifie évite des calculs "
                "inutiles — c'est un réflexe payant à l'examen.",
            ),
        ]
        pieges = [
            (c / d, "Vous avez inversé le rapport : c'est la **seconde** fraction "
             "que l'on retourne, pas la première."),
            ((a + b) ** 2 / (c * d), "Vous avez **multiplié** les deux fractions au "
             "lieu de diviser : il fallait retourner la seconde."),
        ]

    elif modele == "inverses":
        expression = r"\frac{1}{x} + \frac{1}{y}"
        reponse = (x + y) / (x * y)
        symboles = ["x", "y"]
        etapes = [
            Etape(
                "Identifier — le piège numéro un du programme",
                "La tentation est d'écrire $\\frac{1}{x+y}$. C'est faux, et c'est "
                "l'erreur la plus fréquente de toute l'année.",
            ),
            Etape(
                "Mettre au même dénominateur",
                "Le dénominateur commun est le produit $xy$.",
                r"\frac{1}{x} + \frac{1}{y} = \frac{y}{xy} + \frac{x}{xy}",
            ),
            Etape(
                "Additionner",
                "",
                r"= \frac{x+y}{xy}",
            ),
            Etape(
                "Vérifier — le contre-exemple qui tranche",
                "Avec $x = y = 1$ : la vraie valeur est $1 + 1 = 2$, "
                "et $\\frac{x+y}{xy} = \\frac{2}{1} = 2$ ✓, "
                "tandis que $\\frac{1}{x+y} = \\frac{1}{2}$ ✗. "
                "Un seul contre-exemple suffit à invalider une règle.",
            ),
            Etape(
                "Interpréter",
                "Cette forme réapparaîtra telle quelle au semestre, dans le calcul "
                "de moyennes harmoniques et de vitesses moyennes — deux objets où "
                "l'erreur $\\frac{1}{x+y}$ donne un résultat absurde.",
            ),
        ]
        pieges = [
            (1 / (x + y), "C'est **l'erreur interdite** de la séance : "
             "$\\frac{1}{x}+\\frac{1}{y} \\neq \\frac{1}{x+y}$. "
             "Testez avec $x=y=1$ : $2 \\neq \\frac{1}{2}$."),
            ((x + y) / (x + y), "Vérifiez votre dénominateur commun : "
             "c'est le **produit** $xy$, pas la somme."),
        ]

    else:  # difference
        p = random.choice([2, 3, 4, 5])
        q, r = random.sample([3, 4, 5, 6], 2)
        expression = sp.latex(p * x / q - x / r)
        reponse = sp.together(p * x / q - x / r)
        symboles = ["x"]
        etapes = [
            Etape(
                "Identifier — une différence de fractions",
                "Même règle que pour la somme : dénominateur commun d'abord. "
                "Le signe moins porte sur **tout** le numérateur de la seconde "
                "fraction.",
            ),
            Etape(
                "Mettre au même dénominateur",
                f"Le dénominateur commun est {q} × {r} = {q*r}.",
                rf"\frac{{{p}x}}{{{q}}} - \frac{{x}}{{{r}}} = "
                rf"\frac{{{p*r}x}}{{{q*r}}} - \frac{{{q}x}}{{{q*r}}}",
            ),
            Etape(
                "Soustraire et factoriser",
                "",
                rf"= \frac{{({p*r} - {q})x}}{{{q*r}}} = "
                rf"{sp.latex(sp.simplify(reponse))}",
            ),
            Etape(
                "Vérifier",
                f"Test avec $x = {q*r}$ : à gauche "
                f"${p} \\times {r} - {q} = {p*r - q}$ ; "
                f"à droite, le numérateur vaut aussi ${p*r-q}$. ✓",
            ),
            Etape(
                "Interpréter",
                "Si le numérateur avait été négatif, l'expression entière changerait "
                "de signe : c'est exactement ce type de lecture qui servira à "
                "déterminer si une grandeur croît ou décroît.",
            ),
        ]
        pieges = [
            (sp.together(x / q - p * x / r),
             "Vous avez appliqué le coefficient à la mauvaise fraction. "
             "Relisez l'énoncé avant de calculer."),
        ]

    enonce = f"""
> Simplifiez et écrivez le résultat sous la forme d'**une seule fraction** :
>
> $$ {expression} $$
"""

    return Exercice(
        enonce=enonce,
        reponse=sp.simplify(reponse),
        etapes=etapes,
        type_reponse="sym",
        libelle="Expression simplifiée",
        symboles=symboles,
        indice="Les règles sont exactement les mêmes qu'avec des nombres. "
        "En cas de doute, remplacez les lettres par 1 ou 2 et vérifiez.",
        pieges=pieges,
    )


# --- Famille 4 : puissances -------------------------------------------------


def gen_puissances() -> Exercice:
    modele = random.choice(["imbriquee", "produit_quotient"])
    m, n = random.sample([2, 3, 4, 5], 2)
    p = random.choice([2, 3, 4, 5, 6])

    if modele == "imbriquee":
        expression = rf"\left(a^{{{m}}}\right)^{{{n}}} \times a^{{-{p}}}"
        reponse = m * n - p
        etapes = [
            Etape(
                "Identifier — deux règles, dans le bon ordre",
                "Une puissance de puissance : on **multiplie** les exposants. "
                "Puis un produit de puissances : on **additionne**. "
                "Confondre les deux est l'erreur classique.",
            ),
            Etape(
                "Traiter la puissance de puissance",
                f"$(a^m)^n = a^{{mn}}$, donc ici $a^{{{m} \\times {n}}}$.",
                rf"\left(a^{{{m}}}\right)^{{{n}}} = a^{{{m*n}}}",
            ),
            Etape(
                "Multiplier les deux puissances",
                "$a^m \\times a^n = a^{m+n}$ : on additionne, en tenant compte du "
                "signe négatif.",
                rf"a^{{{m*n}}} \times a^{{-{p}}} = a^{{{m*n} - {p}}} = a^{{{reponse}}}",
            ),
            Etape(
                "Vérifier — retour à la définition",
                "En cas de doute, réécrivez la puissance comme une multiplication "
                f"répétée : $(a^{m})^{n}$ signifie « $a^{m}$ multiplié {n} fois par "
                f"lui-même », soit {m} × {n} = {m*n} facteurs $a$. "
                "La règle se retrouve ainsi sans l'avoir apprise.",
            ),
            Etape(
                "Interpréter",
                "Les exposants négatifs ne sont pas une bizarrerie : $a^{-p}$ est "
                "une **division**. Toute cette mécanique sera reprise au semestre "
                "pour les fonctions puissances et les rendements d'échelle.",
            ),
        ]
        pieges = [
            (m + n - p,
             f"Vous avez traité $(a^{{{m}}})^{{{n}}}$ comme $a^{{{m}+{n}}}$. "
             "Pour une puissance **de** puissance, on **multiplie** les exposants."),
            (m * n + p,
             "Erreur de signe : $a^{-p}$ correspond à une soustraction de "
             "l'exposant, pas à une addition."),
        ]
    else:
        expression = rf"\frac{{a^{{{m}}} \times a^{{{n}}}}}{{a^{{{p}}}}}"
        reponse = m + n - p
        etapes = [
            Etape(
                "Identifier — produit puis quotient",
                "Deux règles s'enchaînent : $a^m a^n = a^{m+n}$ au numérateur, "
                "puis $\\dfrac{a^m}{a^n} = a^{m-n}$.",
            ),
            Etape(
                "Regrouper le numérateur",
                "On **additionne** les exposants d'un produit.",
                rf"a^{{{m}}} \times a^{{{n}}} = a^{{{m+n}}}",
            ),
            Etape(
                "Diviser",
                "On **soustrait** l'exposant du dénominateur.",
                rf"\frac{{a^{{{m+n}}}}}{{a^{{{p}}}}} = a^{{{m+n}-{p}}} = a^{{{reponse}}}",
            ),
            Etape(
                "Vérifier — le cas particulier révélateur",
                f"Si les exposants s'étaient annulés, on obtiendrait $a^0 = 1$. "
                "Ce n'est pas une convention arbitraire : c'est ce qu'impose la "
                "règle $\\frac{a^m}{a^m} = a^{m-m}$, puisqu'un nombre divisé par "
                "lui-même vaut 1.",
            ),
            Etape(
                "Interpréter",
                "Additionner des exposants revient à multiplier des grandeurs : "
                "c'est exactement le mécanisme qui, au semestre, rendra le "
                "logarithme utile — il fait l'opération inverse.",
            ),
        ]
        pieges = [
            (m * n - p,
             f"Vous avez **multiplié** les exposants du produit. "
             "On ne multiplie les exposants que pour une puissance de puissance."),
            (m + n + p,
             "Une **division** fait soustraire l'exposant, pas l'ajouter."),
        ]

    enonce = f"""
> Simplifiez l'expression suivante (avec $a \\neq 0$) :
>
> $$ {expression} $$
>
> Le résultat s'écrit sous la forme $a^{{n}}$. **Donnez la valeur de $n$.**
"""

    return Exercice(
        enonce=enonce,
        reponse=float(reponse),
        etapes=etapes,
        libelle="Exposant n",
        tolerance=1e-6,
        indice="Attention à l'ordre des règles : une puissance de puissance se "
        "traite en multipliant les exposants, un produit en les additionnant.",
        pieges=[(float(v), msg) for v, msg in pieges],
    )


# --- Famille 5 : racines carrées -------------------------------------------


def gen_racines() -> Exercice:
    k, m = random.choice(
        [(50, 2), (8, 2), (12, 3), (18, 2), (27, 3), (32, 2), (20, 5),
         (45, 5), (75, 3), (98, 2), (24, 6), (28, 7), (40, 10)]
    )
    reponse = float(sp.sqrt(k * m))

    enonce = f"""
> **Sans calculatrice**, calculez :
>
> $$ \\sqrt{{{k}}} \\times \\sqrt{{{m}}} $$
"""

    etapes = [
        Etape(
            "Identifier — la racine traverse le produit",
            "La propriété $\\sqrt{a} \\times \\sqrt{b} = \\sqrt{ab}$ est vraie "
            "(pour $a, b \\geqslant 0$). C'est ce qui rend le calcul faisable "
            "de tête : on regroupe **avant** de chercher la racine.",
        ),
        Etape(
            "Regrouper sous une seule racine",
            "",
            rf"\sqrt{{{k}}} \times \sqrt{{{m}}} = \sqrt{{{k} \times {m}}} = \sqrt{{{k*m}}}",
        ),
        Etape(
            "Reconnaître le carré parfait",
            f"${k*m}$ est un carré parfait : ${int(reponse)}^2 = {k*m}$.",
            rf"\sqrt{{{k*m}}} = {int(reponse)}",
        ),
        Etape(
            "Vérifier — ce que la racine ne fait PAS",
            "Le produit se traverse, **la somme non** : "
            "$\\sqrt{a+b} \\neq \\sqrt{a} + \\sqrt{b}$. "
            "Test : $\\sqrt{2+2} = 2$, alors que "
            "$\\sqrt{2} + \\sqrt{2} \\approx 2{,}83$. "
            "C'est exactement la même structure d'erreur que "
            "$\\frac{1}{a+b} \\neq \\frac{1}{a} + \\frac{1}{b}$.",
        ),
        Etape(
            "Interpréter",
            "Écrire $\\sqrt{a} = a^{1/2}$ montre que ce n'est pas une opération "
            "à part : c'est une puissance, qui obéit aux règles déjà connues. "
            "Rien de nouveau n'a été inventé, une règle a été **prolongée**.",
        ),
    ]

    return Exercice(
        enonce=enonce,
        reponse=reponse,
        etapes=etapes,
        libelle="Résultat",
        tolerance=0.005,
        indice="Ne cherchez pas chaque racine séparément : regroupez d'abord "
        "sous une seule racine.",
        pieges=[
            (float(sp.sqrt(k) + sp.sqrt(m)),
             "Vous avez **additionné** les racines alors que l'énoncé demande un "
             "produit. Et même pour une somme, la racine ne se distribue pas."),
            (float(k * m),
             "Vous avez multiplié les nombres **sous** la racine sans prendre la "
             f"racine à la fin : il reste à calculer $\\sqrt{{{k*m}}}$."),
        ],
    )


# --- Famille 6 : intérêts composés ------------------------------------------


def gen_placement() -> Exercice:
    # On retire tant que l'écart entre intérêts composés et intérêts simples
    # reste trop faible : le diagnostic de l'erreur ne serait pas fiable, et
    # la différence entre les deux logiques ne serait pas visible.
    while True:
        capital = random.choice([4, 5, 6, 8, 10])
        taux = random.choice([4, 5, 6, 8])
        annees = random.choice([3, 4, 5])
        coeff = 1 + taux / 100
        reponse = capital * coeff**annees
        simple = capital * (1 + annees * taux / 100)
        if reponse - simple > 0.02:
            break

    enonce = f"""
> **Villeneuve.** La ville place **{capital} M€** de réserves à un taux de
> **{taux} % par an**. La valeur du placement après $n$ années est
> $V = {capital} \\times ({coeff})^{{n}}$ millions d'euros.
>
> Calculez $V$ après **{annees} ans**, arrondi au centième de million.
"""

    etapes = [
        Etape(
            "Identifier — pourquoi une puissance et non un produit",
            f"Chaque année, le capital est multiplié par {coeff}. Après {annees} ans, "
            f"il a été multiplié {annees} fois par ce même nombre : "
            "c'est la définition d'une puissance. Les intérêts de l'année 2 "
            "portent sur le capital **augmenté** des intérêts de l'année 1.",
        ),
        Etape(
            "Poser le calcul",
            "",
            rf"V = {capital} \times ({coeff})^{{{annees}}}",
        ),
        Etape(
            "Calculer la puissance, puis multiplier",
            f"$({coeff})^{{{annees}}} \\approx {coeff**annees:.4f}$.",
            rf"V \approx {capital} \times {coeff**annees:.4f} "
            rf"\approx {reponse:.2f}\ \text{{M€}}",
        ),
        Etape(
            "Vérifier — comparer aux intérêts simples",
            f"Avec des intérêts **simples**, on aurait "
            f"{capital} × (1 + {annees} × {taux/100}) = "
            f"{simple:.2f} M€. "
            f"Le résultat composé ({reponse:.2f} M€) doit être **légèrement "
            "supérieur** : si vous trouvez moins, il y a une erreur.",
        ),
        Etape(
            "Interpréter",
            f"L'écart est faible sur {annees} ans, mais il croît sans limite avec le "
            "temps : c'est exactement le mécanisme de la dette publique, "
            "que l'on étudiera au semestre (fil rouge F).",
        ),
    ]

    return Exercice(
        enonce=enonce,
        reponse=reponse,
        etapes=etapes,
        libelle=f"Valeur après {annees} ans",
        unite="M€",
        tolerance_abs=0.006,  # accepte un arrondi au centième de million
        indice=f"Le taux ne s'ajoute pas {annees} fois : il se multiplie "
        f"{annees} fois.",
        pieges=[
            (simple,
             "Vous avez calculé des **intérêts simples** : le taux appliqué "
             f"{annees} fois au capital initial. Or les intérêts de l'année 2 "
             "portent aussi sur les intérêts de l'année 1 — d'où une puissance."),
            (capital * (taux / 100) ** annees,
             "Vous avez oublié le **1 +** : le coefficient multiplicateur d'une "
             f"hausse de {taux} % vaut {coeff}, pas {taux/100}."),
            (capital * coeff,
             "Vous n'avez appliqué le coefficient qu'**une seule fois** : "
             f"il faut l'appliquer {annees} fois."),
        ],
    )


# ==========================================================================
# FAMILLE 7 : vrai/faux et contre-exemple (moteur dédié)
# ==========================================================================

REGLES = [
    {
        "latex": r"\frac{1}{a+b} = \frac{1}{a} + \frac{1}{b}",
        "vraie": False,
        "gauche": lambda a, b: 1 / (a + b),
        "droite": lambda a, b: 1 / a + 1 / b,
        "explication": "C'est l'erreur interdite n°1 de la séance. Avec $a=b=1$ : "
        "$\\frac{1}{2}$ à gauche, $2$ à droite. La bonne écriture est "
        "$\\frac{1}{a}+\\frac{1}{b} = \\frac{a+b}{ab}$.",
    },
    {
        "latex": r"\sqrt{a+b} = \sqrt{a} + \sqrt{b}",
        "vraie": False,
        "gauche": lambda a, b: (a + b) ** 0.5,
        "droite": lambda a, b: a**0.5 + b**0.5,
        "explication": "C'est l'erreur interdite n°2. Avec $a=b=2$ : "
        "$\\sqrt{4}=2$ à gauche, $\\approx 2{,}83$ à droite. "
        "La racine traverse les **produits**, jamais les sommes.",
    },
    {
        "latex": r"(a+b)^2 = a^2 + b^2",
        "vraie": False,
        "gauche": lambda a, b: (a + b) ** 2,
        "droite": lambda a, b: a**2 + b**2,
        "explication": "Il manque le double produit : $(a+b)^2 = a^2 + 2ab + b^2$. "
        "Avec $a=b=1$ : $4 \\neq 2$. On le démontrera en séance 2.",
    },
    {
        "latex": r"\frac{a+b}{a+c} = \frac{b}{c}",
        "vraie": False,
        "gauche": lambda a, b, c=3: (a + b) / (a + c),
        "droite": lambda a, b, c=3: b / c,
        "explication": "On ne simplifie **que des facteurs**, jamais des termes "
        "d'une somme. Avec $a=1$, $b=2$, $c=3$ : "
        "$\\frac{3}{4} \\neq \\frac{2}{3}$.",
    },
    {
        "latex": r"\frac{a+b}{c} = \frac{a}{c} + \frac{b}{c}",
        "vraie": True,
        "gauche": lambda a, b, c=3: (a + b) / c,
        "droite": lambda a, b, c=3: a / c + b / c,
        "explication": "Celle-ci est **vraie** : c'est la distributivité de la "
        "division sur la somme. La somme se sépare quand elle est au "
        "**numérateur** — jamais au dénominateur. Toute la difficulté est là.",
    },
    {
        "latex": r"\sqrt{a \times b} = \sqrt{a} \times \sqrt{b} \quad (a, b \geqslant 0)",
        "vraie": True,
        "gauche": lambda a, b: (a * b) ** 0.5,
        "droite": lambda a, b: a**0.5 * b**0.5,
        "explication": "Celle-ci est **vraie** : la racine traverse un produit. "
        "C'est ce qui permet de calculer $\\sqrt{50}\\times\\sqrt{2}$ de tête.",
    },
]


def famille_contre_exemple() -> None:
    cle = "p1_regle"
    k_regle, k_fait = f"{cle}_r", f"{cle}_fait"

    if k_regle not in st.session_state:
        st.session_state[k_regle] = random.choice(REGLES)
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
        verdict = st.radio(
            "Cette règle est :",
            ["Vraie pour tous les nombres", "Fausse"],
            index=None,
            key=f"{cle}_verdict",
            disabled=st.session_state[k_fait],
        )
    with colonne_droite:
        st.caption("Si vous répondez « Fausse », proposez un contre-exemple :")
        val_a = st.number_input(
            "a =", value=1.0, step=1.0, key=f"{cle}_a",
            disabled=st.session_state[k_fait],
        )
        val_b = st.number_input(
            "b =", value=1.0, step=1.0, key=f"{cle}_b",
            disabled=st.session_state[k_fait],
        )

    if not st.session_state[k_fait]:
        if st.button("✅ Valider", key=f"{cle}_valider", type="primary"):
            st.session_state[k_fait] = True
            st.rerun()
        return

    if st.button("🔄 Nouvelle règle", key=f"{cle}_nouveau"):
        for k in list(st.session_state.keys()):
            if k.startswith(cle):
                st.session_state.pop(k, None)
        st.rerun()

    st.markdown("---")
    verdict = st.session_state.get(f"{cle}_verdict")
    val_a = st.session_state.get(f"{cle}_a", 1.0)
    val_b = st.session_state.get(f"{cle}_b", 1.0)

    dit_vraie = verdict == "Vraie pour tous les nombres"

    if verdict is None:
        st.warning("Aucun verdict donné. Voici la correction.")
    elif dit_vraie == regle["vraie"]:
        if regle["vraie"]:
            st.success("✅ Verdict correct : cette règle est bien **vraie**.")
        else:
            st.success("✅ Verdict correct : cette règle est **fausse**.")
    else:
        st.error(
            f"❌ Verdict incorrect : cette règle est en réalité "
            f"**{'vraie' if regle['vraie'] else 'fausse'}**."
        )

    # Test numérique du contre-exemple proposé
    if not regle["vraie"] and verdict == "Fausse":
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
                    f"b = {val_b:g}, les deux membres diffèrent. "
                    "Une seule valeur suffit à démolir une règle prétendument "
                    "générale — c'est la méthode qu'il faut retenir."
                )
            else:
                st.warning(
                    f"⚠️ Avec ces valeurs, les deux membres coïncident : ce n'est "
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
    with st.container(border=True):
        st.markdown("**1. Identifier — de quel type d'énoncé s'agit-il ?**")
        st.markdown(
            "Une règle du type « pour tous $a$, $b$ » est une affirmation "
            "**universelle**. Deux régimes de preuve, radicalement asymétriques :\n\n"
            "- pour la **réfuter** : un seul contre-exemple suffit ;\n"
            "- pour la **prouver** : aucun nombre d'exemples ne suffit, "
            "il faut une démonstration générale."
        )
    with st.container(border=True):
        st.markdown("**2. Calculer — tester les valeurs les plus simples**")
        st.markdown(
            "Commencez par $a = b = 1$, puis $a = 1, b = 2$. "
            "Évitez $0$ (souvent hors domaine) et méfiez-vous des cas trop "
            "symétriques, qui peuvent coïncider par accident."
        )
    with st.container(border=True):
        st.markdown("**3. Vérifier — le verdict sur cette règle**")
        st.markdown(regle["explication"])
    with st.container(border=True):
        st.markdown("**4. Interpréter — ce que cela vous coûte à l'examen**")
        st.markdown(
            "Ces erreurs ne sont pas des étourderies : elles reviennent parce "
            "qu'on suppose implicitement que toute opération « se distribue ». "
            "Le réflexe à installer est de **tester avant d'écrire**, en cinq "
            "secondes, dès qu'une règle vous paraît trop commode."
        )


# ==========================================================================
# MISE EN PAGE
# ==========================================================================

st.markdown("---")

onglets = st.tabs(
    [
        "1️⃣ Ordres de grandeur",
        "2️⃣ Fractions emboîtées",
        "3️⃣ Fractions littérales",
        "4️⃣ Puissances",
        "5️⃣ Racines carrées",
        "6️⃣ Intérêts composés",
        "7️⃣ Vrai ou faux ?",
    ]
)

with onglets[0]:
    st.subheader("Notation scientifique et dépense par habitant")
    executer("p1_ordre", gen_ordre_de_grandeur)

with onglets[1]:
    st.subheader("Une part d'une part")
    executer("p1_frac_emb", gen_fractions_emboitees)

with onglets[2]:
    st.subheader("Fractions avec des lettres")
    executer("p1_frac_lit", gen_fractions_litterales)

with onglets[3]:
    st.subheader("Règles de puissances")
    executer("p1_puiss", gen_puissances)

with onglets[4]:
    st.subheader("Racines carrées")
    executer("p1_racines", gen_racines)

with onglets[5]:
    st.subheader("Coefficient multiplicateur et puissance")
    executer("p1_placement", gen_placement)

with onglets[6]:
    st.subheader("Réfuter une règle par un contre-exemple")
    famille_contre_exemple()

st.markdown("---")
st.caption(
    "Séance de pré-rentrée n°1 — Nombres, fractions et puissances · "
    "Fil rouge A : le budget de Villeneuve · "
    "Mathématiques appliquées pour les sciences humaines et sociales, Sciences Po."
)
