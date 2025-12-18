import streamlit as st
from src.services.auth_service import AuthService
from src.services.prediction_service import PredictionService
from src.model_config import MODELS, get_model_path
from auth import create_users_table

# Create users table
create_users_table()

auth_service = AuthService()
prediction_service = PredictionService()

st.set_page_config(page_title="Crop Disease Detection")

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

# ---------- AUTH ----------
if not st.session_state.logged_in:
    st.title("🔐 User Authentication")

    tab1, tab2 = st.tabs(["Login", "Register"])

    # ---------- LOGIN ----------
    with tab1:
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")

        if st.button("Login"):
            if auth_service.login(username, password):
                st.session_state.logged_in = True
                st.rerun()
            else:
                st.error("Invalid credentials")

    # ---------- REGISTER ----------
    with tab2:
        new_user = st.text_input("New Username")
        new_pass = st.text_input("New Password", type="password")

        if st.button("Register"):
            if auth_service.register(new_user, new_pass):
                st.success("Account created. Please login.")
            else:
                st.error("Username already exists")

    st.stop()

# ---------- MAIN APP ----------
st.title("🌾 Crop Disease Detection System")

if st.button("Logout"):
    st.session_state.logged_in = False
    st.rerun()

uploaded = st.file_uploader("Upload Image", ["jpg", "png", "jpeg"])
model_choice = st.selectbox("Select Model", MODELS.keys())

if uploaded:
    with open("temp.jpg", "wb") as f:
        f.write(uploaded.getbuffer())

    if st.button("Predict"):
        model_path = get_model_path(model_choice)
        label, conf = prediction_service.predict(model_path, "temp.jpg")

        st.success(f"🦠 Disease: {label}")
        st.info(f"🎯 Confidence: {conf:.2f}%")
