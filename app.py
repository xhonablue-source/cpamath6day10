"""
CPA Math 6 — Day 10: Skill Breakout — Multiplying Decimals & Multiplying
Fractions (Prepare for Percent of a Quantity)
Built to match the visual/interactive structure of the Day 5–9 apps by
Xavier Honablue, M.Ed — Chandler Park Academy.

Day 9 finished Lesson 1 (area of a parallelogram). Day 10 is a Skill
Breakout: two short prerequisite-skill reviews — multiplying decimals, and
multiplying fractions — that a student needs *before* the upcoming Percent
of a Quantity lesson. Unlike Day 9, the problems below are original practice
items written for this app (not verbatim worktext text), built at the
Grade 6 standards below and cross-checked for correctness.

The thread that ties the two skill breakouts together, stated explicitly
and revisited throughout: a percent is a fraction with a denominator of
100 (75% = 75/100). A fraction is the *function* — multiply it by a whole
and it hands back that percent's share of the whole. A decimal such as 0.75
is that exact same fraction in base-ten place-value clothing. So "multiply
decimals" and "multiply fractions" are not two unrelated skills — they are
one function, wearing two different notations, and either notation
produces a percent.

Run locally with: streamlit run app.py
Deploy the same way Day 5–9 were deployed: push this folder to a new GitHub
repo (cpamath6day10) and connect it on Streamlit Community Cloud as
cpamath6day10.streamlit.app, then add the card to the launcher app.
"""

from fractions import Fraction

import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
import streamlit as st

# ----------------------------------------------------------------------
# Page config & theme (matches Day 5–9 exactly, plus one new accent color
# for the recurring "Big Picture" callout that threads this lesson)
# ----------------------------------------------------------------------
st.set_page_config(page_title="Day 10 — Multiplying Decimals & Fractions: The Percent Connection",
                    page_icon="🔑", layout="wide")

NAVY = "#1b3a5c"
NAVY_LIGHT = "#eef4fa"
NAVY_BORDER = "#2c4a6e"
GREEN = "#3f7d55"
GREEN_LIGHT = "#eef7f0"
GOLD = "#8a5a20"
GOLD_LIGHT = "#f6ecd9"
RED = "#b03a2e"
RED_LIGHT = "#fdf1ef"
PURPLE = "#5b3a7d"
PURPLE_LIGHT = "#f2eef7"
GRAY = "#7a8290"
TEAL = "#0f6b64"
TEAL_LIGHT = "#e6f3f1"

FILL_A = "#dbe8f6"   # first factor's shaded region
FILL_B = "#f6e3c6"   # second factor's shaded region
FILL_PRODUCT = GREEN  # overlap = the product

CUSTOM_CSS = f"""
<style>
.box {{
    border: 2px solid {NAVY};
    border-radius: 8px;
    padding: 14px 18px;
    margin: 10px 0;
    background: white;
}}
.pill {{
    display: inline-block;
    color: white;
    font-size: 11px;
    font-weight: 700;
    letter-spacing: 0.4px;
    padding: 4px 12px;
    border-radius: 12px;
    margin-bottom: 8px;
}}
.box-readaloud {{ border-color: {NAVY}; }}
.box-readaloud .pill {{ background: {NAVY}; }}
.box-readaloud p {{ font-style: italic; margin: 4px 0 0 0; }}

.box-literacy {{ border-color: {NAVY_BORDER}; background: {NAVY_LIGHT}; }}
.box-literacy .pill {{ background: {NAVY_BORDER}; }}

.box-existing {{ border-color: {GREEN}; background: {GREEN_LIGHT}; }}
.box-existing .pill {{ background: {GREEN}; }}

.box-tools {{ border-color: {GOLD}; background: {GOLD_LIGHT}; }}
.box-tools .pill {{ background: {GOLD}; }}

.box-observer {{ border: 2px dashed {RED}; background: {RED_LIGHT}; }}
.box-observer .pill {{ background: {RED}; }}

.box-method {{ border-color: {PURPLE}; background: {PURPLE_LIGHT}; }}
.box-method .pill {{ background: {PURPLE}; }}

.box-bigidea {{ border: 3px solid {TEAL}; background: {TEAL_LIGHT}; }}
.box-bigidea .pill {{ background: {TEAL}; }}

.ask {{ color: {RED}; font-weight: 700; margin-top: 8px; }}

.roadmap-title {{ color: {NAVY}; font-weight: 700; font-size: 15px; margin-bottom: 0; }}
.roadmap-sub {{ color: #5a6672; font-size: 11.5px; margin-top: -4px; }}

.credit {{ text-align: center; color: #8a939c; font-size: 11px; margin-top: 18px; }}

.itext {{ background: {NAVY_LIGHT}; border-left: 4px solid {NAVY}; padding: 10px 14px; margin: 8px 0; border-radius: 4px; font-size: 14px; }}
.consider {{ background: {PURPLE_LIGHT}; border-left: 4px solid {PURPLE}; padding: 10px 14px; margin: 8px 0; border-radius: 4px; font-size: 13.5px; }}
.pairshare {{ background: {GOLD_LIGHT}; border-left: 4px solid {GOLD}; padding: 10px 14px; margin: 8px 0; border-radius: 4px; font-size: 13.5px; }}
</style>
"""
st.markdown(CUSTOM_CSS, unsafe_allow_html=True)


def box(kind, pill, body_html):
    st.markdown(
        f'<div class="box box-{kind}"><span class="pill">{pill}</span>{body_html}</div>',
        unsafe_allow_html=True,
    )


def read_aloud(text):
    box("readaloud", "🔊 READ ALOUD", f"<p>&ldquo;{text}&rdquo;</p>")


def ask_the_class(text):
    st.markdown(f'<p class="ask">❓ Ask the class: {text}</p>', unsafe_allow_html=True)


