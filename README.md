# 📐 Mathématiques Appliquées - Sciences Po Training App

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://sciencespo-maths-training.streamlit.app/)

This is an interactive educational platform built with **Python** and **Streamlit** to help Sciences Po students master the mathematical tools used in the social sciences. Its companion course is *Mathématiques appliquées pour les sciences humaines et sociales*, taught in two modules: a pre-term module (6 sessions) and a semester module (11 sessions).

Unlike the statistics platform, where the number *is* the answer, applied mathematics is about the chain of reasoning. The application is therefore built around a single principle: **students submit a result, and receive a full step-by-step method in return** — whether they got it right or wrong.

## 🎯 Objectives

The tool allows students to:
1.  **Automate the Technique:** Drill the mechanical gestures (fractions, powers, derivatives) until they become fluent, so that classroom attention can go to reasoning.
2.  **Read a Method:** Every submission unfolds the complete solution path, rebuilt on the student's own randomised figures — never a static answer key.
3.  **Diagnose Their Own Errors:** The app pre-computes the values produced by the most common mistakes, and names the error rather than simply marking the answer wrong.
4.  **Practise Without Stakes:** Nothing is stored, nothing is graded, nothing is transmitted to the instructor.

## 🚀 Features

### 🔄 Infinite Practice
Every exercise is generated randomly upon request. Figures, contexts and expressions change at each attempt, so students practise the *method* rather than memorising a result or a sequence of keystrokes.

### 🎭 Randomisation on Three Axes
Randomising the *numbers* alone is not enough: a student who has met
`u_0 = 12 400, u_{n+1} = 1,08 u_n` twenty times has memorised a template, not a
method, and freezes when the same question arrives in a different shape. Every
generator therefore draws on three axes, defined once in `contextes.py`:

1. **Context** — each exercise family carries two to five scenarios (subscribers,
   library loans, municipal debt, student housing, festival tickets, repair
   workshop…), with units and orders of magnitude that fit the scenario.
2. **Notation** — sequences are named $u$, $v$, $w$ or $c$ and may start at rank
   **0 or 1**; functions are $f(x)$, $g(t)$, $C(q)$, $R(p)$; supply is $O$ or $S$;
   the unknown is not always $x$.
3. **Shape of the object given** — a sequence arrives as a recurrence, a French
   sentence, a table of readings, or two terms from which the ratio must be
   deduced; a quadratic arrives expanded, factored, in vertex form or as a
   product of two affine factors; a growth rate arrives as a percentage, a
   multiplier, a continuous $e^{kt}$ form or a base-100 index.

The correction is rebuilt on whatever was drawn, so no step ever assumes a
particular context, letter or shape — the same constraint that already applied
to numerical parameters.

### 🧭 Method-First Correction
The correction is generated, not written. Each step is rebuilt on the parameters actually drawn, and follows the same four-part template throughout the course: **Identify → Compute → Verify → Interpret** — an echo of the four synthesis blocks closing every lecture (*technique / concept / cours / contexte*).

### 🔍 Computed Distractors
For each exercise, the values obtained through classic mistakes are computed in advance. Dividing millions of euros by inhabitants without converting, adding two nested fractions instead of multiplying them, applying a rate linearly instead of compounding it: each triggers a targeted diagnosis instead of a bare ❌.

### 🔢 Numeric Answers, Either Separator
Numeric answers are typed in a text field parsed by the app itself, not by the
browser: `12,5` and `12.5` are both accepted, as are thousands spaces (`1 250`)
and a trailing unit (`12,5 %`). Streamlit's native number widget delegates parsing
to the browser locale, which silently rejected the dot on French-configured
machines.

### 🧮 Symbolic Answers
Algebraic answers are checked with **SymPy**, so all equivalent forms are accepted: `5x/6`, `x*5/6` and `(5/6)x` are treated as the same expression.

### 📚 Curriculum Covered

All 17 sessions are live, each with 4 to 7 randomised exercise families. The exercises
follow the lecture decks session by session, and reuse the course's *fils rouges*.

**Pre-term module**

