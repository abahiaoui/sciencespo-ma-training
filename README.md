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

### 🧭 Method-First Correction
The correction is generated, not written. Each step is rebuilt on the parameters actually drawn, and follows the same four-part template throughout the course: **Identify → Compute → Verify → Interpret** — an echo of the four synthesis blocks closing every lecture (*technique / concept / cours / contexte*).

### 🔍 Computed Distractors
For each exercise, the values obtained through classic mistakes are computed in advance. Dividing millions of euros by inhabitants without converting, adding two nested fractions instead of multiplying them, applying a rate linearly instead of compounding it: each triggers a targeted diagnosis instead of a bare ❌.

### 🧮 Symbolic Answers
Algebraic answers are checked with **SymPy**, so all equivalent forms are accepted: `5x/6`, `x*5/6` and `(5/6)x` are treated as the same expression.

### 📚 Curriculum Covered

All 17 sessions are live. Each series holds 4 to 7 randomised exercise families.

**Pre-term module**

* **P1 | Fractions and Powers** — scientific notation, nested fractions, algebraic
  fractions, powers, roots, compound interest, refuting a rule by counterexample.
* **P2 | Expanding and Factoring** — distributivity, remarkable identities, difference
  of squares, common factor, threshold between two schemes.
* **P3 | Proportions and Percentages** — share to percentage, applying a rate, points
  versus relative variation, recovering a total, completing a breakdown.
* **P4 | Equations and Inequalities** — first-degree equations, fractions, the bound
  and the direction of an inequality treated separately, modelling from a statement.
* **P5 | Variations and Multiplicative Coefficients** — rate to coefficient, chained
  changes, reciprocal change, rate of variation, repeated growth.
* **P6 | Lines and Slopes** — slope from two points, intercept, prediction,
  intersection, interpreting the slope.

**Semester module**

* **S1 | Functions** — image, antecedent, forbidden values, average cost.
* **S2 | Rate of Change** — average rate, interpretation, the step $h$, the limit.
* **S3 | Differentiation** — polynomials, derivative number, tangent, product rule.
* **S4 | Derivatives and Variations** — critical points, sign of $f'$, extremum value,
  vanishing derivative without extremum.
* **S5 | Limits and Asymptotes** — quotients at infinity, average-cost floor, vertical
  asymptotes, comparative growth.
* **S6 | Convexity** — second derivative, inflection point, curvature, slowing versus
  falling.
* **S7 | Logarithm and Exponential** — log properties, unknown in the exponent,
  derivatives, exponential versus linear.
* **S8 | Optimisation** — optimal quantity, maximum value, minimising average cost,
  second-order condition.
* **S9 | Sequences** — arithmetic, geometric, identifying the type, crossing a
  threshold.
* **S10 | Elasticity** — power functions, price elasticity, elastic versus rigid
  demand, returns to scale.
* **S11 | Two Variables and Lagrangian** — partial derivatives, marginal productivity,
  constrained optimisation, the multiplier. *Not examinable in the final exam.*

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
pages/
    01___P1_Fractions_et_puissances.py      one file per session series
    …                                       (17 files, P1-P6 then S1-S11)
    17___S11_Deux_variables.py
requirements.txt
```

`moteur.py` stays at the **root**, never inside `pages/`: Streamlit only adds the main script's directory to `sys.path`, and any `.py` file placed in `pages/` becomes a navigation entry in the sidebar.

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

Three conventions matter:

* **Steps are rebuilt from the drawn parameters**, never hard-coded. This is the only real design constraint.
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