def consider_this(text):
    st.markdown(f'<div class="consider"><b>CONSIDER THIS...</b><br>{text}</div>', unsafe_allow_html=True)


def pair_share(text):
    st.markdown(f'<div class="pairshare"><b>PAIR/SHARE</b><br>{text}</div>', unsafe_allow_html=True)


def problem_box(label, text):
    """A short problem statement, written for this app (not a verbatim
    worktext quote — Day 10 has no page-for-page source the way Day 9 did)."""
    st.markdown(f'<div class="itext"><b>📝 {label}</b><br>{text}</div>', unsafe_allow_html=True)


def attempt(key):
    k = f"attempts_{key}"
    st.session_state[k] = st.session_state.get(k, 0) + 1
    return st.session_state[k]


def explain(title, lines):
    body = "<br>".join(lines)
    st.markdown(
        f'<div class="box box-tools"><span class="pill">💡 {title}</span>{body}</div>',
        unsafe_allow_html=True,
    )


def big_picture(text):
    box("bigidea", "🔑 THE BIG PICTURE", text)


# ----------------------------------------------------------------------
# Drawing helpers
# ----------------------------------------------------------------------
def draw_hundred_grid(shaded, total=100, color=FILL_A, title=None, figsize=(4.2, 4.4)):
    """A 10x10 hundred-grid with `shaded` of the 100 small squares filled,
    read left-to-right, top-to-bottom — the standard percent/decimal model."""
    fig, ax = plt.subplots(figsize=figsize)
    cols, rows = 10, 10
    for i in range(total):
        r, c = divmod(i, cols)
        y = rows - 1 - r
        filled = i < shaded
        ax.add_patch(Rectangle((c, y), 1, 1, facecolor=color if filled else "white",
                                edgecolor="#b9c2cc", linewidth=0.8))
    ax.set_xlim(0, cols)
    ax.set_ylim(0, rows)
    ax.set_aspect("equal")
    ax.axis("off")
    if title:
        ax.set_title(title, fontsize=11, fontweight="bold", color=NAVY, pad=10)
    return fig


def draw_decimal_area_model(a, b, figsize=(4.6, 4.9)):
    """Area model for two decimals between 0 and 1, to the tenths place.
    Shades `a` of the width and `b` of the height on a 10x10 hundredths
    grid; the double-shaded overlap is the product a*b."""
    cols_shaded = round(a * 10)
    rows_shaded = round(b * 10)
    fig, ax = plt.subplots(figsize=figsize)
    for r in range(10):
        for c in range(10):
            in_a = c < cols_shaded
            in_b = r < rows_shaded
            if in_a and in_b:
                fc = FILL_PRODUCT
            elif in_a:
                fc = FILL_A
            elif in_b:
                fc = FILL_B
            else:
                fc = "white"
            ax.add_patch(Rectangle((c, 9 - r), 1, 1, facecolor=fc, edgecolor="#b9c2cc", linewidth=0.8))
    ax.plot([0, cols_shaded], [10.4, 10.4], color=NAVY, linewidth=2)
    ax.text(cols_shaded / 2, 10.65, f"{a:g} of the width", ha="center", fontsize=9.5, fontweight="bold", color=NAVY)
    ax.plot([-0.5, -0.5], [10 - rows_shaded, 10], color=RED, linewidth=2)
    ax.text(-0.85, 10 - rows_shaded / 2, f"{b:g} of the height", ha="center", va="center", fontsize=9.5,
            fontweight="bold", color=RED, rotation=90)
    ax.text(cols_shaded / 2 if cols_shaded else 0.5, (10 - rows_shaded) if rows_shaded else 9.5,
            "", fontsize=1)  # spacer (keeps layout stable for a=0 or b=0 edge cases)
    ax.set_xlim(-2.6, 10.3)
    ax.set_ylim(-0.4, 11.4)
    ax.set_aspect("equal")
    ax.axis("off")
    return fig


def draw_fraction_array_model(n1, d1, n2, d2, figsize=(4.6, 4.6)):
    """Array model for fraction x fraction: a rectangle split into d1
    columns (n1 shaded, first factor) and d2 rows (n2 shaded, second
    factor). The double-shaded overlap is the product's numerator; the
    total number of small rectangles is the product's denominator."""
    fig, ax = plt.subplots(figsize=figsize)
    for r in range(d2):
        for c in range(d1):
            in_a = c < n1
            in_b = r < n2
            if in_a and in_b:
                fc = FILL_PRODUCT
            elif in_a:
                fc = FILL_A
            elif in_b:
                fc = FILL_B
            else:
                fc = "white"
            ax.add_patch(Rectangle((c, d2 - 1 - r), 1, 1, facecolor=fc, edgecolor=NAVY, linewidth=1.0))
    ax.plot([0, n1], [d2 + 0.35, d2 + 0.35], color=NAVY, linewidth=2)
    ax.text(n1 / 2, d2 + 0.6, f"{n1}/{d1}", ha="center", fontsize=11.5, fontweight="bold", color=NAVY)
    ax.plot([-0.35, -0.35], [d2 - n2, d2], color=RED, linewidth=2)
    ax.text(-0.65, d2 - n2 / 2, f"{n2}/{d2}", ha="center", va="center", fontsize=11.5, fontweight="bold",
            color=RED, rotation=90)
    ax.text(d1 / 2, -0.65, f"total pieces = {d1} × {d2} = {d1 * d2}", ha="center", fontsize=9, color=GRAY,
            style="italic")
    ax.set_xlim(-1.7, d1 + 0.7)
    ax.set_ylim(-1.3, d2 + 1.3)
    ax.set_aspect("equal")
    ax.axis("off")
    return fig


