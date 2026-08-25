"""
Série P1 — Fractions et puissances
Séance de pré-rentrée n°1 : nombres, fractions, puissances.
Fil rouge A : le budget de Villeneuve.
"""

import math
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
manipuler des **fractions**, appliquer les **règles de puissances**,
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
    st.markdown("**Écriture scientifique** ($1 \\leqslant a < 10$)")
    st.latex(r"a \times 10^{n}")
    st.caption("Un million = $10^{6}$ · Un milliard = $10^{9}$")
    st.latex(
        r"\frac{a \times 10^{n}}{b \times 10^{p}} = \frac{a}{b} \times 10^{n-p}"
    )
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


def _sci(valeur: float) -> tuple[float, int]:
    """(mantisse, exposant) tels que valeur = mantisse × 10**exposant, 1 ⩽ mantisse < 10."""
    exposant = math.floor(math.log10(valeur))
    mantisse = valeur / 10**exposant
    if mantisse >= 10:  # garde-fou contre l'imprécision flottante de log10
        mantisse, exposant = mantisse / 10, exposant + 1
    elif mantisse < 1:
        mantisse, exposant = mantisse * 10, exposant - 1
    return mantisse, exposant


def _etapes_grandeur(
    conversion_texte: str,
    mant_n: float, exp_n: int,
    mant_d: float, exp_d: int,
    reponse: float,
    verif_texte: str,
    interpret_texte: str,
    unite_reponse: str = "€",
) -> list:
    diff = exp_n - exp_d
    return [
        Etape(
            "Identifier — pourquoi la notation scientifique",
            "On divise une très grande quantité par une grande quantité. "
            "Poser la division telle quelle est pénible ; en notation scientifique, "
            "elle devient immédiate car les puissances de 10 se traitent séparément.",
        ),
        Etape(
            "Écrire les deux nombres en notation scientifique",
            conversion_texte,
            rf"a \times 10^{{n}} = {mant_n:g} \times 10^{{{exp_n}}}"
            rf"\qquad b \times 10^{{p}} = {mant_d:g} \times 10^{{{exp_d}}}",
        ),
        Etape(
            "Calculer — séparer mantisses et puissances",
            "On applique $\\dfrac{a \\times 10^n}{b \\times 10^p} "
            "= \\dfrac{a}{b} \\times 10^{n-p}$ : les mantisses d'un côté, "
            "les puissances de 10 de l'autre.",
            rf"\frac{{{mant_n:g} \times 10^{{{exp_n}}}}}{{{mant_d:g} \times 10^{{{exp_d}}}}}"
            rf" = \frac{{{mant_n:g}}}{{{mant_d:g}}} \times 10^{{{diff}}}"
            rf" \approx {mant_n/mant_d:.3f} \times 10^{{{diff}}}"
            rf" \approx {reponse:.0f}\ \text{{{unite_reponse}}}",
        ),
        Etape("Vérifier — le résultat est-il plausible ?", verif_texte),
        Etape("Interpréter", interpret_texte),
    ]


def _pieges_grandeur(
    num_brut: float, num_facteur: float, denom_val: float,
    exp_n: int, exp_d: int, reponse: float,
    conversion_manquante_texte: str, num_role_texte: str, question_texte: str,
) -> list:
    diff = exp_n - exp_d
    puissance_manquante = round(math.log10(num_facteur))
    pieges = [
        (
            num_brut / denom_val,
            f"Vous avez divisé les deux nombres **sans convertir** "
            f"{conversion_manquante_texte} : votre résultat est dans la mauvaise "
            f"unité. Il manque un facteur $10^{{{puissance_manquante}}}$.",
        ),
    ]
    if diff != 0:  # sinon ces deux pièges dégénèrent en la bonne réponse
        pieges.append((
            reponse / 10**diff,
            "Vous avez correctement divisé les mantisses mais **perdu la puissance "
            f"de 10** : $10^{{{exp_n}}} / 10^{{{exp_d}}} = 10^{{{diff}}}$, pas $10^{{0}}$.",
        ))
        pieges.append((
            reponse * 10**diff,
            "Vous avez une puissance de 10 **en trop** : vérifiez le calcul "
            f"$10^{{{exp_n}}} / 10^{{{exp_d}}}$ — on **soustrait** les exposants.",
        ))
    pieges.append((
        denom_val / (num_brut * num_facteur),
        f"Vous avez divisé dans le **mauvais sens** : la question demande "
        f"{question_texte}, donc {num_role_texte} au numérateur.",
    ))
    return pieges


