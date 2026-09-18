"""Série S3 — Suites arithmétiques et géométriques. Fil rouge D : Mélodia."""

import random

import streamlit as st

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
"""
    )

with st.sidebar:
    st.header("📝 Aide-mémoire — Séance 3")
    st.markdown("**Suite arithmétique** (raison $r$)")
    st.latex(r"u_{n+1} = u_n + r \qquad u_n = u_0 + n\,r")
    st.markdown("**Suite géométrique** (raison $q$)")
    st.latex(r"u_{n+1} = q\,u_n \qquad u_n = u_0 \times q^{\,n}")
    st.markdown("**Somme arithmétique — l'astuce de Gauss**")
    st.latex(r"\sum_{k=0}^{n} u_k = (n+1) \times \frac{u_0 + u_n}{2}")
    st.markdown("**Somme géométrique** ($q \\neq 1$)")
    st.latex(r"\sum_{k=0}^{n} u_k = u_0 \times \frac{1 - q^{\,n+1}}{1 - q}")
    st.info(
        "**Une suite arithmétique est une fonction affine déguisée**\n\n"
        "$u_n = u_0 + nr$ a exactement la forme $ax + b$, avec la raison "
        "dans le rôle de la pente."
    )

CONTEXTES = [
    ("les abonnements vendus par Mélodia", "abonnements"),
    ("le nombre de places en crèche", "places"),
    ("les dossiers traités par le service", "dossiers"),
]


def _fr(v, n=2):
    return f"{v:,.{n}f}".replace(",", "\u202f").replace(".", ",")


# --- 1. Terme d'une suite arithmétique -------------------------------------


def gen_arithmetique() -> Exercice:
    grandeur, unite = random.choice(CONTEXTES)
    u0 = random.choice([1_200, 2_500, 4_000, 6_500])
    r = random.choice([-250, -150, 300, 450, 900])
    n = random.choice([6, 8, 10, 12, 15])
    reponse = float(u0 + n * r)

    enonce = f"""
> {grandeur.capitalize()} valent **{u0:,} {unite}** l'année 0, et évoluent de
> **{r:+} {unite} chaque année**, toujours du même montant.
>
> Combien en compte-t-on l'année **{n}** ?
""".replace(",", "\u202f")

    etapes = [
        Etape(
            "Identifier — arithmétique, car on ajoute toujours la même quantité",
            f"Chaque année ajoute ${r}$, indépendamment du niveau atteint. C'est la "
            "définition d'une suite arithmétique, et cela suffit à choisir la formule.",
        ),
        Etape(
            "Appliquer $u_n = u_0 + n\\,r$",
            f"Inutile de dérouler les {n} termes : la forme explicite donne "
            "directement le rang cherché.",
            rf"u_{{{n}}} = {u0} + {n} \times ({r}) = {u0} + ({n*r}) = {reponse:.0f}",
        ),
        Etape(
            "Vérifier — le sens de l'évolution",
            f"La raison est {'positive' if r > 0 else 'négative'}, donc la suite est "
            f"{'croissante' if r > 0 else 'décroissante'} : le résultat doit être "
            f"{'supérieur' if r > 0 else 'inférieur'} à {u0:,}. ✓"
            .replace(",", "\u202f"),
        ),
        Etape(
            "Interpréter — une fonction affine déguisée",
            f"Représentée en fonction de $n$, cette suite donnerait une **droite** de "
            f"pente ${r}$ : la raison joue exactement le rôle de la pente vue en "
            "pré-rentrée. Seule différence, les points sont isolés.",
        ),
    ]

    return Exercice(
        enonce=enonce,
        reponse=reponse,
        etapes=etapes,
        libelle=f"Valeur l'année {n}",
        unite=unite,
        tolerance=1e-6,
        indice=f"Combien de fois la raison s'applique-t-elle entre l'année 0 et "
        f"l'année {n} ?",
        pieges=[
            (float(u0 + (n - 1) * r),
             f"Vous avez compté {n - 1} pas. La suite commençant au rang 0, il y a "
             f"bien {n} pas jusqu'au rang {n}."),
            (float(u0 * r),
             "Vous avez **multiplié** par la raison : c'est la formule géométrique."),
        ],
    )


# --- 2. Terme d'une suite géométrique --------------------------------------


def gen_geometrique() -> Exercice:
    grandeur, unite = random.choice(CONTEXTES)
    u0 = random.choice([12_400, 8_000, 15_000, 20_000])
    taux = random.choice([-6, -4, 5, 8, 10, 12])
    raison = 1 + taux / 100
    n = random.choice([5, 7, 9, 12])
    reponse = u0 * raison**n
    lineaire = u0 + n * (u0 * taux / 100)

    enonce = f"""
