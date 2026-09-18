"""Série S1 — Fonctions : images, antécédents, domaine, lectures."""

import random

import streamlit as st
import sympy as sp

from moteur import Etape, Exercice, executer

st.set_page_config(page_title="S1 | Fonctions", page_icon="ƒ", layout="wide")

x, q = sp.symbols("x q")

st.title("ƒ S1 — Fonctions et lectures")

with st.expander("📖 Contexte & objectifs", expanded=True):
    st.markdown(
        """
### 🎯 Ce que cette série entraîne
Calculer une **image**, retrouver un **antécédent**, repérer les valeurs pour
lesquelles une fonction n'est pas définie, et lire ce qu'une fonction dit du problème
qu'elle modélise.

### 🧠 Le déplacement par rapport à la pré-rentrée
Jusqu'ici, on calculait des nombres. Une fonction est un objet d'un autre type : une
**machine** qui associe à chaque entrée une sortie et une seule. On ne lui demande
plus « combien ça fait », mais « comment ça varie ».
"""
    )

with st.sidebar:
    st.header("📝 Aide-mémoire — Séance 1")
    st.markdown("**Vocabulaire**")
    st.latex(r"y = f(x)")
    st.markdown(
        "$x$ : antécédent (l'entrée) · $f(x)$ : image (la sortie)\n\n"
        "Calculer une **image** : on remplace, c'est direct.\n\n"
        "Chercher un **antécédent** : on résout une équation."
    )
    st.markdown("**Valeurs interdites**")
    st.latex(r"\frac{N(x)}{D(x)} \ \text{exige}\ D(x) \neq 0")
    st.latex(r"\sqrt{u(x)} \ \text{exige}\ u(x) \geqslant 0")
    st.info(
        "**Le coût moyen**\n\n"
        r"$CM(q) = \dfrac{C(q)}{q}$ — le coût *par unité*, à ne pas confondre "
        "avec le coût total."
    )

BIENS = [
    ("réparations", "atelier municipal"),
    ("repas servis", "cuisine centrale"),
    ("dossiers traités", "service instructeur"),
    ("logements rénovés", "opérateur public"),
]


def _fr(v, n=2):
    return f"{v:,.{n}f}".replace(",", "\u202f").replace(".", ",")


# --- 1. Calculer une image --------------------------------------------------


def gen_image() -> Exercice:
    a = random.choice([1, 2, 3])
    b = random.choice([-6, -4, -3, 2, 5])
    c = random.choice([-10, -4, 1, 6, 12])
    x0 = random.choice([-3, -2, 2, 3, 4, 5])
    f = a * x**2 + b * x + c
    reponse = float(f.subs(x, x0))

    enonce = f"""
> Soit la fonction $f$ définie par
>
> $$ f(x) = {sp.latex(f)} $$
>
> Calculez $f({x0})$.
"""

    etapes = [
        Etape(
            "Identifier — calculer une image est une substitution",
            "Rien à résoudre : on remplace chaque $x$ par la valeur donnée. "
            "La seule difficulté est le soin, en particulier avec les valeurs "
            "négatives et les carrés.",
        ),
        Etape(
            "Substituer, avec des parenthèses",
            f"On écrit $({x0})$ entre parenthèses partout. "
            f"En particulier $({x0})^2 = {x0**2}$, "
            f"{'positif même si la valeur est négative' if x0 < 0 else 'sans surprise ici'}.",
            rf"f({x0}) = {a}({x0})^2 + ({b})({x0}) + ({c})",
        ),
        Etape(
            "Calculer terme à terme",
            "",
            rf"= {a*x0**2} + ({b*x0}) + ({c}) = {reponse:.0f}",
        ),
        Etape(
            "Vérifier — l'ordre des opérations",
            f"Le carré se calcule **avant** la multiplication par ${a}$ : "
            f"${a} \\times ({x0})^2 = {a} \\times {x0**2} = {a*x0**2}$, "
            f"et non $({a} \\times {x0})^2 = {(a*x0)**2}$. "
            "C'est la faute la plus courante sur ce type de calcul.",
        ),
        Etape(
            "Interpréter",
            f"$f({x0}) = {reponse:.0f}$ se lit : « l'image de ${x0}$ par $f$ vaut "
            f"${reponse:.0f}$ », ou encore « le point de coordonnées "
            f"$({x0}\\,;\\,{reponse:.0f})$ appartient à la courbe ». Les deux "
            "formulations décrivent le même fait.",
        ),
    ]

    return Exercice(
        enonce=enonce,
        reponse=reponse,
        etapes=etapes,
        libelle=f"f({x0}) =",
        tolerance=1e-6,
        indice="Mettez la valeur entre parenthèses partout, et calculez le carré "
        "avant la multiplication.",
        pieges=[
            (float((a * x0) ** 2 + b * x0 + c),
             f"Vous avez calculé $({a} \\times {x0})^2$ au lieu de "
             f"${a} \\times ({x0})^2$. Le carré porte sur $x$ seul."),
            (float(-a * x0**2 + b * x0 + c),
             f"Signe du carré : $({x0})^2$ vaut ${x0**2}$, toujours positif."),
        ],
    )


