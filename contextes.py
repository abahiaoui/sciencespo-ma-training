"""
contextes.py — Banque de contextes, de notations et de formes d'énoncé.

Pourquoi ce module
------------------
Un exercice tiré au hasard ne doit pas varier seulement par ses *nombres*.
Un étudiant qui a rencontré vingt fois

    u_0 = 12 400,  u_{n+1} = 1,08 × u_n

a mémorisé un gabarit, pas une méthode : il sera désarçonné par

    v_1 = 340,  v_{n+1} = v_n - 12

qui relève pourtant exactement du même geste. Le but de ce module est de
rendre le *gabarit* instable et la *méthode* stable.

Trois axes de variation sont outillés ici :

1. le **contexte** — de quoi parle l'énoncé (banques thématiques ci-dessous) ;
2. la **notation** — quelle lettre pour la suite ou la fonction, quel rang
   initial (0 ou 1), quelle variable ($x$, $t$, $q$, $p$) ;
3. la **forme** — par quoi l'objet est donné : une formule, une phrase, un
   tableau de valeurs ; une expression développée ou factorisée.

Règle d'usage
-------------
Un générateur tire son contexte, sa notation et sa forme, puis reconstruit
l'énoncé **et la correction** sur ce qu'il a tiré. Aucun texte de correction
ne doit supposer un contexte, une lettre ou une forme particulière : c'est la
même exigence que pour les paramètres numériques.
"""

import random

from dataclasses import dataclass
from typing import List, Sequence, Tuple

# --------------------------------------------------------------------------
# Contextes
# --------------------------------------------------------------------------


def _contracter(groupe: str) -> str:
    """« le budget » → « du budget », « l'atelier » → « de l'atelier »."""
    for prefixe, contraction in (
        ("le ", "du "),
        ("les ", "des "),
        ("la ", "de la "),
        ("l'", "de l'"),
        ("un ", "d'un "),
        ("une ", "d'une "),
    ):
        if groupe.startswith(prefixe):
            return contraction + groupe[len(prefixe) :]
    return "de " + groupe


def a_contracte(groupe: str) -> str:
    """« le personnel » → « au personnel », « les soins » → « aux soins »."""
    for prefixe, contraction in (
        ("le ", "au "),
        ("les ", "aux "),
        ("la ", "à la "),
        ("l'", "à l'"),
    ):
        if groupe.startswith(prefixe):
            return contraction + groupe[len(prefixe) :]
    return "à " + groupe


@dataclass(frozen=True)
class Contexte:
    """Un habillage d'énoncé.

    Tous les champs ne sont pas pertinents pour toutes les banques : un
    contexte de marché renseigne `bien`, `unite_prix` et `unite_quantite`,
    un contexte d'effectif se contente de `sujet`, `court` et `unite`.
    """

    acteur: str  # « Mélodia », « la mairie de Villeneuve »
    sujet: str  # « le nombre d'abonnés de Mélodia » (groupe nominal complet)
    court: str  # « abonnés » (pour les phrases courtes)
    unite: str  # unité affichée après un nombre dans le champ de réponse
    bien: str = ""  # « un studio », « une place de festival »
    unite_prix: str = ""  # « €/mois », « € »
    unite_quantite: str = ""  # « studios », « places »
    singulier: str = ""  # « studio », « place » : pour « € par studio »
    variable: str = "x"  # variable naturelle du contexte
    monetaire: bool = False
    verbe_hausse: str = "gagne"
    verbe_baisse: str = "perd"

    @property
    def du(self) -> str:
        """Le sujet précédé de « de », contracté : « du nombre… », « de l'effectif… ».

        Sans cela, les énoncés écrivent « les valeurs de le nombre d'abonnés ».
        Une faute d'élision dans un énoncé de mathématiques décrédibilise tout
        le reste, et les étudiants la remarquent avant l'exercice.
        """
        return _contracter(self.sujet)

    @property
    def le_bien(self) -> str:
        """`bien` avec un article défini : « un studio » → « le studio »."""
        for indefini, (masculin, feminin) in (("un ", ("le ", "l'")), ("une ", ("la ", "l'"))):
            if self.bien.startswith(indefini):
                reste = self.bien[len(indefini) :]
                article = feminin if reste[:1].lower() in "aeiouyéèêh" else masculin
                return article + reste
        return self.bien

    @property
    def du_bien(self) -> str:
        """`bien` précédé de « de », contracté : « du studio », « de l'abonnement »."""
        return _contracter(self.le_bien)


