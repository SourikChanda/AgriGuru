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
        if res.status_code == 200:
            return res.json()['list'][:5]
        else:
            return None
    except:
        return None

if city:
    data = get_weather(city)
    if data:
        for entry in data:
            date = entry['dt_txt']
            temp = entry['main']['temp']
            desc = libre_translate(entry['weather'][0]['description'].capitalize(), target_lang)
            st.write(f"{date} | 🌡️ {temp}°C | {desc}")
    else:
        st.warning(t["fetch_error"])

# Crop Recommendation
st.subheader(t["crop_title"])

# Dropdowns (translated)
season_labels = {
    "Kharif": libre_translate("Kharif", target_lang),
    "Rabi": libre_translate("Rabi", target_lang),
    "Zaid": libre_translate("Zaid", target_lang)
}
soil_labels = {
    "Alluvial": libre_translate("Alluvial", target_lang),
    "Black": libre_translate("Black", target_lang),
    "Red": libre_translate("Red", target_lang),
    "Laterite": libre_translate("Laterite", target_lang),
    "Sandy": libre_translate("Sandy", target_lang),
    "Clayey": libre_translate("Clayey", target_lang)
}

season = st.selectbox(t["select_season"], list(season_labels.values()))
soil = st.selectbox(t["select_soil"], list(soil_labels.values()))

# Reverse lookup
rev_season = {v: k for k, v in season_labels.items()}
rev_soil = {v: k for k, v in soil_labels.items()}

def recommend_crops(season, soil):
    if season == "Kharif" and soil == "Alluvial":
        return ["Paddy", "Maize", "Jute"]
    elif season == "Rabi" and soil == "Black":
        return ["Wheat", "Barley", "Gram"]
    elif season == "Zaid":
        return ["Watermelon", "Cucumber", "Bitter Gourd"]
    else:
        return ["Millets", "Pulses", "Sunflower"]

if season and soil:
    crops = recommend_crops(rev_season[season], rev_soil[soil])
    translated_crops = [libre_translate(crop, target_lang) for crop in crops]
    st.success(t["recommendation"] + ": " + ", ".join(translated_crops))