# --- 2. Chercher un antécédent ----------------------------------------------


def gen_antecedent() -> Exercice:
    a = random.choice([2, 3, 4, 5])
    b = random.choice([-12, -7, -3, 4, 9])
    sol = random.choice([-4, -2, 3, 5, 6, 8])
    k = a * sol + b
    f = a * x + b

    enonce = f"""
> Soit la fonction $f$ définie par
>
> $$ f(x) = {sp.latex(f)} $$
>
> Quel est l'**antécédent** de ${k}$ par $f$ ? Autrement dit, pour quelle valeur de
> $x$ a-t-on $f(x) = {k}$ ?
"""

    etapes = [
        Etape(
            "Identifier — image et antécédent ne se calculent pas pareil",
            "Une image se calcule en remplaçant : c'est direct. Un antécédent se "
            "cherche en **résolvant une équation** : c'est le chemin inverse, et il "
            "peut donner plusieurs solutions, ou aucune.",
        ),
        Etape(
            "Poser l'équation",
            "On écrit que la sortie vaut la valeur cherchée.",
            rf"{sp.latex(f)} = {k}",
        ),
        Etape(
            "Résoudre",
            f"On retranche ${b}$ des deux côtés, puis on divise par ${a}$.",
            rf"{a}x = {k - b} \iff x = \frac{{{k - b}}}{{{a}}} = {sol}",
        ),
        Etape(
            "Vérifier — recalculer l'image",
            f"$f({sol}) = {a} \\times {sol} + ({b}) = {k}$. ✓ "
            "Toute recherche d'antécédent se vérifie par un calcul d'image — c'est "
            "gratuit, et ça ferme la question.",
        ),
        Etape(
            "Interpréter",
            f"Ici la fonction est affine, donc il y a exactement un antécédent. "
            "Ce ne sera plus le cas au semestre : une parabole peut avoir deux "
            "antécédents pour une même image, ou aucun. La question « combien de "
            "solutions ? » deviendra alors aussi importante que leur valeur.",
        ),
    ]

    return Exercice(
        enonce=enonce,
        reponse=float(sol),
        etapes=etapes,
        libelle="Antécédent x =",
        tolerance=1e-6,
        indice="Écrivez $f(x) = $ la valeur cherchée, puis résolvez.",
        pieges=[
            (float(a * k + b),
             "Vous avez calculé l'**image** de la valeur donnée, pas son antécédent. "
             "Les deux opérations vont en sens inverse."),
            (float(k + b) / a,
             "Erreur de signe : on **retranche** $b$ des deux côtés."),
        ],
    )


# --- 3. Valeur interdite ----------------------------------------------------


