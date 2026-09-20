"""Série S5 — Discriminant et signe du trinôme. Fil rouge E : le festival (clôture).

Variation sur trois axes (cf. `contextes.py`) : le contexte, la notation (nom de
fonction et variable) et la **forme** du trinôme — termes dans le désordre,
coefficient dominant implicite, trinôme donné comme différence recette-coût.
Repérer $a$, $b$ et $c$ n'est trivial que lorsque l'énoncé les sert dans l'ordre.
"""

import math
import random

import streamlit as st
import sympy as sp

import contextes as cx
from contextes import latex_nombre as L
from moteur import Etape, Exercice, executer

st.set_page_config(page_title="S5 | Discriminant", page_icon="🔺", layout="wide")

st.title("🔺 S5 — Discriminant et signe du trinôme")

with st.expander("📖 Contexte & objectifs", expanded=True):
    st.markdown(
        """
### 🎯 Ce que cette série entraîne
Calculer un **discriminant**, en déduire le nombre de racines, les calculer, et
établir le **signe du trinôme** — donc résoudre une inéquation du second degré.

### 🧠 Ce que le discriminant apporte
En séance 4, les racines se lisaient sur une forme déjà factorisée. Mais la plupart
des expressions arrivent développées, et il faut alors un outil pour savoir **s'il
existe** des racines avant de les chercher. C'est exactement ce que fait $\\Delta$ :
il répond d'abord à la question d'existence, ensuite seulement à celle des valeurs.

### 🎪 Fil rouge E — Le festival (clôture)
Le profit du festival s'écrit $\\pi(p) = -60p^2 + 9\\,000p - 250\\,000$.
Pour quels prix le festival est-il bénéficiaire ?

### ⚠️ Les coefficients ne sont pas toujours dans l'ordre
$f(x) = 5 - 2x + 3x^2$ a pour coefficients $a = 3$, $b = -2$, $c = 5$ : l'ordre
d'écriture ne dit rien du rôle. Et dans $x^2 - 5x + 6$, le coefficient $a$ vaut
$1$ — il est écrit nulle part. Ces deux pièges reviennent à chaque tirage.
"""
    )

with st.sidebar:
    st.header("📝 Aide-mémoire — Séance 5")
    st.latex(r"\Delta = b^2 - 4ac")
    st.markdown("**Les trois cas**")
    st.markdown(
        "$\\Delta > 0$ : **deux** racines distinctes\n\n"
        "$\\Delta = 0$ : **une** racine double\n\n"
        "$\\Delta < 0$ : **aucune** racine réelle"
    )
    st.markdown("**Les racines**")
    st.latex(r"x_{1,2} = \frac{-b \pm \sqrt{\Delta}}{2a}")
    st.markdown("**Signe du trinôme**")
    st.info(
        "Le trinôme est **du signe de $a$** partout, **sauf entre les racines** "
        "où il est du signe contraire.\n\n"
        "Si $\\Delta < 0$, il garde le signe de $a$ sur tout l'axe."
    )
    st.warning(
        "**Identifier $a$, $b$, $c$ avant tout calcul**\n\n"
        "$a$ est le coefficient du carré, où qu'il soit écrit — et il vaut $1$ "
        "quand rien n'est écrit devant le carré."
    )


def _fr(v, n=2):
    return f"{v:,.{n}f}".replace(",", " ").replace(".", ",")


def _maj(texte: str) -> str:
    return texte[:1].upper() + texte[1:]


NOTATIONS = [
    cx.NotationFonction("f", "x"),
    cx.NotationFonction("g", "x"),
    cx.NotationFonction("h", "t"),
    cx.NotationFonction("P", "q"),
    cx.NotationFonction("R", "p"),
]


def _trinome_latex(a, b, c, var, ordre="decroissant") -> str:
    """Le trinôme écrit à la main, pour maîtriser l'ordre des termes.

    SymPy range toujours les puissances dans le même sens ; or savoir lire
    $c + bx + ax^2$ fait partie de ce qui est évalué.
    """
    carre = (
        f"{var}^2"
        if a == 1
        else f"-{var}^2"
        if a == -1
        else rf"{L(a)}\,{var}^2"
    )
    # « 1x » ne s'écrit pas : le coefficient 1 reste implicite.
    facteur_b = "" if abs(b) == 1 else f"{L(abs(b))}\\,"
    terme_b = f"{'+' if b >= 0 else '-'} {facteur_b}{var}" if b else ""
    terme_c = f"{'+' if c >= 0 else '-'} {L(abs(c))}" if c else ""
    if ordre == "croissant":
        debut = L(c) if c else ""
        milieu = terme_b
        fin = (
            f"+ {carre}" if a > 0 else f"- {carre.lstrip('-')}"
        )
        return " ".join(morceau for morceau in (debut, milieu, fin) if morceau).lstrip("+ ")
    return " ".join(morceau for morceau in (carre, terme_b, terme_c) if morceau)


# --- 1. Calculer le discriminant --------------------------------------------


def gen_discriminant() -> Exercice:
    notation = random.choice(NOTATIONS)
    var = notation.var
    cas = random.choice(["deux", "deux", "double", "aucune"])
    forme = random.choice(["decroissant", "croissant", "unitaire"])
    a = 1 if forme == "unitaire" else random.choice([-3, -2, -1, 2, 3])

    if cas == "double":
        r = random.choice([-3, -1, 2, 4])
        b = -2 * a * r
        c = a * r**2
    elif cas == "aucune":
        b = random.choice([-6, -2, 4, 8])
        # Delta = b^2 - 4ac < 0  =>  4ac > b^2
        c = a * random.choice([3, 5, 8])
        while b**2 - 4 * a * c >= 0:
            c = c + a * 2
    else:
        r1 = random.choice([-5, -2, 1, 3])
        r2 = r1 + random.choice([2, 4, 6])
        b = -a * (r1 + r2)
        c = a * r1 * r2

    delta = b**2 - 4 * a * c
    ordre = "croissant" if forme == "croissant" else "decroissant"
    expression = _trinome_latex(a, b, c, var, ordre)

    if forme == "unitaire":
        remarque = (
            f"Rien n'est écrit devant ${var}^2$ : cela signifie $a = 1$, et non "
            "$a = 0$. Un coefficient absent vaut toujours $1$ pour un produit."
        )
    elif forme == "croissant":
        remarque = (
            "Les termes sont écrits dans l'ordre **croissant** des puissances. "
            f"L'ordre d'écriture ne change rien aux rôles : $a$ reste le "
            f"coefficient de ${var}^2$, où qu'il figure."
        )
    else:
        remarque = (
            "Les termes sont dans l'ordre habituel : il reste à relever les signes, "
            "qui font partie des coefficients."
        )

    enonce = f"""
> Soit le trinôme
>
> $$ {notation.de()} = {expression} $$
>
> Calculez son **discriminant** $\\Delta$.
"""

    nb = (
        "deux racines distinctes"
        if delta > 0
        else "une racine double"
        if delta == 0
        else "aucune racine réelle"
    )
    qualificatif = (
        "strictement positif"
        if delta > 0
        else "nul"
        if delta == 0
        else "strictement négatif"
    )
    graphique = (
        "Deux points d'intersection ici."
        if delta > 0
        else "Un seul point : la parabole est tangente à l'axe."
        if delta == 0
        else "Aucun : la parabole est entièrement d'un seul côté de l'axe. "
        "Concrètement, cela signifie que la grandeur modélisée ne s'annule "
        "jamais — un profit toujours négatif, par exemple."
    )

    etapes = [
        Etape(
            "Identifier — repérer $a$, $b$ et $c$, quel que soit l'ordre",
            f"Ici $a = {L(a)}$, $b = {L(b)}$, $c = {L(c)}$. {remarque}",
        ),
        Etape(
            "Appliquer $\\Delta = b^2 - 4ac$",
            f"Attention au produit de signes : $4 \\times {L(a)} \\times {L(c)} = "
            f"{L(4 * a * c)}$, qu'il faut ensuite **retrancher**.",
            rf"\Delta = ({L(b)})^2 - 4 \times ({L(a)}) \times ({L(c)}) "
            rf"= {L(b**2)} - ({L(4 * a * c)}) = {L(delta)}",
        ),
        Etape(
            "Vérifier — conclure sur le nombre de racines",
            f"$\\Delta = {L(delta)}$ est **{qualificatif}** : le trinôme admet donc "
            f"**{nb}**. C'est la première information à en tirer, avant même de "
            "calculer quoi que ce soit.",
        ),
        Etape(
            "Interpréter — ce que $\\Delta$ dit graphiquement",
            f"$\\Delta$ mesure si la parabole **coupe** l'axe horizontal. {graphique}",
        ),
    ]

    return Exercice(
        enonce=enonce,
        reponse=float(delta),
        etapes=etapes,
        libelle="Δ =",
        tolerance=1e-6,
        indice="$\\Delta = b^2 - 4ac$. Notez d'abord les trois coefficients avec "
        "leurs signes — et sans vous fier à l'ordre d'écriture.",
        pieges=[
            (
                float(b**2 + 4 * a * c),
                "Erreur de signe : la formule **retranche** $4ac$.",
            ),
            (
                float(b**2 - 4 * a - c),
                "$4ac$ est un produit des trois facteurs $4$, $a$ et $c$, pas une "
                "soustraction.",
            ),
            (
                float(c**2 - 4 * a * b),
                "Vous avez interverti $b$ et $c$ : $b$ est le coefficient du terme en "
                f"${var}$, $c$ le terme constant — indépendamment de l'ordre "
                "d'écriture.",
            ),
        ],
    )


