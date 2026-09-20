"""Série S3 — Suites arithmétiques et géométriques. Fil rouge D : Mélodia.

Variation sur trois axes (cf. `contextes.py`) : le contexte, la notation
(lettre, rang initial) et la **forme sous laquelle la suite est donnée** —
une règle de récurrence, un taux en pourcentage, une phrase, un tableau de
relevés, ou deux termes dont il faut d'abord déduire la raison.
"""

import random

import streamlit as st

import contextes as cx
from contextes import latex_nombre as L
from moteur import Etape, Exercice, executer

st.set_page_config(page_title="S3 | Suites arithmétiques et géométriques",
                   page_icon="➕", layout="wide")

st.title("➕ S3 — Suites arithmétiques et géométriques")

with st.expander("📖 Contexte & objectifs", expanded=True):
    st.markdown(
        """
### 🎯 Ce que cette série entraîne
Reconnaître le **type** d'une suite, calculer un terme de rang quelconque, et
**sommer** une suite — par l'astuce de Gauss ou par la formule géométrique.

### 🧠 Le réflexe à installer
Face à une suite : les différences sont-elles constantes (**arithmétique**) ou les
rapports le sont-ils (**géométrique**) ? C'est la même opposition qu'entre intérêts
simples et intérêts composés. Et la raison d'une suite géométrique n'est rien d'autre
que le **coefficient multiplicateur** de la pré-rentrée.

### 🎧 Fil rouge D — Mélodia
Mélodia veut connaître le **nombre total** d'abonnements vendus sur sept ans, et pas
seulement l'effectif de la dernière année.

### ⚠️ La raison n'est pas toujours servie sur un plateau
Selon les tirages, l'énoncé vous donne la raison, un taux en pourcentage, ou
seulement **deux termes** dont il faut la déduire. Et la suite ne démarre pas
toujours au rang $0$ : comptez les pas.
"""
    )

with st.sidebar:
    st.header("📝 Aide-mémoire — Séance 3")
    st.markdown("**Suite arithmétique** (raison $r$)")
    st.latex(r"u_{n+1} = u_n + r \qquad u_n = u_0 + n\,r")
    st.markdown("**Suite géométrique** (raison $q$)")
    st.latex(r"u_{n+1} = q\,u_n \qquad u_n = u_0 \times q^{\,n}")
    st.markdown("**Somme arithmétique — l'astuce de Gauss**")
    st.latex(r"S = (\text{nombre de termes}) \times \frac{\text{premier} + \text{dernier}}{2}")
    st.markdown("**Somme géométrique** ($q \\neq 1$)")
    st.latex(r"S = (\text{premier terme}) \times \frac{1 - q^{\,\text{nb termes}}}{1 - q}")
    st.info(
        "**Une suite arithmétique est une fonction affine déguisée**\n\n"
        "$u_n = u_0 + nr$ a exactement la forme $ax + b$, avec la raison "
        "dans le rôle de la pente."
    )
    st.warning(
        "**Deux termes suffisent à retrouver la raison**\n\n"
        "Arithmétique : $r = \\dfrac{u_q - u_p}{q - p}$. "
        "Géométrique : $q^{\\,j - i} = \\dfrac{u_j}{u_i}$."
    )


def _fr(v, n=2):
    return f"{v:,.{n}f}".replace(",", " ").replace(".", ",")


def _maj(texte: str) -> str:
    return texte[:1].upper() + texte[1:]


# --- 1. Terme d'une suite arithmétique -------------------------------------


