"""Série S8 — La dérivation : point de vue local. Fil rouge G : l'atelier municipal.

Variation sur trois axes (cf. `contextes.py`) : l'atelier étudié, la notation
($C$ de $q$, $K$ de $x$…) et la **forme** de la donnée — fonction de coût écrite,
décrite en français, ou réduite à deux relevés ; taux d'accroissement donné par
une formule ou par un tableau de valeurs de plus en plus petites.
"""

import random

import streamlit as st
import sympy as sp

import contextes as cx
from contextes import latex_nombre as L
from moteur import Etape, Exercice, executer

st.set_page_config(page_title="S8 | Dérivation locale", page_icon="🔧", layout="wide")

st.title("🔧 S8 — La dérivation : point de vue local")

with st.expander("📖 Contexte & objectifs", expanded=True):
    st.markdown(
        """
### 🎯 Ce que cette série entraîne
Calculer un **taux d'accroissement**, le faire tendre vers un **nombre dérivé**,
écrire l'**équation de la tangente**, et interpréter le tout comme un **coût
marginal**.

### 🧠 Le coût de l'unité suivante
La question de départ n'est pas mathématique : combien coûte la réparation
supplémentaire ? Le coût total ne répond pas — il augmente toujours. Ce qu'il faut,
c'est la **variation** du coût au voisinage du point où l'on se trouve. C'est
exactement ce que mesure le nombre dérivé.

### 🔧 Fil rouge G — L'atelier municipal de réparation
Son coût total est $C(q) = 40\\,000 + 35q + 0{,}02\\,q^2$, où $q$ est le nombre de
réparations.

### ⚠️ Le coût ne vous sera pas toujours servi en formule
Selon les tirages, la fonction de coût est écrite, décrite en français, ou réduite
à **deux relevés**. Dans ce dernier cas, aucun calcul de fonction n'est possible :
il ne reste que la définition du taux d'accroissement — et elle suffit.
"""
    )

with st.sidebar:
    st.header("📝 Aide-mémoire — Séance 8")
    st.markdown("**Taux d'accroissement**")
    st.latex(r"\tau(h) = \frac{f(a+h) - f(a)}{h}")
    st.markdown("**Nombre dérivé**")
    st.latex(r"f'(a) = \lim_{h \to 0} \frac{f(a+h) - f(a)}{h}")
    st.markdown("**Équation de la tangente en $a$**")
    st.latex(r"y = f'(a)(x - a) + f(a)")
    st.info(
        "**L'interprétation économique**\n\n"
        "$C'(q)$ est le **coût marginal** : ce que coûte approximativement "
        "l'unité suivante."
    )
    st.error(
        "**Niveau, variation totale, variation marginale**\n\n"
        "$C(q)$ : un niveau · $C(b) - C(a)$ : une variation totale · "
        "$C'(q)$ : une variation **par unité**."
    )


def _fr(v, n=2):
    return f"{v:,.{n}f}".replace(",", " ").replace(".", ",")


def _maj(texte: str) -> str:
    return texte[:1].upper() + texte[1:]


def _de(mot: str) -> str:
    """« de repas » mais « d'affiches » : élision devant une voyelle."""
    return ("d'" if mot[:1].lower() in "aeiouyéèêh" else 'de ') + mot


NOTATIONS = [
    cx.NotationFonction("C", "q"),
    cx.NotationFonction("C", "x"),
    cx.NotationFonction("K", "q"),
    cx.NotationFonction("f", "q"),
]


def _cout_latex(fixe, lineaire, quad, var) -> str:
    return rf"{L(fixe)} + {L(lineaire)}\,{var} + {L(quad)}\,{var}^2"


# --- 1. Taux d'accroissement ------------------------------------------------