# --- 2. Calculer les racines ------------------------------------------------


def gen_racines_formule() -> Exercice:
    notation = random.choice(NOTATIONS)
    var = notation.var
    forme = random.choice(["decroissant", "croissant", "unitaire"])
    a = 1 if forme == "unitaire" else random.choice([-2, -1, 2, 3])
    r1 = random.choice([-6, -3, -1, 2, 4])
    r2 = r1 + random.choice([1, 2, 3, 5])
    b = -a * (r1 + r2)
    c = a * r1 * r2
    delta = b**2 - 4 * a * c
    reponse = float(max(r1, r2))
    expression = _trinome_latex(
        a, b, c, var, "croissant" if forme == "croissant" else "decroissant"
    )
    racine_delta = (
        math.isqrt(delta) if math.isqrt(delta) ** 2 == delta else round(math.sqrt(delta), 4)
    )

    enonce = f"""
> Soit le trinôme
>
> $$ {notation.de()} = {expression} $$
>
> Calculez ses racines et donnez la **plus grande**.
"""

    etapes = [
        Etape(
            "Identifier — relever les coefficients, puis vérifier l'existence",
            f"$a = {L(a)}$, $b = {L(b)}$, $c = {L(c)}$"
            + (
                f" — le $1$ devant ${var}^2$ n'est pas écrit, mais il compte."
                if forme == "unitaire"
                else " — quel que soit l'ordre dans lequel l'énoncé les présente."
            )
            + f" D'où $\\Delta = {L(delta)}$, strictement positif : il y a bien deux "
            "racines distinctes. Se lancer dans la formule sans avoir vérifié "
            "$\\Delta$ mène à une racine carrée impossible.",
        ),
        Etape(
            "Appliquer la formule",
            f"$\\sqrt{{{L(delta)}}} = {L(racine_delta)}$.",
            rf"{var}_{{1,2}} = \frac{{-({L(b)}) \pm \sqrt{{{L(delta)}}}}}"
            rf"{{2 \times ({L(a)})}}",
        ),
        Etape(
            "Calculer les deux valeurs",
            "",
            rf"{var}_1 = {L(min(r1, r2))} \qquad {var}_2 = {L(max(r1, r2))}",
        ),
        Etape(
            "Vérifier — par la forme factorisée",
            f"Si les racines sont ${L(r1)}$ et ${L(r2)}$, alors "
            f"${notation.de()} = {L(a)}({var} - ({L(r1)}))({var} - ({L(r2)}))$. "
            f"En développant, on retrouve bien l'énoncé. ✓ C'est la vérification la "
            "plus sûre, et elle prend trente secondes.",
        ),
        Etape(
            "Interpréter",
            "Le discriminant et la forme factorisée disent la même chose de deux "
            "manières : l'une part du développé, l'autre du factorisé. Savoir passer "
            "de l'une à l'autre est ce qui permet de choisir le chemin le plus court "
            "selon la forme sous laquelle l'énoncé arrive.",
        ),
    ]

    return Exercice(
        enonce=enonce,
        reponse=reponse,
        etapes=etapes,
        libelle="Plus grande racine",
        tolerance=1e-6,
        indice="Calculez $\\Delta$ d'abord, puis appliquez la formule.",
        pieges=[
            (float(min(r1, r2)), "C'est la **plus petite** racine."),
            (
                float((b + math.sqrt(delta)) / (2 * a)),
                "Erreur de signe : la formule commence par $-b$, pas par $+b$.",
            ),
        ],
    )


