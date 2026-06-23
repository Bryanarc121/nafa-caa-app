import streamlit as st
from dataclasses import dataclass
from typing import List


@dataclass
class Option:
    label: str
    value: int


@dataclass
class Question:
    number: int
    title: str
    description: str
    options: List[Option]
    allow_multiple: bool = False


QUESTIONS: List[Question] = [
    Question(1, "MERV number of filters",
             "Minimum of MERV 8. One point per MERV number. Example: MERV 8 = 8 points; MERV 16 = 16 points.",
             [Option(str(i), i) for i in range(8, 17)]),

    Question(2, "Gaskets",
             "Gaskets must be installed either on the filter or on the filter frame. Include a picture of the installed gaskets or the mechanism that ensures the air filtration system's integrity.",
             [Option("Yes", 10), Option("No", 0), Option("Don't Know", 0)]),

    Question(3, "Filter monitoring devices",
             "Filter monitoring devices such as pressure gauges, BMS systems, or BMS monitors are installed and functional.",
             [Option("Yes", 10), Option("No", 0), Option("Don't Know", 0)]),

    Question(4, "Filter change record",
             "Up-to-date records showing quantity, size, and frequency for all HVAC units. Include a copy of the records.",
             [Option("Yes", 10), Option("No", 0), Option("Don't Know", 0)]),

    Question(5, "System duct cleaning",
             "Ducts in the air system have been cleaned within the last 3 years. Provide documentation.",
             [Option("Yes", 10), Option("No", 0), Option("Don't Know", 0)]),

    Question(6, "Use of high efficiency filter",
             "Minimum MERV 13.",
             [Option("Yes", 10), Option("No", 0), Option("Don't Know", 0)]),

    Question(7, "System Improvements",
             "Select all improvements completed or installed. Each selected item is worth 10 points.",
             [
                 Option("Coil Cleaning within last two years", 10),
                 Option("UVC Systems installed in air handler units, common areas, or in-duct applications", 10),
                 Option("IAQ Testing/Monitoring completed within the previous 12 months", 10),
                 Option("Gas Phase Filtration installed and changed on a planned periodic basis", 10),
                 Option("External Air Intake Screen such as bio screen, cottonwood screen, or hail guard", 10),
             ],
             allow_multiple=True),

    Question(8, "Bonus: Installed products from a NAFA Manufacturer",
             "Installed filters utilize products manufactured or produced by a NAFA Manufacturing Member.",
             [Option("Yes", 6), Option("No", 0), Option("Don't Know", 0)]),

    Question(9, "Bonus: NAFA Certified Technician",
             "NAFA Certified Technician on recipient staff or yearly filter service contract by a third-party NAFA Certified Technician service crew.",
             [Option("Yes", 6), Option("No", 0), Option("Don't Know", 0)]),
]

MINIMUM_QUALIFYING_SCORE = 62


st.set_page_config(
    page_title="Clean Air Award Facility Assessment",
    page_icon="✅",
    layout="centered",
)


def init_state():
    if "show_result" not in st.session_state:
        st.session_state.show_result = False
    if "answers" not in st.session_state:
        st.session_state.answers = {}
    for q in QUESTIONS:
        if q.number not in st.session_state.answers:
            st.session_state.answers[q.number] = [] if q.allow_multiple else None


def reset_form():
    st.session_state.show_result = False
    for q in QUESTIONS:
        st.session_state.answers[q.number] = [] if q.allow_multiple else None
        for key in (f"q_{q.number}", f"q_{q.number}_multi"):
            if key in st.session_state:
                del st.session_state[key]


def calculate_question_points(q: Question) -> int:
    answer = st.session_state.answers.get(q.number)

    if q.allow_multiple:
        if not answer:
            return 0
        option_map = {opt.label: opt.value for opt in q.options}
        return sum(option_map.get(label, 0) for label in answer)

    if answer is None:
        return 0

    match = next((opt for opt in q.options if opt.label == answer), None)
    return match.value if match else 0


def calculate_total() -> int:
    return sum(calculate_question_points(q) for q in QUESTIONS)


def count_completed() -> int:
    completed = 0
    for q in QUESTIONS:
        answer = st.session_state.answers.get(q.number)
        if q.allow_multiple:
            if isinstance(answer, list) and len(answer) > 0:
                completed += 1
        else:
            if answer is not None:
                completed += 1
    return completed


def get_result(total: int):
    if total >= MINIMUM_QUALIFYING_SCORE:
        return {
            "title": "Ready!",
            "message": "You meet the minimum point threshold. Talk to your air filtration supplier about a NAFA Clean Air Award submission for your facility.",
            "bg": "#78B54B",
            "border": "#5E9339",
            "text": "#111111",
        }

    if total >= 45:
        return {
            "title": "Nearly Ready!",
            "message": "You are below the minimum 62-point threshold. Review the unmet criteria and talk to your air filtration supplier about improvement options.",
            "bg": "#F6C103",
            "border": "#D9A701",
            "text": "#111111",
        }

    return {
        "title": "Not Ready!",
        "message": "You are below the minimum 62-point threshold. Additional work is required before pursuing a Clean Air Award submission.",
        "bg": "#F31A12",
        "border": "#D9A701",
        "text": "#FFFFFF",
    }