def _og_ville() -> Exercice:
    budget = random.choice([150, 180, 210, 240, 300, 360])  # en M€
    pop = random.choice([120_000, 150_000, 180_000, 200_000, 240_000, 250_000])
    num_val, denom_val = budget * 1e6, pop
    reponse = num_val / denom_val
    mant_n, exp_n = _sci(num_val)
    mant_d, exp_d = _sci(denom_val)

    pop_txt = f"{pop:,}".replace(",", " ")
    enonce = f"""
> **Villeneuve.** Le budget annuel de la ville s'élève à **{budget} millions d'euros**
> pour **{pop_txt} habitants**.
>
> Quelle est la **dépense annuelle par habitant** ? Répondez en euros, sans calculatrice.
"""

    etapes = _etapes_grandeur(
        f"Le budget est exprimé en **millions** d'euros : "
        f"{budget} M€ = {budget} × 10⁶ € = {mant_n:g} × 10^{exp_n} €. "
        "C'est la conversion que l'on oublie le plus souvent.",
        mant_n, exp_n, mant_d, exp_d, reponse,
        "Une commune française dépense typiquement de l'ordre de **1 000 à "
        "2 000 € par habitant et par an**. Un résultat en centimes ou en "
        "millions signalerait une erreur de conversion, pas une erreur de calcul.",
        f"Chaque habitant de Villeneuve « coûte » environ **{_fmt(reponse, 0)} €** "
        "de dépense publique locale par an. Ce nombre n'a de sens que **comparé** : "
        "à une autre ville, à une autre année, ou à la moyenne nationale. "
        "C'est tout l'objet de la séance 2.",
        unite_reponse="€/habitant",
    )
    pieges = _pieges_grandeur(
        budget, 1e6, denom_val, exp_n, exp_d, reponse,
        "les millions d'euros en euros", "le budget", "des euros *par habitant*",
    )

    return Exercice(
        enonce=enonce, reponse=reponse, etapes=etapes,
        libelle="Dépense par habitant", unite="€", tolerance=0.01,
        indice="Convertissez d'abord les millions d'euros en euros. "
        "Puis divisez les mantisses d'un côté, les puissances de 10 de l'autre.",
        pieges=pieges,
    )


def _og_departement() -> Exercice:
    budget_md = random.choice([1, 2, 3, 4, 5, 6])  # en Md€
    pop = random.choice(
        [800_000, 1_000_000, 1_200_000, 1_500_000, 1_800_000, 2_200_000, 2_800_000]
    )
    num_val, denom_val = budget_md * 1e9, pop
    reponse = num_val / denom_val
    mant_n, exp_n = _sci(num_val)
    mant_d, exp_d = _sci(denom_val)

    pop_txt = f"{pop:,}".replace(",", " ")
    unite_md = "milliard" + ("s" if budget_md > 1 else "")
    enonce = f"""
> **Le département dont dépend Villeneuve.** Son budget annuel s'élève à
> **{budget_md} {unite_md} d'euros** pour **{pop_txt} habitants**.
>
> Quelle est la **dépense annuelle par habitant** ? Répondez en euros, sans calculatrice.
"""

    etapes = _etapes_grandeur(
        f"Le budget est exprimé en **milliards** d'euros : "
        f"{budget_md} Md€ = {budget_md} × 10⁹ € = {mant_n:g} × 10^{exp_n} €. "
        "Une échelle bien plus grande que celle d'une commune.",
        mant_n, exp_n, mant_d, exp_d, reponse,
        "À l'échelle d'un département, la dépense par habitant reste en général de "
        "l'ordre de **quelques centaines à quelques milliers d'euros**. Un résultat "
        "en centimes ou en centaines de milliers signalerait une erreur de conversion.",
        f"Le département dépense environ **{_fmt(reponse, 0)} €** par habitant et "
        "par an — un ordre de grandeur différent de celui de la ville, alors que la "
        "méthode de calcul est rigoureusement identique. C'est ce qui compte : la "
        "méthode ne dépend pas de l'échelle.",
        unite_reponse="€/habitant",
    )
    pieges = _pieges_grandeur(
        budget_md, 1e9, denom_val, exp_n, exp_d, reponse,
        "les milliards d'euros en euros", "le budget", "des euros *par habitant*",
    )

    return Exercice(
        enonce=enonce, reponse=reponse, etapes=etapes,
        libelle="Dépense par habitant", unite="€", tolerance=0.01,
        indice="Convertissez d'abord les milliards d'euros en euros. "
        "Puis divisez les mantisses d'un côté, les puissances de 10 de l'autre.",
        pieges=pieges,
    )


def _og_ecole() -> Exercice:
    budget = random.choice([10, 12, 15, 18, 20, 25])  # M€, budget scolaire de la ville
    nb_eleves = random.choice([2_000, 2_500, 3_000, 4_000, 5_000, 6_000, 8_000])
    num_val, denom_val = budget * 1e6, nb_eleves
    reponse = num_val / denom_val
    mant_n, exp_n = _sci(num_val)
    mant_d, exp_d = _sci(denom_val)

    nb_txt = f"{nb_eleves:,}".replace(",", " ")
    enonce = f"""
> **Villeneuve.** Le budget consacré aux établissements scolaires s'élève à
> **{budget} millions d'euros** par an, pour **{nb_txt} élèves** scolarisés dans la ville.
>
> Quel est le **coût annuel par élève** ? Répondez en euros, sans calculatrice.
"""

    etapes = _etapes_grandeur(
        f"Le budget est exprimé en **millions** d'euros : "
        f"{budget} M€ = {budget} × 10⁶ € = {mant_n:g} × 10^{exp_n} €. "
        "Le nombre d'élèves, lui, se compte déjà en milliers.",
        mant_n, exp_n, mant_d, exp_d, reponse,
        "Un établissement scolaire coûte typiquement de l'ordre de **quelques "
        "milliers d'euros par élève et par an**, tout compris (personnel, locaux, "
        "matériel). Un résultat en dizaines d'euros ou en millions signalerait une "
        "erreur de conversion.",
        f"Chaque élève « coûte » environ **{_fmt(reponse, 0)} €** par an à la "
        "collectivité. Ce chiffre est de la même nature que la dépense par habitant "
        "vue plus haut : un budget total rapporté à un effectif.",
        unite_reponse="€/élève",
    )
    pieges = _pieges_grandeur(
        budget, 1e6, denom_val, exp_n, exp_d, reponse,
        "les millions d'euros en euros", "le budget", "un coût *par élève*",
    )

    return Exercice(
        enonce=enonce, reponse=reponse, etapes=etapes,
        libelle="Coût par élève", unite="€", tolerance=0.01,
        indice="Convertissez d'abord les millions d'euros en euros. "
        "Puis divisez les mantisses d'un côté, les puissances de 10 de l'autre.",
        pieges=pieges,
    )


def _og_voirie() -> Exercice:
    budget = random.choice([2, 3, 4, 5, 6, 8, 10])  # M€, entretien de la voirie
    km = random.choice([80, 100, 150, 200, 250, 300, 400, 500])
    num_val, denom_val = budget * 1e6, km
    reponse = num_val / denom_val
    mant_n, exp_n = _sci(num_val)
    mant_d, exp_d = _sci(denom_val)

    enonce = f"""
> **Villeneuve.** Le budget d'entretien de la voirie s'élève à
> **{budget} millions d'euros** par an, pour **{km} kilomètres** de routes communales.
>
> Quel est le **coût annuel par kilomètre entretenu** ? Répondez en euros, sans calculatrice.
"""

    etapes = _etapes_grandeur(
        f"Le budget est exprimé en **millions** d'euros : "
        f"{budget} M€ = {budget} × 10⁶ € = {mant_n:g} × 10^{exp_n} €. "
        "Le linéaire de voirie, lui, se compte déjà en kilomètres.",
        mant_n, exp_n, mant_d, exp_d, reponse,
        "L'entretien de voirie coûte, selon les tronçons, de quelques milliers à "
        "plusieurs dizaines de milliers d'euros par kilomètre et par an. Un résultat "
        "en centimes ou en dizaines de millions signalerait une erreur de conversion.",
        f"Chaque kilomètre de voirie coûte environ **{_fmt(reponse, 0)} €** par an à "
        "entretenir. Multiplié par tout le réseau communal, ce chiffre explique une "
        "part importante du budget des transports.",
        unite_reponse="€/km",
    )
    pieges = _pieges_grandeur(
        budget, 1e6, denom_val, exp_n, exp_d, reponse,
        "les millions d'euros en euros", "le budget", "un coût *par kilomètre*",
    )

    return Exercice(
        enonce=enonce, reponse=reponse, etapes=etapes,
        libelle="Coût par kilomètre", unite="€", tolerance=0.01,
        indice="Convertissez d'abord les millions d'euros en euros. "
        "Puis divisez les mantisses d'un côté, les puissances de 10 de l'autre.",
        pieges=pieges,
    )


def _og_pib() -> Exercice:
    # (PIB en Md€, population en millions) — paires choisies pour rester dans une
    # fourchette de PIB par habitant plausible (quelques milliers à ~50 000 €).
    budget_md, pop_millions = random.choice(
        [
            (50, 20), (80, 15), (120, 10), (200, 25), (300, 8),
            (400, 30), (600, 12), (800, 40), (150, 5), (1000, 50),
        ]
    )
    num_val, denom_val = budget_md * 1e9, pop_millions * 1e6
    reponse = num_val / denom_val
    mant_n, exp_n = _sci(num_val)
    mant_d, exp_d = _sci(denom_val)

    enonce = f"""
> **Économie.** Un pays — appelons-le la Norlandie — produit une richesse totale
> (PIB) de **{budget_md} milliards d'euros** par an, pour une population de
> **{pop_millions} millions d'habitants**.
>
> Quel est le **PIB par habitant** de ce pays ? Répondez en euros, sans calculatrice.
"""

    etapes = _etapes_grandeur(
        f"Le PIB est exprimé en **milliards** d'euros : "
        f"{budget_md} Md€ = {budget_md} × 10⁹ € = {mant_n:g} × 10^{exp_n} €. "
        "La population, en millions, se convertit de la même façon.",
        mant_n, exp_n, mant_d, exp_d, reponse,
        "Le PIB par habitant se situe, selon les pays, entre quelques milliers et "
        "environ 50 000 € par an. Un résultat en centimes ou en millions signalerait "
        "une erreur de conversion.",
        f"Le PIB par habitant de la Norlandie est d'environ **{_fmt(reponse, 0)} €**. "
        "C'est l'indicateur le plus utilisé pour comparer des économies, mais il ne "
        "dit rien des **inégalités internes** : deux pays au même PIB par habitant "
        "peuvent avoir des niveaux de vie très différents selon la façon dont la "
        "richesse y est répartie.",
        unite_reponse="€/habitant",
    )
    pieges = _pieges_grandeur(
        budget_md, 1e9, denom_val, exp_n, exp_d, reponse,
        "les milliards d'euros en euros", "le PIB", "des euros *par habitant*",
    )

    return Exercice(
        enonce=enonce, reponse=reponse, etapes=etapes,
        libelle="PIB par habitant", unite="€", tolerance=0.01,
        indice="Convertissez d'abord milliards et millions en euros et en habitants. "
        "Puis divisez les mantisses d'un côté, les puissances de 10 de l'autre.",
        pieges=pieges,
    )


