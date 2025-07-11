import streamlit as st
import requests

# Page config
st.set_page_config(page_title="AgriGuru Multilingual", layout="centered")

# Language selector
languages = {
    "English": "en",
    "Hindi": "hi",
    "Bengali": "bn",
    "Tamil": "ta"
}
language = st.selectbox("🌐 Select Language / भाषा चुनें", list(languages.keys()))
target_lang = languages[language]

# LibreTranslate API function with better endpoint and fallback
def libre_translate(text, target_lang):
    if target_lang == "en":
        return text
    try:
        response = requests.post(
            "https://translate.argosopentech.com/translate",
            json={
                "q": text,
                "source": "en",
                "target": target_lang,
                "format": "text"
            },
            timeout=5
        )
        if response.status_code == 200:
            return response.json()["translatedText"]
        else:
            st.error(f"Translation failed with status code {response.status_code}")
            return text
    except Exception as e:
        st.error(f"Translation error: {e}")
        return text

# UI text keys
ui_texts = {
    "title": "🌾 AgriGuru – Smart Farming Assistant",
    "weather_title": "🌦️ Weather Forecast",
    "enter_city": "Enter your District/City",
    "fetch_error": "Could not fetch weather. Please check the name.",
    "crop_title": "🧠 Rule-Based Crop Recommendation",
    "select_season": "Select Crop Season",
    "select_soil": "Select Soil Type",
    "recommendation": "Recommended Crops"
}

# Translate UI text
t = {key: libre_translate(val, target_lang) for key, val in ui_texts.items()}

# UI
st.title(t["title"])
st.subheader(t["weather_title"])

# Weather input
api_key = "0a16832edf4445ce698396f2fa890ddd"  # Replace with your actual key
city = st.text_input(t["enter_city"])

def get_weather(city_name):
    try:
        url = f"http://api.openweathermap.org/data/2.5/forecast?q={city_name},IN&appid={api_key}&units=metric"
        res = requests.get(url)
        if res.status
