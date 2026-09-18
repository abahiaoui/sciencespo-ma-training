"""Série S3 — Dérivation : nombre dérivé, règles de calcul, tangente."""

import random

import streamlit as st
import sympy as sp

from moteur import Etape, Exercice, executer

st.set_page_config(page_title="S3 | Dérivation", page_icon="📉", layout="wide")

x = sp.Symbol("x")

st.title("📉 S3 — Dérivation")

with st.expander("📖 Contexte & objectifs", expanded=True):
    st.markdown(
        """
### 🎯 Ce que cette série entraîne
Dériver un polynôme, calculer un **nombre dérivé**, écrire l'équation d'une
**tangente**, appliquer la règle du produit, et surtout interpréter $f'(a)$ avec
son unité.

### 🧠 Ce qui change par rapport à la séance 2
En séance 2, chaque taux demandait de repasser par la limite. Les règles de dérivation
rendent ce détour inutile : on obtient directement une **fonction** $f'$ qui donne la
pente en tout point. Le gain n'est pas de confort, il est de nature — on passe d'un
nombre à un objet qu'on peut à son tour étudier.
"""
    )

with st.sidebar:
    st.header("📝 Aide-mémoire — Séance 3")
    st.markdown("**Dérivées de référence**")
    st.latex(r"(x^n)' = n\,x^{n-1} \qquad (k)' = 0 \qquad (kx)' = k")
    st.markdown("**Opérations**")
    st.latex(r"(u+v)' = u' + v'")
    st.latex(r"(ku)' = k\,u'")
    st.latex(r"(uv)' = u'v + uv'")
    st.markdown("**Tangente en $a$**")
    st.latex(r"y = f'(a)(x-a) + f(a)")
    st.error(
        "**L'erreur interdite**\n\n"
        r"$(uv)' \neq u'v'$"
        "\n\nLa dérivée d'un produit n'est **pas** le produit des dérivées."
    )
    st.info(
        "**L'unité de $f'$**\n\n"
        "Si $f$ est en euros et $x$ en unités produites, $f'$ est en "
        "**euros par unité**."
    )

CONTEXTES = [
    ("le coût de production", "réparations", "€"),
    ("la dépense d'entretien", "équipements", "€"),
    ("le temps de traitement", "dossiers", "minutes"),
    ("la consommation d'énergie", "bâtiments", "kWh"),
]


def _fr(v, n=2):
    return f"{v:,.{n}f}".replace(",", "\u202f").replace(".", ",")


# --- 1. Dériver un polynôme -------------------------------------------------


def gen_derivee_polynome() -> Exercice:
    a = random.choice([1, 2, 3, 4])
    b = random.choice([-6, -4, -2, 3, 5])
    c = random.choice([-8, -3, 2, 7])
    d = random.choice([-5, 0, 4, 9])
    degre3 = random.random() < 0.5

    f = (a * x**3 if degre3 else 0) + b * x**2 + c * x + d
    reponse = sp.expand(sp.diff(f, x))

    enonce = f"""
> Soit la fonction $f$ définie par
>
> $$ f(x) = {sp.latex(f)} $$
>
> Calculez $f'(x)$.
"""

    etapes = [
        Etape(
            "Identifier — une somme se dérive terme à terme",
            "La dérivée d'une somme est la somme des dérivées. On peut donc traiter "
            "chaque monôme séparément, ce qui n'est vrai ni pour un produit ni pour "
            "un quotient.",
        ),
        Etape(
            "Appliquer $(x^n)' = n\\,x^{n-1}$ terme par terme",
            "L'exposant descend en facteur, puis diminue de 1. Le terme constant "
            f"(${d}$) disparaît : une constante ne varie pas, sa pente est nulle.",
            rf"f'(x) = {sp.latex(reponse)}",
        ),
        Etape(
            "Vérifier — le degré a baissé d'une unité",
            f"$f$ est de degré ${sp.degree(f, x)}$, donc $f'$ doit être de degré "
            f"${sp.degree(reponse, x) if reponse != 0 else 0}$. ✓ "
            "Cette vérification de degré détecte immédiatement un exposant oublié.",
        ),
        Etape(
            "Interpréter",
            "$f'$ n'est pas un nombre mais une **fonction** : elle donne la pente de "
            "la tangente en chaque point. C'est ce changement de statut qui permettra, "
            "dès la séance suivante, d'étudier les variations de $f$ en étudiant le "
            "**signe** de $f'$.",
        ),
    ]

    return Exercice(
        enonce=enonce,
        reponse=reponse,
        etapes=etapes,
        type_reponse="sym",
        libelle="f'(x) =",
        symboles=["x"],
        indice="Dérivez chaque terme séparément. Que devient le terme constant ?",
        pieges=[
            (sp.expand(sp.diff(f, x) + d),
             "Vous avez gardé le terme constant. La dérivée d'une constante est "
             "**nulle** : une grandeur qui ne bouge pas n'a pas de pente."),
            (sp.expand(f / x) if f != 0 else sp.Integer(0),
             "Vous avez divisé par $x$ au lieu d'appliquer la règle "
             "$(x^n)' = n x^{n-1}$ : l'exposant doit aussi descendre en facteur."),
        ],
    )