def _og_carbone() -> Exercice:
    # (émissions en Mt de CO2, population en millions).
    emissions_mt, pop_millions = random.choice(
        [
            (100, 10), (300, 20), (50, 25), (400, 10), (150, 30),
            (600, 15), (80, 40), (250, 50), (900, 45), (60, 6),
        ]
    )
    num_val, denom_val = emissions_mt * 1e6, pop_millions * 1e6
    reponse = num_val / denom_val
    mant_n, exp_n = _sci(num_val)
    mant_d, exp_d = _sci(denom_val)

    enonce = f"""
> **Environnement.** Un pays industrialisé émet **{emissions_mt} millions de tonnes
> de CO2** par an, pour une population de **{pop_millions} millions d'habitants**.
>
> Quelle est l'**empreinte carbone par habitant** de ce pays, en tonnes de CO2 par an ?
> Sans calculatrice.
"""

    etapes = _etapes_grandeur(
        f"Les émissions sont exprimées en **millions de tonnes** : "
        f"{emissions_mt} Mt = {emissions_mt} × 10⁶ t = {mant_n:g} × 10^{exp_n} t. "
        "La population, en millions, se convertit de la même façon.",
        mant_n, exp_n, mant_d, exp_d, reponse,
        "Selon les pays, un habitant émet entre 2 et 20 tonnes de CO2 par an ; les "
        "plus gros émetteurs par habitant dépassent parfois 30 tonnes. Un résultat "
        "en dixièmes de tonne ou en milliers de tonnes signalerait une erreur de "
        "conversion.",
        f"Ce pays émet environ **{_fmt(reponse, 1)} tonnes de CO2 par habitant** et "
        "par an. Ramener une grandeur nationale à l'échelle individuelle est ce qui "
        "permet de comparer des pays de tailles très différentes sur un pied "
        "d'égalité — la même logique que le PIB par habitant.",
        unite_reponse="t CO2/habitant",
    )
    pieges = _pieges_grandeur(
        emissions_mt, 1e6, denom_val, exp_n, exp_d, reponse,
        "les millions de tonnes en tonnes", "les émissions", "des tonnes *par habitant*",
    )

    return Exercice(
        enonce=enonce, reponse=reponse, etapes=etapes,
        libelle="Émissions par habitant", unite="t CO2", tolerance=0.01,
        indice="Convertissez les deux quantités en unités de base (tonnes, "
        "habitants). Puis divisez les mantisses d'un côté, les puissances de 10 "
        "de l'autre.",
        pieges=pieges,
    )


def _og_densite() -> Exercice:
    # (population en millions, superficie en km²) — du territoire très peu peuplé
    # au territoire très dense.
    pop_millions, superficie_km2 = random.choice(
        [
            (10, 50_000), (5, 20_000), (60, 550_000), (25, 250_000),
            (80, 400_000), (15, 900_000), (10, 9_000_000), (120, 300_000),
            (8, 80_000), (200, 3_000_000),
        ]
    )
    num_val, denom_val = pop_millions * 1e6, superficie_km2
    reponse = num_val / denom_val
    mant_n, exp_n = _sci(num_val)
    mant_d, exp_d = _sci(denom_val)

    superficie_txt = f"{superficie_km2:,}".replace(",", " ")
    enonce = f"""
> **Géographie humaine.** Un territoire compte **{pop_millions} millions d'habitants**
> répartis sur **{superficie_txt} km²**.
>
> Quelle est la **densité de population** de ce territoire, en habitants par km² ?
> Sans calculatrice.
"""

    etapes = _etapes_grandeur(
        f"La population est exprimée en **millions** : "
        f"{pop_millions} millions = {pop_millions} × 10⁶ hab. = "
        f"{mant_n:g} × 10^{exp_n} hab. La superficie, en km², est déjà une unité de base.",
        mant_n, exp_n, mant_d, exp_d, reponse,
        "La densité de population varie énormément selon les territoires : de moins "
        "de 5 habitants par km² dans les zones les plus vastes et les moins peuplées, "
        "à plusieurs centaines dans les territoires les plus denses. Un résultat en "
        "dizaines de milliers ou en millièmes signalerait une erreur de conversion.",
        f"Ce territoire compte environ **{_fmt(reponse, 1)} habitants par km²**. "
        "Contrairement aux exemples précédents, ce rapport ne divise pas un budget "
        "par un effectif mais un effectif par une surface : la méthode de notation "
        "scientifique reste exactement la même, ce qui montre qu'elle s'applique à "
        "n'importe quel rapport de deux grandeurs, pas seulement à des calculs "
        "monétaires.",
        unite_reponse="hab./km²",
    )
    pieges = _pieges_grandeur(
        pop_millions, 1e6, denom_val, exp_n, exp_d, reponse,
        "les millions d'habitants en habitants", "la population",
        "des habitants *par km²*",
    )

    return Exercice(
        enonce=enonce, reponse=reponse, etapes=etapes,
        libelle="Densité de population", unite="hab./km²", tolerance=0.01,
        indice="Convertissez d'abord les millions d'habitants en habitants. "
        "Puis divisez les mantisses d'un côté, les puissances de 10 de l'autre.",
        pieges=pieges,
    )