init_state()

st.markdown(
    """
    <style>
    .main-title {
        color: #001489;
        font-size: 2.6rem;
        line-height: 1.08;
        font-weight: 800;
        margin-bottom: 0.75rem;
    }
    .blue-banner {
        background: #001489;
        color: #ffffff;
        padding: 18px 20px;
        margin-bottom: 20px;
        font-size: 1.05rem;
        line-height: 1.45;
    }
    .question-card {
        background: #ffffff;
        border: 1px solid #c7cbe0;
        border-radius: 10px;
        padding: 18px;
        margin-bottom: 14px;
        box-shadow: 0 1px 2px rgba(0,0,0,0.04);
    }
    .question-number {
        font-size: 0.82rem;
        font-weight: 700;
        color: #64748b;
        margin-bottom: 6px;
        text-transform: uppercase;
        letter-spacing: 0.03em;
    }
    .question-title {
        font-size: 1.08rem;
        font-weight: 800;
        color: #111111;
        margin-bottom: 6px;
    }
    .question-desc {
        font-size: 0.95rem;
        color: #222222;
        margin-bottom: 10px;
        line-height: 1.45;
    }
    .points-caption {
        font-size: 0.9rem;
        color: #475569;
        margin-bottom: 16px;
    }
    .result-burst {
        clip-path: polygon(
            50% 0%, 55% 10%, 65% 2%, 68% 14%, 80% 5%, 78% 20%, 92% 12%, 86% 28%,
            100% 25%, 90% 38%, 98% 50%, 90% 62%, 100% 75%, 86% 72%, 92% 88%, 78% 80%,
            80% 95%, 68% 86%, 65% 98%, 55% 90%, 50% 100%, 45% 90%, 35% 98%, 32% 86%,
            20% 95%, 22% 80%, 8% 88%, 14% 72%, 0% 75%, 10% 62%, 2% 50%, 10% 38%,
            0% 25%, 14% 28%, 8% 12%, 22% 20%, 20% 5%, 32% 14%, 35% 2%, 45% 10%
        );
        padding: 48px 34px;
        text-align: center;
        margin-top: 16px;
        margin-bottom: 10px;
        border: 3px solid;
        font-weight: 700;
    }
    .result-title {
        font-size: 2rem;
        line-height: 1.2;
        margin-bottom: 12px;
        font-weight: 800;
    }
    .result-message {
        font-size: 1.35rem;
        line-height: 1.35;
        font-weight: 700;
    }
    .score-box {
        background: #f8fafc;
        border: 1px solid #cbd5e1;
        border-radius: 12px;
        padding: 14px 16px;
        margin-top: 10px;
        margin-bottom: 14px;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

st.markdown('<div class="main-title">Clean Air Award Facility<br>Assessment Form</div>', unsafe_allow_html=True)

st.markdown(
    f"""
    <div class="blue-banner">
        Perform this self-assessment for your facility by entering points based on the criteria.<br>
        To be considered for the Clean Air Award, nominees need a minimum of <strong>{MINIMUM_QUALIFYING_SCORE} points</strong>.
    </div>
    """,
    unsafe_allow_html=True,
)

for q in QUESTIONS:
    max_points = sum(opt.value for opt in q.options) if q.allow_multiple else max(opt.value for opt in q.options)

    st.markdown(
        f"""
        <div class="question-card">
            <div class="question-number">Criteria {q.number}</div>
            <div class="question-title">{q.title}</div>
            <div class="question-desc">{q.description}</div>
            <div class="points-caption"><strong>Maximum points:</strong> {max_points}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    labels = [opt.label for opt in q.options]

    if q.allow_multiple:
        selected = st.multiselect(
            f"Select all that apply for Criteria {q.number}",
            options=labels,
            default=st.session_state.answers[q.number],
            key=f"q_{q.number}_multi",
        )
        st.session_state.answers[q.number] = selected
    else:
        selected = st.selectbox(
            f"Select answer for Criteria {q.number}",
            options=["Choose One"] + labels,
            index=0 if st.session_state.answers[q.number] is None else (labels.index(st.session_state.answers[q.number]) + 1),
            key=f"q_{q.number}",
            label_visibility="collapsed",
        )

        if selected == "Choose One":
            st.session_state.answers[q.number] = None
        else:
            st.session_state.answers[q.number] = selected

    st.caption(f"Assigned value: {calculate_question_points(q)}")

completed = count_completed()
total = calculate_total()

col1, col2 = st.columns(2)
with col1:
    if st.button("Show Result", use_container_width=True):
        st.session_state.show_result = True

with col2:
    if st.button("Clear", use_container_width=True):
        reset_form()
        st.rerun()

if st.session_state.show_result:
    result = get_result(total)

    st.markdown(
        f"""
        <div class="score-box">
            <strong>Total Points:</strong> {total}<br>
            <strong>Completed Criteria:</strong> {completed}/{len(QUESTIONS)}<br>
            <strong>Minimum Required:</strong> {MINIMUM_QUALIFYING_SCORE} points
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(
        f"""
        <div class="result-burst" style="background:{result['bg']}; border-color:{result['border']}; color:{result['text']};">
            <div class="result-title">{result['title']}</div>
            <div class="result-message">{result['message']}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )
