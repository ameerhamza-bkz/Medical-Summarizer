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
        # # --- Prepare the prompt for the LLM API ---
        # prompt = (
        #     f"Diagnosis: {diagnosis}\n"
        #     f"Medicines: {medicines}\n"
        #     "Explain the diagnosis, medicine uses, composition, and precautions in an easy to understand manner "
        #     "to help the patient understand the diagnosis and prescribed medicines easily. "
        #     "add a little joke at end to cheer patient"
        # )
        prompt = f"""
        You are a highly accurate medical explanation assistant.
        Your job is to explain a diagnosis and the prescribed medicines clearly for a patient,
        using only information you are certain about. If any detail is unknown or not provided,
        state "Not enough information provided" instead of guessing.

        Guidelines:
        1. Use plain, non-technical language a non-medical person can understand.
        2. Explain:
        - What the diagnosis means.
        - What each medicine does.
        - The medicine's main ingredients or composition (if known).
        - Key precautions or warnings.
        3. Do NOT make up symptoms, effects, or drug names.
        4. Keep it friendly and encouraging.
        5. Add a short, light-hearted joke at the end to make the patient smile.

        Examples:

        Example 1:
        Diagnosis: Hypertension
        Medicines: Amlodipine
        Explanation:
        Hypertension means your blood pressure is higher than normal, which can put extra strain on your heart and blood vessels. 
        Amlodipine is a medicine that helps relax your blood vessels, making it easier for blood to flow and lowering your blood pressure. 
        Its active ingredient is amlodipine besylate. 
        Precautions: Take it at the same time each day, avoid grapefruit juice, and don’t skip doses. 
        Joke: "Think of your blood pressure like a balloon — we just don’t want it to float away!"

        Example 2:
        Diagnosis: Type 2 Diabetes
        Medicines: Metformin
        Explanation:
        Type 2 diabetes means your body has trouble using insulin properly, which makes it harder to control your blood sugar. 
        Metformin helps lower blood sugar by reducing sugar production in the liver and improving insulin sensitivity. 
        Its active ingredient is metformin hydrochloride. 
        Precautions: Take it with food to avoid stomach upset, and keep monitoring your blood sugar. 
        Joke: "We just want your sugar levels sweet, but not dessert-sweet!"

        Now, explain the following for the patient:

        Diagnosis: {diagnosis}
        Medicines: {medicines}
        Explanation:
        """


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