def gen_taux() -> Exercice:
    ctx = cx.tirer(cx.PRODUCTIONS)
    notation = random.choice(NOTATIONS)
    var = notation.var
    v = sp.Symbol(var)
    fixe = random.choice([30_000, 40_000, 50_000])
    lineaire = random.choice([25, 35, 45])
    quad = random.choice([0.01, 0.02, 0.05])
    q0 = random.choice([200, 400, 600, 800])
    h = random.choice([100, 200, 50])
    presentation = random.choice(["formule", "phrase", "deux_releves"])

    cout = fixe + lineaire * v + quad * v**2
    c0 = float(cout.subs(v, q0))
    c1 = float(cout.subs(v, q0 + h))
    reponse = (c1 - c0) / h

    if presentation == "formule":
        enonce = f"""
> Pour **{ctx.acteur}**, le coût total de ${var}$ {ctx.unite_quantite} est
>
> $$ {notation.de()} = {_cout_latex(fixe, lineaire, quad, var)}
>    \\qquad \\text{{(en euros)}} $$
>
> Calculez le **taux d'accroissement** du coût entre ${var} = {q0}$ et
> ${var} = {q0 + h}$ {ctx.unite_quantite}.
"""
        lecture = "La fonction de coût est donnée : les deux valeurs se calculent."
    elif presentation == "phrase":
        enonce = f"""
> **{_maj(ctx.acteur)}** supporte **{_fr(fixe, 0)} €** de coûts fixes, puis
> **{_fr(lineaire, 0)} €** par {ctx.singulier} produit, auxquels s'ajoute un terme
> d'encombrement de **{_fr(quad, 2)} € par {ctx.singulier} et par {ctx.singulier}**
> — autrement dit ${L(quad)}\\,{var}^2$ au total.
>
> Calculez le **taux d'accroissement** du coût entre ${var} = {q0}$ et
> ${var} = {q0 + h}$ {ctx.unite_quantite}.
"""
        lecture = (
            f"La phrase décrit la fonction ${notation.de()} = "
            f"{_cout_latex(fixe, lineaire, quad, var)}$ : un terme fixe, un terme "
            "proportionnel, un terme quadratique. Traduire la phrase en formule est "
            "le premier geste."
        )
    else:
        tableau = cx.tableau_latex(
            [f"Production ${var}$", f"${q0}$", f"${q0 + h}$"],
            [["Coût total (€)", f"${L(c0, 0)}$", f"${L(c1, 0)}$"]],
        )
        tableau = "\n".join("> " + ligne for ligne in tableau.splitlines())
        enonce = f"""
> **{_maj(ctx.acteur)}** a relevé son coût total à deux niveaux de production :
>
{tableau}
>
> Calculez le **taux d'accroissement** du coût entre ces deux niveaux.
"""
        lecture = (
            "Aucune fonction n'est donnée, et il n'en faut pas : le taux "
            "d'accroissement ne demande que **deux valeurs** et l'écart qui les "
            "sépare. C'est ce qui le rend calculable sur des données réelles, où "
            "l'on n'a jamais de formule."
        )

    etapes = [
        Etape(
            "Identifier — un taux rapporte une variation à un écart",
            f"{lecture} La variation brute du coût ne suffit pas : elle dépend de la "
            "largeur de l'intervalle. Pour obtenir un coût **par unité**, il faut "
            "diviser par l'écart de quantité.",
            rf"\tau = \frac{{{notation.de(var + '_0 + h')} - "
            rf"{notation.de(var + '_0')}}}{{h}}",
        ),
        Etape(
            "Relever les deux coûts",
            f"${notation.de(str(q0))} = {L(c0, 0)}$ € et "
            f"${notation.de(str(q0 + h))} = {L(c1, 0)}$ €.",
            rf"{notation.de(str(q0 + h))} - {notation.de(str(q0))} = "
            rf"{L(c1 - c0, 0)}\ \text{{€}}",
        ),
        Etape(
            "Former le rapport",
            "",
            rf"\tau = \frac{{{L(c1 - c0, 0)}}}{{{h}}} \approx {L(round(reponse, 2))}"
            rf"\ \text{{€ par {ctx.singulier}}}",
        ),
        Etape(
            "Vérifier — l'unité et l'ordre de grandeur",
            f"Le résultat s'exprime en **euros par {ctx.singulier}**, et vaut "
            f"{_fr(reponse)} € — un peu plus que le coût unitaire de base "
            f"({_fr(lineaire, 0)} €), ce qui est cohérent avec le terme en "
            f"${var}^2$ qui alourdit le coût quand la production augmente. ✓",
        ),
        Etape(
            "Interpréter — « en moyenne » sur l'intervalle",
            f"Entre {q0} et {q0 + h} {ctx.unite_quantite}, chaque {ctx.singulier} "
            f"supplémentaire a coûté **{_fr(reponse)} € en moyenne**. Le mot « en "
            "moyenne » est essentiel : le coût du premier et celui du dernier ne sont "
            "pas les mêmes. C'est cette imprécision que la dérivée viendra lever.",
        ),
    ]

    return Exercice(
        enonce=enonce,
        reponse=reponse,
        etapes=etapes,
        libelle="Taux d'accroissement",
        unite=f"€/{ctx.singulier}",
        tolerance=0.005,
        indice="Calculez les deux coûts, puis divisez leur écart par l'écart de "
        "quantité.",
        pieges=[
            (
                float(c1 - c0),
                f"C'est la **variation totale** du coût en euros. Il reste à la "
                f"diviser par les {h} {ctx.unite_quantite} d'écart.",
            ),
            (
                float(c1) / (q0 + h),
                "Vous avez calculé un **coût moyen** au point d'arrivée. Le taux "
                "d'accroissement porte sur la variation, pas sur le niveau.",
            ),
        ],
    )