def gen_arithmetique() -> Exercice:
    ctx = cx.tirer(cx.EFFECTIFS)
    notation = cx.tirer_notation_suite()
    n0 = notation.depart
    premier = random.choice([1_200, 2_500, 4_000, 6_500])
    r = random.choice([-250, -150, 300, 450, 900])
    rang = n0 + random.choice([6, 8, 10, 12, 15])
    pas = rang - n0
    reponse = float(premier + pas * r)
    presentation = random.choice(["phrase", "recurrence", "deux_termes"])

    if presentation == "recurrence":
        signe = "+" if r > 0 else "-"
        enonce = f"""
> On modélise {ctx.sujet} par la suite définie par
>
> $$ {notation.initial} = {L(premier)} \\qquad
>    {notation.suivant} = {notation.courant} {signe} {L(abs(r))} $$
>
> Calculez **${notation.terme(rang)}$**.
"""
        donnee_raison = (
            f"La récurrence ajoute ${L(r)}$ à chaque pas : la raison est donnée "
            "telle quelle."
        )
    elif presentation == "phrase":
        enonce = f"""
> {_maj(ctx.sujet)} s'élève à **{_fr(premier, 0)} {ctx.unite}** au relevé de rang
> ${n0}$, et {cx.phrase_flux(ctx, r, periode="à chaque relevé")} — toujours du même
> montant.
>
> Combien en compte-t-on au rang **{rang}** ?
"""
        donnee_raison = (
            f"« Toujours du même montant » est la signature d'une suite "
            f"**arithmétique** : la raison vaut ${L(r)}$."
        )
    else:
        intermediaire = n0 + random.choice([3, 4])
        valeur_inter = premier + (intermediaire - n0) * r
        enonce = f"""
> {_maj(ctx.sujet)} suit une suite **arithmétique**. On a relevé deux valeurs :
>
> $$ {notation.initial} = {L(premier)} \\qquad
>    {notation.terme(intermediaire)} = {L(valeur_inter)} $$
>
> Calculez **${notation.terme(rang)}$**.
"""
        donnee_raison = (
            f"La raison n'est pas donnée : il faut la reconstituer. Entre le rang "
            f"${n0}$ et le rang ${intermediaire}$, il y a "
            f"${intermediaire - n0}$ pas pour un écart total de "
            f"${L(valeur_inter - premier)}$, d'où "
            f"$r = \\dfrac{{{L(valeur_inter - premier)}}}{{{intermediaire - n0}}} "
            f"= {L(r)}$."
        )

    etapes = [
        Etape(
            "Identifier — arithmétique, car on ajoute toujours la même quantité",
            f"Chaque pas ajoute la même quantité, indépendamment du niveau atteint. "
            f"C'est la définition d'une suite arithmétique, et cela suffit à choisir "
            f"la formule. {donnee_raison}",
        ),
        Etape(
            "Compter les pas",
            f"Le premier terme est ${notation.initial}$, la cible est "
            f"${notation.terme(rang)}$ : la raison s'applique **{pas} fois**"
            + (
                f", et non {rang} — la suite ne démarre pas au rang $0$."
                if n0 == 1
                else ". Comme la suite démarre au rang $0$, ce compte coïncide "
                "avec le rang."
            ),
        ),
        Etape(
            "Appliquer la forme explicite",
            f"Inutile de dérouler les {pas} termes intermédiaires.",
            rf"{notation.terme(rang)} = {L(premier)} + {pas} \times ({L(r)}) "
            rf"= {L(reponse)}",
        ),
        Etape(
            "Vérifier — le sens de l'évolution",
            f"La raison est {'positive' if r > 0 else 'négative'}, donc la suite est "
            f"{'croissante' if r > 0 else 'décroissante'} : le résultat doit être "
            f"{'supérieur' if r > 0 else 'inférieur'} à {_fr(premier, 0)}. ✓",
        ),
        Etape(
            "Interpréter — une fonction affine déguisée",
            f"Représentée en fonction de $n$, cette suite donnerait une **droite** de "
            f"pente ${L(r)}$ : la raison joue exactement le rôle de la pente vue en "
            "pré-rentrée. Seule différence, les points sont isolés.",
        ),
    ]

    return Exercice(
        enonce=enonce,
        reponse=reponse,
        etapes=etapes,
        libelle=f"{notation.lettre}_{rang} =",
        unite=ctx.unite,
        tolerance=1e-6,
        indice=f"Combien de fois la raison s'applique-t-elle entre le rang {n0} et "
        f"le rang {rang} ?",
        pieges=[
            (
                float(premier + rang * r),
                f"Vous avez compté {rang} pas. La suite démarrant au rang {n0}, "
                f"il n'y en a que {pas}.",
            )
            if n0 == 1
            else (
                float(premier + (pas - 1) * r),
                f"Vous avez compté {pas - 1} pas. La suite démarrant au rang 0, "
                f"il y a bien {pas} pas jusqu'au rang {rang}.",
            ),
            (
                float(premier * r),
                "Vous avez **multiplié** par la raison : c'est la formule géométrique. "
                "Ici on ajoute.",
            ),
        ],
    )


