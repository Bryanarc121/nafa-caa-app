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


QUESTIONS: List[Question] = [
    Question(
        1,
        "What is the MERV rating of the filters?",
        "Minimum of MERV 8. One point per MERV number.",
        [Option(str(i), i) for i in range(8, 17)],
    ),
    Question(
        2,
        "Was the work performed by a NAFA Certified Technician (NCT) on the facility staff?",
        "NAFA Certified Technician (NCT) on facility staff.",
        [Option("Yes", 10), Option("No", 0), Option("Don't Know", 0)],
    ),
    Question(
        3,
        "Was the work performed by a 3rd party NAFA Certified Technician (NCT) via service contract?",
        "NAFA Certified Technician (NCT) on contracted vendor.",
        [Option("Yes", 10), Option("No", 0), Option("Don't Know", 0)],
    ),
    Question(
        4,
        "Are gaskets in place?",
        "Installed to prevent air bypass (doors, channels, between filters, etc.).",
        [Option("Yes", 10), Option("No", 0), Option("Don't Know", 0)],
    ),
    Question(
        5,
        "Are there filter monitoring devices in place and functional?",
        "For example, pressure gauges. Installed and functional.",
        [Option("Yes", 10), Option("No", 0), Option("Don't Know", 0)],
    ),
    Question(
        6,
        "Do you have filter change record(s)?",
        "Up-to-date records showing size, number, and frequency for all HVAC units.",
        [Option("Yes", 10), Option("No", 0), Option("Don't Know", 0)],
    ),
    Question(
        7,
        "System filter upgrade?",
        "Was there an upgrade of the filtration system within the preceding 12 months by a NAFA Certified Air Filter Specialist (CAFS)?",
        [Option("Yes", 10), Option("No", 0), Option("Don't Know", 0)],
    ),
    Question(
        8,
        "Installed products",
        "Does the facility utilize air filters or air-filtration-related products manufactured or produced by a NAFA Manufacturing Member?",
        [Option("Yes", 10), Option("No", 0), Option("Don't Know", 0)],
    ),
    Question(
        9,
        "System duct cleaning",
        "Were the ducts in the air system cleaned within the last 3 years?",
        [Option("Yes", 10), Option("No", 0), Option("Don't Know", 0)],
    ),
    Question(
        10,
        "Coil cleaning or UV light installation?",
        "Have the coils been cleaned within the last 2 years, or have UV lights been installed for coil/system cleanliness in the last 2 years?",
        [Option("Coil cleaning", 6), Option("UV Lights", 10), Option("None", 0)],
    ),
]


st.set_page_config(
    page_title="NAFA CAA Readiness Assessment",
    page_icon="✅",
    layout="centered",
)


def init_state():
    if "show_result" not in st.session_state:
        st.session_state.show_result = False
    if "answers" not in st.session_state:
        st.session_state.answers = {q.number: None for q in QUESTIONS}


def reset_form():
    st.session_state.show_result = False
    for q in QUESTIONS:
        st.session_state.answers[q.number] = None
        key = f"q_{q.number}"
        if key in st.session_state:
            del st.session_state[key]


def calculate_total() -> int:
    total = 0
    for q in QUESTIONS:
        selected_label = st.session_state.answers[q.number]
        if selected_label is None:
            continue
        match = next((opt for opt in q.options if opt.label == selected_label), None)
        if match:
            total += match.value
    return total


def count_completed() -> int:
    return sum(1 for value in st.session_state.answers.values() if value is not None)


def get_result(total: int):
    if total >= 52:
        return {
            "title": "You Are Ready!",
            "message": (
                "Talk to your air filtration supplier for a "
                "NAFA Clean Air Award submission for your facility."
            ),
            "bg": "#78B54B",
            "border": "#5E9339",
            "text": "#111111",
        }
    elif total >= 40:
        return {
            "title": "Partially Ready!",
            "message": (
                "Talk to your air filtration supplier on how you can "
                "improve air filtration in your facility."
            ),
            "bg": "#F6C103",
            "border": "#D9A701",
            "text": "#111111",
        }
    else:
        return {
            "title": "You Are Not Ready!",
            "message": (
                "Talk to your air filtration supplier on how you can "
                "improve air filtration in your facility."
            ),
            "bg": "#F31A12",
            "border": "#D9A701",
            "text": "#FFFFFF",
        }


init_state()

st.markdown(
    """
    <style>
    .question-card {
        background: #ffffff;
        border: 1px solid #e5e7eb;
        border-radius: 16px;
        padding: 18px;
        margin-bottom: 14px;
        box-shadow: 0 1px 2px rgba(0,0,0,0.04);
    }
    .question-number {
        font-size: 0.82rem;
        font-weight: 600;
        color: #64748b;
        margin-bottom: 6px;
        text-transform: uppercase;
        letter-spacing: 0.03em;
    }
    .question-title {
        font-size: 1.05rem;
        font-weight: 700;
        color: #0f172a;
        margin-bottom: 6px;
    }
    .question-desc {
        font-size: 0.93rem;
        color: #475569;
        margin-bottom: 10px;
        line-height: 1.45;
    }
    .result-burst {
        clip-path: polygon(
            50% 0%, 55% 10%, 65% 2%, 68% 14%, 80% 5%, 78% 20%, 92% 12%, 86% 28%,
            100% 25%, 90% 38%, 98% 50%, 90% 62%, 100% 75%, 86% 72%, 92% 88%, 78% 80%,
            80% 95%, 68% 86%, 65% 98%, 55% 90%, 50% 100%, 45% 90%, 35% 98%, 32% 86%,
            20% 95%, 22% 80%, 8% 88%, 14% 72%, 0% 75%, 10% 62%, 2% 50%, 10% 38%,
            0% 25%, 14% 28%, 8% 12%, 22% 20%, 20% 5%, 32% 14%, 35% 2%, 45% 10%
        );
        padding: 46px 34px;
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
        font-size: 1.6rem;
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

st.title("NAFA CAA Readiness Assessment")
st.write(
    "Complete each question, then click **Show Result**. "
    "Thresholds: **52+ Ready**, **40–51 Partially Ready**, **39 and below Not Ready**."
)

for q in QUESTIONS:
    st.markdown(
        f"""
        <div class="question-card">
            <div class="question-number">Question {q.number}</div>
            <div class="question-title">{q.title}</div>
            <div class="question-desc">{q.description}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    labels = [opt.label for opt in q.options]
    selected = st.selectbox(
        f"Select answer for Question {q.number}",
        options=["Choose One"] + labels,
        index=0 if st.session_state.answers[q.number] is None else (labels.index(st.session_state.answers[q.number]) + 1),
        key=f"q_{q.number}",
        label_visibility="collapsed",
    )

    if selected == "Choose One":
        st.session_state.answers[q.number] = None
        st.caption("Assigned value: -")
    else:
        st.session_state.answers[q.number] = selected
        option_value = next(opt.value for opt in q.options if opt.label == selected)
        st.caption(f"Assigned value: {option_value}")

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
            <strong>Total Score:</strong> {total}<br>
            <strong>Completed Questions:</strong> {completed}/{len(QUESTIONS)}<br>
            <strong>Thresholds:</strong> 52+ Ready, 40–51 Partially Ready, 39 and below Not Ready
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