# --- 2. Du taux au nombre dérivé -------------------------------------------


def gen_nombre_derive() -> Exercice:
    ctx = cx.tirer(cx.PRODUCTIONS)
    notation = random.choice(NOTATIONS)
    var = notation.var
    fixe = random.choice([30_000, 40_000])
    lineaire = random.choice([25, 35, 45])
    quad = random.choice([0.01, 0.02, 0.05])
    q0 = random.choice([200, 400, 500, 800])
    reponse = lineaire + 2 * quad * q0
    presentation = random.choice(["formule_tau", "tableau_tau"])

    valeurs_h = [1, 0.1, 0.01]
    taus = [reponse + quad * h for h in valeurs_h]

    if presentation == "formule_tau":
        enonce = f"""
> Pour **{ctx.acteur}**, le coût total est
>
> $$ {notation.de()} = {_cout_latex(fixe, lineaire, quad, var)} $$
>
> On montre que le taux d'accroissement entre ${var}_0$ et ${var}_0 + h$ vaut
>
> $$ \\tau(h) = {L(lineaire)} + {L(2 * quad)}\\,{var}_0 + {L(quad)}\\,h $$
>
> Quel est le **nombre dérivé** ${notation.derivee(str(q0))}$, c'est-à-dire la
> limite de $\\tau(h)$ quand $h \\to 0$ ?
"""
        lecture = (
            f"Les deux premiers termes ne dépendent pas de $h$ : ils ne bougent pas. "
            f"Le terme ${L(quad)}h$, lui, devient aussi petit qu'on veut."
        )
    else:
        # Tableau construit hors de la f-string : une expression de f-string ne
        # peut pas contenir de contre-oblique avant Python 3.12.
        tableau = cx.tableau_latex(
            ["$h$", "$1$", "$0{,}1$", "$0{,}01$"],
            [[r"$\tau(h)$ (€)"] + [f"${L(round(t, 4))}$" for t in taus]],
        )
        tableau = "\n".join("> " + ligne for ligne in tableau.splitlines())
        enonce = f"""
> Pour **{ctx.acteur}**, on a calculé le taux d'accroissement du coût entre
> ${var} = {q0}$ et ${var} = {q0} + h$, pour des valeurs de $h$ de plus en plus
> petites :
>
{tableau}
>
> Vers quelle valeur le taux tend-il quand $h \\to 0$ ? C'est le **nombre dérivé**
> ${notation.derivee(str(q0))}$.
"""
        lecture = (
            "Le tableau suffit à lire la limite : les décimales se stabilisent à "
            "mesure que $h$ diminue. C'est exactement ainsi qu'on procède quand on "
            "ne dispose pas d'une expression littérale."
        )

    etapes = [
        Etape(
            "Identifier — faire tendre, ce n'est pas remplacer",
            "On ne peut pas poser $h = 0$ dans le rapport initial : le dénominateur "
            "s'annulerait. Mais après simplification, l'expression obtenue est "
            "parfaitement définie en 0, et c'est vers cette valeur que le taux tend.",
        ),
        Etape(
            "Observer ce qui dépend de $h$",
            lecture,
            rf"\tau(1) = {L(round(taus[0], 3))} \quad "
            rf"\tau(0{{,}}1) = {L(round(taus[1], 4))} \quad "
            rf"\tau(0{{,}}01) = {L(round(taus[2], 4))}",
        ),
        Etape(
            "Conclure",
            "",
            rf"{notation.derivee(str(q0))} = {L(lineaire)} + {L(2 * quad)} "
            rf"\times {q0} = {L(round(reponse, 2))}\ \text{{€ par {ctx.singulier}}}",
        ),
        Etape(
            "Vérifier — ce que devient la sécante",
            "Quand $h$ diminue, le second point glisse vers le premier et la droite "
            "sécante **pivote**. Sa position limite est la **tangente**, et sa pente "
            f"vaut {_fr(reponse)}. Le nombre dérivé n'est rien d'autre que cette "
            "pente.",
        ),
        Etape(
            "Interpréter — le coût marginal",
            f"À {q0} {ctx.unite_quantite}, le {ctx.singulier} suivant coûte environ "
            f"**{_fr(reponse)} €**. C'est le **coût marginal**, et c'est ce nombre — "
            "et non le coût total, ni le coût moyen — qui détermine s'il vaut la "
            "peine de produire davantage : il suffit de le comparer au prix facturé.",
        ),
    ]

    return Exercice(
        enonce=enonce,
        reponse=reponse,
        etapes=etapes,
        libelle=f"{notation.nom}'({q0}) =",
        unite="€",
        tolerance=0.002,
        indice="Que devient chacun des termes quand $h$ s'approche de 0 ?",
        pieges=[
            (
                float(taus[0]),
                "Vous avez posé $h = 1$ et non $h \\to 0$ : le terme en $h$ doit "
                "disparaître entièrement.",
            ),
            (
                float(lineaire),
                f"Vous avez oublié le terme ${L(2 * quad)}\\,{var}_0$, qui dépend du "
                "point où l'on se place. Le coût marginal n'est pas constant.",
            ),
        ],
    )