def draw_double_number_line(percent, whole, figsize=(6.6, 2.7)):
    """A double number line: the top scale runs 0-100 (percent), the
    bottom scale runs 0-whole (quantity), aligned proportionally, with a
    marker showing the given percent and its matching amount."""
    part = percent / 100 * whole
    fig, ax = plt.subplots(figsize=figsize)
    ax.plot([0, 10], [1, 1], color=NAVY, linewidth=2)
    for pct in [0, 25, 50, 75, 100]:
        x = pct / 100 * 10
        ax.plot([x, x], [0.9, 1.1], color=NAVY, linewidth=1.5)
        ax.text(x, 1.28, f"{pct}%", ha="center", fontsize=9.5, color=NAVY, fontweight="bold")
    ax.plot([0, 10], [0, 0], color=RED, linewidth=2)
    for pct in [0, 25, 50, 75, 100]:
        x = pct / 100 * 10
        val = pct / 100 * whole
        ax.plot([x, x], [-0.1, 0.1], color=RED, linewidth=1.5)
        ax.text(x, -0.34, f"{val:g}", ha="center", fontsize=9.5, color=RED, fontweight="bold")
    xm = percent / 100 * 10
    ax.plot([xm, xm], [-0.18, 1.18], color=GOLD, linewidth=2, linestyle="--")
    ax.text(xm, 1.58, f"{percent:g}% of {whole:g}  =  {part:g}", ha="center", fontsize=10.5, fontweight="bold",
            color=GOLD)
    ax.set_xlim(-0.7, 10.7)
    ax.set_ylim(-0.65, 1.95)
    ax.axis("off")
    return fig


# ----------------------------------------------------------------------
# Sidebar — Sign In + Roadmap (mirrors Day 5–9)
# ----------------------------------------------------------------------
with st.sidebar:
    st.subheader("Sign In")
    st.text_input("Your name:", key="student_name")
    st.selectbox("Choose your shape avatar:", ["Rectangle", "Square", "Parallelogram", "L-Shape", "T-Shape"], key="avatar")
    st.selectbox(
        "Pick your learning mode:",
        ["Focus Champ", "Growth Mode", "Problem Solver", "Data Boss", "Brain Builder"],
        key="learning_mode",
    )
    st.markdown("---")
    st.markdown('<p class="roadmap-title">Day 10 Roadmap</p>', unsafe_allow_html=True)
    st.markdown('<p class="roadmap-sub">Skill Breakout — Prepare for Percent of a Quantity</p>', unsafe_allow_html=True)

    steps = [
        "1. Welcome Back & Warm-Up",
        "2. Skill Breakout 1: Decimals — Explore & Model",
        "3. Skill Breakout 1: Decimals — Practice & Check",
        "4. Skill Breakout 2: Fractions — Explore & Model",
        "5. Skill Breakout 2: Fractions — Practice & Check",
        "6. Refine: Same Percent, Two Paths",
        "7. Refine: Error Alert",
        "8. Additional Practice",
        "9. Engage / Explore / Enrich & Math Journal",
    ]
    if "step" not in st.session_state:
        st.session_state.step = 0
    for i, label in enumerate(steps):
        marker = "▶ " if i == st.session_state.step else ""
        if st.button(marker + label, key=f"nav_{i}", use_container_width=True):
            st.session_state.step = i
            st.rerun()
    st.markdown("---")
    st.caption("Lesson mode: Skill Breakout — two prerequisite skills (multiply decimals, multiply "
               "fractions) reviewed and connected before Percent of a Quantity.")
    st.caption("Standards: 6.NS.B.3 (multiply decimals) · 5.NF.B.4 (multiply fractions — foundational) · "
               "6.RP.A.3.c (percent of a quantity) · MP.2, MP.4, MP.7, MP.8")

# ----------------------------------------------------------------------
# Roadmap step content
# ----------------------------------------------------------------------
step = st.session_state.step
name = st.session_state.get("student_name", "") or "class"

st.markdown(f"## {steps[step]}")
st.progress((step + 1) / len(steps))

# ======================================================================
# STEP 0 — Welcome back / warm-up
# ======================================================================
if step == 0:
    st.markdown("### 🧠 Opener Question")
    st.write("Look at the grid below. 75 of the 100 small squares are shaded.")
    st.pyplot(draw_hundred_grid(75, title="75 out of 100 squares shaded"), use_container_width=False)
    st.write("Which of these correctly describe the shaded amount? Select all that apply.")
    opener_opts = {
        "75%": True,
        "75/100": True,
        "0.75": True,
        "just “75”, no units needed": False,
        "7.5": False,
    }
    opener_picks = []
    for label in opener_opts:
        if st.checkbox(label, key=f"opener_{label}"):
            opener_picks.append(label)
    if st.button("Check my answer", key="check_opener"):
        attempt("opener")
        correct = {k for k, v in opener_opts.items() if v}
        if set(opener_picks) == correct:
            st.balloons()
            st.success("Correct! 75%, 75/100, and 0.75 are three outfits for the exact same amount — "
                       "seventy-five hundredths.")
        else:
            st.error("Not quite — check the grid again. One correct description is a fraction, one is a "
                     "percent, and one is a decimal. All three name the very same shaded amount.")

    big_picture(
        "A percent is a fraction that always has 100 on the bottom. 75% literally means 75/100. And a "
        "fraction has a job to do: multiply it by a whole, and the fraction is the <b>function</b> — the "
        "working machine — that takes the whole in and hands the percent's share of it back out. "
        "75/100 &times; 60 = 45 means &ldquo;the fraction 75/100, acting on 60, produces 45.&rdquo; A "
        "decimal like 0.75 is that <i>exact same fraction</i>, just written in base-ten place-value "
        "clothing instead of a numerator and denominator. Today you build two engines that run that "
        "same machine &mdash; multiplying decimals, and multiplying fractions &mdash; because &ldquo;find "
        "the percent of a number&rdquo; will always secretly be one of these two skills."
    )
    read_aloud(
        "Every time you hear the words 'percent of,' your brain should hear 'multiply by a fraction out "
        "of 100.' Today we build the two engines that make that happen: multiplying decimals, and "
        "multiplying fractions."
    )
    ask_the_class("If 20% of a number means 20/100 of that number, what operation turns 20% and a number "
                  "into an answer?")
    box("literacy", "📖 QUICK REVIEW",
        "<b>Percent</b> means &ldquo;per hundred.&rdquo; Any percent can be written as a fraction over "
        "100, and any fraction over 100 can be written as a two-place decimal. Same value, three names.")
    box("tools", "Today's tools",
        "Notebook &amp; pencil &middot; the 10-by-10 grid model &middot; a calculator only for checking "
        "your work, never for a first attempt.")

