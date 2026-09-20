"""Série S2 — Les suites : généralités. Fil rouge D : Mélodia.

Trois axes de variation, comme partout dans l'application (cf. `contextes.py`) :
le **contexte** (quel effectif est suivi), la **notation** (quelle lettre, quel
rang initial) et la **forme** de l'énoncé (récurrence écrite, phrase en
français, tableau de relevés). Une suite donnée par un tableau et une suite
donnée par une formule appellent le même raisonnement ; c'est précisément ce
qu'il faut que l'étudiant découvre ici, et non le jour de l'examen.
"""

import random

import streamlit as st

import contextes as cx
from contextes import latex_nombre as L
from moteur import Etape, Exercice, executer

st.set_page_config(page_title="S2 | Suites : généralités", page_icon="🔢", layout="wide")

st.title("🔢 S2 — Les suites : généralités")

with st.expander("📖 Contexte & objectifs", expanded=True):
    st.markdown(
        """
### 🎯 Ce que cette série entraîne
Lire une définition **par récurrence**, calculer des termes, passer à la **forme
explicite**, et déterminer les **variations** d'une suite.

### 🧠 Discret ou continu ?
Une suite n'est définie que pour des rangs **entiers** : elle se représente par un
nuage de points, jamais par une courbe continue. C'est la différence de nature avec
les fonctions de la séance 1, et elle a une conséquence pratique — on ne peut pas
« lire entre deux points ».

### 🎧 Fil rouge D — Mélodia
Mélodia comptait **12 400 abonnés** fin 2020. Deux scénarios sont envisagés :
**+900 abonnés par an**, ou **+8 % par an**.

### ⚠️ Les énoncés changent d'habit
D'un tirage à l'autre, la suite peut s'appeler $u$, $v$, $w$ ou $c$, démarrer au
rang **0 ou au rang 1**, et vous être donnée par une formule, par une phrase ou
par un tableau de relevés. Le geste, lui, ne change jamais.
"""
    )

with st.sidebar:
    st.header("📝 Aide-mémoire — Séance 2")
    st.markdown("**Notation**")
    st.latex(r"u_n \quad \text{terme de rang } n")
    st.markdown("$n$ est le **rang**, $u_n$ est la **valeur**. Ne pas les confondre.")
    st.markdown("**Deux façons de définir une suite**")
    st.latex(r"\text{Récurrence : } u_{n+1} = f(u_n) \ \text{ et un premier terme}")
    st.latex(r"\text{Explicite : } u_n = g(n)")
    st.markdown("**Variations**")
    st.latex(r"u_{n+1} - u_n > 0 \;\Rightarrow\; \text{croissante}")
    st.info(
        "**Récurrence ou explicite ?**\n\n"
        "La récurrence donne le **mécanisme**, l'explicite donne l'**accès direct** "
        "à n'importe quel rang sans calculer les précédents."
    )
    st.warning(
        "**Comptez les pas, ne recopiez pas la formule**\n\n"
        "Si la suite démarre au rang $1$, il n'y a que $n-1$ pas jusqu'au rang $n$. "
        "La formule explicite s'écrit alors $u_n = u_1 \\times q^{\\,n-1}$."
    )
    st.error(
        "**Un nuage de points, pas une courbe**\n\n"
        "Une suite n'existe qu'aux rangs entiers. $u_{2{,}5}$ n'a pas de sens."
    )


def _fr(v, n=2):
    return f"{v:,.{n}f}".replace(",", " ").replace(".", ",")


def _maj(texte: str) -> str:
    return texte[:1].upper() + texte[1:]


# --- 1. Lire une définition par récurrence ---------------------------------