# --- 2. Nombre dérivé -------------------------------------------------------


def gen_nombre_derive() -> Exercice:
    a = random.choice([1, 2, 3])
    b = random.choice([-12, -8, -5, 4, 6])
    c = random.choice([-10, -2, 3, 15])
    x0 = random.choice([-2, 1, 2, 3, 4])
    f = a * x**2 + b * x + c
    fp = sp.diff(f, x)
    reponse = float(fp.subs(x, x0))

    enonce = f"""
> Soit la fonction $f$ définie par
>
> $$ f(x) = {sp.latex(f)} $$
>
> Calculez le **nombre dérivé** $f'({x0})$.
"""

    etapes = [
        Etape(
            "Identifier — dériver d'abord, remplacer ensuite",
            "L'ordre est impératif : on calcule la fonction dérivée, **puis** on y "
            "substitue la valeur. Substituer avant de dériver reviendrait à dériver "
            "une constante, ce qui donnerait toujours zéro.",
        ),
        Etape(
            "Calculer la fonction dérivée",
            "",
            rf"f'(x) = {sp.latex(fp)}",
        ),
        Etape(
            "Substituer",
            "",
            rf"f'({x0}) = {sp.latex(fp.subs(x, x0))} = {reponse:.0f}",
        ),
        Etape(
            "Vérifier — l'ordre de grandeur par le taux d'accroissement",
            f"Le taux entre ${x0}$ et ${x0} + 0{{,}}01$ vaut "
            f"${float((f.subs(x, x0+0.01) - f.subs(x, x0))/0.01):.3f}$, très proche de "
            f"${reponse:.0f}$. ✓ C'est exactement la définition de la séance 2, "
            "et ce contrôle reste possible en cas de doute.",
        ),
        Etape(
            "Interpréter",
            f"$f'({x0}) = {reponse:.0f}$ signifie qu'**au voisinage de ${x0}$**, "
            f"$f$ varie de ${reponse:.0f}$ unité(s) quand $x$ augmente d'une unité. "
            f"La fonction y est donc "
            f"{'croissante' if reponse > 0 else 'décroissante' if reponse < 0 else 'stationnaire'}. "
            "Le mot « au voisinage » compte : cette pente ne vaut qu'localement.",
        ),
    ]

    return Exercice(
        enonce=enonce,
        reponse=reponse,
        etapes=etapes,
        libelle=f"f'({x0}) =",
        tolerance=1e-6,
        indice="Dérivez la fonction complète avant de remplacer $x$.",
        pieges=[
            (float(f.subs(x, x0)),
             f"Vous avez calculé $f({x0})$, l'**image**, et non le nombre dérivé. "
             "L'image est une hauteur, la dérivée est une pente."),
            (float(sp.diff(f.subs(x, x0), x)) if False else 0.0,
             "Substituer avant de dériver donne toujours zéro : une fois $x$ remplacé, "
             "il ne reste qu'une constante."),
        ],
    )


