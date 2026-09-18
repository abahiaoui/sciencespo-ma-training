"""Série P4 — Équations et inéquations du premier degré."""

import random
from fractions import Fraction

import streamlit as st
import sympy as sp

from moteur import Etape, Exercice, executer

st.set_page_config(page_title="P4 | Équations et inéquations", page_icon="⚖️", layout="wide")

x = sp.Symbol("x")

st.title("⚖️ P4 — Équations et inéquations")

with st.expander("📖 Contexte & objectifs", expanded=True):
    st.markdown(
        """
### 🎯 Ce que cette série entraîne
Résoudre une équation du premier degré, traduire un énoncé en équation, et manipuler
une **inéquation** — où une seule opération, la multiplication ou la division par un
nombre négatif, oblige à **renverser le sens** de l'inégalité.

### 🧠 Le principe unique
Une équation est une balance : tout ce qu'on fait d'un côté, on le fait de l'autre.
Cette règle suffit à tout résoudre. L'inéquation obéit à la même logique, avec une
seule exception — celle qu'il faut connaître par cœur.
"""
    )

with st.sidebar:
    st.header("📝 Aide-mémoire — Séance 4")
    st.markdown("**Équation du premier degré**")
    st.latex(r"ax + b = cx + d \iff (a-c)x = d - b \iff x = \frac{d-b}{a-c}")
    st.markdown("**Inéquation : les opérations sûres**")
    st.latex(r"a < b \iff a + k < b + k")
    st.latex(r"a < b \iff ka < kb \quad (k > 0)")
    st.error(
        "**La seule exception**\n\n"
        r"$a < b \iff ka > kb \quad (k < 0)$"
        "\n\nMultiplier ou diviser par un **négatif renverse** le sens."
    )
    st.info(
        "**Le réflexe**\n\n"
        "Toute solution d'équation se vérifie en la réinjectant dans l'énoncé. "
        "Trente secondes, zéro risque."
    )

CONTEXTES = [
    ("abonnement de transport", "trajets", "€"),
    ("forfait de restauration scolaire", "repas", "€"),
    ("contrat de maintenance", "interventions", "€"),
    ("licence logicielle", "utilisateurs", "€"),
]


def _fr(v, n=2):
    return f"{v:,.{n}f}".replace(",", "\u202f").replace(".", ",")


# --- 1. Équation du premier degré ------------------------------------------


def gen_equation() -> Exercice:
    a = random.choice([2, 3, 4, 5, 6, 7])
    c = random.choice([-3, -2, -1, 1, 2, 3])
    while a == c or a + c == 0:
        c = random.choice([-3, -2, -1, 1, 2, 3])
    sol = random.choice([-4, -3, -2, 2, 3, 4, 5, 6])
    b = random.choice([-8, -5, -2, 1, 4, 7])
    d = (a - c) * sol + b

    enonce = f"""
> Résolvez l'équation suivante :
>
> $$ {sp.latex(a*x + b)} = {sp.latex(c*x + d)} $$
"""

    etapes = [
        Etape(
            "Identifier — regrouper d'un côté, isoler de l'autre",
            "Il y a des $x$ des deux côtés et des constantes des deux côtés. "
            "La stratégie est toujours la même : rassembler les $x$ à gauche, "
            "les nombres à droite.",
        ),
        Etape(
            "Calculer — déplacer les termes",
            f"On retranche ${sp.latex(c*x)}$ des deux côtés, puis ${b}$ des deux côtés. "
            "Chaque opération s'applique aux deux membres, sans exception.",
            rf"{sp.latex(a*x + b)} = {sp.latex(c*x + d)} \iff "
            rf"{sp.latex((a-c)*x)} = {d - b}",
        ),
        Etape(
            "Isoler l'inconnue",
            f"On divise les deux membres par ${a - c}$. C'est licite car ce nombre "
            "n'est pas nul.",
            rf"x = \frac{{{d - b}}}{{{a - c}}} = {sol}",
        ),
        Etape(
            "Vérifier — réinjecter la solution",
            f"À gauche : ${a} \\times {sol} + ({b}) = {a*sol + b}$. "
            f"À droite : ${c} \\times {sol} + {d} = {c*sol + d}$. "
            "Les deux membres coïncident. ✓ Cette vérification est toujours possible "
            "et devrait être systématique.",
        ),
        Etape(
            "Interpréter",
            "Résoudre une équation, c'est répondre à la question « pour quelle valeur "
            "ces deux quantités deviennent-elles égales ? ». Appliquée à deux "
            "dispositifs publics, cette valeur est un **seuil de bascule**.",
        ),
    ]

    return Exercice(
        enonce=enonce,
        reponse=float(sol),
        etapes=etapes,
        libelle="x =",
        tolerance=1e-6,
        indice="Rassemblez les $x$ d'un côté et les nombres de l'autre avant de diviser.",
        pieges=[
            (float(d + b) / (a - c),
             "Erreur de signe en déplaçant la constante : passer $b$ de l'autre côté, "
             "c'est le **retrancher**, pas l'ajouter."),
            (float(d - b) / (a + c),
             "Erreur de signe en regroupant les $x$ : le coefficient devient "
             f"$a - c = {a - c}$, pas $a + c$."),
        ],
    )