* **P1 | Numbers, fractions and powers** — scientific notation, nested fractions,
  algebraic fractions, powers, roots, counterexamples. *(Fil rouge A: Villeneuve's budget)*
* **P2 | Expanding and factoring** — distributivity, remarkable identities, difference
  of squares, common factor. *(Fil rouge A)*
* **P3 | Equations in one variable** — first degree, zero-product equations, isolating
  a variable. *(Fil rouge B: Vélocité bike scheme)*
* **P4 | Inequalities and systems** — the bound and the direction treated separately,
  2×2 systems. *(Fil rouge B, closing)*
* **P5 | Percentages, indices and changes** — multiplicative coefficient, chained and
  reciprocal changes, base-100 indices. *(Fil rouge C: student housing)*
* **P6 | Functions and affine functions** — image vs antecedent, slope, supply-demand
  equilibrium, sign of a product. *(Fil rouge C, closing)*

**Semester module**

* **S1 | Affine functions, supply and demand** — equilibrium, reading both slopes,
  moving *along* vs *shifting* the curve, sign of a product. *(Fil rouge D: Mélodia)*
* **S2 | Sequences: general concepts** — recurrence, explicit form, variations, notation.
* **S3 | Arithmetic and geometric sequences** — terms, identifying the type, sums.
* **S4 | Quadratics: parabola and factored form** — orientation, roots, vertex.
  *(Fil rouge E: Villeneuve festival)*
* **S5 | Discriminant and sign of a quadratic** — Δ, roots, quadratic inequalities.
  *(Fil rouge E, closing)*
* **S6 | The exponential function** — properties, discrete to continuous, why intuition
  fails. *(Fil rouge F: Villeneuve's debt)*
* **S7 | The natural logarithm** — unknown in the exponent, doubling time, average
  annual growth rate. *(Fil rouge F, closing)*
* **S8 | Differentiation: the local view** — rate of change, derivative number,
  tangent, marginal cost. *(Fil rouge G: municipal repair workshop)*
* **S9 | The derivative function and variations** — rules, sign of f′, variation table.
* **S10 | Second derivative, convexity and optimisation** — curvature, first- and
  second-order conditions. *(Fil rouge G, closing)*
* **S11 | Several variables and constrained optimisation** — partial derivatives,
  Lagrangian, the multiplier. *(Fil rouge H)* — *not examinable in the final exam.*

## 💻 Usage

### 🌐 Online (Recommended)
You can use the application directly in your browser without installing anything. This is the best method for students.

👉 **[Click here to open the App](https://sciencespo-maths-training.streamlit.app/)**

### 🛠️ Local Installation (For Developers)
To run this app locally on your machine:

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/abahiaoui/sciencespo-maths-training.git
    cd sciencespo-maths-training
    ```

2.  **Install requirements:**
    Make sure you have Python installed.
    ```bash
    pip install -r requirements.txt
    ```

3.  **Run the app:**
    ```bash
    streamlit run Accueil.py
    ```

## 🧩 Repository Structure

```
Accueil.py                                  main script (home page)
moteur.py                                   shared engine: grading + rendering
contextes.py                                shared banks: contexts, notations, shapes
pages/
    01___P1_Fractions_et_puissances.py      one file per session series
    …                                       (17 files, P1-P6 then S1-S11)
    17___S11_Optimisation_sous_contrainte.py
requirements.txt
```

`moteur.py` and `contextes.py` stay at the **root**, never inside `pages/`: Streamlit only adds the main script's directory to `sys.path`, and any `.py` file placed in `pages/` becomes a navigation entry in the sidebar.

`contextes.py` holds the reusable material for the three randomisation axes:
context banks (`EFFECTIFS`, `MONETAIRES`, `PRODUCTIONS`, `MARCHES`, `DISPOSITIFS`,
`BUDGETS`), notation helpers (`tirer_notation_suite`, `NotationFonction`), French
phrasing helpers that keep elisions and agreements correct (`ctx.du`, `ctx.du_bien`,
`a_contracte`, `phrase_taux`, `phrase_flux`), a `latex_nombre` formatter (French
decimal comma, thin thousands separator) and `tableau_latex` for statements given
as a table.

### ➕ Adding a Session

A session file contains **generators only** — all grading and rendering logic lives in `moteur.py`. A generator returns an `Exercice` object:

```python
from moteur import Etape, Exercice, executer

def gen_mon_exercice() -> Exercice:
    a = random.choice([2, 3, 5])          # randomly drawn parameters
    return Exercice(
        enonce=f"> Calculez $4 \\times {a}$.",
        reponse=4 * a,
        libelle="Résultat",
        etapes=[
            Etape("Identifier — de quoi s'agit-il ?", "…"),
            Etape("Calculer", "…", latex=r"4 \times a = …"),
            Etape("Vérifier", "…"),
            Etape("Interpréter", "…"),
        ],
        pieges=[(a + 4, "Vous avez additionné au lieu de multiplier.")],
        indice="…",
    )

executer("cle_unique", gen_mon_exercice)
```

A generator that follows the three-axis rule looks like this instead:

```python
import contextes as cx
from contextes import latex_nombre as L

def gen_mon_exercice() -> Exercice:
    ctx = cx.tirer(cx.EFFECTIFS)                 # axis 1: context
    notation = cx.tirer_notation_suite()         # axis 2: letter + starting rank
    forme = random.choice(["recurrence", "phrase", "tableau"])   # axis 3: shape
    …
```

The conventions that matter:

* **Steps are rebuilt from the drawn parameters**, never hard-coded. This is the only real design constraint.
* **Nothing in the correction may assume a context, a letter or a shape.** If a step says « la suite démarre au rang 0 » while the draw started at 1, the exercise is wrong even though the answer is right.
* **French prose is generated too.** Use `ctx.du`, `ctx.du_bien`, `a_contracte()` for elisions, and prefer impersonal turns of phrase (« On modélise… ») over past participles, whose agreement depends on the gender of the context drawn.
* **Numbers in maths mode go through `latex_nombre`** (`12\,400`, `1{,}08`); a thin space or a plain comma typed inside `$…$` is ignored or mis-spaced by KaTeX. Outside maths mode, use the page's local `_fr`.
* **No backslash inside an f-string expression** (`f"{'\\infty' if …}"`): that is a syntax error before Python 3.12, even though Streamlit Cloud runs a newer version. Compute the string beforehand.
* **`session_state` keys are global to the session, not to the page.** Prefix them with the session code (`p1_`, `p2_`, `s3_`…) so that two series never collide.
* **Tolerance:** `tolerance` is relative (0.005 by default); `tolerance_abs` overrides it when set. A distractor lying too close to the correct answer is automatically ignored.

Generators can be tested outside the server with `streamlit.testing.v1.AppTest`:

```python
from streamlit.testing.v1 import AppTest
at = AppTest.from_file("pages/01___P1_Fractions_et_puissances.py").run()
assert not at.exception
```

## 👨‍💻 Author & Contact

**Ahmed BAHIAOUI**

This tool was developed to support the Applied Mathematics course at Sciences Po.

If you encounter any technical issues or have questions about the exercises, please feel free to contact me:

* 📧 **Sciences Po:** [ahmed.bahiaoui@sciencespo.fr](mailto:ahmed.bahiaoui@sciencespo.fr)
* 📧 **Fallback:** [ahmed.bahiaoui.mail@gmail.com](mailto:ahmed.bahiaoui.mail@gmail.com)
