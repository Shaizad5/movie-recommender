import streamlit as st
import requests
from datetime import datetime
import pandas as pd

# ================= CONFIG =================
API_BASE = "https://movie-recommender-1-eopi.onrender.com"
TMDB_IMG = "https://image.tmdb.org/t/p/w500"

st.set_page_config(page_title="CineScope", layout="wide")

# ================= MULTILINGUAL =================
LANG = {
    "English": {
        "login":"Login","create":"Create Account","search":"Search",
        "watchlist":"Watchlist","profile":"Profile","analytics":"Analytics",
        "mood":"Mood","rate":"Rate","review":"Review",
        "save_rating":"Save Rating","submit_review":"Submit Review",
        "add_watchlist":"Add to Watchlist","open":"Open",
        "view":"View","grid":"Grid","list":"List","genre":"Genre"
    },
    "Hindi": {
        "login":"लॉगिन","create":"खाता बनाएं","search":"खोजें",
        "watchlist":"वॉचलिस्ट","profile":"प्रोफाइल","analytics":"एनालिटिक्स",
        "mood":"मूड","rate":"रेट","review":"समीक्षा",
        "save_rating":"रेट सेव करें","submit_review":"समीक्षा भेजें",
        "add_watchlist":"वॉचलिस्ट में जोड़ें","open":"खोलें",
        "view":"देखें","grid":"ग्रिड","list":"सूची","genre":"शैली"
    },
    "Telugu": {
        "login":"లాగిన్","create":"ఖాతా సృష్టించండి","search":"వెతకండి",
        "watchlist":"వాచ్‌లిస్ట్","profile":"ప్రొఫైల్","analytics":"విశ్లేషణ",
        "mood":"మూడ్","rate":"రేట్","review":"రివ్యూ",
        "save_rating":"రేటింగ్ సేవ్ చేయండి","submit_review":"రివ్యూ పంపండి",
        "add_watchlist":"వాచ్‌లిస్ట్‌లో జోడించండి","open":"తెరవండి",
        "view":"వీక్షణ","grid":"గ్రిడ్","list":"జాబితా","genre":"జానర్"
    },
    "Arabic": {
        "login":"تسجيل الدخول","create":"إنشاء حساب","search":"بحث",
        "watchlist":"قائمة المشاهدة","profile":"الملف","analytics":"تحليلات",
        "mood":"مزاج","rate":"تقييم","review":"مراجعة",
        "save_rating":"حفظ التقييم","submit_review":"إرسال مراجعة",
        "add_watchlist":"إضافة للقائمة","open":"فتح",
        "view":"عرض","grid":"شبكة","list":"قائمة","genre":"النوع"
    }
}

lang = st.sidebar.selectbox("🌐 Language", list(LANG.keys()))
T = LANG[lang]

# ================= LOGIN =================
if "users" not in st.session_state:
    st.session_state.users = {}

if "logged" not in st.session_state:
    st.session_state.logged = False

if not st.session_state.logged:
    st.title("🔐 " + T["login"])
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")

    if st.button(T["login"]):
        if email in st.session_state.users and st.session_state.users[email] == password:
            st.session_state.logged = True
            st.session_state.username = email
            st.rerun()
        else:
            st.error("Invalid credentials")

    if st.button(T["create"]):
        st.session_state.users[email] = password
        st.success("Account created")

    st.stop()

# ================= SESSION =================
if "watchlist" not in st.session_state:
    st.session_state.watchlist = []
if "ratings" not in st.session_state:
    st.session_state.ratings = {}
if "reviews" not in st.session_state:
    st.session_state.reviews = {}

# ================= API =================
def fetch_movies(q):
    try:
        r = requests.get(f"{API_BASE}/tmdb/search", params={"query": q})
        return r.json().get("results", [])
    except:
        return []

# ================= NAV =================
menu = st.sidebar.radio("Menu", ["Home", T["mood"], T["genre"], T["watchlist"], T["profile"], T["analytics"]])

# ================= HOME =================
if menu == "Home":
    st.title("🎬 CineScope")
    query = st.text_input(T["search"])

    if query:
        movies = fetch_movies(query)
        cols = st.columns(5)

        for i, m in enumerate(movies[:10]):
            with cols[i % 5]:
                if m.get("poster_path"):
                    st.image(TMDB_IMG + m["poster_path"])
                st.write(m["title"])

                if st.button(T["open"] + f" {i}"):
                    st.session_state.selected = m

# ================= DETAILS =================
if "selected" in st.session_state:
    m = st.session_state.selected

    st.header(m["title"])
    if m.get("poster_path"):
        st.image(TMDB_IMG + m["poster_path"], width=200)

    st.write(m.get("overview", ""))

    rating = st.slider(T["rate"], 1, 5)
    if st.button(T["save_rating"]):
        st.session_state.ratings[m["id"]] = rating

    review = st.text_area(T["review"])
    if st.button(T["submit_review"]):
        st.session_state.reviews.setdefault(m["id"], []).append({
            "user": st.session_state.username,
            "text": review,
            "date": datetime.now().strftime("%d %b %Y")
        })

    if m["id"] in st.session_state.reviews:
        for r in st.session_state.reviews[m["id"]]:
            st.write(f"{r['user']} ({r['date']}): {r['text']}")

    if st.button(T["add_watchlist"]):
        st.session_state.watchlist.append({
            "title": m["title"],
            "poster": m.get("poster_path"),
            "date": datetime.now().strftime("%d %b %Y"),
            "genre": "General"
        })

# ================= MOOD =================
elif menu == T["mood"]:
    moods = {
        "Feel-Good": "comedy",
        "Thriller": "thriller",
        "Romantic": "romance",
        "Adventure": "action",
        "Emotional": "drama",
        "Mind-bending": "sci-fi"
    }
    mood = st.selectbox(T["mood"], list(moods.keys()))
    movies = fetch_movies(moods[mood])
    for m in movies[:10]:
        st.write(m["title"])

# ================= GENRE =================
elif menu == T["genre"]:
    genres = ["Action","Comedy","Drama","Romance","Sci-Fi","Thriller"]
    g = st.selectbox(T["genre"], genres)
    movies = fetch_movies(g)
    for m in movies[:10]:
        st.write(m["title"])

# ================= WATCHLIST =================
elif menu == T["watchlist"]:
    st.title(T["watchlist"])
    view = st.radio(T["view"], [T["grid"], T["list"]])

    if view == T["list"]:
        for w in st.session_state.watchlist:
            st.write(w["title"], "-", w["date"], "-", w["genre"])
    else:
        cols = st.columns(5)
        for i, w in enumerate(st.session_state.watchlist):
            with cols[i % 5]:
                if w["poster"]:
                    st.image(TMDB_IMG + w["poster"])
                st.write(w["title"])

# ================= PROFILE =================
elif menu == T["profile"]:
    st.title(T["profile"])
    st.write("User:", st.session_state.username)
    st.write("Ratings:", st.session_state.ratings)
    st.write("Reviews:", st.session_state.reviews)

# ================= ANALYTICS =================
elif menu == T["analytics"]:
    st.title("📊 " + T["analytics"])

    if st.session_state.ratings:
        df = pd.DataFrame({"Ratings": list(st.session_state.ratings.values())})
        st.bar_chart(df)

    st.write("Watchlist:", len(st.session_state.watchlist))