# Effectifs : tout ce qui se compte en individus, en dossiers, en passages.
# Banque de référence des séances sur les suites.
EFFECTIFS: List[Contexte] = [
    Contexte(
        acteur="Mélodia",
        sujet="le nombre d'abonnés de la plateforme Mélodia",
        court="abonnés",
        unite="abonnés",
        variable="n",
    ),
    Contexte(
        acteur="la médiathèque municipale",
        sujet="le nombre de prêts annuels de la médiathèque",
        court="prêts",
        unite="prêts",
        variable="n",
    ),
    Contexte(
        acteur="le service des titres de séjour",
        sujet="le nombre de dossiers en attente d'instruction",
        court="dossiers",
        unite="dossiers",
        variable="n",
        verbe_hausse="voit arriver",
        verbe_baisse="résorbe",
    ),
    Contexte(
        acteur="le club d'aviron",
        sujet="l'effectif des licenciés du club d'aviron",
        court="licenciés",
        unite="licenciés",
        variable="n",
    ),
    Contexte(
        acteur="la ligne de bus 14",
        sujet="la fréquentation quotidienne de la ligne de bus 14",
        court="voyageurs",
        unite="voyageurs",
        variable="n",
    ),
]

# Grandeurs monétaires : budgets, dettes, loyers, chiffres d'affaires.
# Banque de référence des séances sur les pourcentages et l'exponentielle.
MONETAIRES: List[Contexte] = [
    Contexte(
        acteur="la commune de Villeneuve",
        sujet="l'encours de la dette de Villeneuve",
        court="dette",
        unite="M€",
        monetaire=True,
        variable="t",
        verbe_hausse="alourdit sa dette de",
        verbe_baisse="allège sa dette de",
    ),
    Contexte(
        acteur="le département",
        sujet="la dotation annuelle versée au département",
        court="dotation",
        unite="M€",
        monetaire=True,
        variable="t",
        verbe_hausse="augmente de",
        verbe_baisse="diminue de",
    ),
    Contexte(
        acteur="le parc locatif du centre-ville",
        sujet="le loyer moyen d'un studio du centre-ville",
        court="loyer",
        unite="€",
        monetaire=True,
        bien="un studio",
        variable="t",
        verbe_hausse="augmente de",
        verbe_baisse="diminue de",
    ),
    Contexte(
        acteur="la coopérative Fil & Trame",
        sujet="le chiffre d'affaires de la coopérative Fil & Trame",
        court="chiffre d'affaires",
        unite="k€",
        monetaire=True,
        variable="t",
        verbe_hausse="augmente de",
        verbe_baisse="diminue de",
    ),
    Contexte(
        acteur="le fonds de soutien aux associations",
        sujet="le montant du fonds de soutien aux associations",
        court="fonds",
        unite="k€",
        monetaire=True,
        variable="t",
        verbe_hausse="est abondé de",
        verbe_baisse="est amputé de",
    ),
]

# Productions : une quantité produite ou traitée, et son coût.
# Banque de référence des séances sur la dérivation et l'optimisation.
PRODUCTIONS: List[Contexte] = [
    Contexte(
        acteur="l'atelier municipal de réparation",
        sujet="le coût total de l'atelier municipal",
        court="coût",
        unite="€",
        bien="un vélo réparé",
        unite_quantite="vélos",
        singulier="vélo",
        unite_prix="€",
        variable="q",
        monetaire=True,
    ),
    Contexte(
        acteur="l'imprimerie associative",
        sujet="le coût total de l'imprimerie associative",
        court="coût",
        unite="€",
        bien="une affiche",
        unite_quantite="affiches",
        singulier="affiche",
        unite_prix="€",
        variable="q",
        monetaire=True,
    ),
    Contexte(
        acteur="la conserverie solidaire",
        sujet="le coût de production de la conserverie solidaire",
        court="coût",
        unite="€",
        bien="un bocal",
        unite_quantite="bocaux",
        singulier="bocal",
        unite_prix="€",
        variable="q",
        monetaire=True,
    ),
    Contexte(
        acteur="la cuisine centrale",
        sujet="le coût de fonctionnement de la cuisine centrale",
        court="coût",
        unite="€",
        bien="un repas",
        unite_quantite="repas",
        singulier="repas",
        unite_prix="€",
        variable="q",
        monetaire=True,
    ),
]