# ======================================================================
# STEP 1 — Skill Breakout 1: Multiplying Decimals — Explore & Model
# ======================================================================
elif step == 1:
    st.write("**Skill Breakout 1 — Multiplying Decimals.** Before you can find a percent of anything, "
             "you need to be fast and accurate multiplying decimals. Let's rebuild the rule from a "
             "picture first.")
    st.markdown("### Explore — 0.5 × 0.4 on a hundredths grid")
    st.pyplot(draw_decimal_area_model(0.5, 0.4), use_container_width=False)
    consider_this("Before you count the overlap, predict: will 0.5 × 0.4 be bigger or smaller than 0.5? "
                  "Why might that be?")
    st.write("The blue columns show 0.5 (five of the ten columns). The gold rows show 0.4 (four of the "
             "ten rows). The green overlap — where both are shaded — is the product: 20 of the 100 tiny "
             "squares, which is 0.20.")
    box("existing", "🧠 WHY THIS WORKS",
        "Multiplying two decimals that are each less than 1 always <i>shrinks</i> the amount, because "
        "you're taking a fractional part of an already-fractional part — exactly like the grid shows.")

    st.markdown("### The standard algorithm")
    box("method", "Possible work — 0.6 × 0.24",
        "Step 1 — multiply as if there were no decimal points at all: 6 × 24 = 144<br>"
        "Step 2 — count the total decimal places in the two factors: 0.6 has 1, 0.24 has 2 → 3 total<br>"
        "Step 3 — place the decimal point 3 places from the right in the answer: <b>0.144</b>")

    st.markdown("### A percent-flavored example")
    problem_box("Try this", "40% of the 60 students in 6th grade bring lunch from home. How many students "
                "is that? 40% = 0.40, so we need 0.40 × 60.")
    box("method", "Possible work — 0.40 × 60",
        "Multiply as whole numbers: 40 × 60 = 2,400<br>"
        "Count decimal places: 0.40 has 2, 60 has 0 → 2 total<br>"
        "Place the point 2 places from the right: <b>24.00 = 24 students</b>")

    st.markdown("#### Now you try")
    dtry = st.number_input("0.75 × 60 =", min_value=0.0, step=0.5, key="decimal_try")
    if st.button("Check my answer", key="check_decimal_try"):
        n = attempt("decimal_try")
        if abs(dtry - 45) < 0.01:
            st.balloons()
            st.success("Correct! 0.75 × 60 = 45. Hang on to that number — you'll see it again very soon.")
        else:
            st.error("Not yet — multiply 75 × 60 first, then count the decimal places (2, from 0.75) and "
                     "place the point.")
            if n >= 2:
                explain("Redo help", ["75 × 60 = 4,500", "0.75 has 2 decimal places", "= <b>45.00 = 45</b>"])
    pair_share("How is 0.75 × 60 like finding a percent of 60?")

# ======================================================================
# STEP 2 — Skill Breakout 1: Multiplying Decimals — Practice & Check
# ======================================================================
elif step == 2:
    st.write("**Skill Breakout 1 — Practice & Check.** Same rule every time: multiply like whole numbers, "
             "then count and place the decimal point.")

    st.markdown("### Problem 1")
    problem_box("Practice", "Find the product: 0.3 × 0.8")
    p1 = st.number_input("0.3 × 0.8 =", min_value=0.0, step=0.01, key="dec_p1")
    if st.button("Check Problem 1", key="check_dec1"):
        n = attempt("dec1")
        if abs(p1 - 0.24) < 0.005:
            st.success("Correct! 3 × 8 = 24, and 0.3 and 0.8 together have 2 decimal places → 0.24.")
        else:
            st.error("Not yet — multiply 3 × 8, then count 2 total decimal places.")
            if n >= 2:
                explain("Redo help", ["3 × 8 = 24", "0.3 + 0.8 → 1 + 1 = 2 decimal places", "= <b>0.24</b>"])

    st.markdown("### Problem 2")
    problem_box("Practice", "Find the product: 1.2 × 0.5")
    p2 = st.number_input("1.2 × 0.5 =", min_value=0.0, step=0.01, key="dec_p2")
    if st.button("Check Problem 2", key="check_dec2"):
        n = attempt("dec2")
        if abs(p2 - 0.6) < 0.005:
            st.success("Correct! 12 × 5 = 60, and 1.2 and 0.5 together have 2 decimal places → 0.60 = 0.6.")
        else:
            st.error("Not yet — multiply 12 × 5, then count 2 total decimal places.")
            if n >= 2:
                explain("Redo help", ["12 × 5 = 60", "1 + 1 = 2 decimal places", "= <b>0.60 = 0.6</b>"])

    st.markdown("### Problem 3 — A hoodie on sale")
    problem_box("Practice", "A hoodie costs $40. It's 25% off, which means you pay 0.75 of the original "
                "price. How much do you pay?")
    p3 = st.number_input("Price you pay ($):", min_value=0.0, step=0.5, key="dec_p3")
    if st.button("Check Problem 3", key="check_dec3"):
        n = attempt("dec3")
        if abs(p3 - 30) < 0.01:
            st.balloons()
            st.success("Correct! 0.75 × 40 = 30, so you pay $30.")
        else:
            st.error("Not yet — multiply 0.75 by 40.")
            if n >= 2:
                explain("Redo help", ["0.75 × 40", "75 × 40 = 3,000", "2 decimal places → <b>$30.00</b>"])

    st.markdown("### Problem 4 — Sales tax (watch the decimal point!)")
    problem_box("Practice", "Sales tax is 8%, which means 0.08 of the price is added as tax. A skateboard "
                "costs $60. How much is the tax?")
    p4 = st.radio("Choose the tax amount:", ["$0.48", "$4.80", "$8.00", "$48.00"], key="dec_p4", index=None)
    if st.button("Check Problem 4", key="check_dec4"):
        n = attempt("dec4")
        if p4 == "$4.80":
            st.success("Correct! 0.08 × 60 = 4.80. The tax is $4.80.")
        else:
            st.error("Not yet — 8 × 60 = 480, and 0.08 has 2 decimal places. Where does the point land?")
            if n >= 2:
                explain("Redo help", ["8 × 60 = 480", "0.08 has 2 decimal places", "= <b>4.80 → $4.80</b>"])

    box("literacy", "📖 RECAP — the decimal-multiplication rule",
        "Multiply the digits as if they were whole numbers. Then count the <b>total</b> number of decimal "
        "places across <b>both</b> factors, and place the decimal point that many places from the right "
        "in the answer.")
    pair_share("How is finding 8% tax like finding 75% of the hoodie price? What's the same about the steps?")