# --- 3. Signe du trinôme (QCM) ---------------------------------------------


def gen_signe() -> Exercice:
    notation = random.choice(NOTATIONS)
    var = notation.var
    v = sp.Symbol(var)
    a = random.choice([-3, -2, -1, 1, 2, 3])
    r1 = random.choice([-5, -2, 1, 3])
    r2 = r1 + random.choice([2, 4, 6])
    b = -a * (r1 + r2)
    c = a * r1 * r2
    f = a * v**2 + b * v + c
    presentation = random.choice(["developpee", "factorisee", "racines_seules"])

    signe_ext = "positif" if a > 0 else "négatif"
    signe_int = "négatif" if a > 0 else "positif"

    bonne = f"{notation.nom} est {signe_int} entre {r1} et {r2}, et {signe_ext} à l'extérieur"
    inverse = f"{notation.nom} est {signe_ext} entre {r1} et {r2}, et {signe_int} à l'extérieur"
    partout = f"{notation.nom} est {signe_ext} sur tout l'axe"
    signe_var = f"{notation.nom} est du signe de ${var}$ sur tout l'axe"
    options = [bonne, inverse, partout, signe_var]
    random.shuffle(options)

    if presentation == "factorisee":
        corps = (
            f"$$ {notation.de()} = {L(a)}\\,({var} "
            f"{'-' if r1 >= 0 else '+'} {L(abs(r1))})\\,({var} "
            f"{'-' if r2 >= 0 else '+'} {L(abs(r2))}) $$"
        )
        complement = (
            "\n>\n> La forme factorisée affiche les racines : il n'y a rien à calculer "
            "avant d'étudier le signe."
        )
        lecture_a = (
            f"Sous forme factorisée, le coefficient dominant est le facteur de tête, "
            f"${L(a)}$."
        )
    elif presentation == "racines_seules":
        corps = (
            f"> Un trinôme de coefficient dominant $a = {L(a)}$ a pour racines "
            f"${L(r1)}$ et ${L(r2)}$."
        )
        complement = ""
        lecture_a = f"Le coefficient dominant est donné : $a = {L(a)}$."
    else:
        corps = f"$$ {notation.de()} = {sp.latex(f)} $$"
        complement = f"\n>\n> dont les racines sont ${L(r1)}$ et ${L(r2)}$."
        lecture_a = f"Le coefficient de ${var}^2$ vaut ${L(a)}$."

    if presentation == "racines_seules":
        enonce = f"""
{corps}
>
> Quel est son **signe** selon les valeurs de ${var}$ ?
"""
    else:
        enonce = f"""
> Soit le trinôme
>
> {corps}{complement}
>
> Quel est son **signe** selon les valeurs de ${var}$ ?
"""

    milieu = (r1 + r2) / 2

    etapes = [
        Etape(
            "Identifier — la règle tient en une phrase",
            f"Un trinôme est **du signe de $a$** partout, **sauf entre les racines** "
            f"où il prend le signe contraire. {lecture_a} Donc {signe_ext} à "
            f"l'extérieur et {signe_int} entre les racines.",
        ),
        Etape(
            "Appliquer",
            f"Les racines sont ${L(r1)}$ et ${L(r2)}$. Elles découpent l'axe en trois "
            "zones, et le signe alterne en les traversant.",
        ),
        Etape(
            "Vérifier — un test par zone",
            f"${notation.nom}({L(r1 - 1)}) = {L(float(f.subs(v, r1 - 1)))}$ · "
            f"${notation.nom}({L(milieu)}) = {L(float(f.subs(v, milieu)))}$ · "
            f"${notation.nom}({L(r2 + 1)}) = {L(float(f.subs(v, r2 + 1)))}$. ✓ "
            "En cas de doute sur la règle, ces trois calculs la remplacent "
            "intégralement.",
        ),
        Etape(
            "Interpréter — pourquoi le signe plutôt que les variations",
            "Une question du type « pour quels prix l'activité est-elle bénéficiaire ? » "
            "porte sur le **signe** du profit, pas sur ses variations. "
            "Le trinôme est positif sur un intervalle, pas à partir d'un seuil : "
            "il y a deux bornes, et les oublier revient à ne répondre qu'à la moitié "
            "de la question.",
        ),
    ]

    return Exercice(
        enonce=enonce,
        reponse=bonne,
        etapes=etapes,
        type_reponse="qcm",
        options=options,
        libelle="Signe du trinôme",
        indice="Quel est le signe de $a$ ? Le trinôme prend ce signe hors des racines.",
        pieges=[
            (
                inverse,
                f"C'est l'inverse : le trinôme est du signe de $a$ (donc {signe_ext}) "
                "**à l'extérieur** des racines.",
            ),
            (
                partout,
                "Ce ne serait vrai que si $\\Delta < 0$. Ici il y a deux racines, donc "
                "un changement de signe.",
            ),
            (
                signe_var,
                f"Le signe du trinôme dépend de la position de ${var}$ par rapport aux "
                f"racines, pas du signe de ${var}$.",
            ),
        ],
    )


