import streamlit as st

from src.billing.service import require_feature

from src.dashboard import (
    setup_page,
    apply_theme,
    load_filtered_data,
    page_header
)

from src.security.access import current_user
from src.ai.copilot import answer_question

setup_page("AI Business Copilot", "🤖")
apply_theme()

user = current_user()

try:
    require_feature(user["company_id"], "ai_copilot")
except PermissionError as exc:
    st.warning(str(exc))
    st.stop()

df = load_filtered_data()

page_header(
    "OpsPilot AI Copilot",
    "Ask questions about your business performance"
)

st.caption(
    f"Workspace: {user['company_name']} | "
    "Answers use your current dashboard filters."
)

examples = [
    "What is my total revenue?",
    "What is my gross profit margin?",
    "Show top 5 customers",
    "Which plant has the highest profit?",
    "How many orders do I have?"
]

question = st.selectbox(
    "Try an example",
    ["Custom question"] + examples
)

if question == "Custom question":
    question = st.text_input(
        "Ask your business question",
        placeholder="Which plant generated the highest profit?"
    )

if st.button("Ask OpsPilot AI", type="primary"):
    if question.strip():
        with st.chat_message("assistant"):
            st.markdown(
                answer_question(df, question)
            )
    else:
        st.warning("Please enter a question.")

st.divider()
st.info(
    "This version uses deterministic business analytics. "
    "It does not call an external AI model."
)