# ======================================================================
# STEP 3 — Skill Breakout 2: Multiplying Fractions — Explore & Model
# ======================================================================
elif step == 3:
    st.write("**Skill Breakout 2 — Multiplying Fractions.** The second engine. In math, the word "
             "&ldquo;of&rdquo; is code for &ldquo;multiply&rdquo; — an array model shows exactly why.")
    st.markdown("### Explore — 3/4 × 2/3 on an array model")
    st.pyplot(draw_fraction_array_model(3, 4, 2, 3), use_container_width=False)
    consider_this("How many small rectangles are there in all? How many are double-shaded (both blue AND "
                  "gold)?")
    st.write("3/4 of the width is shaded blue. 2/3 of the height is shaded gold. The green, double-shaded "
             "overlap is the product: 6 of the 12 small rectangles, or 6/12 — which simplifies to 1/2.")
    box("method", "Possible work — 3/4 × 2/3",
        "Multiply numerators straight across: 3 × 2 = 6<br>"
        "Multiply denominators straight across: 4 × 3 = 12<br>"
        "3/4 × 2/3 = 6/12 = <b>1/2</b>")

    st.markdown("### A percent-flavored example")
    problem_box("Try this", "3/4 of the 60 students in 6th grade play a sport. How many students is that?")
    box("method", "Possible work — 3/4 × 60",
        "3/4 × 60/1 = (3 × 60) / (4 × 1) = 180/4 = <b>45 students</b>")
    box("existing", "👀 LOOK BACK",
        "Flip back to Skill Breakout 1: 0.75 × 60 also equaled 45. That is not a coincidence — 3/4 and "
        "0.75 are the exact same amount, so multiplying by either one produces the exact same answer.")

    st.markdown("#### Now you try")
    ftry = st.number_input("2/5 × 60 =", min_value=0.0, step=1.0, key="fraction_try")
    if st.button("Check my answer", key="check_fraction_try"):
        n = attempt("fraction_try")
        if abs(ftry - 24) < 0.01:
            st.balloons()
            st.success("Correct! 2/5 × 60 = 120/5 = 24. Keep that number too — 2/5 is the same amount as "
                       "0.4, or 40%.")
        else:
            st.error("Not yet — multiply the numerator by 60, then divide by the denominator.")
            if n >= 2:
                explain("Redo help", ["2/5 × 60/1 = (2 × 60)/5", "= 120/5", "= <b>24</b>"])
    pair_share("Why does multiplying a fraction by a whole number make sense as repeated shrinking, the "
              "same way the array model does?")

# ======================================================================
# STEP 4 — Skill Breakout 2: Multiplying Fractions — Practice & Check
# ======================================================================
elif step == 4:
    st.write("**Skill Breakout 2 — Practice & Check.** Same rule every time: multiply numerators straight "
             "across, multiply denominators straight across, then simplify.")

    st.markdown("### Problem 1")
    problem_box("Practice", "Find the product: 1/2 × 1/3")
    p1 = st.radio("Choose the product:", ["1/6", "2/5", "1/5", "2/6"], key="frac_p1", index=None)
    if st.button("Check Problem 1", key="check_frac1"):
        n = attempt("frac1")
        if p1 == "1/6":
            st.success("Correct! 1 × 1 = 1 on top, 2 × 3 = 6 on bottom → 1/6.")
        else:
            st.error("Not yet — multiply straight across (numerator × numerator, denominator × "
                     "denominator). Do NOT add.")
            if n >= 2:
                explain("Redo help", ["1/2 × 1/3 = (1×1)/(2×3)", "= <b>1/6</b>",
                                       "(2/5 comes from adding instead of multiplying — watch for that trap!)"])

    st.markdown("### Problem 2")
    problem_box("Practice", "Find the product: 5/6 × 12")
    p2 = st.number_input("5/6 × 12 =", min_value=0.0, step=1.0, key="frac_p2")
    if st.button("Check Problem 2", key="check_frac2"):
        n = attempt("frac2")
        if abs(p2 - 10) < 0.01:
            st.success("Correct! 5/6 × 12/1 = 60/6 = 10.")
        else:
            st.error("Not yet — multiply 5 × 12 first, then divide by 6.")
            if n >= 2:
                explain("Redo help", ["5/6 × 12/1 = (5×12)/6", "= 60/6", "= <b>10</b>"])

    st.markdown("### Problem 3 — Half a recipe")
    problem_box("Practice", "A recipe calls for 2/3 cup of flour. You are making 1/2 of the recipe. How "
                "much flour do you need?")
    p3 = st.radio("Choose the amount of flour:", ["1/3 cup", "2/6 cup written as 1/5", "5/6 cup", "1/6 cup"],
                  key="frac_p3", index=None)
    if st.button("Check Problem 3", key="check_frac3"):
        n = attempt("frac3")
        if p3 == "1/3 cup":
            st.success("Correct! 2/3 × 1/2 = 2/6 = 1/3 cup.")
        else:
            st.error("Not yet — multiply 2/3 × 1/2 straight across, then simplify.")
            if n >= 2:
                explain("Redo help", ["2/3 × 1/2 = (2×1)/(3×2)", "= 2/6", "= <b>1/3 cup</b>"])

    st.markdown("### Problem 4 — Reserved seats")
    problem_box("Practice", "1/4 of the 80 seats in the gym are reserved for guests. How many seats is that?")
    p4 = st.number_input("Reserved seats:", min_value=0, step=1, key="frac_p4")
    if st.button("Check Problem 4", key="check_frac4"):
        n = attempt("frac4")
        if p4 == 20:
            st.balloons()
            st.success("Correct! 1/4 × 80 = 80/4 = 20 seats.")
        else:
            st.error("Not yet — divide 80 by 4.")
            if n >= 2:
                explain("Redo help", ["1/4 × 80/1 = 80/4", "= <b>20</b>"])

    box("literacy", "📖 RECAP — the fraction-multiplication rule",
        "Multiply the numerators straight across, multiply the denominators straight across, then "
        "simplify. Never add the numerators or denominators — that's a different operation entirely.")
    pair_share("A classmate says 1/2 × 1/3 should be 2/5 because &ldquo;you add the tops and add the "
              "bottoms.&rdquo; What would you say to them?")