def _og_medecins() -> Exercice:
    # (médecins en milliers, population en millions) — convention de santé
    # publique : un taux « pour 100 000 habitants ».
    medecins_k, pop_millions = random.choice(
        [
            (200, 60), (150, 40), (80, 20), (300, 80), (50, 10),
            (400, 100), (100, 50), (60, 30), (250, 70), (30, 15),
        ]
    )
    medecins, pop = medecins_k * 1000, pop_millions * 1_000_000
    reponse = medecins / pop * 100_000

    mant_n, exp_n = _sci(medecins)
    mant_d, exp_d = _sci(pop)
    diff = exp_n - exp_d

    pop_txt = f"{pop:,}".replace(",", " ")
    medecins_txt = f"{medecins:,}".replace(",", " ")

    enonce = f"""
> **Démographie médicale.** Un pays compte **{medecins_txt} médecins en activité**
> pour une population de **{pop_txt} habitants**.
>
> En épidémiologie et en santé publique, ce type de rapport s'exprime presque
> toujours **pour 100 000 habitants**. Combien ce pays compte-t-il de **médecins
> pour 100 000 habitants** ? Arrondissez à l'unité.
"""

    etapes = [
        Etape(
            "Identifier — pourquoi « pour 100 000 habitants »",
            "Le rapport brut médecins/habitants est un nombre minuscule, illisible "
            "tel quel. La convention en démographie et en santé publique est de le "
            "**multiplier par 100 000** pour obtenir un nombre lisible, comparable "
            "d'un pays à l'autre.",
        ),
        Etape(
            "Écrire les deux nombres en notation scientifique",
            f"{medecins_txt} médecins et {pop_txt} habitants.",
            rf"a \times 10^{{n}} = {mant_n:g} \times 10^{{{exp_n}}}\ \text{{médecins}}"
            rf"\qquad b \times 10^{{p}} = {mant_d:g} \times 10^{{{exp_d}}}\ \text{{hab.}}",
        ),
        Etape(
            "Calculer le taux brut, puis ramener à 100 000 habitants",
            "On divise, puis on multiplie par $10^5$ : les deux opérations se "
            "traitent en une seule fois sur les puissances de 10.",
            rf"\frac{{{mant_n:g} \times 10^{{{exp_n}}}}}{{{mant_d:g} \times 10^{{{exp_d}}}}}"
            rf" \times 10^{{5}} = \frac{{{mant_n:g}}}{{{mant_d:g}}} \times 10^{{{diff}+5}}"
            rf" \approx {mant_n/mant_d:.3f} \times 10^{{{diff+5}}} \approx {reponse:.0f}",
        ),
        Etape(
            "Vérifier — le résultat est-il plausible ?",
            "Selon les pays, on compte de l'ordre de **100 à 500 médecins pour "
            "100 000 habitants**. Un résultat à un chiffre ou à six chiffres "
            "signalerait une erreur de conversion.",
        ),
        Etape(
            "Interpréter",
            f"Ce pays compte environ **{round(reponse)} médecins pour 100 000 "
            "habitants**. Cette mise à l'échelle permet de comparer des pays de "
            "tailles très différentes : un grand pays a mécaniquement plus de "
            "médecins qu'un petit, mais pas forcément plus **par habitant**.",
        ),
    ]

    pieges = [
        (
            medecins / pop,
            "Vous avez oublié de **multiplier par 100 000** : votre résultat est le "
            "taux brut, illisible tel quel.",
        ),
        (
            medecins / pop * 1000,
            "Vous avez multiplié par 1 000 au lieu de 100 000 : relisez la "
            "convention « pour 100 000 habitants ».",
        ),
        (
            pop / medecins * 100_000,
            "Vous avez divisé dans le **mauvais sens** : ce sont les médecins qu'on "
            "rapporte à la population, pas l'inverse.",
        ),
        (
            medecins_k / pop_millions,
            "Vous avez divisé les nombres **tels qu'affichés** (en milliers et en "
            "millions) sans les ramener à la même unité de base avant de calculer "
            "le taux.",
        ),
    ]

    return Exercice(
        enonce=enonce, reponse=reponse, etapes=etapes,
        libelle="Médecins pour 100 000 habitants", tolerance_abs=1,
        indice="Divisez d'abord le nombre de médecins par la population, puis "
        "multipliez par 100 000 pour obtenir un taux lisible.",
        pieges=pieges,
    )


