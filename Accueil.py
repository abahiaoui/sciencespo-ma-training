"""
Accueil.py — Page d'accueil de la plateforme d'exercices.
Mathématiques appliquées pour les sciences humaines et sociales — Sciences Po.
"""

import streamlit as st

st.set_page_config(
    page_title="Maths appliquées | Plateforme d'exercices",
    page_icon="📐",
    layout="wide",
)

# --------------------------------------------------------------------------
# En-tête
# --------------------------------------------------------------------------

st.title("📐 Mathématiques appliquées")
st.subheader("Plateforme d'entraînement — Sciences Po, 2026-2027")

st.markdown(
    """
Bienvenue. Cette plateforme accompagne les deux modules du cours : la
**pré-rentrée** (6 séances) et le **module de semestre** (11 séances).
Elle ne remplace ni le cours ni les exercices faits en classe : elle sert à
**automatiser les gestes techniques**, pour que votre attention en séance
puisse porter sur le raisonnement.
"""
)

st.markdown("---")

# --------------------------------------------------------------------------
# Le principe
# --------------------------------------------------------------------------

st.header("Comment ça marche")

colonne_1, colonne_2, colonne_3 = st.columns(3)

with colonne_1:
    with st.container(border=True):
        st.markdown("### 🎲 Un énoncé tiré au hasard")
        st.markdown(
            "À **chaque tentative**, ce ne sont pas seulement les nombres qui "
            "changent : le **contexte**, les **lettres** employées et la "
            "**forme** sous laquelle l'énoncé arrive changent aussi. "
            "Il n'y a donc rien à apprendre par cœur — et le jour de l'examen, "
            "aucune présentation ne vous surprendra."
        )

with colonne_2:
    with st.container(border=True):
        st.markdown("### ✍️ Une seule réponse à donner")
        st.markdown(
            "Vous saisissez **le résultat**, rien d'autre. Pas de rédaction, "
            "pas de justification à taper : c'est sur papier que vous "
            "rédigerez, et en séance qu'on en discutera."
        )

with colonne_3:
    with st.container(border=True):
        st.markdown("### 🧭 La méthode complète en retour")
        st.markdown(
            "À la validation, la plateforme déroule la **démarche entière, "
            "étape par étape**, reconstruite sur les nombres de *votre* "
            "énoncé — que votre réponse soit juste ou fausse."
        )

st.info(
    """
**Le point important.** Si vous avez juste, lisez quand même la correction :
un bon résultat obtenu par une démarche approximative ne vaut rien en contrôle.
Si vous avez faux, la plateforme essaie de diagnostiquer **quelle erreur
précise** produit votre valeur — c'est souvent plus instructif que la bonne réponse.
"""
)

st.markdown(
    """
Enfin : **rien n'est enregistré, rien n'est noté**. Aucune de vos réponses ne
m'est transmise et n'entre dans votre moyenne. Vous pouvez vous tromper autant
que vous voulez — c'est même l'usage recommandé.
"""
)

st.markdown("---")

# --------------------------------------------------------------------------
# Progression
# --------------------------------------------------------------------------

st.header("Les séries d'exercices")

st.markdown("#### Module de pré-rentrée")

PRE_RENTREE = [
    ("P1", "Nombres, fractions et puissances", "Notation scientifique, fractions, puissances, racines", True),
    ("P2", "Développer et factoriser", "Identités remarquables, facteur commun", True),
    ("P3", "Équations à une variable", "Premier degré, produit nul, isoler une variable", True),
    ("P4", "Inéquations et systèmes", "Sens de l'inégalité, systèmes 2×2", True),
    ("P5", "Pourcentages, indices et évolutions", "Coefficient multiplicateur, indices base 100", True),
    ("P6", "Fonctions et fonctions affines", "Image, antécédent, pente, offre et demande", True),
]

