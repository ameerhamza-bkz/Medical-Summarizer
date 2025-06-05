from dotenv import load_dotenv
import streamlit as st
import requests
import json
import os

# Set your OpenRouter API key here
load_dotenv()  # loads variables from .env into environment
API_KEY = os.getenv("API_KEY")

st.set_page_config(page_title="Medical Assistant", page_icon="🩺", layout="centered")

st.title("🩺 Medical Diagnosis & Prescription Explainer")
st.write(
    "Enter your diagnosis and prescribed medicines. "
    "This assistant will explain your diagnosis, the medicines, their uses, composition, and precautions in simple terms."
)

with st.form("medical_form"):
    diagnosis = st.text_input("Diagnosis", placeholder="e.g., Hypertension")
    medicines = st.text_input("Prescribed Medicines (comma separated)", placeholder="e.g., Metformin, Lisinopril")
    submitted = st.form_submit_button("Explain")

if submitted:
    if not diagnosis or not medicines:
        st.warning("Please fill in both fields.")
    else:
        # Prepare prompt and API call
        prompt = (
            f"Diagnosis: {diagnosis}\n"
            f"Medicines: {medicines}\n"
            "Explain the diagnosis, medicine uses, composition, and precautions in an easy to understand manner to help the patient understand the diagnosis and prescribed medicines easily. add a little joke at end to cheer patient"
        )
        url = "https://openrouter.ai/api/v1/chat/completions"
        headers = {
            "Authorization": f"Bearer {API_KEY}",
            "Content-Type": "application/json",
        }
        data = {
            "model": "deepseek/deepseek-r1:free",
            "messages": [
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        }
        with st.spinner("Contacting the medical assistant..."):
            try:
                response = requests.post(url, headers=headers, data=json.dumps(data), timeout=60)
                response.raise_for_status()
                reply = response.json()['choices'][0]['message']['content']
                st.success("Explanation:")
                st.markdown(reply)
            except Exception as e:
                st.error(f"Error: {e}")


