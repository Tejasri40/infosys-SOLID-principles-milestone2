import streamlit as st
from PIL import Image
from src.services.auth_service import AuthService
from src.services.prediction_service import PredictionService
from src.model_config import MODELS, get_model_path
from auth import create_users_table

# Create users table
create_users_table()

auth_service = AuthService()
prediction_service = PredictionService()

st.set_page_config(page_title="Crop Disease Detection", layout="wide")

# ---------- SESSION STATE ----------
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

# ---------- SIDEBAR ----------
st.sidebar.title("Menu")
page = st.sidebar.radio(
    "Select Option",
    ["Disease Prediction", "Chatbot Assistance"]
)

if st.sidebar.button("Logout"):
    st.session_state.logged_in = False
    st.rerun()

# ---------- DISEASE PREDICTION ----------
if page == "Disease Prediction":

    st.title("🌾 Crop Disease Detection System")

    uploaded = st.file_uploader("Upload Image", ["jpg", "png", "jpeg"])
    model_choice = st.selectbox("Select Model", MODELS.keys())

    if uploaded is not None:
        from PIL import Image

        # Image Preview (CENTER)
        image = Image.open(uploaded)
        st.image(
            image,
            caption=None,
            use_container_width=False,
            width=200
        )

        # Save image
        with open("temp.jpg", "wb") as f:
            f.write(uploaded.getbuffer())

        # Predict Button
        if st.button("Predict Disease"):
            model_path = get_model_path(model_choice)
            label, conf = prediction_service.predict(model_path, "temp.jpg")

            # Disease Result
            st.markdown(
                f"""
                <div style="
                    background-color:#e9fbe9;
                    padding:15px;
                    border-radius:8px;
                    font-size:15px;
                    font-weight:600;
                ">
                🦠 Disease: {label}
                </div>
                """,
                unsafe_allow_html=True
            )

            st.markdown("<br>", unsafe_allow_html=True)

            # Confidence Result
            st.markdown(
                f"""
                <div style="
                    background-color:#eaf3ff;
                    padding:15px;
                    border-radius:8px;
                    font-size:15px;
                    font-weight:600;
                ">
                🎯 Confidence: {conf:.2f}%
                </div>
                """,
                unsafe_allow_html=True
            )


# ---------- CHATBOT ASSISTANCE ----------
elif page == "Chatbot Assistance":

    st.title("🤖 Crop AI Assistant")

    # Center layout using columns
    left, center, right = st.columns([1, 2, 1])

    with center:
        botpress_html = """
        <script src="https://cdn.botpress.cloud/webchat/v3.5/inject.js"></script>

        <style>
          #webchat {
            width: 100%;
            height: 600px;
            border-radius: 12px;
            box-shadow: 0px 4px 15px rgba(0,0,0,0.15);
          }

          #webchat .bpWebchat {
            position: unset;
            width: 100%;
            height: 100%;
            max-height: 100%;
          }

          #webchat .bpFab {
            display: none;
          }
        </style>

        <div id="webchat"></div>

        <script>
          window.botpress.on("webchat:ready", () => {
            window.botpress.open();
          });

          window.botpress.init({
            botId: "ad6b7fa2-df6c-42c3-92ec-5c681410ba53",
            clientId: "5d6de969-9800-4318-8252-809d1d182916",
            selector: "#webchat",
            configuration: {
              themeMode: "light",
              color: "#3276EA",
              hideWidget: true
            }
          });
        </script>
        """

        st.components.v1.html(botpress_html, height=650)
