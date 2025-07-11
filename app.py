import streamlit as st
import pandas as pd
import requests
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
from deep_translator import GoogleTranslator

# Language translation setup
languages = {
    "English": "en",
    "Hindi": "hi",
    "Bengali": "bn",
    "Marathi": "mr",
    "Tamil": "ta"
}

st.set_page_config(page_title="AgriGuru Lite", layout="centered")

# 🌐 Language selection
selected_lang = st.selectbox("🌐 Select Language", list(languages.keys()))
target_lang = languages[selected_lang]

# Translation function: translate **any** text from auto-detected source to target_lang
def _(text):
    if target_lang == "en":
        return text
    try:
        return GoogleTranslator(source='auto', target=target_lang).translate(text)
    except Exception:
        return text

# Translate input text *from user language* to English for internal processing
def to_english(text):
    if target_lang == "en":
        return text
    try:
        return GoogleTranslator(source=target_lang, target='en').translate(text)
    except Exception:
        return text

st.title(_("🌾 AgriGuru Lite – Smart Farming Assistant"))

# ---------------- LOAD PRODUCTION DATA ----------------
@st.cache_data
def load_production_data():
    return pd.read_csv("crop_production.csv")

try:
    prod_df = load_production_data()

    # For selectboxes, show values in user language but keep English for processing
    # So we translate the options to target_lang for display

    # Get unique states in English
    unique_states_en = prod_df["State_Name"].dropna().unique()

    # Translate states to user language for display
    states_display = [_(state) for state in unique_states_en]

    # User selects displayed state name
    state_display_selected = st.selectbox(_("🌍 Select State"), states_display)
    # Translate back to English
    state_selected_en = to_english(state_display_selected)

    # Filter districts for the selected state (English)
    districts_en = prod_df[prod_df["State_Name"] == state_selected_en]["District_Name"].dropna().unique()
    districts_display = [_(district) for district in districts_en]
    district_display_selected = st.selectbox(_("🏞️ Select District"), districts_display)
    district_selected_en = to_english(district_display_selected)

    # Seasons
    seasons_en = prod_df["Season"].dropna().unique()
    seasons_display = [_(season) for season in seasons_en]
    season_display_selected = st.selectbox(_("🗓️ Select Season"), seasons_display)
    season_selected_en = to_english(season_display_selected)

    st.markdown(f"### 📍 {_('Selected Region')}: **{district_display_selected}, {state_display_selected}** | {_('Season')}: **{season_display_selected}**")

except FileNotFoundError:
    st.warning(_("Please upload `crop_production.csv`."))


# ---------------- WEATHER FORECAST ----------------
st.subheader(_("🌦️ 5-Day Weather Forecast"))
weather_api_key = "0a16832edf4445ce698396f2fa890ddd"

def get_weather(city):
    url = f"http://api.openweathermap.org/data/2.5/forecast?q={city}&appid={weather_api_key}&units=metric"
    res = requests.get(url)
    if res.status_code == 200:
        return res.json()['list'][:5]
    return None
district_to_city = {
    "MALDAH": "Malda",
    "BARDHAMAN": "Bardhaman",
    "NADIA": "Krishnanagar",
    "24 PARAGANAS NORTH": "Barasat",
    "24 PARAGANAS SOUTH": "Diamond Harbour",
    "HOWRAH": "Howrah",
    "KOLKATA": "Kolkata"
}
if district_selected_en:
    city = district_to_city.get(district_selected_en.upper(), district_selected_en)
    city_query= GoogleTranslator(source='auto', target='en').translate(city)
    forecast = get_weather(city_query)
    if forecast:
        for day in forecast:
            # Translate weather description to user language
            description_translated = _(day['weather'][0]['description'])
            st.write(f"{day['dt_txt']} | 🌡️ {day['main']['temp']}°C | {description_translated}")
    else:
        st.warning(_("⚠️ Weather unavailable. Try entering a nearby city manually."))

# ---------------- SOIL TYPE BUTTONS ----------------
st.subheader(_("🧱 Explore Suitable Crops by Soil Type"))