> {grandeur.capitalize()} valent **{u0:,} {unite}** l'année 0 et évoluent de
> **{taux:+} % par an**, au même taux chaque année.
>
> Combien en compte-t-on l'année **{n}** ? Arrondissez à l'unité.
""".replace(",", "\u202f")

    etapes = [
        Etape(
            "Identifier — la raison, c'est le coefficient multiplicateur",
            f"Un pourcentage s'applique à la valeur **courante**, donc chaque année "
            f"multiplie par le même nombre ${raison}$. Ce nombre est exactement le "
            "coefficient multiplicateur de la pré-rentrée : rien de nouveau, un nom "
            "de plus.",
        ),
        Etape(
            "Appliquer $u_n = u_0 \\times q^{\\,n}$",
            "",
            rf"u_{{{n}}} = {u0} \times ({raison})^{{{n}}} "
            rf"\approx {u0} \times {raison**n:.5f} \approx {reponse:.0f}",
        ),
        Etape(
            "Vérifier — comparer au cas linéaire",
            f"Si la variation absolue de la première année s'était répétée, on "
            f"obtiendrait {lineaire:,.0f} {unite}. Le résultat géométrique "
            f"({reponse:,.0f}) est "
            f"{'supérieur' if reponse > lineaire else 'inférieur'} : "
            + ("les hausses portent chaque année sur une base plus grande."
               if taux > 0 else
               "les baisses portent chaque année sur une base plus petite, donc "
               "elles ralentissent.")
            + " ✓".replace(",", "\u202f"),
        ),
        Etape(
            "Interpréter",
            f"Sur {n} ans, l'écart avec le raisonnement linéaire atteint déjà "
            f"{abs(reponse - lineaire):,.0f} {unite}. C'est ce mécanisme qui rendra "
            "les projections de long terme si sensibles au taux retenu — on le "
            "retrouvera avec la dette en séance 6.".replace(",", "\u202f"),
        ),
    ]

    return Exercice(
        enonce=enonce,
        reponse=reponse,
        etapes=etapes,
        libelle=f"Valeur l'année {n}",
        unite=unite,
        tolerance=0.002,
        indice="Le coefficient multiplicateur s'applique une fois par an.",
        pieges=[
            (float(lineaire),
             "Vous avez répété la **même variation absolue** chaque année. Un "
             "pourcentage porte sur la valeur courante, qui change."),
            (float(u0 * raison),
             "Vous n'avez appliqué le coefficient qu'une seule fois."),
        ],
    )


# --- 3. Reconnaître le type (QCM) ------------------------------------------


def gen_reconnaitre() -> Exercice:
    est_geometrique = random.choice([True, False])
    u0 = random.choice([1_000, 2_000, 4_000])

    if est_geometrique:
        raison = random.choice([1.5, 2, 0.5, 1.25])
        termes = [u0 * raison**k for k in range(4)]
        bonne = "Géométrique : le rapport entre termes consécutifs est constant"
    else:
        r = random.choice([300, 600, 750, -250])
        termes = [u0 + k * r for k in range(4)]
        while min(termes) <= 0:
            r = random.choice([300, 600, 750])
            termes = [u0 + k * r for k in range(4)]
        bonne = "Arithmétique : la différence entre termes consécutifs est constante"

    options = [
        "Arithmétique : la différence entre termes consécutifs est constante",
        "Géométrique : le rapport entre termes consécutifs est constant",
        "Ni l'une ni l'autre",
    ]

    liste = " · ".join(
        f"$u_{k} = {t:,.0f}$".replace(",", "\u202f") for k, t in enumerate(termes)
    )
    diffs = [termes[k + 1] - termes[k] for k in range(3)]
    rapports = [termes[k + 1] / termes[k] for k in range(3)]

    enonce = f"""
> On relève les quatre premières valeurs d'une suite :
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
            "**rapports** : s'ils sont constants, elle est géométrique.",
        ),
        Etape(
            "Test des différences",
            "Différences : "
            + ", ".join(f"${d:,.0f}$".replace(",", "\u202f") for d in diffs)
            + (" — non constantes." if est_geometrique else " — constantes."),
        ),
        Etape(
            "Test des rapports",
            "Rapports : " + ", ".join(f"${r:.4g}$" for r in rapports)
            + (" — constants." if est_geometrique else " — non constants."),
        ),
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
        indice="Différences d'abord, rapports ensuite.",
        pieges=[
            (o, "Refaites les deux tests : "
                + ("les différences ne sont pas constantes ici."
                   if est_geometrique else "les rapports ne sont pas constants ici."))
            for o in options if o != bonne
        ],
    )


# --- 4. Somme d'une suite ---------------------------------------------------


