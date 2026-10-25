import os
import streamlit as st
from google import genai

# 1. पेज सेटअप
st.set_page_config(
    page_title="CUSB Campus Assistant | by Ravi Arya",
    page_icon="🎓",
    layout="wide"
)

# 2. साइडबार - प्रोफाइल
with st.sidebar:
    image_file = None
    for filename in ["profile.jpg", "profile.jpeg", "profile.png", "profile.JPG", "profile.PNG"]:
        if os.path.exists(filename):
            image_file = filename
            break

    if image_file:
        st.image(image_file, width=150, caption="Ravi Arya")
    else:
        st.warning("फ़ोटो नहीं मिली! कृपया फ़ोटो का नाम 'profile.jpg' रखें।")
        st.image("https://img.icons8.com/fluency/96/user-male-circle.png", width=100)

    st.title("About Developer")
    st.markdown("""
    **Ravi Arya**  
    *M.Sc. Computer Science*  
    Department of Computer Science  
    **Central University of South Bihar (CUSB)**
    
    ---
    ### 🛠️ Project Details
    - **Bot:** CUSB Campus Assistant
    - **Tech Stack:** Python, Streamlit, Google Gemini AI
    - **Model:** gemini-2.5-flash
    
    ---
    *Built with ❤️ for CUSB Campus Community.*
    """)
    st.caption("Version 1.0 | © 2026 Ravi Arya")

# 3. मुख्य हेडर
st.title("🎓 CUSB Campus Assistant")
st.markdown("##### *Central University of South Bihar (CUSB) के लिए AI सहायक*")
st.markdown("**Developed by Ravi Arya** | Department of Computer Science, CUSB")
st.divider()

# 4. Google GenAI Client सेटअप (AQ टोकन सपोर्टेड)
api_key = st.secrets.get("GEMINI_API_KEY", "AQ.Ab8RN6Ixv-owdQ41AD1NpI-oxrctKtd7yQo6b_BI_H1pdOur9Q")
client = genai.Client(api_key=api_key)

# 5. CUSB डेटा लोड करें
try:
    with open("cusb_data.txt", "r", encoding="utf-8") as f:
        cusb_context = f.read()
except Exception:
    cusb_context = "Central University of South Bihar (CUSB), SH-7, Gaya-Panchanpur Road, Gaya, Bihar - 824236."

# 6. चैट हिस्ट्री
if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "assistant",
            "content": "नमस्ते! मैं **CUSB Campus Assistant** हूँ, जिसे **Ravi Arya** ने बनाया है। यूनिवर्सिटी, कोर्स, फीस, हॉस्टल या लोकेशन से जुड़ा कोई भी सवाल पूछें!"
        }
    ]

# पिछली बातचीत दिखाएं
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

# 7. यूज़र इनपुट और रिस्पॉन्स
prompt = st.chat_input("अपना सवाल यहाँ लिखें (उदा. M.Sc CS फीस, गया जंक्शन से दूरी, हॉस्टल)...")
if prompt:
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)

    with st.chat_message("assistant"):
        with st.spinner("उत्तर तैयार हो रहा है..."):
            full_prompt = (
                f"You are the official AI campus assistant for Central University of South Bihar (CUSB), Gaya, "
                f"developed by Ravi Arya (Department of Computer Science, CUSB).\n"
                f"Answer the student's question politely, clearly, and in detail in Hindi/Hinglish.\n\n"
                f"Context from file:\n{cusb_context}\n\n"
                f"Student Question: {prompt}\n\n"
                f"Instructions: Use the context provided above. If specific information (like transit distances from Gaya Junction ~13-15 km or complete fee breakdown) is not in the context, "
                f"use your general knowledge about CUSB to give an accurate and helpful answer. Do not give incomplete or one-line empty answers."
            )
            try:
                response = client.models.generate_content(
                    model="gemini-2.5-flash",
                    contents=full_prompt
                )
                reply = response.text
                st.write(reply)
                st.session_state.messages.append({"role": "assistant", "content": reply})
            except Exception as e:
                st.error(f"Error: {e}")