def gen_domaine() -> Exercice:
    a = random.choice([1, 2, 3, 4])
    b = random.choice([-12, -9, -6, -4, 5, 8, 10])
    num = random.choice([1, 3, 5, 2 * x + 1, x - 4])
    reponse = float(sp.Rational(-b, a))

    enonce = f"""
> Soit la fonction $f$ définie par
>
> $$ f(x) = \\frac{{{sp.latex(num)}}}{{{sp.latex(a*x + b)}}} $$
>
> Pour quelle valeur de $x$ cette fonction n'est-elle **pas définie** ?
"""

    etapes = [
        Etape(
            "Identifier — où une fonction peut-elle échouer ?",
            "Deux situations seulement au programme : un **dénominateur nul** et une "
            "**racine carrée d'un nombre négatif**. Ici, c'est un quotient : le "
            "danger est au dénominateur.",
        ),
        Etape(
            "Annuler le dénominateur",
            "On cherche la valeur qui rendrait la division impossible.",
            rf"{sp.latex(a*x + b)} = 0 \iff x = \frac{{{-b}}}{{{a}}} "
            rf"= {sp.latex(sp.Rational(-b, a))}",
        ),
        Etape(
            "Vérifier — que se passe-t-il à cette valeur ?",
            f"Pour $x = {sp.latex(sp.Rational(-b, a))}$, le dénominateur vaut $0$ et "
            "l'expression n'a aucun sens — la division par zéro n'est pas « égale à "
            "l'infini », elle n'est simplement pas définie.",
        ),
        Etape(
            "Interpréter — la valeur interdite a souvent un sens",
            "Dans un modèle, une valeur interdite signale fréquemment une limite du "
            "modèle lui-même : un effectif nul, une capacité saturée. Le coût moyen "
            "$C(q)/q$ en est l'exemple type — il n'est pas défini en $q = 0$, ce qui "
            "se comprend très bien : le coût par unité n'existe pas s'il n'y a aucune "
            "unité.",
        ),
    ]

    return Exercice(
        enonce=enonce,
        reponse=reponse,
        etapes=etapes,
        libelle="Valeur interdite x =",
        tolerance=1e-6,
        indice="Cherchez ce qui rendrait le dénominateur nul.",
        pieges=[
            (float(sp.Rational(b, a)),
             "Erreur de signe : résoudre $ax + b = 0$ donne $x = -b/a$."),
            (0.0,
             "Ce n'est pas $x$ qui doit être non nul, mais le **dénominateur**. "
             f"Ici, $x = 0$ donne un dénominateur de ${b}$, parfaitement acceptable."),
        ],
    )


# --- 4. Coût moyen ----------------------------------------------------------


def gen_cout_moyen() -> Exercice:
    bien, service = random.choice(BIENS)
    fixe = random.choice([1200, 1800, 2400, 3000, 4500])
    unitaire = random.choice([6, 8, 12, 15, 20])
    q0 = random.choice([20, 30, 40, 50, 60, 75])
    cout_total = fixe + unitaire * q0
    reponse = cout_total / q0

    enonce = f"""
> Le coût total d'un **{service}** produisant $q$ {bien} est modélisé par
>
> $$ C(q) = {fixe} + {unitaire}q \\qquad \\text{{(en euros)}} $$
>
> Calculez le **coût moyen** par unité pour $q = {q0}$ {bien}.
"""

    etapes = [
        Etape(
            "Identifier — coût total et coût moyen sont deux fonctions différentes",
            "Le coût total répond à « combien coûte l'ensemble ? » ; le coût moyen à "
            "« combien coûte **une** unité ? ». Le second s'obtient en divisant le "
            "premier par la quantité.",
            r"CM(q) = \frac{C(q)}{q}",
        ),
        Etape(
            "Calculer le coût total, puis diviser",
            f"$C({q0}) = {fixe} + {unitaire} \\times {q0} = {cout_total}$ €.",
            rf"CM({q0}) = \frac{{{cout_total}}}{{{q0}}} = {reponse:.2f}\ \text{{€}}",
        ),
        Etape(
            "Vérifier — décomposer le coût moyen",
            f"On peut aussi écrire $CM(q) = \\frac{{{fixe}}}{{q}} + {unitaire}$, soit "
            f"$\\frac{{{fixe}}}{{{q0}}} + {unitaire} = {fixe/q0:.2f} + {unitaire} = "
            f"{reponse:.2f}$ €. ✓ Cette écriture est plus parlante : le coût moyen est "
            "le coût unitaire **plus** la part de coût fixe supportée par chaque unité.",
        ),
        Etape(
            "Interpréter — pourquoi le coût moyen baisse",
            f"Le terme $\\frac{{{fixe}}}{{q}}$ diminue quand $q$ augmente : le coût "
            "fixe se répartit sur davantage d'unités. C'est le mécanisme des "
            "**économies d'échelle**, et c'est la raison pour laquelle on étudiera "
            "les variations de cette fonction plutôt que ses seules valeurs.",
        ),
    ]

    return Exercice(
        enonce=enonce,
        reponse=reponse,
        etapes=etapes,
        libelle="Coût moyen",
        unite="€",
        tolerance=0.005,
        indice="Coût total divisé par la quantité.",
        pieges=[
            (float(cout_total),
             "C'est le **coût total**, pas le coût moyen. Il reste à le diviser par "
             f"les {q0} unités."),
            (float(unitaire),
             "Vous avez donné le coût unitaire variable. Le coût moyen y ajoute la "
             "part de coût fixe supportée par chaque unité."),
            (float(fixe) / q0,
             "Vous n'avez réparti que le coût **fixe**. Il faut y ajouter le coût "
             "unitaire variable."),
        ],
    )


# --- 5. Lire une variation (QCM) --------------------------------------------