def gen_ordre_de_grandeur() -> Exercice:
    return random.choice(
        [
            _og_ville, _og_departement, _og_ecole, _og_voirie,
            _og_pib, _og_carbone, _og_densite, _og_medecins,
        ]
    )()


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


def gen_fractions_operations() -> Exercice:
    modele = random.choice(["somme", "difference", "division", "inverses"])
    denoms = [2, 3, 4, 5, 6, 8, 9, 10, 12]

    if modele == "somme":
        q1, q2 = random.sample(denoms, 2)
        n1 = random.randint(1, q1 - 1)
        n2 = random.randint(1, q2 - 1)
        commun = q1 * q2
        reponse = float(Fraction(n1, q1) + Fraction(n2, q2))
        expression = rf"\frac{{{n1}}}{{{q1}}} + \frac{{{n2}}}{{{q2}}}"
        etapes = [
            Etape(
                "Identifier — une somme de fractions",
                "Pour additionner deux fractions, il faut d'abord les mettre au "
                "**même dénominateur**. Le produit des deux dénominateurs "
                f"convient toujours (ici {q1} × {q2} = {commun}), même s'il "
                "n'est pas le plus petit.",
            ),
            Etape(
                "Mettre au même dénominateur",
                "On multiplie chaque fraction par ce qui lui manque.",
                rf"\frac{{{n1}}}{{{q1}}} + \frac{{{n2}}}{{{q2}}} = "
                rf"\frac{{{n1*q2}}}{{{commun}}} + \frac{{{n2*q1}}}{{{commun}}}",
            ),
            Etape(
                "Additionner les numérateurs",
                "Le dénominateur ne change plus.",
                rf"= \frac{{{n1*q2} + {n2*q1}}}{{{commun}}} = "
                rf"\frac{{{n1*q2+n2*q1}}}{{{commun}}} \approx {reponse:.4f}",
            ),
            Etape(
                "Vérifier — encadrement rapide",
                f"Chaque fraction est inférieure à 1, donc la somme doit être "
                f"inférieure à 2 : {_fmt(reponse, 4)} satisfait bien cet "
                "encadrement.",
            ),
            Etape(
                "Interpréter",
                "Regrouper deux fractions en une seule est le geste qui "
                "reviendra sans cesse : pour combiner deux parts en "
                "statistique, ou factoriser un résultat en calcul de dérivée.",
            ),
        ]
        pieges = [
            (float(Fraction(n1 + n2, q1 + q2)),
             "Vous avez additionné **les numérateurs entre eux et les "
             "dénominateurs entre eux**. C'est faux : testez avec deux "
             "moitiés, $\\frac12+\\frac12=1$, et non $\\frac24$ (qui vaut "
             "$\\frac12$)."),
            (float(Fraction(n1 + n2, commun)),
             "Vous avez trouvé le bon dénominateur commun mais oublié de "
             "**multiplier aussi les numérateurs** par ce qui manquait à "
             "chacun."),
        ]
        libelle, indice = "Résultat", (
            "Cherchez un dénominateur commun — le produit des deux convient "
            "toujours — puis convertissez chaque numérateur."
        )

    elif modele == "difference":
        while True:
            q1, q2 = random.sample(denoms, 2)
            n1 = random.randint(1, q1 - 1)
            n2 = random.randint(1, q2 - 1)
            if Fraction(n1, q1) > Fraction(n2, q2):
                break
        commun = q1 * q2
        reponse = float(Fraction(n1, q1) - Fraction(n2, q2))
        expression = rf"\frac{{{n1}}}{{{q1}}} - \frac{{{n2}}}{{{q2}}}"
        etapes = [
            Etape(
                "Identifier — une différence de fractions",
                "Même règle que pour la somme : dénominateur commun d'abord. "
                "Le signe moins porte sur **tout** le numérateur de la "
                "seconde fraction.",
            ),
            Etape(
                "Mettre au même dénominateur",
                f"Le dénominateur commun est {q1} × {q2} = {commun}.",
                rf"\frac{{{n1}}}{{{q1}}} - \frac{{{n2}}}{{{q2}}} = "
                rf"\frac{{{n1*q2}}}{{{commun}}} - \frac{{{n2*q1}}}{{{commun}}}",
            ),
            Etape(
                "Soustraire",
                "",
                rf"= \frac{{{n1*q2} - {n2*q1}}}{{{commun}}} = "
                rf"\frac{{{n1*q2-n2*q1}}}{{{commun}}} \approx {reponse:.4f}",
            ),
            Etape(
                "Vérifier — le signe",
                "Le résultat doit être **positif**, puisque la première "
                "fraction est plus grande que la seconde : "
                f"{_fmt(reponse, 4)} confirme ce sens.",
            ),
            Etape(
                "Interpréter",
                "Si le numérateur final avait été négatif, l'expression "
                "entière aurait changé de signe : c'est exactement ce type de "
                "lecture qui servira à déterminer si une grandeur croît ou "
                "décroît.",
            ),
        ]
        pieges = [
            (float(Fraction(n2, q2) - Fraction(n1, q1)),
             "Vous avez **inversé l'ordre** de la soustraction : le résultat "
             "a le bon dénominateur mais le mauvais signe."),
            (float(Fraction(n1, q1) + Fraction(n2, q2)),
             "Vous avez **additionné** au lieu de soustraire : relisez "
             "l'énoncé, c'est bien une différence."),
        ]
        libelle, indice = "Résultat", (
            "Même méthode que pour une somme, mais le signe moins porte sur "
            "tout le numérateur de la seconde fraction."
        )

    elif modele == "division":
        k = random.randint(2, 9)
        c, d = random.sample(denoms, 2)
        reponse = float(Fraction(d, c))
        expression = rf"\frac{{{k}}}{{{c}}} \div \frac{{{k}}}{{{d}}}"
        etapes = [
            Etape(
                "Identifier — diviser deux fractions",
                "Diviser par une fraction, c'est **multiplier par son "
                "inverse**. Ici, les deux fractions partagent le même "
                "numérateur — un point commun qui va se simplifier tout "
                "seul.",
            ),
            Etape(
                "Transformer la division en multiplication",
                "On retourne la seconde fraction.",
                rf"\frac{{{k}}}{{{c}}} \div \frac{{{k}}}{{{d}}} = "
                rf"\frac{{{k}}}{{{c}}} \times \frac{{{d}}}{{{k}}}",
            ),
            Etape(
                "Simplifier",
                f"Le facteur {k} apparaît au numérateur **et** au "
                "dénominateur : il se simplifie directement.",
                rf"= \frac{{{k} \times {d}}}{{{c} \times {k}}} = "
                rf"\frac{{{d}}}{{{c}}} \approx {reponse:.4f}",
            ),
            Etape(
                "Vérifier — plausibilité",
                (f"{d} > {c}, donc le résultat doit être **supérieur à 1**."
                 if d > c else
                 f"{d} < {c}, donc le résultat doit être **inférieur à 1**.")
                + f" C'est bien le cas : {_fmt(reponse, 4)}.",
            ),
            Etape(
                "Interpréter",
                "Reconnaître qu'un facteur commun se simplifie avant de "
                "multiplier évite des calculs inutiles — un réflexe payant à "
                "l'examen.",
            ),
        ]
        pieges = [
            (float(Fraction(c, d)),
             "Vous avez inversé le rapport : c'est la **seconde** fraction "
             "que l'on retourne, pas la première."),
            (float(Fraction(k * k, c * d)),
             "Vous avez **multiplié** les deux fractions au lieu de diviser : "
             "il fallait retourner la seconde."),
        ]
        libelle, indice = "Résultat", (
            "Retournez la seconde fraction et multipliez. Le numérateur "
            "commun aux deux fractions se simplifie."
        )

    else:  # inverses
        n1, n2 = random.sample([2, 3, 4, 5, 6, 7, 8, 9], 2)
        commun = n1 * n2
        reponse = float(Fraction(1, n1) + Fraction(1, n2))
        expression = rf"\frac{{1}}{{{n1}}} + \frac{{1}}{{{n2}}}"
        etapes = [
            Etape(
                "Identifier — le piège numéro un du programme",
                f"La tentation est d'écrire $\\frac{{1}}{{{n1}+{n2}}}$. C'est "
                "faux, et c'est l'erreur la plus fréquente de toute l'année.",
            ),
            Etape(
                "Mettre au même dénominateur",
                f"Le dénominateur commun est le produit ${n1} \\times {n2} = "
                f"{commun}$.",
                rf"\frac{{1}}{{{n1}}} + \frac{{1}}{{{n2}}} = "
                rf"\frac{{{n2}}}{{{commun}}} + \frac{{{n1}}}{{{commun}}}",
            ),
            Etape(
                "Additionner",
                "",
                rf"= \frac{{{n1+n2}}}{{{commun}}} \approx {reponse:.4f}",
            ),
            Etape(
                "Vérifier — le contre-exemple qui tranche",
                f"La valeur correcte vaut environ {reponse:.4f}, tandis que "
                f"le raccourci $\\frac{{1}}{{{n1}+{n2}}} \\approx "
                f"{1/(n1+n2):.4f}$ donne un résultat différent — la preuve "
                "que ce raccourci est faux.",
            ),
            Etape(
                "Interpréter",
                "Cette forme réapparaîtra telle quelle au semestre, dans le "
                "calcul de moyennes harmoniques et de vitesses moyennes — "
                "deux objets où le raccourci donne un résultat absurde.",
            ),
        ]
        pieges = [
            (float(Fraction(1, n1 + n2)),
             "C'est **l'erreur interdite** de la séance : "
             f"$\\frac{{1}}{{{n1}}}+\\frac{{1}}{{{n2}}} \\neq "
             f"\\frac{{1}}{{{n1}+{n2}}}$."),
            (float(Fraction(2, n1 + n2)),
             "Vous avez additionné les numérateurs sans passer par le bon "
             "dénominateur commun : c'est le **produit**, pas la somme, "
             "qu'il fallait utiliser."),
        ]
        libelle, indice = "Résultat", (
            "N'écrivez jamais $\\frac{1}{a}+\\frac{1}{b}$ comme "
            "$\\frac{1}{a+b}$. Passez par le dénominateur commun, qui est un "
            "produit."
        )

    enonce = f"""
> Calculez le résultat suivant :
>
> $$ {expression} $$
"""

    return Exercice(
        enonce=enonce,
        reponse=reponse,
        etapes=etapes,
        libelle=libelle,
        tolerance=0.001,
        indice=indice,
        pieges=pieges,
    )


