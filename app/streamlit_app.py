import streamlit as st
import os
import time
import sys

# ensure project root is on path so sibling packages can be imported
ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)

from login_page import login_page
from preprocessing.pdf_loader import extract_text
# module name is selection_splitter, not section_splitter
from preprocessing.selection_splitter import split_sections
from generation.summarizer import summarize
from generation.methodology_explainer import explain_methodology
# keyword_extractors is the correct filename
from insights.keyword_extractors import extract_keywords
from insights.citation_extractors import extract_citations
from export.export_pdf import export_summary_to_pdf

# -----------------------------
# HISTORY FOLDER FUNCTIONALITY
# -----------------------------
HISTORY_FOLDER = "history"

if not os.path.exists(HISTORY_FOLDER):
    os.makedirs(HISTORY_FOLDER)


def save_pdf_to_history(uploaded_pdf):
    """Save uploaded PDF into history folder."""
    timestamp = time.strftime("%Y%m%d_%H%M%S")
    filename = f"{timestamp}_{uploaded_pdf.name}"
    filepath = os.path.join(HISTORY_FOLDER, filename)

    with open(filepath, "wb") as f:
        f.write(uploaded_pdf.getbuffer())

    return filepath


# -----------------------------
# LOGIN PAGE
# -----------------------------
is_logged_in = login_page()

if is_logged_in:

    # -----------------------------
    # LOGOUT BUTTON
    # -----------------------------
    logout_col = st.columns(1)[0]
    with logout_col:
        if st.button("⬅ Logout"):
            st.session_state.logged_in = False
            st.success("You have been logged out.")
            st.rerun()

    st.title("📘 AI Research Paper Assistant")

    # -----------------------------
    # PDF UPLOAD
    # -----------------------------
    pdf = st.file_uploader("Upload Research Paper PDF", type=["pdf"])

    if pdf:
        st.success("📄 PDF successfully added!")

        # Save to history
        save_pdf_to_history(pdf)
        st.success("📁 PDF saved to history!")

        # Extract text
        text = extract_text(pdf)
        st.success("✅ PDF successfully read!")

        # Split sections
        sections = split_sections(text)
        final_output = ""

        st.header("📌 Section Summaries")

        # -----------------------------
        # SECTION SUMMARIES
        # -----------------------------
        for sec, content in sections.items():
            st.subheader(sec.capitalize())
            summary = summarize(content)
            st.write(summary)
            final_output += f"\n\n### {sec.capitalize()} Summary:\n{summary}\n"

        # -----------------------------
        # METHODOLOGY EXPLANATION
        # -----------------------------
        if "methodology" in sections:
            st.subheader("🧪 Methodology Explained")
            explanation = explain_methodology(sections["methodology"])
            st.write(explanation)
            final_output += f"\n\n### Methodology Explained:\n{explanation}\n"

        # -----------------------------
        # LIMITATIONS SUMMARY
        # -----------------------------
        if "limitations" in sections:
            st.subheader("⚠ Limitations Summary")
            limits = summarize(sections["limitations"])
            st.write(limits)
            final_output += f"\n\n### Limitations Summary:\n{limits}\n"

        # -----------------------------
        # KEYWORDS
        # -----------------------------
        st.subheader("🔑 Extracted Keywords")
        keywords = extract_keywords(text)
        st.write(keywords)
        final_output += f"\n\n### Keywords:\n{keywords}\n"

        # -----------------------------
        # CITATIONS
        # -----------------------------
        st.subheader("📚 Extracted Citations")
        citations = extract_citations(text)
        st.write(citations)
        final_output += f"\n\n### Citations:\n{citations}\n"

        # -----------------------------
        # HISTORY MANAGEMENT
        # -----------------------------
        st.header("📂 PDF Upload History")
        history_files = os.listdir(HISTORY_FOLDER)

        if history_files:
            for file in history_files:
                file_path = os.path.join(HISTORY_FOLDER, file)
                st.write(f"📄 {file}")

                col1, col2 = st.columns(2)

                # Download button
                with col1:
                    with open(file_path, "rb") as f:
                        st.download_button(
                            label="⬇ Download",
                            data=f,
                            file_name=file,
                            key=f"download_{file}"
                        )

                # Delete button
                with col2:
                    if st.button("🗑 Delete", key=f"delete_{file}"):
                        os.remove(file_path)
                        st.warning(f"Deleted: {file}")
                        st.rerun()
        else:
            st.info("No history found.")

        # -----------------------------
        # EXPORT SUMMARY TO PDF
        # -----------------------------
        pdf_path = export_summary_to_pdf(final_output)

        with open(pdf_path, "rb") as f:
            pdf_data = f.read()

        st.download_button(
            label="📥 Export Summary to PDF",
            data=pdf_data,
            file_name="Research_Summary.pdf",
            mime="application/pdf"
        )