# --- 3. Équation de la tangente ---------------------------------------------


def gen_tangente() -> Exercice:
    ctx = cx.tirer(cx.PRODUCTIONS)
    notation = random.choice(NOTATIONS)
    var = notation.var
    v = sp.Symbol(var)
    quad = random.choice([0.02, 0.05, 0.1])
    lineaire = random.choice([20, 35, 50])
    fixe = random.choice([10_000, 20_000, 40_000])
    q0 = random.choice([200, 300, 500])
    q1 = q0 + random.choice([50, 100, 150])
    presentation = random.choice(["abscisse", "point", "pente_donnee"])

    cout = quad * v**2 + lineaire * v + fixe
    derivee = sp.diff(cout, v)
    pente = float(derivee.subs(v, q0))
    hauteur = float(cout.subs(v, q0))
    reponse = pente * (q1 - q0) + hauteur
    vraie = float(cout.subs(v, q1))

    entete = (
        f"> Le coût de **{ctx.acteur}** est "
        f"${notation.de()} = {_cout_latex(fixe, lineaire, quad, var)}$."
    )

    if presentation == "abscisse":
        enonce = f"""
{entete}
>
> On trace la **tangente** à cette courbe au point d'abscisse ${var} = {q0}$.
>
> Quelle est l'**ordonnée de cette tangente** pour ${var} = {q1}$ ?
"""
        ingredients = (
            f"${notation.derivee()} = {sp.latex(derivee)}$, donc "
            f"${notation.derivee(str(q0))} = {L(round(pente, 2))}$. Et "
            f"${notation.de(str(q0))} = {L(hauteur, 0)}$ €."
        )
    elif presentation == "point":
        enonce = f"""
{entete}
>
> On trace la **tangente** à cette courbe au point
> $A\\,({q0}\\,;\\,{L(hauteur, 0)})$.
>
> Quelle est l'**ordonnée de cette tangente** pour ${var} = {q1}$ ?
"""
        ingredients = (
            f"L'ordonnée du point de contact est donnée : "
            f"${notation.de(str(q0))} = {L(hauteur, 0)}$ €. Il ne reste qu'à "
            f"calculer la pente : ${notation.derivee()} = {sp.latex(derivee)}$, donc "
            f"${notation.derivee(str(q0))} = {L(round(pente, 2))}$."
        )
    else:
        enonce = f"""
{entete}
>
> On sait que le coût marginal en ${var} = {q0}$ vaut
> ${notation.derivee(str(q0))} = {L(round(pente, 2))}$ € et que
> ${notation.de(str(q0))} = {L(hauteur, 0)}$ €.
>
> En **approchant la courbe par sa tangente** en ce point, quel coût prévoyez-vous
> pour ${var} = {q1}$ ?
"""
        ingredients = (
            "Les deux ingrédients sont fournis : la pente et le point de contact. "
            "L'exercice se réduit à écrire l'équation de la tangente et à "
            "l'évaluer — c'est exactement le raisonnement « si on produit "
            f"{q1 - q0} unités de plus, cela coûtera environ… »."
        )

    etapes = [
        Etape(
            "Identifier — une tangente est une droite, définie par deux données",
            f"Sa pente est ${notation.derivee(str(q0))}$ et elle passe par le point de "
            f"la courbe $({q0}\\,;\\,{notation.de(str(q0))})$. Ces deux informations "
            "la déterminent entièrement.",
            rf"y = {notation.derivee('a')}\,({var} - a) + {notation.de('a')}",
        ),
        Etape(
            "Réunir les deux ingrédients",
            ingredients,
            rf"y = {L(round(pente, 2))}\,({var} - {q0}) + {L(hauteur, 0)}",
        ),
        Etape(
            f"Évaluer en ${var} = {q1}$",
            "",
            rf"y = {L(round(pente, 2))} \times {q1 - q0} + {L(hauteur, 0)} "
            rf"\approx {L(reponse, 0)}\ \text{{€}}",
        ),
        Etape(
            "Vérifier — comparer à la courbe",
            f"La courbe elle-même vaut ${notation.de(str(q1))} = {L(vraie, 0)}$ €, "
            f"contre {_fr(reponse, 0)} € pour la tangente. L'écart de "
            f"{_fr(abs(vraie - reponse), 0)} € est normal : la tangente **approche** "
            "la courbe, exactement au point de contact, et s'en éloigne d'autant plus "
            "qu'on s'écarte. ✓",
        ),
        Etape(
            "Interpréter — à quoi sert la tangente",
            "Remplacer une courbe par sa tangente est l'usage le plus courant de la "
            "dérivée hors des mathématiques : c'est ce que fait tout raisonnement du "
            "type « si on produit 50 unités de plus, cela coûtera environ… ». "
            "Valable localement, trompeur au-delà — et l'écart calculé ci-dessus "
            "chiffre précisément cette limite.",
        ),
    ]

    return Exercice(
        enonce=enonce,
        reponse=reponse,
        etapes=etapes,
        libelle=f"Ordonnée de la tangente en {var} = {q1}",
        unite="€",
        tolerance=0.002,
        indice="Écrivez l'équation de la tangente, puis remplacez la variable.",
        pieges=[
            (
                vraie,
                "Vous avez calculé la valeur de la **courbe**, pas celle de la "
                "tangente. Les deux ne coïncident qu'au point de contact.",
            ),
            (
                float(pente * q1 + hauteur),
                f"Vous avez oublié de retrancher $a = {q0}$ : l'équation est "
                f"${notation.derivee('a')}({var} - a) + {notation.de('a')}$.",
            ),
        ],
    )