# --- 2. Terme d'une suite géométrique --------------------------------------


def gen_geometrique() -> Exercice:
    ctx = cx.tirer(cx.EFFECTIFS + cx.MONETAIRES)
    notation = cx.tirer_notation_suite()
    n0 = notation.depart
    premier = random.choice([12_400, 8_000, 15_000, 20_000, 5_400])
    taux = random.choice([-6, -4, 5, 8, 10, 12])
    q = 1 + taux / 100
    rang = n0 + random.choice([5, 7, 9, 12])
    pas = rang - n0
    reponse = premier * q**pas
    lineaire = premier + pas * (premier * taux / 100)
    presentation = random.choice(["taux", "coefficient", "recurrence"])

    if presentation == "taux":
        enonce = f"""
> {_maj(ctx.sujet)} vaut **{_fr(premier, 0)} {ctx.unite}** au rang ${n0}$ et
> {cx.phrase_taux(taux, periode="à chaque rang")}, au même taux à chaque fois.
>
> Quelle est sa valeur au rang **{rang}** ? Arrondissez à l'unité.
"""
        lecture = (
            f"Un pourcentage s'applique à la valeur **courante** : passer de $100$ à "
            f"$100 {'+' if taux > 0 else '-'} {abs(taux)}\\,\\%$ revient à multiplier "
            f"par ${L(q)}$. C'est le coefficient multiplicateur de la pré-rentrée, "
            "et c'est la raison de la suite."
        )
    elif presentation == "coefficient":
        enonce = f"""
> {_maj(ctx.sujet)} vaut **{_fr(premier, 0)} {ctx.unite}** au rang ${n0}$. D'un rang
> au suivant, cette grandeur est **multipliée par ${L(q)}$**.
>
> Quelle est sa valeur au rang **{rang}** ? Arrondissez à l'unité.
"""
        lecture = (
            f"La raison est donnée directement : $q = {L(q)}$. Elle est "
            f"{'supérieure' if q > 1 else 'inférieure'} à $1$, donc la suite "
            f"{'croît' if q > 1 else 'décroît'} — ce qui correspond à une évolution "
            f"de ${taux:+}\\,\\%$ par pas."
        )
    else:
        enonce = f"""
> On modélise {ctx.sujet} par la suite définie par
>
> $$ {notation.initial} = {L(premier)} \\qquad
>    {notation.suivant} = {L(q)} \\times {notation.courant} $$
>
> Calculez **${notation.terme(rang)}$**. Arrondissez à l'unité.
"""
        lecture = (
            f"La récurrence multiplie par ${L(q)}$ à chaque pas : c'est donc une "
            f"suite **géométrique** de raison $q = {L(q)}$, ce qui correspond à "
            f"${taux:+}\\,\\%$ par pas."
        )

    etapes = [
        Etape(
            "Identifier — la raison, c'est le coefficient multiplicateur",
            lecture,
        ),
        Etape(
            "Compter les pas",
            f"De ${notation.initial}$ à ${notation.terme(rang)}$, la multiplication "
            f"est répétée **{pas} fois** : c'est cet exposant qu'il faut écrire"
            + (
                f", et non {rang}."
                if n0 == 1
                else ", identique au rang puisque la suite démarre à $0$."
            ),
        ),
        Etape(
            "Appliquer la forme explicite",
            "",
            rf"{notation.terme(rang)} = {L(premier)} \times ({L(q)})^{{{pas}}} "
            rf"\approx {L(round(reponse))}",
        ),
        Etape(
            "Vérifier — comparer au cas linéaire",
            f"Si la variation absolue du premier pas s'était répétée à l'identique, on "
            f"obtiendrait {_fr(lineaire, 0)} {ctx.unite}. Le résultat géométrique "
            f"({_fr(reponse, 0)}) est "
            f"{'supérieur' if reponse > lineaire else 'inférieur'} : "
            + (
                "les hausses portent chaque fois sur une base plus grande."
                if taux > 0
                else "les baisses portent chaque fois sur une base plus petite, donc "
                "elles ralentissent."
            )
            + " ✓",
        ),
        Etape(
            "Interpréter",
            f"Sur {pas} pas, l'écart avec le raisonnement linéaire atteint déjà "
            f"{_fr(abs(reponse - lineaire), 0)} {ctx.unite}. C'est ce mécanisme qui "
            "rendra les projections de long terme si sensibles au taux retenu — on le "
            "retrouvera avec la dette en séance 6.",
        ),
    ]

    return Exercice(
        enonce=enonce,
        reponse=reponse,
        etapes=etapes,
        libelle=f"{notation.lettre}_{rang} =",
        unite=ctx.unite,
        tolerance=0.002,
        indice="Le coefficient multiplicateur s'applique une fois par pas. Combien "
        f"y a-t-il de pas entre le rang {n0} et le rang {rang} ?",
        pieges=[
            (
                float(lineaire),
                "Vous avez répété la **même variation absolue** à chaque pas. Un "
                "pourcentage porte sur la valeur courante, qui change.",
            ),
            (
                float(premier * q),
                "Vous n'avez appliqué le coefficient qu'une seule fois.",
            ),
            (
                float(premier * q**rang),
                f"L'exposant est le nombre de **pas** ({pas}), pas le rang ({rang}) : "
                f"la suite démarre au rang {n0}.",
            )
            if n0 == 1
            else (
                float(premier * q ** (pas - 1)),
                "Vous avez retiré un pas : la suite démarre au rang $0$, donc "
                f"l'exposant est bien {pas}.",
            ),
        ],
    )