# --- 2. Équation avec parenthèses et fractions -----------------------------


def gen_equation_fractions() -> Exercice:
    k = random.choice([2, 3, 4, 5])
    m = random.choice([2, 3, 6])
    sol = random.choice([-3, -2, 2, 3, 4, 6])
    b = random.choice([-4, -1, 2, 5])
    # k*(x + b) / m = x + r   =>  k*x + k*b = m*x + m*r
    r = sp.Rational(k * (sol + b) - m * sol, m)

    enonce = f"""
> Résolvez l'équation suivante :
>
> $$ \\frac{{{k}({sp.latex(x + b)})}}{{{m}}} = {sp.latex(x + r)} $$
"""

    etapes = [
        Etape(
            "Identifier — supprimer le dénominateur d'abord",
            f"Tant qu'une fraction subsiste, les manipulations sont pénibles. "
            f"La première opération consiste à multiplier **les deux membres** par "
            f"${m}$, ce qui fait disparaître le dénominateur.",
        ),
        Etape(
            "Multiplier les deux membres",
            f"Attention : à droite, le facteur ${m}$ porte sur **toute** l'expression, "
            "donc sur une parenthèse.",
            rf"{k}({sp.latex(x + b)}) = {m}({sp.latex(x + r)})",
        ),
        Etape(
            "Développer puis regrouper",
            "",
            rf"{sp.latex(sp.expand(k*(x+b)))} = {sp.latex(sp.expand(m*(x+r)))} "
            rf"\iff {sp.latex(sp.expand(k*x - m*x))} = {sp.latex(sp.expand(m*r - k*b))}"
            rf" \iff x = {sol}",
        ),
        Etape(
            "Vérifier — réinjecter",
            f"À gauche : $\\frac{{{k} \\times ({sol} + ({b}))}}{{{m}}} = "
            f"{sp.latex(sp.Rational(k*(sol+b), m))}$. "
            f"À droite : ${sol} + {sp.latex(r)} = {sp.latex(sol + r)}$. ✓",
        ),
        Etape(
            "Interpréter",
            "L'ordre des opérations compte autant que les opérations elles-mêmes : "
            "supprimer le dénominateur, puis développer, puis regrouper. Suivre cette "
            "séquence évite la quasi-totalité des erreurs.",
        ),
    ]

    return Exercice(
        enonce=enonce,
        reponse=float(sol),
        etapes=etapes,
        libelle="x =",
        tolerance=1e-6,
        indice=f"Commencez par multiplier les deux membres par {m}, sans oublier la "
        "parenthèse à droite.",
        pieges=[],
    )


# --- 3. Inéquation : la borne ----------------------------------------------


def gen_inequation() -> Exercice:
    a = random.choice([-6, -5, -4, -3, -2])  # coefficient négatif : le cas piégeux
    sol = random.choice([-3, -2, 2, 3, 4])
    b = random.choice([-6, -2, 3, 7])
    d = a * sol + b

    enonce = f"""
> On considère l'inéquation suivante :
>
> $$ {sp.latex(a*x + b)} \\;>\\; {d} $$
>
> La solution s'écrit $x < s$ ou $x > s$ selon le cas. **Donnez la valeur de $s$.**
>
> *(La question du sens de l'inégalité est traitée dans l'onglet suivant.)*
"""

    etapes = [
        Etape(
            "Identifier — une inéquation se résout comme une équation…",
            "…avec une exception unique. On isole $x$ exactement de la même façon : "
            "on déplace la constante, puis on divise par le coefficient.",
        ),
        Etape(
            "Déplacer la constante",
            f"Ajouter ou retrancher un nombre des deux côtés **ne change jamais** le "
            "sens d'une inégalité. Cette opération est toujours sûre.",
            rf"{sp.latex(a*x + b)} > {d} \iff {sp.latex(a*x)} > {d - b}",
        ),
        Etape(
            "Diviser par le coefficient — l'exception",
            f"Le coefficient vaut ${a}$, il est **négatif**. Diviser les deux membres "
            f"par ${a}$ **renverse** le sens de l'inégalité.",
            rf"{sp.latex(a*x)} > {d - b} \iff x < \frac{{{d - b}}}{{{a}}} = {sol}",
        ),
        Etape(
            "Vérifier — tester une valeur de chaque côté",
            f"Prenons $x = {sol - 1}$ (à gauche du seuil) : "
            f"${a} \\times {sol - 1} + ({b}) = {a*(sol-1) + b}$, "
            f"qui est bien $> {d}$. ✓ "
            f"Prenons $x = {sol + 1}$ : ${a*(sol+1) + b}$, qui ne l'est pas. ✓ "
            "Deux tests suffisent à confirmer à la fois la borne et le sens.",
        ),
        Etape(
            "Interpréter",
            "Une inéquation ne donne pas une valeur mais un **ensemble** de valeurs. "
            "En politique publique, c'est la forme naturelle d'une condition "
            "d'éligibilité ou d'un critère de soutenabilité.",
        ),
    ]

    return Exercice(
        enonce=enonce,
        reponse=float(sol),
        etapes=etapes,
        libelle="Valeur du seuil s",
        tolerance=1e-6,
        indice="La borne se calcule exactement comme dans une équation. "
        "Le sens de l'inégalité est une question séparée.",
        pieges=[
            (float(d + b) / a,
             "Erreur de signe en déplaçant la constante : on la **retranche** des deux "
             "côtés."),
        ],
    )