# ======================================================================
# STEP 5 — Refine: Same Percent, Two Paths
# ======================================================================
elif step == 5:
    st.write("**Refine — Same Percent, Two Paths.** You've now built both engines. Let's run them "
             "side by side on the exact same problem and prove they always agree.")

    st.markdown("### 75% of 60 — the decimal way and the fraction way")
    col_a, col_b = st.columns(2)
    with col_a:
        box("method", "Decimal method", "75% = 0.75<br>0.75 × 60<br>75 × 60 = 4,500<br>2 decimal places → "
            "<b>45.00 = 45</b>")
    with col_b:
        box("method", "Fraction method", "75% = 3/4<br>3/4 × 60<br>(3 × 60)/4 = 180/4<br>= <b>45</b>")
    st.pyplot(draw_double_number_line(75, 60), use_container_width=False)

    big_picture(
        "75% = 75/100 = 3/4 = 0.75. Whichever notation a problem hands you, it's the exact same "
        "function underneath &mdash; convert if you need to, then multiply. That's the whole secret to "
        "&ldquo;percent of a quantity&rdquo; problems."
    )

    st.markdown("#### Prove it yourself — 20% of 45")
    consider_this("20% is the same amount as which fraction? (Hint: 20/100 simplifies.)")
    col_c, col_d = st.columns(2)
    with col_c:
        dec_ans = st.number_input("Decimal method: 0.20 × 45 =", min_value=0.0, step=0.5, key="prove_dec")
    with col_d:
        frac_ans = st.number_input("Fraction method: 1/5 × 45 =", min_value=0.0, step=0.5, key="prove_frac")
    if st.button("Check both methods", key="check_prove"):
        n = attempt("prove")
        if abs(dec_ans - 9) < 0.01 and abs(frac_ans - 9) < 0.01:
            st.balloons()
            st.success("Correct — both methods land on 9! 0.20 × 45 = 9 and 1/5 × 45 = 45/5 = 9. Same "
                       "function, two notations, same answer.")
        else:
            st.error("Not yet — 20% = 0.20 = 1/5. Multiply 45 by each notation and compare.")
            if n >= 2:
                explain("Redo help", ["0.20 × 45 = 9.00", "1/5 × 45 = 45/5 = 9", "Both equal <b>9</b>"])
    ask_the_class("Why will the decimal method and the fraction method for the SAME percent always give "
                  "the SAME answer?")

# ======================================================================
# STEP 6 — Refine: Error Alert
# ======================================================================
elif step == 6:
    st.write("**Refine — Error Alert.** Two real traps show up on almost every percent problem. Let's "
             "name them before they become your mistakes.")

    st.markdown("### Trap #1 — Marcus forgets to convert the percent")
    problem_box("What happened", "Marcus was finding 6% sales tax on a $50 shirt. He wrote: "
                "&ldquo;6 × 50 = 300, so the tax is $300.&rdquo;")
    m_pick = st.radio("What did Marcus forget to do?", [
        "He forgot to convert 6% to 0.06 (or 6/100) before multiplying",
        "He multiplied the wrong two numbers",
        "He should have divided instead of multiplied",
        "Nothing — $300 is correct",
    ], key="marcus_pick", index=None)
    if st.button("Check my answer", key="check_marcus"):
        n = attempt("marcus")
        if m_pick == "He forgot to convert 6% to 0.06 (or 6/100) before multiplying":
            st.success("Correct! 6% = 0.06. 0.06 × 50 = 3.00, so the tax is $3.00 — not $300. Leaving a "
                       "percent as a whole number before multiplying makes the answer 100 times too big.")
        else:
            st.error("Not yet — think about what 6% actually equals as a decimal or fraction.")
    box("observer", "📕 ERROR ALERT — restated",
        "A percent is <b>not</b> ready to multiply until it's been converted to a decimal (divide by "
        "100) or a fraction (put it over 100 and simplify). Skip that step, and the answer comes out "
        "100 times too large.")

    st.markdown("### Trap #2 — Priya adds instead of multiplies")
    problem_box("What happened", "Priya was multiplying 2/3 × 3/5. She wrote: 2 + 3 = 5 on top, 3 + 5 = 8 "
                "on bottom, so her answer was 5/8.")
    priya_guess = st.text_area("Type what you think Priya did wrong:", key="priya_guess", height=80)
    if st.button("Reveal what actually happened", key="reveal_priya"):
        box("observer", "📕 ERROR ALERT — Priya's mistake",
            "Priya <b>added</b> the numerators and <b>added</b> the denominators. Fraction multiplication "
            "is never addition — you multiply straight across instead: 2/3 × 3/5 = (2×3)/(3×5) = 6/15 = "
            "<b>2/5</b>.")
    pair_share("How could drawing an array model help Priya catch her own mistake next time?")
    box("literacy", "⚠️ THE #1 MISTAKE ON THIS TOPIC — restated",
        "Watch for two traps: (1) multiplying by a whole-number percent instead of its decimal or "
        "fraction form — this makes answers 100× too big; (2) adding fraction numerators/denominators "
        "instead of multiplying straight across.")

