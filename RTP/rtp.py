import streamlit as st
import numpy as np
import pandas as pd
import time
import pydeck as pdk
import re
def is_valid_name(name):
    return len(name.split()) >= 2

def is_valid_email(email):
    return re.match(r"^[\w\.-]+@[\w\.-]+\.\w+$", email)

def is_valid_phone(phone):
    return phone.isdigit() and len(phone) == 10
if "app_started" not in st.session_state:
    st.session_state.app_started = False

# ---------------- OVERLAY SPLASH ----------------
if not st.session_state.app_started:
    st.markdown("""
    <style>
    .overlay {
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background: linear-gradient(270deg, #000000, #00c853, #2962ff, #d50000, #000000);
        background-size: 800% 800%;
        animation: gradientMove 6s ease infinite;
        display: flex;
        justify-content: center;
        align-items: center;
        z-index: 9999;
        color: white;
        flex-direction: column;
    }

    @keyframes gradientMove {
        0% {background-position:0% 50%;}
        50% {background-position:100% 50%;}
        100% {background-position:0% 50%;}
    }

    .title {
        font-size: 48px;
        font-weight: bold;
    }

    .subtitle {
        font-size: 20px;
        margin-top: 10px;
    }
    </style>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="overlay">
        <div class="title">🛡️ Smart Tourist Safety</div>
        <div class="subtitle">Your Safety, Our Priority 🚀</div>
    </div>
    """, unsafe_allow_html=True)

    time.sleep(2)

    st.session_state.app_started = True
    st.rerun()

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="Smart Tourist Safety System",
    page_icon="🛡️",
    layout="wide"
)
st.markdown("""
<style>

/* 🌟 Glass effect cards */
.block-container {
    background: rgba(255, 255, 255, 0.15);  /* white glass */
    padding: 20px;
    border-radius: 20px;

    backdrop-filter: blur(15px);
    -webkit-backdrop-filter: blur(15px);

    border: 1px solid rgba(255, 255, 255, 0.3); /* soft white border */
    box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3); /* subtle depth */
}

/* ✨ Buttons styling */
.stButton>button {
    background: rgba(255, 255, 255, 0.2);
    color: white;
    border-radius: 12px;
    border: 1px solid rgba(255, 255, 255, 0.4);
    padding: 10px 20px;
    font-size: 16px;
    backdrop-filter: blur(10px);
}

.stButton>button:hover {
    background: rgba(255, 255, 255, 0.35);
    transform: scale(1.05);
    transition: 0.3s;
}

/* Hover effect */
.stButton>button:hover {
    transform: scale(1.05);
    transition: 0.3s;
}

/* Titles glow */
h1, h2, h3 {
    color: #ffffff;
    text-shadow: 0px 0px 8px rgba(0, 0, 0, 0.6);
}

</style>
""", unsafe_allow_html=True)