# --- 4. Inéquation : le sens (QCM) -----------------------------------------


def gen_sens_inegalite() -> Exercice:
    a = random.choice([-5, -4, -3, -2, 2, 3, 4, 5])
    seuil = random.choice([-2, 3, 4, 6, 8])
    sens_initial = random.choice(["<", ">"])
    if a > 0:
        sens_final = sens_initial
    else:
        sens_final = ">" if sens_initial == "<" else "<"

    options = [
        f"x {sens_final} {seuil}",
        f"x {'>' if sens_final == '<' else '<'} {seuil}",
    ]
    random.shuffle(options)
    reponse = f"x {sens_final} {seuil}"

    enonce = f"""
> On a abouti, après calcul, à l'étape suivante :
>
> $$ {sp.latex(a*x)} \\;{sens_initial}\\; {a*seuil} $$
>
> Quelle est la solution de cette inéquation ?
"""

    etapes = [
        Etape(
            "Identifier — quel est le signe du coefficient ?",
            f"Le coefficient de $x$ vaut ${a}$ : il est "
            f"**{'positif' if a > 0 else 'négatif'}**. C'est la seule information qui "
            "décide du sens final, et il faut se poser la question **avant** de diviser.",
        ),
        Etape(
            "Appliquer la règle",
            f"Diviser par un nombre {'positif conserve' if a > 0 else 'négatif renverse'} "
            f"le sens de l'inégalité. Le sens ${sens_initial}$ devient donc "
            f"${sens_final}$.",
            rf"{sp.latex(a*x)} {sens_initial} {a*seuil} \iff x {sens_final} {seuil}",
        ),
        Etape(
            "Vérifier — le test numérique tranche toujours",
            f"Testons $x = {seuil - 1 if sens_final == '<' else seuil + 1}$ : "
            f"${a} \\times {seuil - 1 if sens_final == '<' else seuil + 1} = "
            f"{a * (seuil - 1 if sens_final == '<' else seuil + 1)}$, et l'on vérifie "
            f"que ce nombre est bien ${sens_initial}\\ {a*seuil}$. ✓ "
            "En cas de doute sur le sens, ce test de cinq secondes lève l'ambiguïté "
            "sans qu'il soit besoin de se rappeler la règle.",
        ),
        Etape(
            "Interpréter — pourquoi le sens se renverse",
            "Multiplier par un nombre négatif retourne l'axe des nombres : ce qui "
            "était à droite passe à gauche. $2 < 3$, mais $-2 > -3$. La règle n'est "
            "pas une convention arbitraire, c'est une conséquence de cette symétrie.",
        ),
    ]

    return Exercice(
        enonce=enonce,
        reponse=reponse,
        etapes=etapes,
        type_reponse="qcm",
        options=options,
        libelle="Solution",
        indice="Regardez le signe du coefficient de $x$ avant toute chose.",
        pieges=[
            (f"x {'>' if sens_final == '<' else '<'} {seuil}",
             f"Le coefficient ${a}$ est "
             f"**{'positif' if a > 0 else 'négatif'}** : diviser par lui "
             f"{'conserve' if a > 0 else 'renverse'} le sens de l'inégalité."),
        ],
    )


# --- 5. Mise en équation ----------------------------------------------------


