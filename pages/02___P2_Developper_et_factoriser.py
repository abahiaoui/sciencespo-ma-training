"""Série P2 — Développer et factoriser. Identités remarquables, facteur commun."""

import random

import streamlit as st
import sympy as sp

from moteur import Etape, Exercice, executer

st.set_page_config(page_title="P2 | Développer et factoriser", page_icon="✳️", layout="wide")

x, q, n, p_, y = sp.symbols("x q n p y")

st.title("✳️ P2 — Développer et factoriser")

with st.expander("📖 Contexte & objectifs", expanded=True):
    st.markdown(
        """
### 🎯 Ce que cette série entraîne
Distribuer un facteur sans perdre un signe, développer un produit de deux parenthèses,
reconnaître une **identité remarquable** au passage, et faire le chemin inverse :
**factoriser**, c'est-à-dire réécrire une somme sous forme de produit.

### 🧠 Pourquoi les deux sens comptent
Développer sert à **comparer** deux expressions ; factoriser sert à **résoudre** et à
**lire un signe**. Au semestre, factoriser une dérivée sera le seul moyen de savoir si
une grandeur augmente ou diminue.
"""
    )

with st.sidebar:
    st.header("📝 Aide-mémoire — Séance 2")
    st.latex(r"k(a+b) = ka + kb")
    st.latex(r"(a+b)(c+d) = ac + ad + bc + bd")
    st.markdown("**Les trois identités remarquables**")
    st.latex(r"(a+b)^2 = a^2 + 2ab + b^2")
    st.latex(r"(a-b)^2 = a^2 - 2ab + b^2")
    st.latex(r"a^2 - b^2 = (a+b)(a-b)")
    st.error(
        "**L'erreur interdite**\n\n"
        r"$(a+b)^2 \neq a^2 + b^2$"
        "\n\nIl manque le **double produit** $2ab$."
    )
    st.info(
        "**Le réflexe de vérification**\n\n"
        "Remplacez la lettre par $1$ ou $2$ dans l'expression de départ et dans votre "
        "résultat. Les deux doivent donner le même nombre."
    )

CONTEXTES = [
    ("une subvention", "associations"),
    ("une aide au logement", "ménages"),
    ("une bourse", "étudiants"),
    ("une prime de transport", "agents"),
]


# --- 1. Distributivité simple ----------------------------------------------


def gen_distributivite() -> Exercice:
    a = random.choice([-4, -3, -2, 2, 3, 5])
    b = random.choice([2, 3, 4, 5])
    c = random.choice([-6, -5, -3, 3, 4, 7])
    d = random.choice([2, 3, 4, 6])
    e = random.choice([1, 2, 3])
    f = random.choice([-3, -1, 1, 2, 4])

    expr = a * (b * x + c) + d * (e * x + f)
    reponse = sp.expand(expr)
    coef, const = reponse.coeff(x), reponse.subs(x, 0)

    enonce = f"""
> Développez et réduisez :
>
> $$ {sp.latex(a)}({sp.latex(b*x + c)}) + {sp.latex(d)}({sp.latex(e*x + f)}) $$
"""

    etapes = [
        Etape(
            "Identifier — deux distributions puis une réduction",
            "Chaque facteur se distribue sur **tous** les termes de sa parenthèse. "
            "Le signe fait partie du facteur : c'est là que se perdent la plupart "
            "des points.",
        ),
        Etape(
            "Distribuer chaque facteur",
            f"Attention en particulier à ${sp.latex(a)} \\times {sp.latex(c)} = "
            f"{sp.latex(a*c)}$.",
            rf"{sp.latex(a*(b*x+c))} \;+\; {sp.latex(sp.expand(d*(e*x+f)))}",
        ),
        Etape(
            "Regrouper les termes semblables",
            "On additionne d'un côté les termes en $x$, de l'autre les constantes. "
            "Ce sont deux familles distinctes qui ne se mélangent jamais.",
            rf"({coef})x + ({const}) = {sp.latex(reponse)}",
        ),
        Etape(
            "Vérifier — le test à $x = 1$",
            f"Dans l'expression de départ : "
            f"${a} \\times {b + c} + {d} \\times {e + f} = "
            f"{a*(b+c) + d*(e+f)}$. "
            f"Dans le résultat : ${coef} + ({const}) = {coef + const}$. "
            "Les deux coïncident. ✓",
        ),
        Etape(
            "Interpréter",
            "Développer sert à **comparer** : deux expressions écrites différemment "
            "ne sont comparables qu'une fois réduites à la même forme. C'est ce qu'on "
            "fera systématiquement pour départager deux dispositifs publics.",
        ),
    ]

    return Exercice(
        enonce=enonce,
        reponse=reponse,
        etapes=etapes,
        type_reponse="sym",
        libelle="Expression développée et réduite",
        symboles=["x"],
        indice="Distribuez d'abord, réduisez ensuite. Ne sautez pas l'étape "
        "intermédiaire : c'est là que les signes se perdent.",
        pieges=[
            (
                sp.expand(a * b * x + c + d * e * x + f),
                "Vous n'avez distribué que sur le **premier** terme de chaque "
                "parenthèse. Le facteur porte sur tous les termes.",
            ),
            (
                sp.expand(a * (b * x - c) + d * (e * x + f)),
                f"Erreur de signe : ${sp.latex(a)} \\times {sp.latex(c)}$ vaut "
                f"${sp.latex(a*c)}$.",
            ),
        ],
    )