# --- 3. Équation de la tangente ---------------------------------------------


def gen_tangente() -> Exercice:
    a = random.choice([1, 2])
    b = random.choice([-6, -3, 2, 4])
    c = random.choice([-4, 1, 5])
    x0 = random.choice([1, 2, 3])
    x1 = x0 + random.choice([1, 2, 3])
    f = a * x**2 + b * x + c
    fp = sp.diff(f, x)
    pente = fp.subs(x, x0)
    hauteur = f.subs(x, x0)
    reponse = float(pente * (x1 - x0) + hauteur)

    enonce = f"""
> Soit $f(x) = {sp.latex(f)}$. On trace la **tangente** à la courbe au point
> d'abscisse ${x0}$.
>
> Quelle est l'ordonnée de cette tangente pour $x = {x1}$ ?
"""

    etapes = [
        Etape(
            "Identifier — une tangente est une droite, définie par deux données",
            f"Sa pente est $f'({x0})$ et elle passe par le point de la courbe "
            f"$({x0}\\,;\\,f({x0}))$. Ces deux informations suffisent à l'écrire "
            "entièrement.",
            r"y = f'(a)(x-a) + f(a)",
        ),
        Etape(
            "Calculer les deux ingrédients",
            f"$f'(x) = {sp.latex(fp)}$, donc $f'({x0}) = {pente}$. "
            f"Et $f({x0}) = {hauteur}$.",
            rf"y = {pente}(x - {x0}) + {hauteur}",
        ),
        Etape(
            "Évaluer en $x = {}$".format(x1),
            "",
            rf"y = {pente}({x1} - {x0}) + {hauteur} = {pente*(x1-x0)} + {hauteur} "
            rf"= {reponse:.0f}",
        ),
        Etape(
            "Vérifier — comparer à la courbe",
            f"La courbe elle-même vaut $f({x1}) = {float(f.subs(x, x1)):.0f}$ en ce "
            f"point, alors que la tangente donne ${reponse:.0f}$. L'écart est normal : "
            "la tangente **approche** la courbe, exactement au point de contact, et "
            "s'en éloigne d'autant plus qu'on s'en écarte.",
        ),
        Etape(
            "Interpréter — l'approximation affine",
            "Remplacer une courbe par sa tangente est l'usage le plus fréquent de la "
            "dérivée hors des mathématiques : c'est ce que fait tout raisonnement du "
            "type « si on augmente de 1 %, l'effet sera de… ». Valable localement, "
            "trompeur au-delà.",
        ),
    ]

    return Exercice(
        enonce=enonce,
        reponse=reponse,
        etapes=etapes,
        libelle=f"Ordonnée de la tangente en x = {x1}",
        tolerance=1e-6,
        indice=f"Écrivez l'équation de la tangente, puis remplacez $x$ par {x1}.",
        pieges=[
            (float(f.subs(x, x1)),
             "Vous avez calculé la valeur de la **courbe**, pas celle de la tangente. "
             "Les deux ne coïncident qu'au point de contact."),
            (float(pente * x1 + hauteur),
             f"Vous avez oublié de retrancher $a = {x0}$ : l'équation est "
             f"$f'(a)(x - a) + f(a)$, et non $f'(a)x + f(a)$."),
        ],
    )


# --- 4. Règle du produit ----------------------------------------------------