def gen_recurrence() -> Exercice:
    ctx = cx.tirer(cx.EFFECTIFS)
    notation = cx.tirer_notation_suite()
    n0 = notation.depart
    pas = random.choice([3, 4, 5])
    rang = n0 + pas
    depart = random.choice([12_400, 8_000, 15_000, 20_000, 6_500])
    modele = random.choice(["affine", "multiplicatif", "mixte"])
    presentation = random.choice(["formule", "phrase", "tableau"])

    if modele == "multiplicatif":
        coef = random.choice([1.05, 1.08, 1.12, 0.95])
        ajout = 0
        regle = rf"{notation.suivant} = {L(coef)} \times {notation.courant}"
        en_mots = f"multiplié par ${L(coef)}$"
        en_phrase = f"{ctx.sujet} {cx.phrase_taux((coef - 1) * 100, periode='')}"
        raison_variation = (
            "le coefficient multiplicateur est supérieur à 1"
            if coef > 1
            else "le coefficient multiplicateur est inférieur à 1"
        )
    elif modele == "affine":
        coef = 1
        ajout = random.choice([900, 1200, -600, 1500, -450])
        signe = "+" if ajout > 0 else "-"
        regle = rf"{notation.suivant} = {notation.courant} {signe} {L(abs(ajout))}"
        en_mots = f"{'augmenté' if ajout > 0 else 'diminué'} de ${L(abs(ajout))}$"
        en_phrase = f"{ctx.acteur} {cx.phrase_flux(ctx, ajout, periode='')}"
        raison_variation = (
            "on ajoute chaque année un nombre positif"
            if ajout > 0
            else "on ajoute chaque année un nombre négatif"
        )
    else:
        coef = random.choice([1.05, 1.10, 0.90])
        ajout = random.choice([150, 300, -200])
        signe = "+" if ajout > 0 else "-"
        regle = (
            rf"{notation.suivant} = {L(coef)} \times {notation.courant} "
            rf"{signe} {L(abs(ajout))}"
        )
        en_mots = (
            f"multiplié par ${L(coef)}$, puis "
            f"{'augmenté' if ajout > 0 else 'diminué'} de ${L(abs(ajout))}$"
        )
        en_phrase = (
            f"{ctx.sujet} {cx.phrase_taux((coef - 1) * 100, periode='')}, "
            f"puis {'on en ajoute' if ajout > 0 else 'on en retire'} encore "
            f"{_fr(abs(ajout), 0)} {ctx.unite}"
        )
        raison_variation = "les deux effets — le coefficient et l'ajout — vont dans le même sens"

    valeurs = [float(depart)]
    for _ in range(pas):
        valeurs.append(valeurs[-1] * coef + ajout)
    reponse = valeurs[pas]

    if presentation == "formule":
        enonce = f"""
> On modélise {ctx.sujet} par une suite $({notation.courant})$ définie
> **par récurrence** :
>
> $$ {notation.initial} = {L(depart)} \\qquad {regle} $$
>
> Calculez **${notation.terme(rang)}$**.
"""
        origine = f"le premier terme ${notation.initial}$, donné dans l'énoncé"
    elif presentation == "phrase":
        enonce = f"""
> Au 1ᵉʳ janvier 2020, {ctx.sujet} s'élevait à **{_fr(depart, 0)} {ctx.unite}**.
> Chaque année depuis, {en_phrase}.
>
> On note ${notation.courant}$ {ctx.sujet} au bout de $n$ relevés annuels, la
> convention étant que ${notation.initial}$ correspond à l'année 2020.
>
> Calculez **${notation.terme(rang)}$**.
"""
        origine = (
            f"la valeur de 2020, qui est ${notation.initial}$ d'après la convention "
            "annoncée dans l'énoncé"
        )
    else:
        connus = min(3, pas)
        tableau = cx.tableau_suite(notation, valeurs[:connus])
        enonce = f"""
> {_maj(ctx.sujet)} fait l'objet d'un relevé annuel. Les premières valeurs sont :
>
{chr(10).join('> ' + ligne for ligne in tableau.splitlines())}
>
> Le mécanisme est le même à chaque étape : chaque terme est le précédent
> {en_mots}.
>
> Calculez **${notation.terme(rang)}$**.
"""
        origine = (
            f"le dernier terme lisible dans le tableau, "
            f"${notation.terme(n0 + connus - 1)} = {L(valeurs[connus - 1])}$ — "
            "inutile de repartir du début"
        )

    detail = " · ".join(
        f"${notation.terme(n0 + k)} = {L(valeurs[k])}$" for k in range(pas + 1)
    )

    etapes = [
        Etape(
            "Identifier — une récurrence se déroule pas à pas",
            f"La définition ne livre pas ${notation.terme(rang)}$ directement : elle "
            f"dit seulement comment passer d'un terme au suivant. Chaque terme est le "
            f"précédent {en_mots}. Le point de départ est {origine}.",
        ),
        Etape(
            "Compter les pas avant de calculer",
            f"La suite démarre au rang **{n0}** et l'on vise le rang **{rang}** : il y "
            f"a donc **{pas} pas**, pas {rang}. Ce décompte est la seule difficulté "
            "réelle de l'exercice — et l'erreur la plus fréquente quand le rang "
            "initial n'est pas $0$.",
        ),
        Etape(
            "Calculer les termes successifs",
            detail,
        ),
        Etape(
            "Vérifier — le sens de l'évolution",
            f"La suite est **{'croissante' if reponse > depart else 'décroissante'}**, "
            f"ce qui est cohérent avec la règle : {raison_variation}. ✓ Un résultat "
            "qui contredirait ce sens signalerait une erreur de signe.",
        ),
        Etape(
            "Interpréter — la limite de la récurrence",
            f"Pour ${notation.terme(rang)}$, dérouler {pas} lignes reste faisable. "
            f"Pour ${notation.terme(40)}$, ce serait absurde. C'est précisément la "
            "raison d'être de la **forme explicite**, objet de l'onglet suivant : "
            "elle donne n'importe quel rang sans calculer les précédents.",
        ),
    ]

    pieges = [
        (
            valeurs[pas - 1],
            f"Vous vous êtes arrêté un cran trop tôt : c'est "
            f"${notation.terme(rang - 1)}$. Entre le rang {n0} et le rang {rang}, "
            f"il y a {pas} applications de la règle.",
        ),
        (
            valeurs[pas] * coef + ajout,
            f"Vous avez appliqué la règle une fois de trop. La suite démarre au rang "
            f"**{n0}** : il n'y a que {pas} pas jusqu'au rang {rang}.",
        ),
    ]
    if pas > 1:
        pieges.append(
            (valeurs[1], "Vous n'avez appliqué la règle qu'**une seule fois**.")
        )

    return Exercice(
        enonce=enonce,
        reponse=reponse,
        etapes=etapes,
        libelle=f"{notation.lettre}_{rang} =",
        unite=ctx.unite,
        tolerance=0.002,
        indice=f"Combien de pas séparent le rang {n0} du rang {rang} ?",
        pieges=pieges,
    )