# ---------------- BACKGROUND IMAGE (UPDATED URL) ----------------
def set_bg_url():
    st.markdown(
        """
        <style>
        .stApp {
            background-image: url("https://i.pinimg.com/1200x/ed/f3/6b/edf36bbb7e4830ac5e30596100d32934.jpg");
            background-size: cover;
            background-position: center;
            background-repeat: no-repeat;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

set_bg_url()

# ---------------- SESSION STATE ----------------
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "page" not in st.session_state:
    st.session_state.page = "login"
if "tracking" not in st.session_state:
    st.session_state.tracking = False
if "movement" not in st.session_state:
    st.session_state.movement = []
if "idle_time" not in st.session_state:
    st.session_state.idle_time = 0
if "alert" not in st.session_state:
    st.session_state.alert = False
if "alert_shown" not in st.session_state:
    st.session_state.alert_shown = False
if "app_started" not in st.session_state:
    st.session_state.app_started = False

# ---------------- SPLASH SCREEN ----------------
if not st.session_state.app_started:
    st.title("Smart Tourist Safety System")
    time.sleep(2)
    st.session_state.app_started = True
    st.rerun()

# ---------------- LOGIN ----------------
def login():
    st.title("Login")
    name = st.text_input("Full Name")
    email = st.text_input("Email")
    phone = st.text_input("Phone Number")
    country_list = [
    "India", "USA", "UK", "Canada", "Australia", "Germany", "France",
    "Japan", "China", "Brazil", "South Africa", "Russia"
]
    country = st.selectbox("Country", country_list)
    emergency = st.text_input("Emergency Contact")
    gender = st.selectbox("Gender", ["Male", "Female", "Other"])
    age = st.number_input("Age", min_value=1, max_value=100)

    if st.button("Login"):
        if not is_valid_name(name):
            st.error("Enter full name (first & last name)")
        elif not is_valid_email(email):
            st.error("Enter valid email (example123@gmail.com)")
        elif not is_valid_phone(phone):
            st.error("Enter valid 10-digit phone number")
        elif not country:
            st.error("Country is required")
        elif not is_valid_phone(emergency):
            st.error("Enter valid emergency contact number")
        else:
            st.session_state.logged_in = True
            st.session_state.page = "dashboard"
            st.rerun()

# ---------------- NAVBAR ----------------
def navbar():
    col1, col2, col3, col4, col5 = st.columns(5)

    if col1.button("📍 Live Map"):
        st.session_state.page = "map"
        st.rerun()

    if col2.button("🚨 SOS"):
        st.session_state.page = "sos"
        st.rerun()

    if col3.button("🏥 Nearby"):
        st.session_state.page = "nearby"
        st.rerun()

    if col4.button("🏠 Dashboard"):
        st.session_state.page = "dashboard"
        st.rerun()

    if col5.button("🚪 Logout"):
        st.session_state.logged_in = False
        st.session_state.page = "dashboard"   # 👈 IMPORTANT CHANGE
        st.rerun()

# ---------------- DASHBOARD ----------------
def dashboard():
    st.title("📊 Dashboard")
    navbar()
    st.write("Select a module to continue.")

# ---------------- GEO-FENCING ----------------
def check_zone(lat, lon):
    # 🔥 paste dynamic code here
    zones = []

    if lat > 17.5:
        zones.append({"name": "High Risk Area", "lat": lat, "lon": lon, "radius": 0.02})

    current_hour = time.localtime().tm_hour
    if current_hour >= 22 or current_hour <= 5:
        zones.append({"name": "Night Unsafe Zone", "lat": lat, "lon": lon, "radius": 0.03})

    if "speed_history" in st.session_state:
        if len(st.session_state.speed_history) > 3:
            if np.mean(st.session_state.speed_history) < 1:
                zones.append({"name": "Suspicious Idle Area", "lat": lat, "lon": lon, "radius": 0.01})

    for z in zones:
        dist = np.sqrt((lat - z["lat"])**2 + (lon - z["lon"])**2)
        if dist < z["radius"]:
            return False, z["name"]

    return True, "Safe Area"
#---------live map---------
def live_map():
    st.title("📍 Live Tracking")
    navbar()

    # Start / Stop buttons
    col1, col2 = st.columns(2)

    with col1:
        if st.button("▶️ Start Tracking"):
            st.session_state.tracking = True

    with col2:
        if st.button("⏹ Stop Tracking"):
            st.session_state.tracking = False

    # Default value
    if "tracking" not in st.session_state:
        st.session_state.tracking = False

    # ✅ MAIN TRACKING BLOCK (CORRECT PLACE)
    if st.session_state.tracking:

        # 📍 Random location
        lat = np.random.uniform(17.3, 17.6)
        lon = np.random.uniform(78.3, 78.6)

        # 🗺️ Map
        st.pydeck_chart(pdk.Deck(
            map_style=None,
            initial_view_state=pdk.ViewState(
                latitude=lat,
                longitude=lon,
                zoom=13,
                pitch=50,
            ),
            layers=[
                pdk.Layer(
                    "ScatterplotLayer",
                    data=pd.DataFrame({"lat":[lat], "lon":[lon]}),
                    get_position='[lon, lat]',
                    get_color='[255, 0, 0]',
                    get_radius=300,
                )
            ]
        ))

        # 📍 Coordinates
        st.write(f"📍 Location: {lat:.4f}, {lon:.4f}")

        # 🧠 GEO-FENCING
        is_safe, zone = check_zone(lat, lon)

        st.write(f"🧠 Zone Detected: **{zone}**")

        # 🚦 Risk
        risk = "🟢 SAFE"

        if "High" in zone:
            risk = "🔴 HIGH RISK"
        elif "Night" in zone:
            risk = "🟠 MEDIUM RISK"
        elif "Suspicious" in zone:
            risk = "🟡 LOW RISK"

        st.markdown(f"### 🚦 Risk Level: {risk}")

        # 🚨 Alert
        if not is_safe:
            st.error(f"⚠️ DANGER ZONE: {zone}")

            st.markdown("""
            <audio autoplay>
            <source src="https://www.soundjay.com/buttons/beep-01a.mp3" type="audio/mp3">
            </audio>
            """, unsafe_allow_html=True)

        else:
            st.success("✅ SAFE AREA")
            st.progress(np.random.randint(30, 100))
            st.caption("📡 Tracking Signal Strength")

        # 🔄 refresh
        time.sleep(2)
        st.rerun()
# ---------------- SOS ----------------
def sos():
    st.title("🚨 Emergency SOS")
    navbar()

    st.warning("⚠️ Select Emergency Type")

    # 🎯 Emergency type selection
    option = st.selectbox(
        "Choose Situation",
        ["Accident 🚑", "Crime 🚓", "Fire 🔥", "Medical Emergency 🏥", "General Help 📞"]
    )

    # 👤 Whom to alert based on situation
    if option == "Accident 🚑":
        contacts = ["Ambulance", "Hospital", "Family"]
    elif option == "Crime 🚓":
        contacts = ["Police", "Family"]
    elif option == "Fire 🔥":
        contacts = ["Fire Station", "Police"]
    elif option == "Medical Emergency 🏥":
        contacts = ["Hospital", "Ambulance", "Family"]
    else:
        contacts = ["Family", "Friends"]

    selected = st.multiselect("Send SOS To:", contacts)

    # 📍 Simulated location
    lat = np.random.uniform(17.3, 17.6)
    lon = np.random.uniform(78.3, 78.6)

    if st.button("🚨 Send SOS"):
        if selected:
            st.error("🚨 SOS ALERT SENT!")
            st.write(f"📍 Location: {lat:.4f}, {lon:.4f}")

            st.success(f"Alert sent to: {', '.join(selected)}")

            # 🗺️ Show location on map
            st.map(pd.DataFrame({"lat":[lat], "lon":[lon]}))

        else:
            st.warning("⚠️ Please select at least one contact")

# ---------------- NEARBY ----------------
def nearby():
    st.title("🏥 Nearby Services")
    navbar()

    # 📍 User location
    user_lat = np.random.uniform(17.3, 17.6)
    user_lon = np.random.uniform(78.3, 78.6)

    st.success(f"📍 Your Location: {user_lat:.4f}, {user_lon:.4f}")

    # 📊 Data
    df = pd.DataFrame({
        "Name": ["City Hospital", "Apollo Hospital", "Police Station", "Bus Stand",
                 "Hotel Paradise", "Restaurant Spice"],
        "Type": ["Hospital", "Hospital", "Police", "Bus Stand", "Hotel", "Restaurant"],
        "lat": [17.44, 17.45, 17.46, 17.47, 17.43, 17.48],
        "lon": [78.44, 78.45, 78.46, 78.47, 78.43, 78.48]
    })

    # 🎯 Filter
    option = st.selectbox(
        "Select Service",
        ["All", "Hospital", "Police", "Hotel", "Restaurant", "Bus Stand"]
    )

    if option != "All":
        df = df[df["Type"] == option]

    # 🎨 Assign colors
    def get_color(t):
        if t == "Hospital":
            return [255, 0, 0]      # Red
        elif t == "Police":
            return [0, 0, 255]      # Blue
        elif t == "Hotel":
            return [0, 255, 0]      # Green
        elif t == "Restaurant":
            return [255, 165, 0]    # Orange
        else:
            return [255, 255, 0]    # Yellow

    df["color"] = df["Type"].apply(get_color)

    # 🗺️ Layer for places
    layer = pdk.Layer(
        "ScatterplotLayer",
        data=df,
        get_position='[lon, lat]',
        get_fill_color='color',
        get_radius=200,
        pickable=True
    )

    # 📍 User location layer
    user_layer = pdk.Layer(
        "ScatterplotLayer",
        data=pd.DataFrame({"lat":[user_lat], "lon":[user_lon]}),
        get_position='[lon, lat]',
        get_fill_color='[0, 0, 0]',
        get_radius=300
    )

    # 🗺️ View
    view = pdk.ViewState(
        latitude=user_lat,
        longitude=user_lon,
        zoom=12,
        pitch=0
    )

    # 🚀 Render map
    st.pydeck_chart(pdk.Deck(
        layers=[layer, user_layer],
        initial_view_state=view,
        tooltip={"text": "{Name} ({Type})"}
    ))

    # 📋 Data
    st.write("### 📋 Nearby Places")
    st.dataframe(df)
# ---------------- MAIN ----------------
if not st.session_state.logged_in:
    login()
else:
    if st.session_state.page == "dashboard":
        dashboard()
    elif st.session_state.page == "map":
        live_map()
    elif st.session_state.page == "sos":
        sos()
    elif st.session_state.page == "nearby":
        nearby()