soil_crop_map = {
    "Alluvial": ["Rice", "Sugarcane", "Wheat", "Jute"],
    "Black": ["Cotton", "Soybean", "Sorghum"],
    "Red": ["Millets", "Groundnut", "Potato"],
    "Laterite": ["Cashew", "Tea", "Tapioca"],
    "Sandy": ["Melons", "Pulses", "Groundnut"],
    "Clayey": ["Rice", "Wheat", "Lentil"],
    "Loamy": ["Maize", "Barley", "Sugarcane"]
}

soil_types = list(soil_crop_map.keys())
soil_types_display = [_(soil) for soil in soil_types]

soil_cols = st.columns(3)
for i, soil_display in enumerate(soil_types_display):
    with soil_cols[i % 3]:
        if st.button(soil_display):
            soil_key = soil_types[i]
            # Translate crop names to user language
            crops_translated = [_(crop) for crop in soil_crop_map[soil_key]]
            st.info(_("🌾 Suitable Crops: ") + ", ".join(crops_translated))

st.divider()

# ---------------- USER INPUT FOR ML ----------------
st.markdown(_("### 📥 Enter Soil and Climate Data (for ML Prediction)"))

n = st.number_input(_("Nitrogen"), min_value=0.0, key="n_input")
p = st.number_input(_("Phosphorous"), min_value=0.0, key="p_input")
k = st.number_input(_("Potassium"), min_value=0.0, key="k_input")
temp = st.number_input(_("Temperature (°C)"), min_value=0.0, key="temp_input")
humidity = st.number_input(_("Humidity (%)"), min_value=0.0, key="humidity_input")
moisture = st.number_input(_("Moisture (%)"), min_value=0.0, key="moisture_input")


# ---------------- ML MODEL: FILTERED BY DISTRICT CROPS ----------------
st.subheader(_("🌿 ML-Powered Crop Recommendation (Filtered by District)"))

@st.cache_data
def load_soil_dataset():
    df = pd.read_csv("data_core.csv")
    le = LabelEncoder()
    df["soil_encoded"] = le.fit_transform(df["Soil Type"])
    features = ["Nitrogen", "Phosphorous", "Potassium", "Temparature", "Humidity", "Moisture", "soil_encoded"]
    X = df[features]
    y = df["Crop Type"]
    model = RandomForestClassifier()
    model.fit(X, y)
    return model, le, df

try:
    soil_model, soil_encoder, soil_df = load_soil_dataset()

    # Show soil type options translated for user
    soil_types_ml = soil_df["Soil Type"].unique()
    soil_types_ml_display = [_(soil) for soil in soil_types_ml]
    soil_display_selected = st.selectbox(_("🧪 Select Soil Type for ML"), soil_types_ml_display)
    soil_selected_en = to_english(soil_display_selected)

    if st.button(_("Predict Best Crops in District")):
        encoded_soil = soil_encoder.transform([soil_selected_en])[0]
        input_data = [[n, p, k, temp, humidity, moisture, encoded_soil]]

        # Get all unique crops from the district in English
        district_crops = prod_df[
            (prod_df["District_Name"] == district_selected_en) &
            (prod_df["State_Name"] == state_selected_en)
        ]["Crop"].dropna().unique()

        # Get ML predicted probabilities for all crops
        proba = soil_model.predict_proba(input_data)[0]
        labels = soil_model.classes_
        crop_scores = {label: prob for label, prob in zip(labels, proba)}

        # Sort only crops grown in district
        recommended = [(crop, crop_scores[crop]) for crop in district_crops if crop in crop_scores]
        recommended = sorted(recommended, key=lambda x: x[1], reverse=True)[:5]

        if recommended:
            st.success(_("✅ Top Recommended Crops Grown in Your District:"))
            for crop, score in recommended:
                # Translate crop name to user language
                crop_translated = _(crop)
                st.write(f"🌱 **{crop_translated}** – " + _("Confidence: ") + f"{score:.2f}")
        else:
            st.warning(_("❌ No matching crops from prediction found in this district."))

except FileNotFoundError:
    st.warning(_("Please upload `data_core.csv`."))