SEMESTRE = [
    ("S1", "Reprise : fonctions affines, offre et demande", "Équilibre, déplacements, signe d'un produit", True),
    ("S2", "Les suites : généralités", "Récurrence, forme explicite, variations", True),
    ("S3", "Suites arithmétiques et géométriques", "Termes, raisons, sommes", True),
    ("S4", "Le second degré : parabole et forme factorisée", "Orientation, racines, sommet", True),
    ("S5", "Discriminant et signe du trinôme", "Δ, racines, inéquation du second degré", True),
    ("S6", "La fonction exponentielle", "Propriétés, du discret au continu", True),
    ("S7", "Le logarithme népérien", "Inconnue en exposant, temps de doublement", True),
    ("S8", "La dérivation : point de vue local", "Taux d'accroissement, nombre dérivé, tangente", True),
    ("S9", "La fonction dérivée et les variations", "Règles de calcul, tableau de variations", True),
    ("S10", "Dérivée seconde, convexité et optimisation", "Courbure, premier et second ordre", True),
    ("S11", "Plusieurs variables et optimisation sous contrainte", "Dérivées partielles, Lagrangien", True),
]


def afficher_series(series):
    for code, titre, contenu, disponible in series:
        colonne_code, colonne_titre, colonne_etat = st.columns([1, 5, 2])
        colonne_code.markdown(f"**{code}**")
        colonne_titre.markdown(f"**{titre}** — {contenu}")
        if disponible:
            colonne_etat.markdown("🟢 Disponible")
        else:
            colonne_etat.markdown("⚪ À venir")


afficher_series(PRE_RENTREE)

st.markdown("#### Module de semestre")
afficher_series(SEMESTRE)

st.caption(
    "Une série par séance, accessible depuis le menu de gauche. Les énoncés sont "
    "tirés au hasard : revenez-y autant de fois que nécessaire."
)

st.markdown("---")

st.header("Les fils rouges")

st.markdown(
    """
Chaque groupe de séances suit une situation concrète, reprise d'une séance à l'autre
jusqu'à sa résolution complète. Les exercices de la plateforme s'appuient sur les
mêmes situations que les slides.

| | Fil rouge | Séances |
|---|---|---|
| **A** | Le budget de Villeneuve | P1 – P2 |
| **B** | Vélocité, le service de vélos | P3 – P4 |
| **C** | Le logement étudiant | P5 – P6 |
| **D** | Mélodia, plateforme de streaming | S1 – S3 |
| **E** | Le festival de Villeneuve | S4 – S5 |
| **F** | La dette de Villeneuve | S6 – S7 |
| **G** | L'atelier municipal de réparation | S8 – S10 |
| **H** | L'arbitrage budgétaire | S11 |
"""
)

st.markdown("---")

# --------------------------------------------------------------------------
# Conseils d'usage
# --------------------------------------------------------------------------

colonne_gauche, colonne_droite = st.columns(2)

with colonne_gauche:
    st.header("Comment travailler avec")
    st.markdown(
        """
1. **Faites d'abord sur papier**, sans calculatrice quand c'est possible.
   Saisissez seulement le résultat obtenu.
2. **Lisez la correction en entier**, y compris quand vous avez juste.
   Comparez sa démarche à la vôtre : c'est là qu'est le travail utile.
3. **Refaites jusqu'à ce que ce soit fluide**, pas jusqu'à avoir eu bon
   une fois. Un exercice est acquis quand la démarche vient sans hésitation.
4. **Notez ce qui bloque** et posez la question en séance suivante.
"""
    )

with colonne_droite:
    st.header("Rappel des modalités")
    st.markdown(
        """
- **Le contrôle continu**, sur le module de semestre.
- **Un examen final** de 1h30 à la fin du module de semestre ; les notions
  de pré-rentrée y sont exigibles.
"""
    )
    st.latex(r"\text{Moyenne} = \tfrac{2}{3}\,CC + \tfrac{1}{3}\,EF")
    st.markdown(
        "Le contrôle continu pèse donc **deux fois plus** que l'examen final : "
        "c'est le travail régulier qui détermine l'essentiel de la moyenne, "
        "pas une performance sur 1h30."
    )

st.markdown("---")

st.markdown(
    """
**Ahmed Bahiaoui** — Sciences Po
· 📧 [ahmed.bahiaoui@sciencespo.fr](mailto:ahmed.bahiaoui@sciencespo.fr)
· 📚 Les slides sont déposées sur Moodle après chaque séance.
"""
)