# Marchés : un prix et une quantité, donc une offre et une demande.
# Banque de référence des séances sur les fonctions affines et l'équilibre.
MARCHES: List[Contexte] = [
    Contexte(
        acteur="le marché du logement étudiant",
        sujet="le marché du studio étudiant",
        court="studios",
        unite="studios",
        bien="un studio",
        unite_prix="€",
        unite_quantite="studios",
        singulier="studio",
        variable="p",
        monetaire=True,
    ),
    Contexte(
        acteur="le festival de Villeneuve",
        sujet="le marché des places du festival",
        court="places",
        unite="places",
        bien="une place",
        unite_prix="€",
        unite_quantite="places",
        singulier="place",
        variable="p",
        monetaire=True,
    ),
    Contexte(
        acteur="Mélodia",
        sujet="le marché de l'abonnement musical",
        court="abonnements",
        unite="milliers d'abonnements",
        bien="un abonnement mensuel",
        unite_prix="€",
        unite_quantite="milliers d'abonnements",
        singulier="millier d'abonnements",
        variable="p",
        monetaire=True,
    ),
    Contexte(
        acteur="l'atelier de vélos reconditionnés",
        sujet="le marché du vélo reconditionné",
        court="vélos",
        unite="vélos",
        bien="un vélo reconditionné",
        unite_prix="€",
        unite_quantite="vélos",
        singulier="vélo",
        variable="p",
        monetaire=True,
    ),
]

# Dispositifs tarifaires : deux offres concurrentes, d'où équations et seuils.
# Banque de référence des séances sur les équations et les inéquations.
DISPOSITIFS: List[Tuple[Contexte, str, str]] = [
    (
        Contexte(
            acteur="Vélocité",
            sujet="le service de vélos en libre-service Vélocité",
            court="trajets",
            unite="trajets",
            bien="un trajet",
            unite_prix="€",
            unite_quantite="trajets",
            singulier="trajet",
            variable="x",
            monetaire=True,
        ),
        "l'abonnement annuel",
        "le paiement à l'unité",
    ),
    (
        Contexte(
            acteur="la piscine municipale",
            sujet="la tarification de la piscine municipale",
            court="entrées",
            unite="entrées",
            bien="une entrée",
            unite_prix="€",
            unite_quantite="entrées",
            singulier="entrée",
            variable="x",
            monetaire=True,
        ),
        "la carte d'abonné",
        "le ticket à l'unité",
    ),
    (
        Contexte(
            acteur="le réseau de bus",
            sujet="la tarification du réseau de bus",
            court="voyages",
            unite="voyages",
            bien="un voyage",
            unite_prix="€",
            unite_quantite="voyages",
            singulier="voyage",
            variable="x",
            monetaire=True,
        ),
        "le forfait mensuel",
        "le titre à l'unité",
    ),
    (
        Contexte(
            acteur="la salle de concert",
            sujet="la billetterie de la salle de concert",
            court="concerts",
            unite="concerts",
            bien="un concert",
            unite_prix="€",
            unite_quantite="concerts",
            singulier="concert",
            variable="x",
            monetaire=True,
        ),
        "le pass saison",
        "le billet à l'unité",
    ),
]

# Budgets publics : des masses en euros, à ventiler ou à comparer.
# Banque de référence des séances de pré-rentrée (fractions, puissances).
BUDGETS: List[Contexte] = [
    Contexte(
        acteur="la ville de Villeneuve",
        sujet="le budget de fonctionnement de Villeneuve",
        court="budget",
        unite="€",
        monetaire=True,
        variable="x",
    ),
    Contexte(
        acteur="la région",
        sujet="le budget des transports régionaux",
        court="budget transports",
        unite="€",
        monetaire=True,
        variable="x",
    ),
    Contexte(
        acteur="l'université",
        sujet="la dotation de fonctionnement de l'université",
        court="dotation",
        unite="€",
        monetaire=True,
        variable="x",
    ),
    Contexte(
        acteur="l'intercommunalité",
        sujet="le budget du service des déchets",
        court="budget déchets",
        unite="€",
        monetaire=True,
        variable="x",
    ),
]