# --- 2. Passer de la récurrence à l'explicite ------------------------------


def gen_explicite() -> Exercice:
    ctx = cx.tirer(cx.EFFECTIFS)
    notation = cx.tirer_notation_suite()
    n0 = notation.depart
    modele = random.choice(["arithmetique", "geometrique"])
    presentation = random.choice(["recurrence", "phrase", "tableau"])
    depart = random.choice([12_400, 9_000, 15_000, 7_200])
    rang = random.choice([12, 15, 20, 25])
    pas = rang - n0
    exposant = notation.exposant  # « n » ou « n-1 »

    if modele == "geometrique":
        taux = random.choice([5, 8, 10, -4])
        coef = 1 + taux / 100
        regle = rf"{notation.suivant} = {L(coef)} \times {notation.courant}"
        explicite = rf"{notation.courant} = {L(depart)} \times {L(coef)}^{{\,{exposant}}}"
        reponse = depart * coef**pas
        naif = depart + pas * (depart * taux / 100)
        message_naif = (
            f"Vous avez ajouté {pas} fois la variation de la **première** année. "
            "Or un pourcentage porte chaque année sur la valeur courante, pas sur "
            "la valeur initiale."
        )
        commentaire = (
            f"D'un rang au suivant, on multiplie toujours par le même coefficient "
            f"${L(coef)}$. Après $k$ étapes, on a donc multiplié $k$ fois : c'est une "
            "**puissance**. Le coefficient multiplicateur de la pré-rentrée "
            "réapparaît ici tel quel."
        )
        en_phrase = f"{ctx.sujet} {cx.phrase_taux(taux, periode='')}"
    else:
        raison = random.choice([900, 1200, 1500, -400])
        coef = 1
        signe = "+" if raison > 0 else "-"
        regle = rf"{notation.suivant} = {notation.courant} {signe} {L(abs(raison))}"
        explicite = (
            rf"{notation.courant} = {L(depart)} {signe} {L(abs(raison))}"
            rf"\,({exposant})"
            if n0 == 1
            else rf"{notation.courant} = {L(depart)} {signe} {L(abs(raison))}\,n"
        )
        reponse = float(depart + pas * raison)
        naif = float(depart + rang * raison)
        message_naif = (
            f"Vous avez compté {rang} pas. La suite démarrant au rang **{n0}**, "
            f"il n'y en a que {pas} jusqu'au rang {rang}."
            if n0 == 1
            else f"Vous avez compté {rang + 1} pas au lieu de {pas}."
        )
        commentaire = (
            f"D'un rang au suivant, on ajoute toujours la même quantité "
            f"${L(raison)}$. Après $k$ étapes, on a donc ajouté $k$ fois cette "
            "quantité : la dépendance en $n$ est **affine**."
        )
        en_phrase = f"{ctx.acteur} {cx.phrase_flux(ctx, raison, periode='')}"

    if presentation == "recurrence":
        enonce = f"""
> {_maj(ctx.sujet)} suit la récurrence
>
> $$ {notation.initial} = {L(depart)} \\qquad {regle} $$
>
> Sans dérouler tous les termes, calculez **${notation.terme(rang)}$**.
"""
    elif presentation == "phrase":
        enonce = f"""
> {_maj(ctx.sujet)} était de **{_fr(depart, 0)} {ctx.unite}** lors du premier relevé,
> noté ${notation.initial}$. D'un relevé au suivant, {en_phrase}.
>
> Sans dérouler tous les termes, calculez **${notation.terme(rang)}$**.
"""
    else:
        if modele == "geometrique":
            premiers = [depart * coef**k for k in range(3)]
        else:
            premiers = [depart + k * raison for k in range(3)]
        tableau = cx.tableau_suite(notation, premiers)
        enonce = f"""
> Voici les trois premiers relevés {ctx.du} :
>
{chr(10).join('> ' + ligne for ligne in tableau.splitlines())}
>
> Cette suite est **{'géométrique' if modele == 'geometrique' else 'arithmétique'}**.
> Sans dérouler tous les termes, calculez **${notation.terme(rang)}$**.
"""

    etapes = [
        Etape(
            "Identifier — repérer le mécanisme",
            commentaire,
        ),
        Etape(
            "Compter les pas : c'est ici que tout se joue",
            f"Le premier terme est ${notation.initial}$ et l'on vise "
            f"${notation.terme(rang)}$ : il y a donc **{pas} pas**. C'est ce nombre — "
            f"et non {rang} — qui apparaît dans la formule. D'où l'exposant "
            f"${exposant}$ plutôt que $n$ tout court."
            if n0 == 1
            else f"Le premier terme est ${notation.initial}$ et l'on vise "
            f"${notation.terme(rang)}$ : il y a exactement **{pas} pas**. Comme la "
            "suite démarre au rang $0$, ce nombre de pas coïncide avec le rang.",
        ),
        Etape(
            "Écrire la forme explicite",
            f"La forme explicite exprime ${notation.courant}$ **directement en "
            f"fonction de $n$**, sans passer par les termes précédents.",
            explicite,
        ),
        Etape(
            "Substituer",
            "",
            rf"{notation.terme(rang)} \approx {L(round(reponse))}",
        ),
        Etape(
            "Vérifier — sur un petit rang",
            f"La formule doit redonner les premiers termes : pour $n = {n0}$, elle "
            f"donne bien ${L(depart)}$. ✓ Tester la formule sur un rang connu "
            "est la seule vérification fiable d'un passage à l'explicite — et elle "
            "prend dix secondes.",
        ),
        Etape(
            "Interpréter — pourquoi les deux écritures coexistent",
            "La récurrence dit **ce qui se passe** d'une année à l'autre ; l'explicite "
            "permet de **projeter** à n'importe quel horizon. Une projection à 40 ans "
            "n'est possible que sous la seconde forme.",
        ),
    ]

    pieges = [(naif, message_naif)]
    if n0 == 1:
        trop = (
            depart * coef**rang
            if modele == "geometrique"
            else depart + rang * raison
        )
        pieges.append(
            (
                trop,
                f"Vous avez compté {rang} pas. La suite démarrant au rang $1$, "
                f"l'exposant correct est ${exposant}$ : il n'y a que {pas} pas "
                f"jusqu'au rang {rang}.",
            )
        )
    else:
        pieges.append(
            (
                depart * coef ** (rang - 1)
                if modele == "geometrique"
                else depart + (rang - 1) * raison,
                "Vous avez retiré un pas sans raison : la suite démarre au rang $0$, "
                f"donc il y a bien {pas} pas jusqu'au rang {rang}. Le réflexe "
                "« $n-1$ » n'est justifié que si le premier terme est de rang $1$.",
            )
        )

    return Exercice(
        enonce=enonce,
        reponse=reponse,
        etapes=etapes,
        libelle=f"{notation.lettre}_{rang} =",
        unite=ctx.unite,
        tolerance=0.002,
        indice=f"Combien de fois la règle s'applique-t-elle entre le rang {n0} et "
        f"le rang {rang} ?",
        pieges=pieges,
    )