def gen_mise_en_equation() -> Exercice:
    service, unite, _ = random.choice(CONTEXTES)
    abo = random.choice([20, 24, 30, 36, 45])
    prix_reduit = random.choice([1, 2, 3])
    prix_plein = prix_reduit + random.choice([1, 2, 3])
    seuil = Fraction(abo, prix_plein - prix_reduit)
    reponse = float(seuil)

    enonce = f"""
> Pour un **{service}**, deux formules sont proposées :
>
> - **Formule A** : un abonnement de **{abo} €**, puis **{prix_reduit} €** par
>   {unite[:-1]} ;
> - **Formule B** : aucun abonnement, mais **{prix_plein} €** par {unite[:-1]}.
>
> À partir de combien de {unite} la formule A devient-elle plus avantageuse ?
> Donnez le nombre de {unite} pour lequel les deux formules coûtent exactement
> la même chose.
"""

    etapes = [
        Etape(
            "Identifier — traduire avant de calculer",
            f"On note $n$ le nombre de {unite}. Chaque formule donne une dépense "
            "totale : une partie fixe, plus une partie proportionnelle à $n$. "
            "C'est la traduction qui est notée, pas la résolution.",
            rf"C_A(n) = {abo} + {prix_reduit}n \qquad C_B(n) = {prix_plein}n",
        ),
        Etape(
            "Poser l'équation d'égalité",
            "Les deux formules coûtent la même chose quand leurs dépenses sont égales.",
            rf"{abo} + {prix_reduit}n = {prix_plein}n",
        ),
        Etape(
            "Résoudre",
            f"On rassemble les $n$ d'un côté : "
            f"${prix_plein}n - {prix_reduit}n = {prix_plein - prix_reduit}n$.",
            rf"{abo} = {prix_plein - prix_reduit}n \iff n = "
            rf"\frac{{{abo}}}{{{prix_plein - prix_reduit}}} = {sp.latex(sp.Rational(seuil.numerator, seuil.denominator))}"
            rf" \approx {reponse:.2f}",
        ),
        Etape(
            "Vérifier — comparer de part et d'autre du seuil",
            f"Pour $n = {int(reponse) + 2}$ : formule A coûte "
            f"{abo + prix_reduit*(int(reponse)+2)} €, formule B "
            f"{prix_plein*(int(reponse)+2)} € — A est bien moins chère au-delà du "
            "seuil. ✓",
        ),
        Etape(
            "Interpréter — ce que dit le seuil",
            f"En dessous de {reponse:.1f} {unite}, l'abonnement ne se rentabilise pas. "
            "Le raisonnement est identique pour un investissement public : un coût "
            "fixe élevé n'est justifié que par un volume d'usage suffisant. "
            "La question « à partir de combien ? » revient sans cesse.",
        ),
    ]

    return Exercice(
        enonce=enonce,
        reponse=reponse,
        etapes=etapes,
        libelle=f"Nombre de {unite} au seuil",
        tolerance=0.005,
        indice="Écrivez les deux dépenses en fonction de $n$, puis cherchez quand "
        "elles sont égales.",
        pieges=[
            (float(abo) / prix_plein,
             "Vous avez divisé par le prix plein au lieu de l'**écart** entre les deux "
             "prix unitaires. C'est cet écart qui permet de rattraper l'abonnement."),
            (float(abo) / prix_reduit,
             "Le dénominateur est l'écart entre les deux tarifs, pas le tarif réduit."),
            (float(abo) / (prix_plein + prix_reduit),
             "Les deux tarifs se **soustraient** : on cherche de combien la formule B "
             "est plus chère par unité."),
        ],
    )


# ==========================================================================

st.markdown("---")

onglets = st.tabs(
    [
        "1️⃣ Équation simple",
        "2️⃣ Fractions et parenthèses",
        "3️⃣ Inéquation : la borne",
        "4️⃣ Inéquation : le sens",
        "5️⃣ Mise en équation",
    ]
)

with onglets[0]:
    st.subheader("Résoudre une équation du premier degré")
    executer("p4_equation", gen_equation)

with onglets[1]:
    st.subheader("Supprimer le dénominateur avant tout")
    executer("p4_fractions", gen_equation_fractions)

with onglets[2]:
    st.subheader("Calculer la borne d'une inéquation")
    executer("p4_inequation", gen_inequation)

with onglets[3]:
    st.subheader("Le sens se renverse-t-il ?")
    executer("p4_sens", gen_sens_inegalite)

with onglets[4]:
    st.subheader("Traduire un énoncé en équation")
    executer("p4_traduire", gen_mise_en_equation)

st.markdown("---")
st.caption(
    "Séance de pré-rentrée n°4 — Équations et inéquations · "
    "Mathématiques appliquées pour les sciences humaines et sociales, Sciences Po."
)