# --- 2. Double distributivité ----------------------------------------------


def gen_double_distributivite() -> Exercice:
    a = random.choice([1, 2, 3])
    b = random.choice([-5, -3, -2, 2, 4])
    c = random.choice([1, 2])
    d = random.choice([-4, -1, 3, 5, 6])

    reponse = sp.expand((a * q + b) * (c * q + d))

    enonce = f"""
> Développez et réduisez :
>
> $$ ({sp.latex(a*q + b)})({sp.latex(c*q + d)}) $$
"""

    etapes = [
        Etape(
            "Identifier — quatre produits, pas deux",
            "Chaque terme de la première parenthèse multiplie **chaque** terme de la "
            "seconde. Deux termes par deux termes font quatre produits.",
        ),
        Etape(
            "Écrire les quatre produits",
            "Dans l'ordre, sans en oublier ni en inventer.",
            rf"{sp.latex(a*c*q**2)} + {sp.latex(a*d*q)} + {sp.latex(b*c*q)} "
            rf"+ ({sp.latex(b*d)})",
        ),
        Etape(
            "Réduire",
            "Seuls les deux termes en $q$ se regroupent : "
            f"${sp.latex(a*d)} + ({sp.latex(b*c)}) = {sp.latex(a*d + b*c)}$.",
            rf"= {sp.latex(reponse)}",
        ),
        Etape(
            "Vérifier — le test à $q = 1$",
            f"Départ : $({a + b}) \\times ({c + d}) = {(a+b)*(c+d)}$. "
            f"Arrivée : ${sp.latex(reponse.subs(q, 1))}$. ✓ "
            "Dix secondes qui évitent une faute.",
        ),
        Etape(
            "Interpréter",
            "Un produit de deux facteurs devient une somme de trois termes : "
            "la forme change, la valeur non. C'est exactement ce va-et-vient "
            "entre produit et somme qui sera l'outil central du semestre.",
        ),
    ]

    return Exercice(
        enonce=enonce,
        reponse=reponse,
        etapes=etapes,
        type_reponse="sym",
        libelle="Expression développée et réduite",
        symboles=["q"],
        indice="Quatre produits. Écrivez-les tous avant de réduire.",
        pieges=[
            (
                sp.expand(a * c * q**2 + b * d),
                "Vous n'avez fait que **deux** produits (les premiers entre eux, "
                "les seconds entre eux). Il en manque deux — c'est la même erreur "
                "que $(a+b)^2 = a^2+b^2$.",
            ),
        ],
    )


# --- 3. Identité remarquable : reconnaître le double produit ----------------