def gen_lecture() -> Exercice:
    bien, service = random.choice(BIENS)
    fixe = random.choice([1500, 2000, 3600])
    unitaire = random.choice([8, 10, 15])

    bonne = (
        "Le coût moyen diminue quand q augmente, sans jamais descendre "
        f"en dessous de {unitaire} €."
    )
    options = [
        bonne,
        "Le coût moyen augmente quand q augmente, car le coût total augmente.",
        f"Le coût moyen finit par atteindre 0 si q est assez grand.",
        f"Le coût moyen est constant et vaut {unitaire} € quelle que soit la quantité.",
    ]
    random.shuffle(options)

    enonce = f"""
> Pour un **{service}**, le coût moyen par unité s'écrit
>
> $$ CM(q) = \\frac{{{fixe}}}{{q}} + {unitaire} $$
>
> Laquelle de ces affirmations décrit correctement son comportement quand $q$
> augmente ?
"""

    etapes = [
        Etape(
            "Identifier — deux termes, deux comportements",
            f"Le coût moyen est une **somme** : un terme qui dépend de $q$ "
            f"($\\frac{{{fixe}}}{{q}}$) et un terme constant (${unitaire}$). "
            "Il faut analyser chacun séparément avant de conclure.",
        ),
        Etape(
            "Calculer quelques valeurs",
            f"$CM(10) = {fixe/10 + unitaire:.1f}$ € · "
            f"$CM(100) = {fixe/100 + unitaire:.1f}$ € · "
            f"$CM(1000) = {fixe/1000 + unitaire:.1f}$ €. "
            "La tendance est nette : le coût moyen diminue, de plus en plus lentement.",
        ),
        Etape(
            "Vérifier — jusqu'où peut-il descendre ?",
            f"Le premier terme tend vers 0 quand $q$ devient grand, mais le second "
            f"reste égal à ${unitaire}$ quoi qu'il arrive. Le coût moyen **s'approche** "
            f"de {unitaire} € sans jamais l'atteindre : c'est une asymptote, notion "
            "qu'on formalisera en séance 5.",
        ),
        Etape(
            "Interpréter — attention au piège du coût total",
            "Le coût **total** augmente bien avec $q$ ; le coût **moyen** diminue. "
            "Les deux affirmations sont vraies simultanément et ne se contredisent "
            "pas. Confondre les deux fonctions est l'erreur d'interprétation "
            "dominante sur ce chapitre.",
        ),
    ]

    return Exercice(
        enonce=enonce,
        reponse=bonne,
        etapes=etapes,
        type_reponse="qcm",
        options=options,
        libelle="Affirmation correcte",
        indice="Regardez séparément ce que devient chaque terme quand $q$ grandit.",
        pieges=[
            ("Le coût moyen augmente quand q augmente, car le coût total augmente.",
             "Vous confondez coût **total** et coût **moyen**. Le total augmente, "
             "le moyen diminue : les deux sont vrais en même temps."),
            (f"Le coût moyen finit par atteindre 0 si q est assez grand.",
             f"Le terme constant ${unitaire}$ ne disparaît jamais : le coût moyen "
             f"s'approche de {unitaire} €, sans jamais descendre en dessous."),
            (f"Le coût moyen est constant et vaut {unitaire} € quelle que soit la quantité.",
             f"Vous avez ignoré le terme $\\frac{{{fixe}}}{{q}}$, qui dépend bien de "
             "$q$ et qui domine pour les petites quantités."),
        ],
    )


# ==========================================================================

st.markdown("---")

onglets = st.tabs(
    [
        "1️⃣ Calculer une image",
        "2️⃣ Trouver un antécédent",
        "3️⃣ Valeur interdite",
        "4️⃣ Coût moyen",
        "5️⃣ Lire un comportement",
    ]
)

with onglets[0]:
    st.subheader("De l'entrée à la sortie")
    executer("s1_image", gen_image)

with onglets[1]:
    st.subheader("De la sortie à l'entrée")
    executer("s1_antecedent", gen_antecedent)

with onglets[2]:
    st.subheader("Là où la fonction n'existe pas")
    executer("s1_domaine", gen_domaine)

with onglets[3]:
    st.subheader("Coût total et coût moyen")
    executer("s1_cout_moyen", gen_cout_moyen)

with onglets[4]:
    st.subheader("Ce que la fonction raconte")
    executer("s1_lecture", gen_lecture)

st.markdown("---")
st.caption(
    "Semestre — séance n°1 : Fonctions et lectures · "
    "Mathématiques appliquées pour les sciences humaines et sociales, Sciences Po."
)