# --- 4. Coût marginal contre coût de l'unité suivante (QCM) ----------------


def gen_marginal() -> Exercice:
    ctx = cx.tirer(cx.PRODUCTIONS)
    notation = random.choice(NOTATIONS)
    var = notation.var
    q0 = random.choice([300, 500, 800])
    marginal = random.choice([47, 55, 63, 71])
    prix = random.choice([100, 90, 60])
    presentation = random.choice(["derivee", "fonction", "phrase"])

    avantageux = (
        f"Le {ctx.singulier} suivant coûte environ {marginal} € et rapporte "
        f"{prix} € : il est avantageux de produire davantage."
    )
    pas_avantageux = (
        f"Le {ctx.singulier} suivant coûte environ {marginal} € et rapporte "
        f"{prix} € : il n'est pas avantageux de produire davantage."
    )
    total = f"Le coût total vaut {marginal} € à ce niveau de production."
    moyen = f"Chaque {ctx.singulier} coûte {marginal} € en moyenne depuis le début."
    bonne = avantageux if marginal < prix else pas_avantageux
    options = [avantageux, pas_avantageux, total, moyen]
    random.shuffle(options)

    if presentation == "derivee":
        corps = (
            f"> On a calculé le coût marginal au niveau de production "
            f"${var} = {q0}$ {ctx.unite_quantite} :\n>\n"
            f"> $$ {notation.derivee(str(q0))} = {marginal} \\ \\text{{€}} $$"
        )
    elif presentation == "fonction":
        # Une fonction de coût dont la dérivée vaut exactement `marginal` en q0.
        pente_quad = random.choice([0.01, 0.02])
        base = marginal - 2 * pente_quad * q0
        corps = (
            f"> Son coût total est ${notation.de()} = 40\\,000 + {L(base)}\\,{var} + "
            f"{L(pente_quad)}\\,{var}^2$, et sa dérivée "
            f"${notation.derivee()} = {L(base)} + {L(2 * pente_quad)}\\,{var}$.\n>\n"
            f"> Au niveau ${var} = {q0}$ {ctx.unite_quantite}, elle vaut donc "
            f"${notation.derivee(str(q0))} = {marginal}$ €."
        )
    else:
        corps = (
            f"> Une note interne indique : « à {q0} {ctx.unite_quantite}, produire "
            f"un {ctx.singulier} de plus coûterait environ **{marginal} €** »."
        )

    enonce = f"""
> Pour **{ctx.acteur}** :
>
{corps}
>
> Chaque {ctx.singulier} est facturé **{prix} €**.
>
> Quelle est la bonne lecture ?
"""

    etapes = [
        Etape(
            "Identifier — trois grandeurs à ne pas confondre",
            f"${notation.de()}$ est un **niveau** (le coût total). "
            f"$\\frac{{{notation.de()}}}{{{var}}}$ est un **coût moyen**. "
            f"${notation.derivee()}$ est le coût de l'**unité suivante**. "
            "Les trois sont différents, et seule la troisième éclaire la décision de "
            "produire une unité de plus.",
        ),
        Etape(
            "Comparer au prix",
            f"Le {ctx.singulier} suivant coûte environ {marginal} € et rapporte "
            f"{prix} €. L'écart est de **{prix - marginal:+} €** : produire une unité "
            f"de plus {'améliore' if marginal < prix else 'dégrade'} donc le résultat.",
        ),
        Etape(
            "Vérifier — la validité de l'approximation",
            f"${notation.derivee(str(q0))}$ est une valeur **locale** : elle vaut pour "
            "l'unité suivante, pas pour les cinq cents suivantes. Le coût marginal "
            "augmente avec la production, donc la conclusion peut s'inverser plus "
            "loin.",
        ),
        Etape(
            "Interpréter — la règle de décision",
            "Tant que le coût marginal reste inférieur au prix, produire davantage "
            "améliore le résultat ; dès qu'il le dépasse, c'est l'inverse. "
            "L'optimum est donc atteint quand les deux s'égalisent — c'est exactement "
            "ce que la séance 9 formalisera, et c'est la raison pour laquelle on "
            "raisonne sur la dérivée et non sur le coût total.",
        ),
    ]

    return Exercice(
        enonce=enonce,
        reponse=bonne,
        etapes=etapes,
        type_reponse="qcm",
        options=options,
        libelle="Lecture correcte",
        indice="Le coût marginal se compare au **prix**, pas au coût total.",
        pieges=[
            (
                total,
                "Vous confondez le coût **marginal** et le coût **total**. "
                "Le total se chiffre en dizaines de milliers d'euros ici.",
            ),
            (
                moyen,
                "C'est la définition du coût **moyen**, qui inclut la répartition des "
                "coûts fixes. Le coût marginal ne porte que sur l'unité suivante.",
            ),
            (
                pas_avantageux if marginal < prix else avantageux,
                f"Comparez les deux nombres : {marginal} € de coût contre {prix} € de "
                f"recette. L'écart est "
                f"{'favorable' if marginal < prix else 'défavorable'} à la production "
                "supplémentaire.",
            ),
        ],
    )


# ==========================================================================

st.markdown("---")

onglets = st.tabs(
    [
        "1️⃣ Taux d'accroissement",
        "2️⃣ Le nombre dérivé",
        "3️⃣ Équation de la tangente",
        "4️⃣ Lire un coût marginal",
    ]
)

with onglets[0]:
    st.subheader("Rapporter une variation à un écart")
    executer("s8_taux", gen_taux)

with onglets[1]:
    st.subheader("Quand les deux points se rapprochent")
    executer("s8_derive", gen_nombre_derive)

with onglets[2]:
    st.subheader("Approcher la courbe par sa tangente")
    executer("s8_tangente", gen_tangente)

with onglets[3]:
    st.subheader("Le coût de l'unité suivante")
    executer("s8_marginal", gen_marginal)

st.markdown("---")
st.caption(
    "Semestre — séance n°8 : La dérivation, point de vue local · "
    "Fil rouge G : l'atelier municipal de réparation · Sciences Po."
)