def gen_identite() -> Exercice:
    k = random.choice([2, 3, 4, 5, 6, 7, 8, 9])
    signe = random.choice([1, -1])
    lettre = random.choice(["p", "x"])
    v = p_ if lettre == "p" else x

    expression = sp.expand((v + signe * k) ** 2)
    forme = f"({lettre} {'+' if signe > 0 else '-'} k)^2"

    enonce = f"""
> L'expression suivante est une identité remarquable :
>
> $$ {sp.latex(expression)} $$
>
> Elle se factorise sous la forme $({lettre} {'+' if signe > 0 else '-'} k)^2$.
> **Donnez la valeur de $k$.**
"""

    etapes = [
        Etape(
            "Identifier — trois termes, deux carrés",
            f"La forme $a^2 \\pm 2ab + b^2$ se reconnaît à deux carrés encadrant un "
            f"**double produit**. Ici $({lettre})^2$ et ${k**2}$ sont les carrés ; le "
            f"terme du milieu doit valoir $2 \\times {lettre} \\times k$.",
        ),
        Etape(
            "Trouver $k$ par le carré, puis vérifier par le double produit",
            f"Le terme constant vaut ${k**2}$, donc $k = \\sqrt{{{k**2}}} = {k}$. "
            f"C'est une hypothèse : il faut la **confirmer** avec le terme du milieu.",
            rf"2 \times {lettre} \times {k} = {2*k}{lettre}",
        ),
        Etape(
            "Vérifier — le double produit confirme",
            f"Le terme du milieu de l'énoncé est bien ${sp.latex(2*signe*k*v)}$. "
            "L'hypothèse est confirmée : sans cette vérification, on ne saurait pas "
            "distinguer une vraie identité d'un trinôme quelconque.",
            rf"{forme.replace('k', str(k))} = {sp.latex(expression)}",
        ),
        Etape(
            "Interpréter",
            "L'intérêt de la forme factorisée est qu'elle est un **carré** : elle est "
            "donc toujours positive ou nulle, et nulle en un seul point. "
            f"Ici, l'expression s'annule uniquement pour ${lettre} = "
            f"{-signe*k}$. Cette lecture sera reprise pour l'étude du signe.",
        ),
    ]

    return Exercice(
        enonce=enonce,
        reponse=float(k),
        etapes=etapes,
        libelle="Valeur de k",
        tolerance=1e-6,
        indice="Le terme constant est le carré de $k$. Vérifiez ensuite avec le "
        "terme du milieu, qui doit valoir le double produit.",
        pieges=[
            (float(k**2), "Vous avez donné le terme constant lui-même. $k$ en est la "
             "**racine carrée**."),
            (float(2 * k), "Vous avez donné le coefficient du double produit, qui vaut "
             "$2k$ et non $k$."),
        ],
    )


# --- 4. Différence de carrés : factoriser ----------------------------------


def gen_difference_carres() -> Exercice:
    a = random.choice([1, 1, 2, 3])
    b = random.choice([2, 3, 4, 5, 6, 7, 8, 9, 10, 12])
    expression = sp.expand(a**2 * y**2 - b**2)
    reponse = sp.factor(expression)

    enonce = f"""
> **Factorisez** l'expression suivante :
>
> $$ {sp.latex(expression)} $$
"""

    etapes = [
        Etape(
            "Identifier — une différence de deux carrés",
            f"Deux termes, un signe moins, et chacun est un carré : "
            f"${sp.latex(a**2*y**2)} = ({sp.latex(a*y)})^2$ et "
            f"${b**2} = {b}^2$. C'est la troisième identité remarquable.",
        ),
        Etape(
            "Appliquer $a^2 - b^2 = (a+b)(a-b)$",
            "On identifie les deux carrés, puis on écrit directement le produit.",
            rf"({sp.latex(a*y)})^2 - {b}^2 = ({sp.latex(a*y + b)})({sp.latex(a*y - b)})",
        ),
        Etape(
            "Vérifier — redévelopper",
            f"$({sp.latex(a*y + b)})({sp.latex(a*y - b)}) = "
            f"{sp.latex(a**2*y**2)} - {sp.latex(a*b*y)} + {sp.latex(a*b*y)} - {b**2}$. "
            "Les deux termes du milieu s'annulent : c'est précisément pourquoi il n'y "
            "a pas de double produit dans cette identité.",
        ),
        Etape(
            "Interpréter",
            f"Sous forme factorisée, on voit immédiatement que l'expression s'annule "
            f"pour $y = {sp.nsimplify(sp.Rational(b, a))}$ et "
            f"$y = {sp.nsimplify(-sp.Rational(b, a))}$ — information invisible dans la "
            "forme développée. Factoriser, c'est rendre les zéros lisibles.",
        ),
    ]

    return Exercice(
        enonce=enonce,
        reponse=reponse,
        etapes=etapes,
        type_reponse="sym",
        forme="factorisee",
        libelle="Forme factorisée",
        symboles=["y"],
        indice="Deux carrés séparés par un signe moins : une seule identité "
        "correspond à cette forme.",
        pieges=[
            ((a * y - b) ** 2, "Vous avez utilisé $(a-b)^2$. Or il n'y a **pas** de "
             "terme du milieu dans l'énoncé : c'est la différence de carrés."),
        ],
    )


# --- 5. Facteur commun -----------------------------------------------------