# ======================================================================
# STEP 7 — Additional Practice
# ======================================================================
elif step == 7:
    st.write("**Additional Practice — Real-World Percent Problems.** Pick whichever method — decimal or "
             "fraction — feels faster for each one.")

    st.markdown("### Problem 1 — Restaurant tip")
    problem_box("Practice", "A meal costs $20. You leave a 15% tip. How much is the tip?")
    a1 = st.number_input("Tip amount ($):", min_value=0.0, step=0.5, key="add_p1")
    if st.button("Check Problem 1", key="check_add1"):
        n = attempt("add1")
        if abs(a1 - 3) < 0.01:
            st.success("Correct! 0.15 × 20 = $3.00.")
        else:
            st.error("Not yet — 15% = 0.15. Multiply 0.15 × 20.")
            if n >= 2:
                explain("Redo help", ["0.15 × 20", "15 × 20 = 300", "2 decimal places → <b>$3.00</b>"])

    st.markdown("### Problem 2 — Jacket discount")
    problem_box("Practice", "A jacket costs $90 and is 1/3 off. How much money is taken off the price?")
    a2 = st.number_input("Discount amount ($):", min_value=0.0, step=1.0, key="add_p2")
    if st.button("Check Problem 2", key="check_add2"):
        n = attempt("add2")
        if abs(a2 - 30) < 0.01:
            st.balloons()
            st.success("Correct! 1/3 × 90 = 90/3 = $30 off.")
        else:
            st.error("Not yet — divide 90 by 3.")
            if n >= 2:
                explain("Redo help", ["1/3 × 90/1 = 90/3", "= <b>$30</b>"])

    st.markdown("### Problem 3 — Class survey")
    problem_box("Practice", "90% of the 30 students in a class say chocolate is their favorite ice cream "
                "flavor. How many students is that?")
    a3 = st.number_input("Number of students:", min_value=0, step=1, key="add_p3")
    if st.button("Check Problem 3", key="check_add3"):
        n = attempt("add3")
        if a3 == 27:
            st.success("Correct! 0.90 × 30 = 27 students.")
        else:
            st.error("Not yet — multiply 0.90 by 30.")
            if n >= 2:
                explain("Redo help", ["0.90 × 30", "90 × 30 = 2,700", "2 decimal places → <b>27</b>"])

    st.markdown("### Problem 4 — Bag of marbles")
    problem_box("Practice", "A bag has 40 marbles. 3/10 of them are blue. How many blue marbles are there?")
    a4 = st.number_input("Blue marbles:", min_value=0, step=1, key="add_p4")
    if st.button("Check Problem 4", key="check_add4"):
        n = attempt("add4")
        if a4 == 12:
            st.balloons()
            st.success("Correct! 3/10 × 40 = 120/10 = 12 marbles.")
        else:
            st.error("Not yet — multiply 3 × 40, then divide by 10.")
            if n >= 2:
                explain("Redo help", ["3/10 × 40/1 = (3×40)/10", "= 120/10", "= <b>12</b>"])
    pair_share("For each problem above, did you reach for the decimal method or the fraction method? What "
              "made you choose it?")