# --- 3. Variations d'une suite (QCM) ---------------------------------------


def gen_variations() -> Exercice:
    ctx = cx.tirer(cx.EFFECTIFS)
    notation = cx.tirer_notation_suite()
    n0 = notation.depart
    sens = random.choice(["croissante", "decroissante", "ni"])
    presentation = random.choice(["tableau", "liste", "explicite"])
    base = random.choice([500, 800, 1000, 1250])

    options = [
        "La suite est croissante",
        "La suite est décroissante",
        "La suite n'est ni croissante ni décroissante",
    ]

    rangs = [n0 + k for k in range(5)]

    if presentation == "explicite":
        # On donne la formule : l'étudiant doit produire lui-même les termes,
        # aux rangs effectivement définis — qui ne commencent pas toujours à 0.
        if sens == "croissante":
            r = random.choice([40, 75, 120])
            formule = rf"{notation.courant} = {base} + {r}\,n"
            termes = [base + r * n for n in rangs]
            bonne = options[0]
            justification = (
                f"La différence ${notation.suivant} - {notation.courant}$ vaut "
                f"${r}$ : constante et **positive**, donc chaque terme dépasse "
                "le précédent."
            )
        elif sens == "decroissante":
            r = random.choice([40, 75, 120])
            formule = rf"{notation.courant} = {base} - {r}\,n"
            termes = [base - r * n for n in rangs]
            bonne = options[1]
            justification = (
                f"La différence ${notation.suivant} - {notation.courant}$ vaut "
                f"$-{r}$ : constante et **négative**, donc chaque terme est "
                "inférieur au précédent."
            )
        else:
            s = random.choice([n0 + 2, n0 + 3])
            formule = rf"{notation.courant} = n^2 - {2 * s}\,n + {base}"
            termes = [n * n - 2 * s * n + base for n in rangs]
            bonne = options[2]
            justification = (
                f"La suite descend jusqu'au rang ${s}$, puis remonte. Les différences "
                "successives changent donc de signe : aucun des deux qualificatifs ne "
                "s'applique sur l'ensemble des rangs."
            )
        enonce = f"""
> On modélise {ctx.sujet} par la suite définie, pour tout $n \\geq {n0}$, par
>
> $$ {formule} $$
>
> Que peut-on dire de ses **variations** ?
"""
    else:
        if sens == "croissante":
            r = random.choice([40, 75, 120])
            termes = [base + k * r for k in range(5)]
            bonne = options[0]
            justification = (
                f"Les différences successives valent toutes ${r}$ : constantes et "
                "**positives**, donc chaque terme dépasse le précédent."
            )
        elif sens == "decroissante":
            r = random.choice([-40, -75, -120])
            termes = [base + k * r for k in range(5)]
            bonne = options[1]
            justification = (
                f"Les différences successives valent toutes ${r}$ : constantes et "
                "**négatives**, donc chaque terme est inférieur au précédent."
            )
        else:
            r = random.choice([150, 200])
            termes = [base + (r if k % 2 else -r) for k in range(5)]
            bonne = options[2]
            justification = (
                "Les différences successives changent de signe : la suite monte, puis "
                "descend, puis remonte. Aucun des deux qualificatifs ne s'applique."
            )

        if presentation == "tableau":
            corps = cx.tableau_suite(notation, termes)
            corps = "\n".join("> " + ligne for ligne in corps.splitlines())
        else:
            liste = " · ".join(
                f"${notation.terme(n0 + k)} = {L(t)}$" for k, t in enumerate(termes)
            )
            corps = f"> {liste}"

        enonce = f"""
> On relève les cinq premières valeurs {ctx.du} :
>
{corps}
>
> Que peut-on dire de ses **variations** ?
"""

    diffs = [termes[k + 1] - termes[k] for k in range(4)]
    liste_diffs = ", ".join(f"${L(d)}$" for d in diffs)

    etapes = [
        Etape(
            "Identifier — la définition passe par la différence",
            f"Une suite est croissante si ${notation.suivant} - {notation.courant} > 0$ "
            "**pour tout $n$**. Le mot « pour tout » est essentiel : il ne suffit pas "
            "que ce soit vrai une fois.",
        ),
        Etape(
            "Produire les termes, puis les différences",
            (
                "La formule explicite donne chaque terme sans dérouler : "
                if presentation == "explicite"
                else "Les termes sont donnés ; il reste à les soustraire deux à deux : "
            )
            + " · ".join(
                f"${notation.terme(n0 + k)} = {L(t)}$" for k, t in enumerate(termes)
            )
            + f".\n\nDifférences successives : {liste_diffs}.",
        ),
        Etape(
            "Vérifier — le signe est-il constant ?",
            justification,
        ),
        Etape(
            "Interpréter — attention aux mots",
            "« Croissante » ne veut pas dire « qui augmente beaucoup », mais « qui "
            "n'a jamais diminué ». Une suite qui gagne une unité par an est "
            "croissante ; une suite qui en gagne mille puis en perd une ne l'est pas.",
        ),
    ]

    return Exercice(
        enonce=enonce,
        reponse=bonne,
        etapes=etapes,
        type_reponse="qcm",
        options=options,
        libelle="Variations",
        indice="Calculez les différences entre termes consécutifs et regardez "
        "leur signe.",
        pieges=[
            (o, f"Recalculez les différences entre termes consécutifs : {liste_diffs}.")
            for o in options
            if o != bonne
        ],
    )