def gen_produit() -> Exercice:
    a = random.choice([1, 2, 3])
    b = random.choice([-4, -2, 3, 5])
    c = random.choice([1, 2])
    d = random.choice([-6, -1, 4])
    u = a * x + b
    v = c * x**2 + d
    f = sp.expand(u * v)
    reponse = sp.expand(sp.diff(f, x))

    enonce = f"""
> Soit la fonction $f$ définie par le **produit**
>
> $$ f(x) = ({sp.latex(u)})({sp.latex(v)}) $$
>
> Calculez $f'(x)$.
"""

    up, vp = sp.diff(u, x), sp.diff(v, x)

    etapes = [
        Etape(
            "Identifier — reconnaître la structure avant de calculer",
            "C'est un produit de deux fonctions. La règle $(uv)' = u'v + uv'$ "
            "s'applique. Attention : $(uv)'$ n'est **pas** $u'v'$ — c'est la même "
            "erreur de structure que $(a+b)^2 \\neq a^2+b^2$.",
        ),
        Etape(
            "Poser $u$, $v$ et leurs dérivées",
            "Écrire ces quatre éléments avant d'assembler évite la quasi-totalité "
            "des fautes.",
            rf"u = {sp.latex(u)},\ u' = {sp.latex(up)} \qquad "
            rf"v = {sp.latex(v)},\ v' = {sp.latex(vp)}",
        ),
        Etape(
            "Assembler",
            "",
            rf"f'(x) = ({sp.latex(up)})({sp.latex(v)}) + ({sp.latex(u)})"
            rf"({sp.latex(vp)}) = {sp.latex(reponse)}",
        ),
        Etape(
            "Vérifier — par le développement",
            f"En développant d'abord, $f(x) = {sp.latex(f)}$, dont la dérivée terme à "
            f"terme donne ${sp.latex(reponse)}$. ✓ Les deux chemins concordent. "
            "Ici le développement était possible ; il ne le sera plus avec un "
            "logarithme ou une exponentielle, d'où l'intérêt de la règle.",
        ),
        Etape(
            "Interpréter",
            "La règle du produit dit qu'un produit varie pour **deux** raisons : "
            "parce que le premier facteur bouge, et parce que le second bouge. "
            "D'où les deux termes. Cette lecture — un effet total est la somme de "
            "plusieurs canaux — reviendra pour l'élasticité.",
        ),
    ]

    return Exercice(
        enonce=enonce,
        reponse=reponse,
        etapes=etapes,
        type_reponse="sym",
        libelle="f'(x) =",
        symboles=["x"],
        indice="Posez $u$, $v$, $u'$ et $v'$ séparément, puis assemblez.",
        pieges=[
            (sp.expand(up * vp),
             "Vous avez calculé $u'v'$. La dérivée d'un produit n'est **jamais** le "
             "produit des dérivées : il faut deux termes, $u'v + uv'$."),
            (sp.expand(up * v),
             "Il manque le second terme $uv'$ : le facteur $v$ varie lui aussi."),
        ],
    )


# --- 5. Interpréter un nombre dérivé (QCM) ---------------------------------