# --- 3. Reconnaître le type (QCM) ------------------------------------------


def gen_reconnaitre() -> Exercice:
    ctx = cx.tirer(cx.EFFECTIFS)
    notation = cx.tirer_notation_suite()
    n0 = notation.depart
    # Le troisième cas — « ni l'une ni l'autre » — doit sortir aussi, faute de
    # quoi les étudiants apprennent que cette option n'est jamais la bonne.
    type_suite = random.choice(["arithmetique", "geometrique", "ni"])
    presentation = random.choice(["liste", "tableau", "mecanisme"])
    base = random.choice([1_000, 2_000, 4_000])

    options = [
        "Arithmétique : la différence entre termes consécutifs est constante",
        "Géométrique : le rapport entre termes consécutifs est constant",
        "Ni l'une ni l'autre",
    ]

    if type_suite == "geometrique":
        q = random.choice([1.5, 2, 0.5, 1.25])
        termes = [base * q**k for k in range(4)]
        bonne = options[1]
        mecanisme = f"à chaque rang, la grandeur est **multipliée par {_fr(q, 2)}**"
        verdict = (
            f"Les rapports valent tous ${L(q)}$ : la suite est **géométrique**. "
            "Les différences, elles, augmentent — elles ne peuvent donc pas servir "
            "de critère ici."
        )
    elif type_suite == "arithmetique":
        r = random.choice([300, 600, 750, -250])
        termes = [base + k * r for k in range(4)]
        while min(termes) <= 0:
            r = random.choice([300, 600, 750])
            termes = [base + k * r for k in range(4)]
        bonne = options[0]
        mecanisme = (
            f"à chaque rang, la grandeur {'augmente' if r > 0 else 'diminue'} de "
            f"**{_fr(abs(r), 0)} {ctx.unite}**"
        )
        verdict = (
            f"Les différences valent toutes ${L(r)}$ : la suite est "
            "**arithmétique**. Inutile d'examiner les rapports."
        )
    else:
        # Croissance ni additive ni multiplicative : un mécanisme quadratique.
        a = random.choice([50, 80, 120])
        termes = [base + a * k * k for k in range(4)]
        bonne = options[2]
        mecanisme = (
            f"au rang $n$, la grandeur vaut ${L(base)} + {L(a)}\\,n^2$ — l'ajout "
            "annuel grossit d'année en année, sans que le rapport soit constant"
        )
        verdict = (
            "Les différences ne sont pas constantes (elles augmentent) et les "
            "rapports ne le sont pas davantage : la suite n'est **ni arithmétique "
            "ni géométrique**. C'est le cas le plus fréquent dans la réalité — les "
            "deux modèles du cours sont des idéalisations."
        )

    diffs = [termes[k + 1] - termes[k] for k in range(3)]
    rapports = [termes[k + 1] / termes[k] for k in range(3)]

    if presentation == "mecanisme":
        enonce = f"""
> On modélise {ctx.sujet} par une suite $({notation.courant})$ dont voici le
> mécanisme : {mecanisme}.
>
> De quel type de suite s'agit-il ?
"""
    elif presentation == "tableau":
        tableau = cx.tableau_suite(notation, termes)
        enonce = f"""
> On relève les quatre premières valeurs {ctx.du} :
>
{chr(10).join('> ' + ligne for ligne in tableau.splitlines())}
>
> De quel type de suite s'agit-il ?
"""
    else:
        liste = " · ".join(
            f"${notation.terme(n0 + k)} = {L(t)}$" for k, t in enumerate(termes)
        )
        enonce = f"""
> On relève les quatre premières valeurs {ctx.du} :
>
> {liste}
>
> De quel type de suite s'agit-il ?
"""

    etapes = [
        Etape(
            "Identifier — deux tests, dans cet ordre",
            "On calcule d'abord les **différences** entre termes consécutifs : si "
            "elles sont constantes, la suite est arithmétique. Sinon, on calcule les "
            "**rapports** : s'ils sont constants, elle est géométrique. Si aucun des "
            "deux tests ne passe, la suite n'est ni l'une ni l'autre — c'est une "
            "réponse parfaitement légitime.",
        ),
        Etape(
            "Produire quelques termes",
            "Quelle que soit la forme de l'énoncé, le test porte sur des nombres : "
            + " · ".join(
                f"${notation.terme(n0 + k)} = {L(t)}$" for k, t in enumerate(termes)
            ),
        ),
        Etape(
            "Test des différences",
            "Différences : "
            + ", ".join(f"${L(d)}$" for d in diffs)
            + (" — constantes." if type_suite == "arithmetique" else " — non constantes."),
        ),
        Etape(
            "Test des rapports",
            "Rapports : "
            + ", ".join(f"${r:.4g}$".replace(".", "{,}") for r in rapports)
            + (" — constants." if type_suite == "geometrique" else " — non constants."),
        ),
        Etape("Conclure", verdict),
        Etape(
            "Interpréter — ce que chaque type implique",
            "Une suite arithmétique traduit un mécanisme **additif** : un contingent "
            "fixe attribué chaque année. Une suite géométrique traduit un mécanisme "
            "**proportionnel** : un taux appliqué à un stock. Identifier le mécanisme "
            "importe souvent davantage que calculer le terme.",
        ),
    ]

    return Exercice(
        enonce=enonce,
        reponse=bonne,
        etapes=etapes,
        type_reponse="qcm",
        options=options,
        libelle="Type de suite",
        indice="Différences d'abord, rapports ensuite. Et rien n'interdit que les "
        "deux tests échouent.",
        pieges=[
            (
                o,
                "Refaites les deux tests sur les termes : "
                + ", ".join(f"${L(d)}$" for d in diffs)
                + " pour les différences, "
                + ", ".join(f"${r:.4g}$".replace(".", "{,}") for r in rapports)
                + " pour les rapports.",
            )
            for o in options
            if o != bonne
        ],
    )