def tirer(banque: Sequence) -> Contexte:
    """Tire un contexte au hasard dans une banque."""
    return random.choice(banque)


def tirer_deux(banque: Sequence[Contexte]) -> Tuple[Contexte, Contexte]:
    """Tire deux contextes **distincts** (pour un exercice comparatif)."""
    return tuple(random.sample(list(banque), 2))  # type: ignore[return-value]


# --------------------------------------------------------------------------
# Phrases : le même fait, dit en français plutôt qu'en formule
# --------------------------------------------------------------------------


def _nombre(valeur: float, decimales: int = 0) -> str:
    """Format français : espace fine insécable pour les milliers, virgule décimale."""
    texte = f"{valeur:,.{decimales}f}"
    return texte.replace(",", " ").replace(".", ",")


def latex_nombre(valeur: float, decimales: int = None) -> str:
    """Nombre en LaTeX à la française : virgule décimale, espace fine aux milliers.

    `12400` devient `12\\,400` et `1.08` devient `1{,}08`. Sans cela, les
    énoncés affichent des nombres à l'anglaise au milieu d'un cours en
    français, ce qui est une faute de forme que les étudiants recopient.
    """
    v = float(valeur)
    if decimales is None:
        if abs(v - round(v)) < 1e-9:
            decimales = 0
        elif abs(v * 100 - round(v * 100)) < 1e-9:
            decimales = 2
        else:
            decimales = 4
    entier, _, decimale = f"{v:,.{decimales}f}".partition(".")
    entier = entier.replace(",", r"\,")
    if not decimale:
        return entier
    return entier + "{,}" + decimale.rstrip("0").ljust(1, "0")


def phrase_flux(ctx: Contexte, delta: float, periode: str = "par an") -> str:
    """« gagne 900 abonnés par an » / « augmente de 1,2 M€ par an ».

    Permet de donner *en toutes lettres* une raison arithmétique, au lieu de
    l'écrire sous forme de récurrence. C'est la même information, mais
    l'étudiant doit la traduire lui-même — ce qui est justement le geste évalué.
    """
    montant = _nombre(abs(delta), 0 if float(delta).is_integer() else 1)
    verbe = ctx.verbe_hausse if delta >= 0 else ctx.verbe_baisse
    return f"{verbe} {montant} {ctx.unite} {periode}".strip()


def phrase_coefficient(coef: float, periode: str = "d'une année sur l'autre") -> str:
    """« est multiplié par 1,08 d'une année sur l'autre »."""
    return f"est multiplié par {_nombre(coef, 2)} {periode}".strip()


def phrase_taux(taux: float, periode: str = "par an") -> str:
    """« augmente de 8 % par an » / « diminue de 5 % par an ».

    Le taux est arrondi avant test : `(1.05 - 1) * 100` vaut 5,000000000000004
    en flottant, et afficherait « 5,0 % » au lieu de « 5 % ».
    """
    taux = round(float(taux), 6)
    verbe = "augmente" if taux >= 0 else "diminue"
    montant = _nombre(abs(taux), 0 if float(taux).is_integer() else 1)
    return f"{verbe} de {montant} % {periode}".strip()


# --------------------------------------------------------------------------
# Notations : la lettre n'est pas la méthode
# --------------------------------------------------------------------------


@dataclass(frozen=True)
class NotationSuite:
    """Comment cette suite s'écrit : quelle lettre, et à quel rang elle démarre.

    Le rang initial est le piège le plus fréquent : avec un départ à 1, la
    forme explicite d'une suite géométrique est $u_n = u_1 q^{n-1}$ et non
    $u_1 q^{n}$. Faire varier ce départ force l'étudiant à *compter les pas*
    au lieu de recopier une formule.
    """

    lettre: str = "u"
    depart: int = 0

    def terme(self, n) -> str:
        """LaTeX du terme de rang `n` : `u_{5}`, `v_{n+1}`…"""
        return rf"{self.lettre}_{{{n}}}"

    @property
    def initial(self) -> str:
        return self.terme(self.depart)

    @property
    def courant(self) -> str:
        return self.terme("n")

    @property
    def suivant(self) -> str:
        return self.terme("n+1")

    def pas(self, rang: int) -> int:
        """Nombre d'applications de la règle entre le terme initial et `rang`."""
        return rang - self.depart

    @property
    def exposant(self) -> str:
        """`n` si la suite part de 0, `n-1` si elle part de 1."""
        return "n" if self.depart == 0 else "n-1"


