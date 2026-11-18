import streamlit as st

from src.billing.service import require_feature

from src.dashboard import (
    setup_page, apply_theme,
    load_filtered_data, page_header
)
from src.security.access import current_user
from src.reports.pdf_report import build_business_report

setup_page("Business Reports", "📄")
apply_theme()

user = current_user()

try:
    require_feature(user["company_id"], "pdf_reports")
except PermissionError as exc:
    st.warning(str(exc))
    st.stop()

df = load_filtered_data()

page_header(
    "Business Reports",
    "Generate financial and operational PDF reports"
)

st.metric("Transactions in Report", f"{len(df):,}")

st.write(
    "The report includes revenue, costs, gross profit, "
    "top customers, and automated business insights."
)

if st.button("Generate PDF Report", type="primary"):
    try:
        pdf = build_business_report(
            df, user["company_name"]
        )

        st.session_state["generated_pdf"] = pdf
        st.session_state["report_company"] = user["company_id"]

    except Exception as exc:
        st.error(f"Report generation failed: {exc}")

if (
    "generated_pdf" in st.session_state
    and st.session_state.get("report_company") == user["company_id"]
):
    st.download_button(
        "Download Business Report",
        data=st.session_state["generated_pdf"],
        file_name="opspilot_business_report.pdf",
        mime="application/pdf"
    )
