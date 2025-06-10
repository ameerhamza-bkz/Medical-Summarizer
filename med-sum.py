# Import required libraries
import streamlit as st
import requests
import json
import os

# --- API Key Setup ---
# If using dotenv, uncomment the next two lines to load from a .env file
# from dotenv import load_dotenv
# load_dotenv()  # Loads environment variables from a .env file

# Option 1: Get API key from Streamlit secrets (recommended for Streamlit Cloud)
API_KEY = st.secrets["openrouter"]["api_key"]

# Option 2: Uncomment to get API key from environment variable (for local development)
# API_KEY = os.getenv("API_KEY")

# --- Streamlit Page Configuration ---
st.set_page_config(
    page_title="Medical Assistant",
    page_icon="🩺",
    layout="centered"
)

# --- App Title and Instructions ---
st.title("🩺 Medical Diagnosis & Prescription Explainer")
st.write(
    "Enter your diagnosis and prescribed medicines. "
    "This assistant will explain your diagnosis, the medicines, their uses, composition, and precautions in simple terms."
)

# --- User Input Form ---
with st.form("medical_form"):
    # Input for diagnosis
    diagnosis = st.text_input(
        "Diagnosis",
        placeholder="e.g., Hypertension"
    )
    # Input for medicines (comma separated)
    medicines = st.text_input(
        "Prescribed Medicines (comma separated)",
        placeholder="e.g., Metformin, Lisinopril"
    )
    # Submit button
    submitted = st.form_submit_button("Explain")

# --- Handle Form Submission ---
if submitted:
    # Validate that both fields are filled
    if not diagnosis or not medicines:
        st.warning("Please fill in both fields.")
    else:
        # --- Prepare the prompt for the LLM API ---
        prompt = (
            f"Diagnosis: {diagnosis}\n"
            f"Medicines: {medicines}\n"
            "Explain the diagnosis, medicine uses, composition, and precautions in an easy to understand manner "
            "to help the patient understand the diagnosis and prescribed medicines easily. "
            "add a little joke at end to cheer patient"
        )

        # --- API Endpoint and Headers ---
        url = "https://openrouter.ai/api/v1/chat/completions"
        headers = {
            "Authorization": f"Bearer {API_KEY}",
            "Content-Type": "application/json",
        }

        # --- Data Payload for API Call ---
        data = {
            "model": "deepseek/deepseek-r1:free",
            "messages": [
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        }

        # --- Make API Call and Display Result ---
        with st.spinner("Contacting the medical assistant..."):
            try:
                response = requests.post(
                    url,
                    headers=headers,
                    data=json.dumps(data),
                    timeout=60
                )
                response.raise_for_status()  # Raise error for bad HTTP status
                reply = response.json()['choices'][0]['message']['content']
                st.success("Explanation:")
                st.markdown(reply)
            except Exception as e:
                st.error(f"Error: {e}")