# --- Famille 4 : puissances -------------------------------------------------


def gen_puissances() -> Exercice:
    modele = random.choice(["imbriquee", "produit_quotient"])
    m, n = random.sample([2, 3, 4, 5], 2)
    p = random.choice([2, 3, 4, 5, 6])
    base = random.choice([2, 3, 5, 6, 7, 10])

    if modele == "imbriquee":
        expression = rf"\left({base}^{{{m}}}\right)^{{{n}}} \times {base}^{{-{p}}}"
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
                f"$(x^m)^n = x^{{mn}}$, donc ici ${base}^{{{m} \\times {n}}}$.",
                rf"\left({base}^{{{m}}}\right)^{{{n}}} = {base}^{{{m*n}}}",
            ),
            Etape(
                "Multiplier les deux puissances",
                "$x^m \\times x^n = x^{m+n}$ : on additionne, en tenant compte du "
                "signe négatif.",
                rf"{base}^{{{m*n}}} \times {base}^{{-{p}}} = "
                rf"{base}^{{{m*n} - {p}}} = {base}^{{{reponse}}}",
            ),
            Etape(
                "Vérifier — retour à la définition",
                "En cas de doute, réécrivez la puissance comme une multiplication "
                f"répétée : $({base}^{m})^{n}$ signifie « ${base}^{m}$ multiplié "
                f"{n} fois par lui-même », soit {m} × {n} = {m*n} facteurs "
                f"${base}$. La règle se retrouve ainsi sans l'avoir apprise.",
            ),
            Etape(
                "Interpréter",
                f"Les exposants négatifs ne sont pas une bizarrerie : ${base}^{{-{p}}}$ "
                "est une **division**. Toute cette mécanique sera reprise au "
                "semestre pour les fonctions puissances et les rendements d'échelle.",
            ),
        ]
        pieges = [
            (m + n - p,
             f"Vous avez traité $({base}^{{{m}}})^{{{n}}}$ comme ${base}^{{{m}+{n}}}$. "
             "Pour une puissance **de** puissance, on **multiplie** les exposants."),
            (m * n + p,
             f"Erreur de signe : ${base}^{{-{p}}}$ correspond à une soustraction "
             "de l'exposant, pas à une addition."),
        ]
    else:
        expression = rf"\frac{{{base}^{{{m}}} \times {base}^{{{n}}}}}{{{base}^{{{p}}}}}"
        reponse = m + n - p
        etapes = [
            Etape(
                "Identifier — produit puis quotient",
                "Deux règles s'enchaînent : $x^m x^n = x^{m+n}$ au numérateur, "
                "puis $\\dfrac{x^m}{x^n} = x^{m-n}$.",
            ),
            Etape(
                "Regrouper le numérateur",
                "On **additionne** les exposants d'un produit.",
                rf"{base}^{{{m}}} \times {base}^{{{n}}} = {base}^{{{m+n}}}",
            ),
            Etape(
                "Diviser",
                "On **soustrait** l'exposant du dénominateur.",
                rf"\frac{{{base}^{{{m+n}}}}}{{{base}^{{{p}}}}} = "
                rf"{base}^{{{m+n}-{p}}} = {base}^{{{reponse}}}",
            ),
            Etape(
                "Vérifier — le cas particulier révélateur",
                f"Si les exposants s'étaient annulés, on obtiendrait ${base}^0 = 1$. "
                "Ce n'est pas une convention arbitraire : c'est ce qu'impose la "
                f"règle $\\frac{{{base}^m}}{{{base}^m}} = {base}^{{m-m}}$, "
                "puisqu'un nombre divisé par lui-même vaut 1.",
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
> Simplifiez l'expression suivante :
>
> $$ {expression} $$
>
> Le résultat s'écrit sous la forme ${base}^{{n}}$. **Donnez la valeur de $n$.**
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
        "3️⃣ Opérations sur les fractions",
        "4️⃣ Puissances",
        "5️⃣ Racines carrées",
        "6️⃣ Intérêts composés",
        "7️⃣ Vrai ou faux ?",
    ]
)

with onglets[0]:
    st.subheader("Notation scientifique et ordres de grandeur")
    executer("p1_ordre", gen_ordre_de_grandeur)

with onglets[1]:
    st.subheader("Une part d'une part")
    executer("p1_frac_emb", gen_fractions_emboitees)

with onglets[2]:
    st.subheader("Additionner, soustraire, diviser des fractions")
    executer("p1_frac_ops", gen_fractions_operations)

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