def gen_facteur_commun() -> Exercice:
    modele = random.choice(["numerique", "expression"])

    if modele == "numerique":
        k = random.choice([6, 8, 9, 12, 15])
        u = random.choice([2, 3, 4, 5])
        v = random.choice([3, 5, 7, 9])
        expression = sp.expand(k * u * n - k * v)
        enonce = f"""
> On souhaite factoriser l'expression suivante :
>
> $$ {sp.latex(expression)} $$
>
> **Donnez le plus grand facteur commun** aux deux termes — celui qu'il faut
> mettre en évidence.
"""
        etapes = [
            Etape(
                "Identifier — le plus grand diviseur commun",
                f"Les deux coefficients sont ${k*u}$ et ${k*v}$. Il faut sortir leur "
                f"**plus grand** diviseur commun, et non un diviseur quelconque : "
                f"sortir ${k // 2 if k % 2 == 0 else 3}$ donnerait une factorisation "
                "correcte mais incomplète.",
            ),
            Etape(
                "Calculer — décomposer les deux coefficients",
                f"${k*u} = {k} \\times {u}$ et ${k*v} = {k} \\times {v}$. "
                f"Le plus grand facteur commun est donc ${k}$.",
                rf"{sp.latex(expression)} = {k}({sp.latex(sp.simplify(expression / k))})",
            ),
            Etape(
                "Vérifier — redistribuer",
                f"${k} \\times {u}n = {k*u}n$ et ${k} \\times ({-v}) = {-k*v}$. ✓ "
                "La vérification d'une factorisation est toujours un développement.",
            ),
            Etape(
                "Interpréter",
                "Factoriser au maximum n'est pas une coquetterie : c'est ce qui rend "
                "la suite lisible. Une expression à moitié factorisée cache encore "
                "l'information qu'on cherchait à faire apparaître.",
            ),
        ]
        return Exercice(
            enonce=enonce,
            reponse=float(k),
            etapes=etapes,
            libelle="Plus grand facteur commun",
            tolerance=1e-6,
            indice="Cherchez le plus grand nombre qui divise les deux coefficients.",
            pieges=[
                (float(k * u), "C'est le premier coefficient, pas le facteur commun : "
                 f"il ne divise pas ${k*v}$."),
                (float(1), "Tout nombre divise par 1 : cela ne factorise rien. "
                 "Cherchez le plus grand diviseur commun."),
            ],
        )

    a = random.choice([2, 3, 4])
    b = random.choice([-5, -3, 1, 3])
    c = random.choice([1, 2])
    d = random.choice([-4, 2, 4, 6])
    commun = x + b
    expression = sp.expand(commun * (a * x + 1) + commun * (c * x + d))
    reponse = sp.factor(expression)

    enonce = f"""
> **Factorisez** l'expression suivante :
>
> $$ ({sp.latex(commun)})({sp.latex(a*x + 1)}) + ({sp.latex(commun)})({sp.latex(c*x + d)}) $$
"""

    etapes = [
        Etape(
            "Identifier — le facteur commun est une expression",
            f"Le bloc $({sp.latex(commun)})$ apparaît dans les deux termes. Un facteur "
            "commun n'est pas nécessairement un nombre : ce peut être une parenthèse "
            "entière. C'est tout l'enjeu de la question.",
        ),
        Etape(
            "Mettre le bloc en évidence",
            "On écrit le bloc devant, et on additionne entre crochets ce qui reste.",
            rf"({sp.latex(commun)})\big[({sp.latex(a*x+1)}) + ({sp.latex(c*x+d)})\big]",
        ),
        Etape(
            "Réduire le crochet",
            "Seul le contenu du crochet se simplifie ; le facteur commun ne bouge plus.",
            rf"= {sp.latex(reponse)}",
        ),
        Etape(
            "Vérifier — pourquoi ne pas développer d'abord",
            "Tout développer puis tenter de refactoriser fonctionne rarement : on perd "
            "de vue le bloc répété. Le réflexe est de **repérer avant de calculer** — "
            "c'est exactement ce qu'on fera devant une dérivée à factoriser.",
        ),
    ]

    return Exercice(
        enonce=enonce,
        reponse=reponse,
        etapes=etapes,
        type_reponse="sym",
        forme="factorisee",
        libelle="Forme factorisée",
        symboles=["x"],
        indice="Ne développez pas. Cherchez ce qui est écrit deux fois à l'identique.",
        pieges=[],
    )


# --- 6. Fil rouge : comparer deux dispositifs ------------------------------