def gen_interpretation() -> Exercice:
    grandeur, unite_x, unite_y = random.choice(CONTEXTES)
    q0 = random.choice([20, 40, 50, 80])
    val = random.choice([-12, -6, 7, 15, 25])

    bonne = (
        f"Au voisinage de {q0} {unite_x}, une {unite_x[:-1]} supplémentaire "
        f"{'augmente' if val > 0 else 'diminue'} {grandeur} d'environ "
        f"{abs(val)} {unite_y}."
    )
    options = [
        bonne,
        f"{grandeur.capitalize()} vaut {abs(val)} {unite_y} pour {q0} {unite_x}.",
        f"{grandeur.capitalize()} {'augmente' if val > 0 else 'diminue'} de "
        f"{abs(val)} {unite_y} au total.",
        f"{grandeur.capitalize()} {'augmente' if val > 0 else 'diminue'} de "
        f"{abs(val)} % par {unite_x[:-1]}.",
    ]
    random.shuffle(options)

    enonce = f"""
> On modélise {grandeur} d'un service par une fonction $C(q)$, où $q$ est le nombre
> de {unite_x} et $C$ s'exprime en {unite_y}.
>
> On a calculé $C'({q0}) = {val}$.
>
> Quelle est la bonne interprétation ?
"""

    etapes = [
        Etape(
            "Identifier — niveau, variation totale ou variation marginale ?",
            "Trois grandeurs sont facilement confondues : $C(q)$ est un **niveau**, "
            "$C(b) - C(a)$ une **variation totale**, et $C'(q)$ une variation **par "
            "unité supplémentaire**, au voisinage d'un point.",
        ),
        Etape(
            "Vérifier l'unité",
            f"$C$ est en {unite_y} et $q$ en {unite_x} : $C'$ s'exprime donc en "
            f"**{unite_y} par {unite_x[:-1]}**. Toute interprétation en pourcentage "
            "est exclue d'emblée par cette seule lecture d'unité.",
        ),
        Etape(
            "Vérifier — l'approximation n'est que locale",
            f"Ajouter 10 {unite_x} ne fera pas varier $C$ de $10 \\times {val} = "
            f"{10*val}$ exactement : la dérivée change au fur et à mesure. "
            "L'approximation ne vaut que pour une petite variation.",
        ),
        Etape(
            "Interpréter — le coût marginal",
            f"En économie, $C'(q)$ porte un nom : le **coût marginal**. C'est ce que "
            "coûte l'unité suivante, et c'est cette grandeur — non le coût total — "
            "qui décide s'il faut produire davantage. On s'en servira en optimisation.",
        ),
    ]

    return Exercice(
        enonce=enonce,
        reponse=bonne,
        etapes=etapes,
        type_reponse="qcm",
        options=options,
        libelle="Interprétation",
        indice="Quelle est l'unité de $C'$ ? Et s'agit-il d'un niveau ou d'une "
        "variation ?",
        pieges=[
            (f"{grandeur.capitalize()} vaut {abs(val)} {unite_y} pour {q0} {unite_x}.",
             "Vous décrivez un **niveau**, c'est-à-dire $C(q)$. La dérivée décrit une "
             "variation."),
            (f"{grandeur.capitalize()} {'augmente' if val > 0 else 'diminue'} de "
             f"{abs(val)} {unite_y} au total.",
             "Vous décrivez une variation **totale**. La dérivée donne une variation "
             "**par unité supplémentaire**."),
            (f"{grandeur.capitalize()} {'augmente' if val > 0 else 'diminue'} de "
             f"{abs(val)} % par {unite_x[:-1]}.",
             f"L'unité de $C'$ est {unite_y} par {unite_x[:-1]}, pas un pourcentage. "
             "Le taux en pourcentage sera l'élasticité, en séance 10."),
        ],
    )


# ==========================================================================

st.markdown("---")

onglets = st.tabs(
    [
        "1️⃣ Dériver un polynôme",
        "2️⃣ Nombre dérivé",
        "3️⃣ Tangente",
        "4️⃣ Règle du produit",
        "5️⃣ Interpréter f'(a)",
    ]
)

with onglets[0]:
    st.subheader("La dérivée terme à terme")
    executer("s3_polynome", gen_derivee_polynome)

with onglets[1]:
    st.subheader("Dériver puis substituer")
    executer("s3_nombre", gen_nombre_derive)

with onglets[2]:
    st.subheader("L'équation de la tangente")
    executer("s3_tangente", gen_tangente)

with onglets[3]:
    st.subheader("Dériver un produit")
    executer("s3_produit", gen_produit)

with onglets[4]:
    st.subheader("Que dit le nombre dérivé ?")
    executer("s3_interpretation", gen_interpretation)

st.markdown("---")
st.caption(
    "Semestre — séance n°3 : Dérivation · "
    "Mathématiques appliquées pour les sciences humaines et sociales, Sciences Po."
)