# --- 4. Fil rouge : pour quels prix l'activité est-elle bénéficiaire ? -----


def gen_festival() -> Exercice:
    ctx = cx.tirer(cx.MARCHES)
    var = random.choice(["p", "x"])
    nom = random.choice(["\\pi", "B", "P"])
    presentation = random.choice(["developpee", "recette_moins_cout"])

    # On retire tant que le profit ne peut pas être positif : sans deux racines,
    # la question « pour quels prix est-il bénéficiaire ? » n'a pas de réponse.
    while True:
        sensibilite = random.choice([50, 60, 75])
        base = random.choice([9_000, 8_400, 9_600, 6_000])
        cout = random.choice([250_000, 300_000, 240_000, 150_000])
        a = -sensibilite
        delta = base**2 - 4 * a * (-cout)
        if delta > 0:
            break

    racine = math.sqrt(delta)
    p1 = (-base + racine) / (2 * a)
    p2 = (-base - racine) / (2 * a)
    bas, haut = min(p1, p2), max(p1, p2)

    if presentation == "recette_moins_cout":
        enonce = f"""
> **{_maj(ctx.sujet)}.** Au prix ${var}$ (en {ctx.unite_prix}), la quantité vendue est
> $N({var}) = {L(base)} - {sensibilite}\\,{var}$, et les coûts fixes s'élèvent à
> **{_fr(cout, 0)} {ctx.unite_prix}**.
>
> Le profit vaut donc $ {nom}({var}) = {var} \\times N({var}) - {L(cout)} $.
>
> Pour quels prix l'activité est-elle **bénéficiaire** ? Donnez la **borne basse**
> de l'intervalle, arrondie au centime.
"""
        mise_en_forme = (
            f"Premier geste : développer pour obtenir un trinôme. "
            f"${var}\\,({L(base)} - {sensibilite}{var}) - {L(cout)} = "
            f"{L(a)}{var}^2 + {L(base)}\\,{var} - {L(cout)}$. Tant que l'expression "
            "n'est pas sous la forme $a{var}^2 + b{var} + c$, le discriminant n'a "
            "pas de sens."
        )
    else:
        enonce = f"""
> **{_maj(ctx.sujet)}.** Au prix ${var}$ (en {ctx.unite_prix}), le profit s'écrit
>
> $$ {nom}({var}) = {L(a)}\\,{var}^2 + {L(base)}\\,{var} - {L(cout)} $$
>
> Pour quels prix l'activité est-elle **bénéficiaire** ? Donnez la **borne basse**
> de l'intervalle, arrondie au centime.
"""
        mise_en_forme = (
            f"Le trinôme est déjà sous la bonne forme : $a = {L(a)}$, "
            f"$b = {L(base)}$, $c = {L(-cout)}$ — sans oublier le signe du terme "
            "constant."
        )

    milieu = (bas + haut) / 2
    etapes = [
        Etape(
            "Identifier — une inéquation du second degré",
            f"« Bénéficiaire » signifie ${nom}({var}) > 0$. On ne cherche pas un prix "
            "mais un **intervalle** de prix. La méthode est en trois temps : racines, "
            f"puis signe, puis conclusion. {mise_en_forme}",
        ),
        Etape(
            "Calculer le discriminant et les racines",
            f"$\\Delta = {L(base)}^2 - 4 \\times ({L(a)}) \\times ({L(-cout)}) = "
            f"{L(delta)}$, positif : deux racines.",
            rf"{var}_{{1,2}} = \frac{{-{L(base)} \pm \sqrt{{{L(delta)}}}}}"
            rf"{{2 \times ({L(a)})}} \quad\Rightarrow\quad "
            rf"{var}_1 \approx {L(bas, 2)} \ ,\ {var}_2 \approx {L(haut, 2)}",
        ),
        Etape(
            "Appliquer la règle de signe",
            f"Ici $a = {L(a)}$ est **négatif** : le trinôme est négatif à l'extérieur "
            "des racines et **positif entre elles**. L'activité est donc bénéficiaire "
            "pour les prix compris entre les deux racines.",
            rf"{nom}({var}) > 0 \iff {var} \in "
            rf"\left]{L(bas, 2)}\,;\,{L(haut, 2)}\right[",
        ),
        Etape(
            "Vérifier",
            f"${nom}({L(milieu, 0)}) = "
            f"{_fr(a * milieu**2 + base * milieu - cout, 0)}$ {ctx.unite_prix} — "
            f"positif ✓, et ${nom}({L(bas - 10, 0)}) = "
            f"{_fr(a * (bas - 10) ** 2 + base * (bas - 10) - cout, 0)}$ "
            f"{ctx.unite_prix} — négatif ✓.",
        ),
        Etape(
            "Interpréter — deux bornes, et c'est le point",
            f"En dessous de {_fr(bas, 2)} {ctx.unite_prix}, les recettes ne couvrent "
            f"pas les {_fr(cout, 0)} {ctx.unite_prix} de coûts. Au-dessus de "
            f"{_fr(haut, 2)} {ctx.unite_prix}, trop peu d'acheteurs restent. La "
            "rentabilité est bornée **des deux côtés** : répondre « à partir de tel "
            "prix » serait une réponse fausse, et c'est l'erreur que cette question "
            "cherche à révéler.",
        ),
    ]

    return Exercice(
        enonce=enonce,
        reponse=float(bas),
        etapes=etapes,
        libelle="Borne basse",
        unite=ctx.unite_prix,
        tolerance=0.002,
        indice="Calculez les deux racines, puis appliquez la règle de signe en "
        "regardant le signe de $a$.",
        pieges=[
            (
                float(haut),
                "C'est la borne **haute** de l'intervalle. L'énoncé demande la borne "
                "basse.",
            ),
            (
                float(base / (2 * sensibilite)),
                "C'est le prix qui **maximise** le profit (le sommet), pas une borne "
                "de rentabilité.",
            ),
        ],
    )


# ==========================================================================

st.markdown("---")

onglets = st.tabs(
    [
        "1️⃣ Calculer Δ",
        "2️⃣ Calculer les racines",
        "3️⃣ Signe du trinôme",
        "4️⃣ Pour quels prix ?",
    ]
)

with onglets[0]:
    st.subheader("Le discriminant et ce qu'il annonce")
    executer("s5_delta", gen_discriminant)

with onglets[1]:
    st.subheader("La formule des racines")
    executer("s5_racines", gen_racines_formule)

with onglets[2]:
    st.subheader("Du signe de a, sauf entre les racines")
    executer("s5_signe", gen_signe)

with onglets[3]:
    st.subheader("Clôture de l'arc festival")
    executer("s5_festival", gen_festival)

st.markdown("---")
st.caption(
    "Semestre — séance n°5 : Discriminant et signe du trinôme · "
    "Fil rouge E : le festival de Villeneuve · Sciences Po."
)
