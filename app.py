import streamlit as st
import tempfile
import json

# Import functions from your separate modules.
from text_extraction import extract_text_with_gemma3
from text_translate import translate_english_to_spanish, translate_spanish_to_english
from text_analysis import run_workflow  # This function implements the LangGraph workflow

# -------------------------------
# Streamlit App Setup
# -------------------------------
st.set_page_config(page_title="826 Valencia AI Editing Tool", layout="wide")
st.title("826 Valencia AI-Powered Editing & Translation Tool")
st.markdown(
    "This tool extracts student writing from an image, analyzes it using a multi-agent workflow "
    "based on LangGraph, and handles translation. Sensitive student documents remain local."
)

# -------------------------------
# Sidebar: Student Metadata and Language Selection
# -------------------------------
st.sidebar.header("Student Metadata")
student_name = st.sidebar.text_input("Student Name", "John Doe")
student_school = st.sidebar.text_input("School", "826 Valencia")
student_dob = st.sidebar.text_input("DOB (YYYY-MM-DD)", "2008-01-01")
student_age = st.sidebar.number_input("Age", min_value=5, max_value=30, value=15)

st.sidebar.header("Original Text Language")
original_language = st.sidebar.radio("Select language", options=["English", "Spanish"])

# -------------------------------
# Step 1: File Upload & Text Extraction
# -------------------------------
st.header("Step 1: Extract Text from Image")
uploaded_file = st.file_uploader("Upload an image of student writing", type=["png", "jpg", "jpeg"])

if uploaded_file is not None:
    # Save the uploaded file temporarily.
    with tempfile.NamedTemporaryFile(delete=False, suffix=".png") as tmp_file:
        tmp_file.write(uploaded_file.getvalue())
        tmp_file_path = tmp_file.name

    st.image(uploaded_file, caption="Uploaded Image", use_column_width=True)
    st.markdown("**Extracting text from image...**")
    extracted_text = extract_text_with_gemma3(tmp_file_path)
    st.subheader("Extracted Text")
    st.text_area("Extracted Text", extracted_text, height=200)
    
    # -------------------------------
    # Step 2: Translation (if needed) for Analysis
    # -------------------------------
    if original_language == "Spanish":
        st.markdown("**Translating Spanish text to English for analysis...**")
        english_text = translate_spanish_to_english(extracted_text)
        st.subheader("Translated to English")
        st.text_area("English Version", english_text, height=200)
    else:
        english_text = extracted_text

    # -------------------------------
    # Step 3: Provide Title & Run Analysis Workflow
    # -------------------------------
    st.header("Step 3: Run Analysis")
    title_input=""
    
    if st.button("Run Analysis"):
        # Build the ocr_json input for the LangGraph workflow.
        ocr_json = {
            "metadata": {
                "name": student_name,
                "school": student_school,
                "DOB": student_dob,
                "Age": student_age,
            },
            "Title": title_input,
            "Story": english_text,
        }
        st.markdown("**Running analysis workflow using LangGraph...**")
        analysis_report = run_workflow(ocr_json, max_iterations=5, context_dir="context_storage")
        st.subheader("Analysis Report")
        st.json(analysis_report)
        
        # -------------------------------
        # Step 4: Back Translation (if original text was Spanish)
        # -------------------------------
        if original_language == "Spanish":
            # We assume the corrected text is available in analysis_report under "FinalEditedText"
            corrected_english = analysis_report.get("FinalEditedText", english_text)
            st.markdown("**Translating corrected text back to Spanish...**")
            translated_spanish = translate_english_to_spanish(corrected_english)
            st.subheader("Final Corrected Text (Spanish)")
            st.text_area("Corrected Spanish Text", translated_spanish, height=200)