def gen_comparaison() -> Exercice:
    aide, beneficiaires = random.choice(CONTEXTES)
    fixe_a = random.choice([80, 100, 120, 150]) * 1000
    unit_a = random.choice([15, 20, 25, 30])
    ecart_unit = random.choice([10, 15, 20])
    unit_b = unit_a + ecart_unit
    seuil = random.choice([2000, 3000, 4000, 5000])
    fixe_b = fixe_a - ecart_unit * seuil

    enonce = f"""
> **Villeneuve** met en place {aide}. Deux dispositifs sont envisagés, chacun avec un
> coût fixe de gestion et une aide unitaire versée à chacun des $n$ {beneficiaires} :
>
> - **Dispositif A** : coût fixe {fixe_a:,} €, aide unitaire {unit_a} €
> - **Dispositif B** : coût fixe {fixe_b:,} €, aide unitaire {unit_b} €
>
> À partir de combien de {beneficiaires} les deux dispositifs coûtent-ils
> exactement la même chose ?
""".replace(",", " ")

    ecart_fixe = fixe_a - fixe_b

    etapes = [
        Etape(
            "Identifier — traduire l'énoncé en expressions",
            "Un coût fixe ne dépend pas de $n$ ; une aide unitaire se multiplie par "
            "$n$. Chaque dispositif donne donc une expression de la même forme.",
            rf"D_A(n) = {fixe_a} + {unit_a}n \qquad D_B(n) = {fixe_b} + {unit_b}n",
        ),
        Etape(
            "Calculer — développer et réduire l'écart",
            "Le signe moins porte sur **les deux** termes de la seconde parenthèse. "
            "C'est l'erreur la plus fréquente de cette question.",
            rf"D_A(n) - D_B(n) = ({fixe_a} + {unit_a}n) - ({fixe_b} + {unit_b}n)"
            rf" = {ecart_fixe} - {ecart_unit}n",
        ),
        Etape(
            "Annuler l'écart",
            "Les deux dispositifs coûtent la même chose quand leur écart est nul.",
            rf"{ecart_fixe} - {ecart_unit}n = 0 \iff n = \frac{{{ecart_fixe}}}"
            rf"{{{ecart_unit}}} = {seuil}",
        ),
        Etape(
            "Vérifier — recalculer les deux coûts au seuil",
            f"$D_A({seuil}) = {fixe_a} + {unit_a} \\times {seuil} = "
            f"{fixe_a + unit_a*seuil}$ et $D_B({seuil}) = {fixe_b} + {unit_b} \\times "
            f"{seuil} = {fixe_b + unit_b*seuil}$. Identiques. ✓",
        ),
        Etape(
            "Interpréter — le seuil de bascule",
            f"En dessous de {seuil:,} {beneficiaires}, le dispositif au coût fixe le "
            f"plus faible (**B**) l'emporte ; au-delà, c'est **A**, dont l'aide "
            "unitaire plus basse finit par compenser son coût fixe plus élevé. "
            "Cette question « à partir de combien ? » est une des plus fréquentes en "
            "évaluation de politique publique.".replace(",", " "),
        ),
    ]

    return Exercice(
        enonce=enonce,
        reponse=float(seuil),
        etapes=etapes,
        libelle=f"Nombre de {beneficiaires}",
        tolerance=1e-6,
        indice="Écrivez les deux dépenses, puis cherchez pour quel $n$ leur "
        "différence s'annule.",
        pieges=[
            (float(fixe_a + fixe_b) / (unit_a + unit_b),
             "Vous avez **additionné** au lieu de soustraire. On cherche l'égalité "
             "des deux coûts, donc l'annulation de leur différence."),
            (float(ecart_fixe) / (unit_a + unit_b),
             "Le dénominateur est l'écart entre les deux aides unitaires, pas leur "
             "somme."),
        ],
    )


# ==========================================================================

st.markdown("---")

onglets = st.tabs(
    [
        "1️⃣ Distributivité",
        "2️⃣ Double distributivité",
        "3️⃣ Identité remarquable",
        "4️⃣ Différence de carrés",
        "5️⃣ Facteur commun",
        "6️⃣ Deux dispositifs",
    ]
)

with onglets[0]:
    st.subheader("Distribuer sans perdre un signe")
    executer("p2_distrib", gen_distributivite)

with onglets[1]:
    st.subheader("Quatre produits, pas deux")
    executer("p2_double", gen_double_distributivite)

with onglets[2]:
    st.subheader("Reconnaître le double produit")
    executer("p2_identite", gen_identite)

with onglets[3]:
    st.subheader("Factoriser une différence de carrés")
    executer("p2_carres", gen_difference_carres)

with onglets[4]:
    st.subheader("Mettre un facteur commun en évidence")
    executer("p2_commun", gen_facteur_commun)

with onglets[5]:
    st.subheader("Application : le seuil de bascule")
    executer("p2_comparaison", gen_comparaison)

st.markdown("---")
st.caption(
    "Séance de pré-rentrée n°2 — Développer et factoriser · "
    "Mathématiques appliquées pour les sciences humaines et sociales, Sciences Po."
)