# --- 4. Rang ou valeur ? (QCM) ---------------------------------------------


def gen_notation() -> Exercice:
    ctx = cx.tirer(cx.EFFECTIFS)
    notation = cx.tirer_notation_suite()
    n0 = notation.depart
    depart = random.choice([12_400, 9_500, 15_200, 6_800])
    taux = random.choice([5, 8, 10])
    coef = 1 + taux / 100
    rang = n0 + random.choice([4, 6, 7])
    annee_base = random.choice([2018, 2020, 2021])
    valeur = depart * coef ** (rang - n0)
    annee = annee_base + (rang - n0)

    bonne = (
        f"{rang} est le rang, soit l'année {annee} ; la valeur associée est "
        f"environ {_fr(valeur, 0)} {ctx.unite}."
    )
    inverse = f"{rang} est le nombre de {ctx.court} ; le rang est environ {_fr(valeur, 0)}."
    annee_brute = f"{rang} désigne l'année {rang}."
    somme = f"{notation.terme(rang)} est la somme des {rang} premiers termes."
    options = [bonne, inverse, annee_brute, somme]
    random.shuffle(options)

    enonce = f"""
> {_maj(ctx.sujet)} s'élevait à **{_fr(depart, 0)} {ctx.unite}** fin {annee_base}.
> Cette valeur est notée ${notation.initial}$, et la grandeur
> {cx.phrase_taux(taux)}.
>
> Que désignent respectivement **{rang}** et **${notation.terme(rang)}$** ?
"""

    etapes = [
        Etape(
            "Identifier — deux objets de nature différente",
            f"Le **rang** $n$ compte les étapes : c'est un entier sans unité. "
            f"La **valeur** ${notation.courant}$ est la grandeur mesurée : ici un "
            f"nombre de {ctx.court}. Les confondre rend toute la suite illisible.",
        ),
        Etape(
            "Situer le rang dans le temps",
            f"${notation.initial}$ correspond à fin {annee_base}. Le rang {rang} est "
            f"donc {rang - n0} années plus tard, soit **{annee}** — et non l'année "
            f"{rang}. Le rang n'est pas une date : c'est un compteur d'étapes depuis "
            "la date de référence.",
        ),
        Etape(
            "Calculer la valeur associée",
            "",
            rf"{notation.terme(rang)} = {L(depart)} \times {L(coef)}^{{{rang - n0}}} "
            rf"\approx {L(round(valeur))}",
        ),
        Etape(
            "Interpréter — pourquoi la convention compte",
            f"Si l'on avait posé ${notation.terme(1 - n0)}$ pour {annee_base}, tous les "
            "rangs seraient décalés d'un cran et la formule changerait d'exposant. "
            "Aucune convention n'est meilleure que l'autre, mais il faut dire laquelle "
            "on adopte — et s'y tenir jusqu'au bout du calcul.",
        ),
    ]

    return Exercice(
        enonce=enonce,
        reponse=bonne,
        etapes=etapes,
        type_reponse="qcm",
        options=options,
        libelle="Interprétation",
        indice="Lequel des deux nombres est un compteur, lequel est une grandeur ?",
        pieges=[
            (
                inverse,
                "Les rôles sont inversés : le rang est le petit entier, la valeur est "
                f"l'effectif en {ctx.court}.",
            ),
            (
                annee_brute,
                f"Le rang compte les étapes **depuis** ${notation.initial}$, qui "
                f"correspond à {annee_base}. Le rang {rang} désigne donc {annee}.",
            ),
            (
                somme,
                f"${notation.courant}$ est un **terme**, pas une somme. Les sommes de "
                "suites seront vues en séance 3.",
            ),
        ],
    )


# ==========================================================================

st.markdown("---")

onglets = st.tabs(
    [
        "1️⃣ Lire une récurrence",
        "2️⃣ Passer à l'explicite",
        "3️⃣ Variations",
        "4️⃣ Rang ou valeur ?",
    ]
)

with onglets[0]:
    st.subheader("Dérouler une suite pas à pas")
    executer("s2_recurrence", gen_recurrence)

with onglets[1]:
    st.subheader("Atteindre n'importe quel rang directement")
    executer("s2_explicite", gen_explicite)

with onglets[2]:
    st.subheader("Croissante, décroissante, ou ni l'un ni l'autre")
    executer("s2_variations", gen_variations)

with onglets[3]:
    st.subheader("Vocabulaire et notation")
    executer("s2_notation", gen_notation)

st.markdown("---")
st.caption(
    "Semestre — séance n°2 : Les suites, généralités · Fil rouge D : Mélodia · "
    "Sciences Po."
)
