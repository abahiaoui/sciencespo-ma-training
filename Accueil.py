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
            "Les nombres changent à **chaque tentative**. Il n'y a donc rien à "
            "apprendre par cœur : ni la réponse, ni la suite d'opérations. "
            "Refaites un exercice autant de fois que nécessaire."
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
    ("P1", "Fractions et puissances", "Nombres, fractions, puissances, racines", True),
    ("P2", "Développer et factoriser", "Identités remarquables, factorisation", False),
    ("P3", "Proportions et pourcentages", "Parts, taux, points de pourcentage", False),
    ("P4", "Variations et coefficients", "Coefficient multiplicateur, évolutions", False),
    ("P5", "Équations et inéquations", "Résolution, changement de sens", False),
    ("P6", "Droites et pentes", "Fonction affine, lecture graphique", False),
]

SEMESTRE = [
    ("S1", "Fonctions et lectures graphiques", "Notion de fonction, domaine, image", False),
    ("S2", "Taux d'accroissement", "Variation moyenne, sécante", False),
    ("S3", "Dérivation", "Nombre dérivé, tangente, règles de calcul", False),
    ("S4", "Dérivées et variations", "Signe de la dérivée, tableau de variations", False),
    ("S5", "Limites et asymptotes", "Comportement aux bornes", False),
    ("S6", "Convexité et point d'inflexion", "Dérivée seconde", False),
    ("S7", "Logarithme et exponentielle", "Propriétés, croissance, dette", False),
    ("S8", "Optimisation (1)", "Recherche d'extremum, conditions", False),
    ("S9", "Optimisation (2)", "Étude complète appliquée", False),
    ("S10", "Suites et récurrence", "Suites arithmétiques et géométriques", False),
    ("S11", "Élasticité et arbitrages", "Dérivée logarithmique, arbitrage", False),
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
    "Les séries sont mises en ligne au fur et à mesure, après la séance "
    "correspondante. Utilisez le menu de gauche pour y accéder."
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
- **Deux notes de contrôle continu**, une par module.
- **Un examen final** de 1h30 à la fin du module de semestre ; les notions
  de pré-rentrée y sont exigibles.
"""
    )
    st.latex(
        r"\text{Moyenne} = \max\!\left( EF \;;\; \tfrac{1}{4}CC_{\text{pré}}"
        r" + \tfrac{1}{4}CC_{\text{sem}} + \tfrac{1}{2}EF \right)"
    )
    st.markdown(
        "Les contrôles continus ne peuvent que vous **avantager** : "
        "on retient la plus grande des deux quantités."
    )

st.markdown("---")

st.markdown(
    """
**Ahmed Bahiaoui** — Sciences Po
· 📧 [ahmed.bahiaoui@sciencespo.fr](mailto:ahmed.bahiaoui@sciencespo.fr)
· 📚 Les slides sont déposées sur Moodle après chaque séance.
"""
)