# --- 4. Somme d'une suite ---------------------------------------------------


def gen_somme() -> Exercice:
    ctx = cx.tirer(cx.EFFECTIFS)
    notation = cx.tirer_notation_suite()
    n0 = notation.depart
    modele = random.choice(["arithmetique", "geometrique"])
    rang = n0 + random.choice([6, 7, 9, 11])
    nb_termes = rang - n0 + 1
    presentation = random.choice(["formule", "phrase"])

    somme_latex = (
        rf"{notation.initial} + {notation.terme(n0 + 1)} + \cdots + "
        rf"{notation.terme(rang)}"
    )

    if modele == "arithmetique":
        premier = random.choice([1_500, 2_400, 3_000])
        r = random.choice([200, 350, 500])
        dernier = premier + (rang - n0) * r
        reponse = float(nb_termes * (premier + dernier) / 2)

        if presentation == "formule":
            enonce = f"""
> Une suite arithmétique vérifie ${notation.initial} = {L(premier)}$ et progresse
> de **{_fr(r, 0)}** à chaque rang.
>
> Calculez la **somme** ${somme_latex}$.
"""
        else:
            enonce = f"""
> {_maj(ctx.sujet)} s'élève à **{_fr(premier, 0)} {ctx.unite}** la première année
> (rang ${n0}$), puis progresse de **{_fr(r, 0)} {ctx.unite} chaque année**.
>
> Combien cela fait-il **au total**, du rang ${n0}$ au rang ${rang}$ inclus ?
"""

        etapes = [
            Etape(
                "Identifier — une somme, pas un terme",
                f"La question porte sur le **cumul** de tous les termes, pas sur la "
                f"valeur au rang {rang}. Pour {nb_termes} termes, additionner à la "
                "main reste possible ; pour quarante, il faut une formule.",
            ),
            Etape(
                "Compter les termes — l'erreur la plus coûteuse",
                f"Du rang ${n0}$ au rang ${rang}$ **inclus**, il y a "
                f"${rang} - {n0} + 1 = {nb_termes}$ termes. On oublie presque toujours "
                "le « $+1$ » : les deux extrémités comptent.",
            ),
            Etape(
                "Calculer le dernier terme",
                "La formule de Gauss a besoin des deux extrémités.",
                rf"{notation.terme(rang)} = {L(premier)} + {rang - n0} \times "
                rf"{L(r)} = {L(dernier)}",
            ),
            Etape(
                "Appliquer l'astuce de Gauss",
                f"On apparie le premier terme avec le dernier, le deuxième avec "
                f"l'avant-dernier : chaque paire vaut ${L(premier + dernier)}$. La "
                "somme vaut donc le nombre de termes multiplié par leur moyenne.",
                rf"S = {nb_termes} \times \frac{{{L(premier)} + {L(dernier)}}}{{2}} "
                rf"= {L(reponse)}",
            ),
            Etape(
                "Vérifier — l'encadrement",
                f"La somme doit tomber entre ${nb_termes} \\times {L(premier)} = "
                f"{L(nb_termes * premier)}$ (si tous les termes valaient le plus "
                f"petit) et ${nb_termes} \\times {L(dernier)} = "
                f"{L(nb_termes * dernier)}$. ${L(reponse)}$ est bien entre les "
                "deux. ✓",
            ),
            Etape(
                "Interpréter",
                "La somme répond à une question différente du terme : « combien au "
                "total sur la période ? » et non « combien la dernière année ? ». "
                "Pour un budget cumulé ou un nombre total d'abonnements vendus, "
                "c'est la somme qui compte.",
            ),
        ]
        pieges = [
            (
                float(dernier),
                "Vous avez donné le **dernier terme**, pas la somme de tous les termes.",
            ),
            (
                float((nb_termes - 1) * (premier + dernier) / 2),
                f"Il y a ${rang} - {n0} + 1 = {nb_termes}$ termes, pas "
                f"${nb_termes - 1}$ : les deux extrémités comptent.",
            ),
        ]
    else:
        premier = random.choice([1_000, 2_500, 5_000])
        taux = random.choice([5, 8, 10])
        q = 1 + taux / 100
        reponse = premier * (1 - q**nb_termes) / (1 - q)

        if presentation == "formule":
            enonce = f"""
> Une suite géométrique vérifie ${notation.initial} = {L(premier)}$ et progresse
> de **{taux} %** à chaque rang.
>
> Calculez la **somme** ${somme_latex}$. Arrondissez à l'unité.
"""
        else:
            enonce = f"""
> {_maj(ctx.sujet)} s'élève à **{_fr(premier, 0)} {ctx.unite}** la première année
> (rang ${n0}$), puis {cx.phrase_taux(taux, periode="chaque année")}.
>
> Combien cela fait-il **au total**, du rang ${n0}$ au rang ${rang}$ inclus ?
> Arrondissez à l'unité.
"""

        etapes = [
            Etape(
                "Identifier — la somme géométrique a sa propre formule",
                "L'astuce de Gauss ne fonctionne pas ici : les termes ne sont pas "
                "espacés régulièrement, donc les paires n'ont pas toutes la même "
                "somme. Une autre formule est nécessaire.",
            ),
            Etape(
                "Compter les termes — l'erreur la plus coûteuse",
                f"Du rang ${n0}$ au rang ${rang}$ **inclus**, il y a "
                f"${rang} - {n0} + 1 = {nb_termes}$ termes. C'est ce nombre qui "
                "apparaît en exposant dans la formule — pas le rang.",
                rf"S = {notation.initial} \times "
                rf"\frac{{1 - q^{{\,{nb_termes}}}}}{{1 - q}}",
            ),
            Etape(
                "Calculer",
                "",
                rf"S = {L(premier)} \times \frac{{1 - ({L(q)})^{{{nb_termes}}}}}"
                rf"{{1 - {L(q)}}} \approx {L(round(reponse))}",
            ),
            Etape(
                "Vérifier — l'encadrement",
                f"La somme doit dépasser ${nb_termes} \\times {L(premier)} = "
                f"{L(nb_termes * premier)}$ (si tous les termes valaient le premier), "
                f"puisque la suite est croissante. ${L(round(reponse))}$ le dépasse "
                "bien. ✓",
            ),
            Etape(
                "Interpréter",
                "Le total cumulé croît beaucoup plus vite que le dernier terme. "
                "C'est pourquoi, sur une dette ou un stock cumulé, raisonner sur la "
                "seule dernière année sous-estime systématiquement l'enjeu.",
            ),
        ]
        pieges = [
            (
                float(premier * q ** (rang - n0)),
                "Vous avez donné le **dernier terme**, pas la somme.",
            ),
            (
                float(premier * (1 - q ** (nb_termes - 1)) / (1 - q)),
                f"Il y a {nb_termes} termes : l'exposant de la formule est "
                f"${nb_termes}$, pas ${nb_termes - 1}$.",
            ),
        ]

    return Exercice(
        enonce=enonce,
        reponse=reponse,
        etapes=etapes,
        libelle="Somme",
        unite=ctx.unite if presentation == "phrase" else "",
        tolerance=0.002,
        indice=f"Combien y a-t-il de termes entre le rang {n0} et le rang {rang}, "
        "bornes comprises ?",
        pieges=pieges,
    )


# ==========================================================================

st.markdown("---")

onglets = st.tabs(
    [
        "1️⃣ Suite arithmétique",
        "2️⃣ Suite géométrique",
        "3️⃣ Reconnaître le type",
        "4️⃣ Sommer une suite",
    ]
)

with onglets[0]:
    st.subheader("Ajouter toujours la même quantité")
    executer("s3_arithmetique", gen_arithmetique)

with onglets[1]:
    st.subheader("Multiplier toujours par le même nombre")
    executer("s3_geometrique", gen_geometrique)

with onglets[2]:
    st.subheader("Le réflexe : différences ou rapports ?")
    executer("s3_reconnaitre", gen_reconnaitre)

with onglets[3]:
    st.subheader("Le total sur la période")
    executer("s3_somme", gen_somme)

st.markdown("---")
st.caption(
    "Semestre — séance n°3 : Suites arithmétiques et géométriques · "
    "Fil rouge D : Mélodia · Sciences Po."
)
