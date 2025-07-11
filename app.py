
st.set_page_config(page_title="AgriGuru Lite", layout="centered")
st.title("🌾 AgriGuru Lite – Smart Farming Assistant")

lang = st.selectbox("🌐 Choose Your Language / अपनी भाषा चुनें", list(translations.keys()))
t = translations[lang]  # Select appropriate translation set
st.set_page_config(page_title="AgriGuru Lite", layout="centered")

# 🔤 Language Selector (first input)
lang = st.selectbox("🌐 Choose Language / भाषा चुनें", ["English", "Hindi"])

# 📦 Load Data
@st.cache_data
def load_crop_data():
    return pd.read_csv("Crop_recommendation.csv")

df = load_crop_data()
X = df.drop("label", axis=1)
y = df["label"]
model = RandomForestClassifier()
model.fit(X, y)




# ---------------- WEATHER FORECAST ----------------
if lang == "English":
    st.title("🌾 AgriGuru Lite – Smart Farming Assistant")
    st.subheader("🌦️ 5-Day Weather Forecast")
    api_key = "0a16832edf4445ce698396f2fa890ddd"  # Replace with your OpenWeatherMap API Key
elif lang == "Hindi":
    st.title("🌾 AgriGuru Lite – स्मार्ट फार्मिंग सहायक")
    st.subheader("🌦️ 5-दिन का मौसम पूर्वानुमान")
location = st.text_input("Enter your City/District (for weather)")

def get_weather(city):
    url = f"http://api.openweathermap.org/data/2.5/forecast?q={city}&appid={api_key}&units=metric"
    res = requests.get(url)
    if res.status_code == 200:
        return res.json()['list'][:5]
    return None

if location:
    forecast = get_weather(location)
    if forecast:
        for day in forecast:
            st.write(f"{day['dt_txt']} | 🌡️ {day['main']['temp']}°C | {day['weather'][0]['description']}")
    else:
        st.warning("Couldn't fetch weather. Please check the city name.")

# ---------------- RULE-BASED CROP RECOMMENDATION ----------------
st.subheader("🧠 Rule-Based Crop Recommendation")

season = st.selectbox("Select the Crop Season", ["Kharif", "Rabi", "Zaid"])
soil = st.selectbox("Select Soil Type", ["Alluvial", "Black", "Red", "Laterite", "Sandy", "Clayey"])

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
    rule_based = recommend_crops(season, soil)
    st.success("Recommended Crops: " + ", ".join(rule_based))

# ---------------- ML-BASED CROP RECOMMENDATION ----------------
st.subheader("🤖 ML-Based Crop Recommendation (via CSV + Random Forest)")

@st.cache_data
def load_crop_data():
    return pd.read_csv("Crop_recommendation.csv")

df = load_crop_data()

X = df.drop("label", axis=1)
y = df["label"]

model = RandomForestClassifier()
model.fit(X, y)

# Crop-to-Season Mapping
crop_seasons = {
    "rice": "Kharif", "maize": "Kharif", "jute": "Kharif", "cotton": "Kharif",
    "kidneybeans": "Kharif", "pigeonpeas": "Kharif", "blackgram": "Kharif", 
    "mothbeans": "Kharif", "mungbean": "Kharif",

    "wheat": "Rabi", "gram": "Rabi", "lentil": "Rabi", "chickpea": "Rabi",
    "grapes": "Rabi", "apple": "Rabi", "orange": "Rabi", "pomegranate": "Rabi",

    "watermelon": "Zaid", "muskmelon": "Zaid", "cucumber": "Zaid",

    "banana": "All Season", "mango": "All Season", "papaya": "All Season",
    "coconut": "All Season", "coffee": "All Season"
}

st.markdown("**Enter Soil and Climate Data for ML Prediction**")
n = st.number_input("Nitrogen (N)", min_value=0.0)
p = st.number_input("Phosphorus (P)", min_value=0.0)
k = st.number_input("Potassium (K)", min_value=0.0)
temp = st.number_input("Temperature (°C)", min_value=0.0)
humidity = st.number_input("Humidity (%)", min_value=0.0)
ph = st.number_input("Soil pH", min_value=0.0)
rainfall = st.number_input("Rainfall (mm)", min_value=0.0)

if st.button("Predict Best Crop"):
    input_data = [[n, p, k, temp, humidity, ph, rainfall]]
    prediction = model.predict(input_data)
    predicted_crop = prediction[0]
    season = crop_seasons.get(predicted_crop, "Unknown")
    st.success(f"🌱 Predicted Crop: **{predicted_crop}** ({season} season)")

# ---------------- LANGUAGE SELECTION ----------------
st.subheader("🌐 Choose Your Language")

lang_options = ["English", "Hindi"]
selected_lang = st.selectbox("Select Language", lang_options)
if st.button("Set Language"):
    st.success(f"Language set to: {selected_lang}")
if selected_lang == "Hindi":
    st.subheader("🌦️ 5-दिन का मौसम पूर्वानुमान")


