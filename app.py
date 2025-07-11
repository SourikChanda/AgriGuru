import streamlit as st
import requests

# Set page config
st.set_page_config(page_title="AgriGuru Multilingual", layout="centered")

# 🌐 Language selector first
language = st.selectbox("🌐 Select Language / भाषा चुनें", ["English", "Hindi", "Bengali", "Tamil"])

# ---- Translation Dictionary ----
texts = {
    "English": {
        "title": "🌾 AgriGuru – Smart Farming Assistant",
        "weather_title": "🌦️ Weather Forecast",
        "enter_city": "Enter your District/City",
        "fetch_error": "Could not fetch weather. Please check the name.",
        "crop_title": "🧠 Rule-Based Crop Recommendation",
        "select_season": "Select Crop Season",
        "select_soil": "Select Soil Type",
        "recommendation": "Recommended Crops"
    },
    "Hindi": {
        "title": "🌾 AgriGuru – स्मार्ट खेती सहायक",
        "weather_title": "🌦️ मौसम पूर्वानुमान",
        "enter_city": "अपना जिला/शहर दर्ज करें",
        "fetch_error": "मौसम डेटा प्राप्त नहीं हो सका। कृपया नाम जांचें।",
        "crop_title": "🧠 नियम आधारित फसल सिफारिश",
        "select_season": "फसल का मौसम चुनें",
        "select_soil": "मिट्टी का प्रकार चुनें",
        "recommendation": "अनुशंसित फसलें"
    },
    "Bengali": {
        "title": "🌾 AgriGuru – স্মার্ট কৃষি সহকারী",
        "weather_title": "🌦️ আবহাওয়ার পূর্বাভাস",
        "enter_city": "আপনার জেলা/শহরের নাম লিখুন",
        "fetch_error": "আবহাওয়া পাওয়া যায়নি। নাম চেক করুন।",
        "crop_title": "🧠 নিয়মভিত্তিক ফসল সুপারিশ",
        "select_season": "ফসলের ঋতু নির্বাচন করুন",
        "select_soil": "মাটির ধরন নির্বাচন করুন",
        "recommendation": "সুপারিশকৃত ফসল"
    },
    "Tamil": {
        "title": "🌾 AgriGuru – ஸ்மார்ட் விவசாய உதவியாளர்",
        "weather_title": "🌦️ வானிலை முன்னறிவு",
        "enter_city": "உங்கள் மாவட்டம்/நகரத்தை உள்ளிடவும்",
        "fetch_error": "வானிலை பெற முடியவில்லை. நகரப்பெயரை சரிபார்க்கவும்.",
        "crop_title": "🧠 விதிமுறை அடிப்படையிலான பயிர் பரிந்துரை",
        "select_season": "பயிர் பருவத்தை தேர்வு செய்க",
        "select_soil": "மண்ணின் வகையை தேர்வு செய்க",
        "recommendation": "பரிந்துரைக்கப்பட்ட பயிர்கள்"
    }
}

t = texts[language]  # selected translation

# ---------- Title ----------
st.title(t["title"])

# ---------- Weather Section ----------
st.subheader(t["weather_title"])
api_key = "your_openweathermap_api_key"  # Replace with your API key
city = st.text_input(t["enter_city"])

def get_weather(city):
    url = f"http://api.openweathermap.org/data/2.5/forecast?q={city},IN&appid={api_key}&units=metric"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()['list'][:5]  # 5 records (~1 per day)
    else:
        return None

if city:
    data = get_weather(city)
    if data:
        for entry in data:
            dt = entry["dt_txt"]
            temp = entry["main"]["temp"]
            desc = entry["weather"][0]["description"]
            st.write(f"{dt} | 🌡️ {temp}°C | {desc}")
    else:
        st.warning(t["fetch_error"])

# ---------- Rule-Based Crop Recommendation ----------
st.subheader(t["crop_title"])

seasons = {
    "English": ["Kharif", "Rabi", "Zaid"],
    "Hindi": ["खरीफ", "रबी", "जायद"],
    "Bengali": ["খরিফ", "রবি", "জায়দ"],
    "Tamil": ["கரிஃப்", "ரபி", "சாயித்"]
}
soils = {
    "English": ["Alluvial", "Black", "Red", "Laterite", "Sandy", "Clayey"],
    "Hindi": ["जलोढ़", "काली", "लाल", "लेटेराइट", "बलुई", "मिट्टीदार"],
    "Bengali": ["পলিমাটি", "কালো", "লাল", "ল্যাটেরাইট", "বেলে", "কাদাযুক্ত"],
    "Tamil": ["ஆலுவியல்", "கருப்பு", "சிவப்பு", "லேட்டரைட்", "மணல்", "களிமண்"]
}

season = st.selectbox(t["select_season"], seasons[language])
soil = st.selectbox(t["select_soil"], soils[language])

def recommend_crops(season, soil):
    if season in ["Kharif", "खरीफ", "খরিফ", "கரிஃப்"] and soil in ["Alluvial", "जलोढ़", "পলিমাটি", "ஆலுவியல்"]:
        return ["Paddy", "Maize", "Jute"]
    elif season in ["Rabi", "रबी", "রবি", "ரபி"] and soil in ["Black", "काली", "কালো", "கருப்பு"]:
        return ["Wheat", "Barley", "Gram"]
    elif season in ["Zaid", "जायद", "জায়দ", "சாயித்"]:
        return ["Watermelon", "Cucumber", "Bitter Gourd"]
    else:
        return ["Millets", "Pulses", "Sunflower"]

if season and soil:
    crops = recommend_crops(season, soil)
    st.success(t["recommendation"] + ": " + ", ".join(crops))