def gen_somme() -> Exercice:
    modele = random.choice(["arithmetique", "geometrique"])
    n = random.choice([6, 7, 9, 11])

    if modele == "arithmetique":
        u0 = random.choice([1_500, 2_400, 3_000])
        r = random.choice([200, 350, 500])
        un = u0 + n * r
        reponse = float((n + 1) * (u0 + un) / 2)
        enonce = f"""
> Une suite arithmétique commence à $u_0 = {u0:,}$ et progresse de **{r}** par rang.
>
> Calculez la **somme** $u_0 + u_1 + \\cdots + u_{{{n}}}$.
""".replace(",", "\u202f")
        etapes = [
            Etape(
                "Identifier — pourquoi une formule plutôt qu'une addition",
                f"Pour {n + 1} termes, additionner à la main reste possible. Pour 40 "
                "termes, il faut une formule. Et c'est bien une somme qui est "
                "demandée, pas le dernier terme.",
            ),
            Etape(
                "Calculer le dernier terme",
                "La formule de la somme a besoin des deux extrémités.",
                rf"u_{{{n}}} = {u0} + {n} \times {r} = {un}",
            ),
            Etape(
                "Appliquer l'astuce de Gauss",
                "On apparie le premier terme avec le dernier, le deuxième avec "
                f"l'avant-dernier : chaque paire vaut ${u0 + un}$. Il suffit donc de "
                "multiplier le nombre de termes par leur moyenne.",
                rf"S = ({n} + 1) \times \frac{{{u0} + {un}}}{{2}} = {reponse:.0f}",
            ),
            Etape(
                "Vérifier — l'encadrement",
                f"La somme doit être comprise entre ${n + 1} \\times {u0} = "
                f"{(n+1)*u0:,}$ (si tous les termes valaient le plus petit) et "
                f"${n + 1} \\times {un} = {(n+1)*un:,}$. "
                f"{reponse:,.0f} est bien entre les deux. ✓".replace(",", "\u202f"),
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
            (float(un),
             "Vous avez donné le **dernier terme**, pas la somme de tous les termes."),
            (float(n * (u0 + un) / 2),
             f"Il y a ${n} + 1 = {n + 1}$ termes, pas ${n}$ : la suite commence au "
             "rang 0."),
        ]
        libelle = "Somme"
    else:
        u0 = random.choice([1_000, 2_500, 5_000])
        taux = random.choice([5, 8, 10])
        q_ = 1 + taux / 100
        reponse = u0 * (1 - q_ ** (n + 1)) / (1 - q_)
        enonce = f"""
> Une suite géométrique commence à $u_0 = {u0:,}$ et progresse de **{taux} %** par rang.
>
> Calculez la **somme** $u_0 + u_1 + \\cdots + u_{{{n}}}$. Arrondissez à l'unité.
""".replace(",", "\u202f")
        etapes = [
            Etape(
                "Identifier — la somme géométrique a sa propre formule",
                "L'astuce de Gauss ne fonctionne pas ici : les termes ne sont pas "
                "espacés régulièrement, donc les paires n'ont pas toutes la même "
                "somme. Une autre formule est nécessaire.",
            ),
            Etape(
                "Compter les termes",
                f"De $u_0$ à $u_{{{n}}}$, il y a **{n + 1}** termes. C'est ce nombre "
                "qui apparaît en exposant dans la formule.",
                rf"S = u_0 \times \frac{{1 - q^{{\,{n}+1}}}}{{1 - q}}",
            ),
            Etape(
                "Calculer",
                "",
                rf"S = {u0} \times \frac{{1 - ({q_})^{{{n+1}}}}}{{1 - {q_}}} "
                rf"\approx {reponse:.0f}",
            ),
            Etape(
                "Vérifier — l'encadrement",
                f"La somme doit dépasser ${n + 1} \\times {u0} = {(n+1)*u0:,}$ "
                "(si tous les termes valaient le premier), puisque la suite est "
                f"croissante. {reponse:,.0f} le dépasse bien. ✓"
                .replace(",", "\u202f"),
            ),
            Etape(
                "Interpréter",
                "Le total cumulé croît beaucoup plus vite que le dernier terme. "
                "C'est pourquoi, sur une dette ou un stock cumulé, raisonner sur la "
                "seule dernière année sous-estime systématiquement l'enjeu.",
            ),
        ]
        pieges = [
            (float(u0 * q_**n),
             "Vous avez donné le **dernier terme**, pas la somme."),
            (float(u0 * (1 - q_**n) / (1 - q_)),
             f"Il y a ${n} + 1 = {n + 1}$ termes : l'exposant de la formule est "
             f"${n + 1}$, pas ${n}$."),
        ]
        libelle = "Somme"

    return Exercice(
        enonce=enonce,
        reponse=reponse,
        etapes=etapes,
        libelle=libelle,
        tolerance=0.002,
        indice="Combien y a-t-il de termes entre le rang 0 et le rang n ?",
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