# ======================================================================
# STEP 8 — Engage / Explore / Enrich & Math Journal
# ======================================================================
elif step == 8:
    st.markdown("#### Engage / Explore / Enrich stations")
    e1, e2, e3 = st.columns(3)
    with e1:
        st.markdown(
            f"""
            <div class="box box-tools">
            <span class="pill">Engage · with teacher</span>
            <i>Still needs support converting a percent into a decimal or fraction before multiplying.</i><br><br>
            1. Rebuild the 0.5 × 0.4 grid and the 3/4 × 2/3 array by hand on graph paper.<br>
            2. Redo Marcus's and Priya's mistakes together, out loud, before trying new numbers.<br>
            3. Additional Practice, problems 1–2 only.
            </div>
            """,
            unsafe_allow_html=True,
        )
    with e2:
        st.markdown(
            """
            <div class="box box-existing">
            <span class="pill">Explore · independent</span>
            <i>Comfortable multiplying decimals and fractions, ready to apply both to real percent problems.</i><br><br>
            1. Additional Practice, problems 1–4.<br>
            2. Refine, Same Percent Two Paths — try it with 50% and 10% of your own chosen whole.<br>
            3. <a href="https://www.ixl.com/math/grade-6/percents-of-numbers-word-problems" target="_blank" rel="noopener noreferrer">📝 HMWK — IXL <b>Percents of numbers: word problems</b> (Grade 6)</a>.
            </div>
            """,
            unsafe_allow_html=True,
        )
    with e3:
        st.markdown(
            """
            <div class="box box-method">
            <span class="pill">Enrich · beyond 100%</span>
            <i>Fluent with both engines, ready for a multi-step problem and a percent bigger than 100%.</i><br><br>
            1. A $80 video game is 20% off. Then 8% tax is added to the <b>discounted</b> price. Find the
            final price (two steps!).<br>
            2. Prove that 150% of a number gives the same result whether you multiply by 1.5 or by 3/2.
            Try it with a number of your own choosing.<br>
            3. Full Additional Practice, all 4 problems.
            </div>
            """,
            unsafe_allow_html=True,
        )
    with st.expander("Check the Enrich video-game problem"):
        e_final = st.number_input("Final price after discount AND tax ($):", min_value=0.0, step=0.01, key="enrich_game")
        if st.button("Check final price", key="check_enrich_game"):
            n = attempt("enrich_game")
            if abs(e_final - 69.12) < 0.02:
                st.balloons()
                st.success("Correct! Discount: 0.20 × 80 = 16, so the sale price is 80 − 16 = $64. Tax: "
                           "0.08 × 64 = 5.12. Final price: 64 + 5.12 = <b>$69.12</b>.")
            else:
                st.error("Not yet — first find the sale price (80 minus 20% of 80), THEN add 8% tax on "
                         "that new price, not the original $80.")
                if n >= 2:
                    explain("Redo help", ["Discount: 0.20 × 80 = 16 → sale price = 80 − 16 = 64",
                                          "Tax: 0.08 × 64 = 5.12",
                                          "Final price = 64 + 5.12 = <b>$69.12</b>"])

    st.markdown("---")
    st.markdown("#### Math Journal — Build your own percent")
    st.caption("Pick a percent and a whole number. The grid will shade that percent for you. Then find "
               "that percent of your whole two ways, and show they match.")
    j_percent = st.slider("My percent:", 1, 100, 40, key="journal_percent")
    j_whole = st.number_input("My whole number:", min_value=1, step=1, value=60, key="journal_whole")
    j_frac = Fraction(j_percent, 100)
    j_part_decimal = (j_percent / 100) * j_whole
    j_part_fraction = j_frac * j_whole
    st.pyplot(draw_hundred_grid(j_percent, title=f"{j_percent}% shaded"), use_container_width=False)
    st.write(f"**{j_percent}%** = **{j_frac}** as a simplified fraction = **{j_percent / 100:g}** as a decimal.")
    st.write(f"{j_percent}% of {j_whole:g} — decimal method: {j_part_decimal:g}. Fraction method: "
             f"{float(j_part_fraction):g}.")
    j_note = st.text_area("Journal sentence — in your own words, why do both methods always match?",
                          height=80, key="journal_note")
    if j_note.strip():
        st.success("Journaled. Nice work connecting the two engines.")

    st.markdown("---")
    st.markdown("#### End of Lesson Checklist")
    checklist = [
        "I can multiply two decimals and correctly place the decimal point.",
        "I can multiply two fractions (or a fraction and a whole number) using the standard algorithm.",
        "I can explain that a percent is a fraction with a denominator of 100.",
        "I can find the percent of a quantity using the decimal method OR the fraction method and get "
        "the same answer either way.",
        "I can catch the 'forgot to convert the percent first' mistake and the 'added instead of "
        "multiplied' fraction mistake.",
    ]
    checked = 0
    for i, item in enumerate(checklist):
        if st.checkbox(item, key=f"eol_{i}"):
            checked += 1
    st.progress(checked / len(checklist))
    if checked == len(checklist):
        st.success(f"{name or 'Mathematician'}, you've checked off every goal for today's Skill Breakout!")

    st.markdown("---")
    icans = [
        ("DECIMALS", "I can multiply decimals and place the decimal point correctly. (6.NS.B.3)"),
        ("FRACTIONS", "I can multiply fractions by multiplying straight across, then simplifying. (5.NF.B.4)"),
        ("CONNECT", "I can show that a percent, its fraction, and its decimal always give the same "
         "answer. (6.RP.A.3.c)"),
        ("PRECISION", "I can catch a forgot-to-convert mistake or an added-instead-of-multiplied "
         "mistake before I make it. (MP.6)"),
    ]
    for tag, text in icans:
        st.markdown(f'<div class="box box-existing" style="border-left:6px solid {GOLD};padding:0.7rem 1rem;">'
                     f'<span class="pill" style="background:{NAVY};">{tag}</span>{text}</div>', unsafe_allow_html=True)
    st.caption(
        "Standards in play: 6.NS.B.3 (multiply multi-digit decimals) · 5.NF.B.4 (multiply fractions — "
        "foundational) · 6.RP.A.3.c (find a percent of a quantity as a rate per 100) · MP.2 (reason "
        "abstractly/quantitatively) · MP.4 (model with mathematics) · MP.7 (look for structure) · "
        "MP.8 (express regularity in repeated reasoning)."
    )
    st.markdown(
        f"""
        <div class="box box-tools">
        Both engines are built: multiplying decimals, and multiplying fractions. And you proved the big
        idea — a percent is just one of those two engines wearing a special &ldquo;out of 100&rdquo;
        badge.
        <br><br><b>{name or 'Mathematician'}, tomorrow both engines go to work on real percent-of-a-quantity
        problems &mdash; and you'll even run one in reverse to find the whole.</b>
        </div>
        """,
        unsafe_allow_html=True,
    )

st.markdown("---")
c_back, c_next = st.columns([1, 1])
if c_back.button("⬅ Back", disabled=(step == 0)):
    st.session_state.step = max(0, step - 1)
    st.rerun()
if c_next.button("Next ➡", disabled=(step == len(steps) - 1)):
    st.session_state.step = min(len(steps) - 1, step + 1)
    st.rerun()

st.caption("Standards in play: 6.NS.B.3 (multiply decimals) · 5.NF.B.4 (multiply fractions — foundational) "
           "· 6.RP.A.3.c (percent of a quantity) · MP.2, MP.4, MP.7, MP.8.")
st.markdown(
    "<div class='credit'>www.cognitivecloud.ai &middot; Developed by Xavier Honablue, M.Ed &middot; "
    "Chandler Park Academy</div>",
    unsafe_allow_html=True,
)
