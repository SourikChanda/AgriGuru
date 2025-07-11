import streamlit as st
import requests

# Set page config
st.set_page_config(page_title="AgriGuru Multilingual", layout="centered")

# Supported languages
languages = {
    "English": "en",
    "Hindi": "hi",
    "Bengali": "bn",
    "Tamil": "ta"
}

language = st.selectbox("🌐 Select Language / भाषा चुनें", list(languages.keys()))
target_lang = languages[language]


# LibreTranslate API Function
def libre_translate(text, target_lang):
    if target_lang == "en":  # No need to translate English
        return text
    try:
        response = requests.post(
            "https://libretranslate.de/translate",
            data={
                "q": text,
                "source": "en",
                "target": target_lang,
                "format": "text"
            }
        )
        if response.status_code == 200:
            return response.json()["translatedText"]
        else:
            return text  # Fallback to original
    except:
        return text


# UI texts to translate
ui_texts = {
    "weather_title": "🌦️ Weather Forecast",
    "enter_city": "Enter your District/City",
    "fetch_error": "Could not fetch weather. Please check the name.",
    "crop_title": "🧠 Rule-Based Crop Recommendation",
    "select_season": "Select Crop Season",
    "select_soil": "Select Soil Type",
    "recommendation": "Recommended Crops",
    "title": "🌾 AgriGuru – Smart Farming Assistant"
}

# Translate UI text dynamically
t = {key: libre_translate(val, target_lang) for key, val in ui_texts.items()}

# Page content
st.title(t["title"])
st.subheader(t["weather_title"])

# 🔑 Weather API Key
api_key = "0a16832edf4445ce698396f2fa890ddd"  # Replace with your OpenWeatherMap key

city = st.text_input(t["enter_city"])

def get_weather(city_name):
    try:
        url = f"http://api.openweathermap.org/data/2.5/forecast?q={city_name},IN&appid={api_key}&units=metric"
        res = requests.get(url)
        if res.status_code == 200:
            data = res.json()
            return data['list'][:5]
        else:
            return None
    except Exception as e:
        return None

if city:
    weather_data = get_weather(city)
    if weather_data:
        for entry in weather_data:
            date = entry['dt_txt']
            temp = entry['main']['temp']
            desc = entry['weather'][0]['description'].capitalize()
            st.write(f"{date} | 🌡️ {temp}°C | {desc}")
    else:
        st.warning(t["fetch_error"])


# ---------- Rule-Based Crop Recommendation ----------
st.subheader(t["crop_title"])

# Season and Soil options (translated)
season_options = {
    "Kharif": libre_translate("Kharif", target_lang),
    "Rabi": libre_translate("Rabi", target_lang),
    "Zaid": libre_translate("Zaid", target_lang)
}

soil_options = {
    "Alluvial": libre_translate("Alluvial", target_lang),
    "Black": libre_translate("Black", target_lang),
    "Red": libre_translate("Red", target_lang),
    "Laterite": libre_translate("Laterite", target_lang),
    "Sandy": libre_translate("Sandy", target_lang),
    "Clayey": libre_translate("Clayey", target_lang)
}

season = st.selectbox(t["select_season"], list(season_options.values()))
soil = st.selectbox(t["select_soil"], list(soil_options.values()))

# Reverse mapping for logic
rev_season = {v: k for k, v in season_options.items()}
rev_soil = {v: k for k, v in soil_options.items()}

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
    eng_season = rev_season.get(season)
    eng_soil = rev_soil.get(soil)
    crops = recommend_crops(eng_season, eng_soil)
    translated_crops = [libre_translate(crop, target_lang) for crop in crops]
    st.success(t["recommendation"] + ": " + ", ".join(translated_crops))