def tirer_notation_suite(lettres: Sequence[str] = ("u", "v", "w", "c")) -> NotationSuite:
    """Tire une lettre et un rang de départ (0 ou 1)."""
    return NotationSuite(lettre=random.choice(list(lettres)), depart=random.choice([0, 1]))


@dataclass(frozen=True)
class NotationFonction:
    """Comment cette fonction s'écrit : quel nom, quelle variable."""

    nom: str = "f"
    var: str = "x"

    def de(self, argument: str = "") -> str:
        """LaTeX de l'image : `f(x)`, `C(q)`, `f(3)`…"""
        return rf"{self.nom}({argument if argument != '' else self.var})"

    def derivee(self, argument: str = "") -> str:
        return rf"{self.nom}'({argument if argument != '' else self.var})"

    def seconde(self, argument: str = "") -> str:
        return rf"{self.nom}''({argument if argument != '' else self.var})"


# Notations neutres : la même fonction, sous quatre habits.
NOTATIONS_NEUTRES = [
    NotationFonction("f", "x"),
    NotationFonction("g", "x"),
    NotationFonction("f", "t"),
    NotationFonction("h", "t"),
    NotationFonction("g", "z"),
]

# Notations économiques : le nom dit déjà ce que la fonction mesure.
NOTATIONS_COUT = [
    NotationFonction("C", "q"),
    NotationFonction("C", "x"),
    NotationFonction("K", "q"),
]

NOTATIONS_BENEFICE = [
    NotationFonction("B", "q"),
    NotationFonction("P", "q"),
    NotationFonction("B", "x"),
]

NOTATIONS_RECETTE = [
    NotationFonction("R", "p"),
    NotationFonction("R", "x"),
    NotationFonction("V", "p"),
]


def tirer_notation(banque: Sequence[NotationFonction] = NOTATIONS_NEUTRES) -> NotationFonction:
    return random.choice(list(banque))


# --------------------------------------------------------------------------
# Formes : le même objet, présenté autrement
# --------------------------------------------------------------------------

#: Par quoi une suite est donnée dans l'énoncé.
FORMES_SUITE = ("recurrence", "phrase", "tableau", "explicite")

#: Par quoi une fonction est donnée dans l'énoncé.
FORMES_FONCTION = ("developpee", "factorisee", "phrase", "tableau")


def tableau_latex(entetes: Sequence[str], lignes: Sequence[Sequence[str]]) -> str:
    """Un petit tableau Markdown, pour donner un objet par ses valeurs.

    Donner une suite par un tableau de termes plutôt que par sa règle oblige
    à *reconstituer* le mécanisme : c'est le geste inverse de celui qu'on
    demande d'habitude, et il révèle immédiatement qui a compris.
    """
    tete = "| " + " | ".join(entetes) + " |"
    separateur = "|" + "|".join([":---:"] * len(entetes)) + "|"
    corps = "\n".join("| " + " | ".join(str(c) for c in ligne) + " |" for ligne in lignes)
    return f"{tete}\n{separateur}\n{corps}"


def tableau_suite(notation: NotationSuite, termes: Sequence[float], decimales: int = 0) -> str:
    """Tableau « rang / valeur » d'une suite, prêt à insérer dans un énoncé."""
    rangs = [notation.depart + k for k in range(len(termes))]
    return tableau_latex(
        ["Rang $n$"] + [f"${r}$" for r in rangs],
        # `latex_nombre` et non `_nombre` : en mode mathématique, KaTeX ignore
        # une espace littérale, et « 12 400 » s'afficherait « 12400 ».
        [[f"${notation.courant}$"] + [f"${latex_nombre(t, decimales)}$" for t in termes]],
    )
