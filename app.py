import requests
import streamlit as st
from datetime import datetime
import random

# =============================

# CONFIG

# =============================

API_BASE = “https://movie-recommender-1-eopi.onrender.com”
TMDB_IMG = “https://image.tmdb.org/t/p/w500”

st.set_page_config(page_title=“CineScope”, page_icon=“🎬”, layout=“wide”)

# =============================

# MULTILINGUAL STRINGS

# =============================

LANG_STRINGS = {
“English”: {
“site_sub”: “Discover · Rate · Review · Watchlist”,
“search_placeholder”: “🔍  avengers, batman, love…”,
“sign_in”: “Sign In”,
“sign_up”: “Sign Up”,
“username”: “Username”,
“password”: “Password”,
“confirm_password”: “Confirm Password”,
“sign_in_btn”: “Sign In →”,
“create_account”: “Create Account →”,
“demo_hint”: “Demo → demo / demo”,
“home”: “Home”,
“mood_pick”: “Mood Pick”,
“watchlist”: “Watchlist”,
“analytics”: “Analytics”,
“profile”: “Profile”,
“sign_out”: “🚪 Sign Out”,
“home_feed”: “Home Feed”,
“category”: “Category”,
“grid_cols”: “Grid columns”,
“activity”: “Activity”,
“open”: “Open →”,
“back_home”: “← Back to Home”,
“add_watchlist”: “🔖 Add to Watchlist”,
“in_watchlist”: “✅ In Watchlist”,
“recommendations”: “✅ Recommendations”,
“rate_review”: “⭐ Rate & Review”,
“your_rating”: “Your Rating”,
“save_rating”: “💾 Save Rating”,
“write_review”: “Write a Review”,
“your_name”: “Your name”,
“stars”: “Stars”,
“review_placeholder”: “Share your thoughts…”,
“submit_review”: “📝 Submit Review”,
“no_reviews”: “No reviews yet. Be the first! 🎬”,
“similar_movies”: “🔎 Similar Movies”,
“more_genre”: “🎭 More in Genre”,
“mood_title”: “🎯 Mood-Based Recommender”,
“mood_subtitle”: “How are you feeling today? We’ll find the perfect movies.”,
“pick”: “Pick”,
“watchlist_title”: “🔖 My Watchlist”,
“watchlist_empty”: “Watchlist is empty”,
“watchlist_hint”: “Open any movie → click 🔖 Add to Watchlist”,
“clear_watchlist”: “🗑️ Clear Watchlist”,
“view”: “View”,
“grid”: “Grid”,
“list”: “List”,
“added”: “Added”,
“analytics_title”: “📊 Analytics Dashboard”,
“movies_rated”: “Movies Rated”,
“reviews”: “Reviews”,
“avg_rating”: “Avg Rating”,
“ratings_dist”: “⭐ Ratings Distribution”,
“genre_breakdown”: “🎭 Genre Breakdown”,
“rate_to_see”: “Rate movies to see your chart”,
“add_to_see”: “Add movies to see genre breakdown”,
“trending”: “📈 Trending Movies”,
“simulated”: “Simulated popularity trend”,
“recent_reviews”: “📝 Recent Reviews”,
“no_reviews_yet”: “No reviews yet.”,
“profile_title”: “👤 My Profile”,
“member_since”: “Member since”,
“rated”: “Rated”,
“top_rated”: “🏆 Top Rated”,
“no_ratings”: “Rate movies to build your profile!”,
“wrong_credentials”: “Wrong username or password.”,
“enter_username”: “Enter a username.”,
“username_taken”: “Username taken.”,
“passwords_no_match”: “Passwords don’t match.”,
“password_short”: “Password too short.”,
“enter_name”: “Enter your name.”,
“write_something”: “Write something.”,
“review_submitted”: “Review submitted! 🎉”,
“rating_saved”: “Saved”,
“min”: “min”,
“votes”: “votes”,
“language”: “Language”,
“search_results”: “results for”,
“movie_explorer”: “Movie Explorer”,
“no_movie_selected”: “No movie selected.”,
},
“हिन्दी”: {
“site_sub”: “खोजें · रेट करें · समीक्षा करें · वॉचलिस्ट”,
“search_placeholder”: “🔍  अवेंजर्स, बैटमैन, प्यार…”,
“sign_in”: “साइन इन”,
“sign_up”: “साइन अप”,
“username”: “उपयोगकर्ता नाम”,
“password”: “पासवर्ड”,
“confirm_password”: “पासवर्ड की पुष्टि करें”,
“sign_in_btn”: “साइन इन →”,
“create_account”: “खाता बनाएं →”,
“demo_hint”: “डेमो → demo / demo”,
“home”: “होम”,
“mood_pick”: “मूड पिक”,
“watchlist”: “वॉचलिस्ट”,
“analytics”: “विश्लेषण”,
“profile”: “प्रोफाइल”,
“sign_out”: “🚪 साइन आउट”,
“home_feed”: “होम फ़ीड”,
“category”: “श्रेणी”,
“grid_cols”: “ग्रिड कॉलम”,
“activity”: “गतिविधि”,
“open”: “खोलें →”,
“back_home”: “← होम पर वापस”,
“add_watchlist”: “🔖 वॉचलिस्ट में जोड़ें”,
“in_watchlist”: “✅ वॉचलिस्ट में है”,
“recommendations”: “✅ सिफारिशें”,
“rate_review”: “⭐ रेट और समीक्षा”,
“your_rating”: “आपकी रेटिंग”,
“save_rating”: “💾 रेटिंग सहेजें”,
“write_review”: “समीक्षा लिखें”,
“your_name”: “आपका नाम”,
“stars”: “तारे”,
“review_placeholder”: “अपने विचार साझा करें…”,
“submit_review”: “📝 समीक्षा जमा करें”,
“no_reviews”: “अभी तक कोई समीक्षा नहीं। पहले बनें! 🎬”,
“similar_movies”: “🔎 समान फिल्में”,
“more_genre”: “🎭 इस शैली में और”,
“mood_title”: “🎯 मूड आधारित सिफारिशकर्ता”,
“mood_subtitle”: “आज आप कैसा महसूस कर रहे हैं? हम सही फिल्में ढूंढेंगे।”,
“pick”: “चुनें”,
“watchlist_title”: “🔖 मेरी वॉचलिस्ट”,
“watchlist_empty”: “वॉचलिस्ट खाली है”,
“watchlist_hint”: “कोई फिल्म खोलें → 🔖 पर क्लिक करें”,
“clear_watchlist”: “🗑️ वॉचलिस्ट साफ़ करें”,
“view”: “दृश्य”,
“grid”: “ग्रिड”,
“list”: “सूची”,
“added”: “जोड़ा गया”,
“analytics_title”: “📊 विश्लेषण डैशबोर्ड”,
“movies_rated”: “रेट की गई फिल्में”,
“reviews”: “समीक्षाएं”,
“avg_rating”: “औसत रेटिंग”,
“ratings_dist”: “⭐ रेटिंग वितरण”,
“genre_breakdown”: “🎭 शैली विश्लेषण”,
“rate_to_see”: “चार्ट देखने के लिए फिल्में रेट करें”,
“add_to_see”: “शैली विश्लेषण के लिए फिल्में जोड़ें”,
“trending”: “📈 ट्रेंडिंग फिल्में”,
“simulated”: “अनुमानित लोकप्रियता”,
“recent_reviews”: “📝 हालिया समीक्षाएं”,
“no_reviews_yet”: “अभी तक कोई समीक्षा नहीं।”,
“profile_title”: “👤 मेरी प्रोफाइल”,
“member_since”: “सदस्य बने”,
“rated”: “रेट किया”,
“top_rated”: “🏆 सर्वश्रेष्ठ रेटेड”,
“no_ratings”: “अपनी प्रोफाइल बनाने के लिए फिल्में रेट करें!”,
“wrong_credentials”: “गलत उपयोगकर्ता नाम या पासवर्ड।”,
“enter_username”: “उपयोगकर्ता नाम दर्ज करें।”,
“username_taken”: “उपयोगकर्ता नाम पहले से लिया गया है।”,
“passwords_no_match”: “पासवर्ड मेल नहीं खाते।”,
“password_short”: “पासवर्ड बहुत छोटा है।”,
“enter_name”: “अपना नाम दर्ज करें।”,
“write_something”: “कुछ लिखें।”,
“review_submitted”: “समीक्षा जमा की गई! 🎉”,
“rating_saved”: “सहेजा गया”,
“min”: “मिनट”,
“votes”: “वोट”,
“language”: “भाषा”,
“search_results”: “परिणाम”,
“movie_explorer”: “मूवी एक्सप्लोरर”,
“no_movie_selected”: “कोई फिल्म नहीं चुनी गई।”,
},
“తెలుగు”: {
“site_sub”: “కనుగొనండి · రేట్ చేయండి · సమీక్షించండి · వాచ్‌లిస్ట్”,
“search_placeholder”: “🔍  అవెంజర్స్, బ్యాట్‌మ్యాన్…”,
“sign_in”: “సైన్ ఇన్”,
“sign_up”: “సైన్ అప్”,
“username”: “వినియోగదారు పేరు”,
“password”: “పాస్‌వర్డ్”,
“confirm_password”: “పాస్‌వర్డ్ నిర్ధారించండి”,
“sign_in_btn”: “సైన్ ఇన్ →”,
“create_account”: “ఖాతా సృష్టించండి →”,
“demo_hint”: “డెమో → demo / demo”,
“home”: “హోమ్”,
“mood_pick”: “మూడ్ పిక్”,
“watchlist”: “వాచ్‌లిస్ట్”,
“analytics”: “విశ్లేషణ”,
“profile”: “ప్రొఫైల్”,
“sign_out”: “🚪 సైన్ అవుట్”,
“home_feed”: “హోమ్ ఫీడ్”,
“category”: “వర్గం”,
“grid_cols”: “గ్రిడ్ కాలమ్‌లు”,
“activity”: “కార్యకలాపాలు”,
“open”: “తెరవండి →”,
“back_home”: “← హోమ్‌కి తిరిగి”,
“add_watchlist”: “🔖 వాచ్‌లిస్ట్‌కి జోడించండి”,
“in_watchlist”: “✅ వాచ్‌లిస్ట్‌లో ఉంది”,
“recommendations”: “✅ సిఫార్సులు”,
“rate_review”: “⭐ రేట్ & సమీక్ష”,
“your_rating”: “మీ రేటింగ్”,
“save_rating”: “💾 రేటింగ్ సేవ్ చేయండి”,
“write_review”: “సమీక్ష రాయండి”,
“your_name”: “మీ పేరు”,
“stars”: “నక్షత్రాలు”,
“review_placeholder”: “మీ అభిప్రాయాలు పంచుకోండి…”,
“submit_review”: “📝 సమీక్ష సమర్పించండి”,
“no_reviews”: “ఇంకా సమీక్షలు లేవు. మొదటివారు అవ్వండి! 🎬”,
“similar_movies”: “🔎 సారూప్య చిత్రాలు”,
“more_genre”: “🎭 ఈ శైలిలో మరిన్ని”,
“mood_title”: “🎯 మూడ్ ఆధారిత సిఫార్సు”,
“mood_subtitle”: “ఈరోజు మీకు ఎలా అనిపిస్తుందో చెప్పండి?”,
“pick”: “ఎంచుకోండి”,
“watchlist_title”: “🔖 నా వాచ్‌లిస్ట్”,
“watchlist_empty”: “వాచ్‌లిస్ట్ ఖాళీగా ఉంది”,
“watchlist_hint”: “ఏదైనా చిత్రం తెరవండి → 🔖 క్లిక్ చేయండి”,
“clear_watchlist”: “🗑️ వాచ్‌లిస్ట్ క్లియర్ చేయండి”,
“view”: “వీక్షణ”,
“grid”: “గ్రిడ్”,
“list”: “జాబితా”,
“added”: “జోడించబడింది”,
“analytics_title”: “📊 విశ్లేషణ డాష్‌బోర్డ్”,
“movies_rated”: “రేట్ చేసిన చిత్రాలు”,
“reviews”: “సమీక్షలు”,
“avg_rating”: “సగటు రేటింగ్”,
“ratings_dist”: “⭐ రేటింగ్ పంపిణీ”,
“genre_breakdown”: “🎭 శైలి విశ్లేషణ”,
“rate_to_see”: “చార్ట్ చూడటానికి చిత్రాలు రేట్ చేయండి”,
“add_to_see”: “శైలి విశ్లేషణకు చిత్రాలు జోడించండి”,
“trending”: “📈 ట్రెండింగ్ చిత్రాలు”,
“simulated”: “అంచనా ప్రజాదరణ”,
“recent_reviews”: “📝 తాజా సమీక్షలు”,
“no_reviews_yet”: “ఇంకా సమీక్షలు లేవు.”,
“profile_title”: “👤 నా ప్రొఫైల్”,
“member_since”: “సభ్యుడు”,
“rated”: “రేట్ చేసారు”,
“top_rated”: “🏆 అత్యుత్తమ రేటింగ్”,
“no_ratings”: “మీ ప్రొఫైల్ నిర్మించడానికి చిత్రాలు రేట్ చేయండి!”,
“wrong_credentials”: “తప్పు వినియోగదారు పేరు లేదా పాస్‌వర్డ్.”,
“enter_username”: “వినియోగదారు పేరు నమోదు చేయండి.”,
“username_taken”: “వినియోగదారు పేరు ఇప్పటికే తీసుకోబడింది.”,
“passwords_no_match”: “పాస్‌వర్డ్‌లు సరిపోలడం లేదు.”,
“password_short”: “పాస్‌వర్డ్ చాలా చిన్నది.”,
“enter_name”: “మీ పేరు నమోదు చేయండి.”,
“write_something”: “ఏదైనా రాయండి.”,
“review_submitted”: “సమీక్ష సమర్పించబడింది! 🎉”,
“rating_saved”: “సేవ్ చేయబడింది”,
“min”: “నిమిషాలు”,
“votes”: “ఓట్లు”,
“language”: “భాష”,
“search_results”: “ఫలితాలు”,
“movie_explorer”: “చిత్ర అన్వేషకుడు”,
“no_movie_selected”: “చిత్రం ఎంచుకోబడలేదు.”,
},
“العربية”: {
“site_sub”: “اكتشف · قيّم · راجع · قائمة المشاهدة”,
“search_placeholder”: “🔍  أفينجرز، باتمان، حب…”,
“sign_in”: “تسجيل الدخول”,
“sign_up”: “إنشاء حساب”,
“username”: “اسم المستخدم”,
“password”: “كلمة المرور”,
“confirm_password”: “تأكيد كلمة المرور”,
“sign_in_btn”: “تسجيل الدخول →”,
“create_account”: “إنشاء حساب →”,
“demo_hint”: “تجريبي → demo / demo”,
“home”: “الرئيسية”,
“mood_pick”: “اختيار المزاج”,
“watchlist”: “قائمة المشاهدة”,
“analytics”: “التحليلات”,
“profile”: “الملف الشخصي”,
“sign_out”: “🚪 تسجيل الخروج”,
“home_feed”: “الصفحة الرئيسية”,
“category”: “الفئة”,
“grid_cols”: “أعمدة الشبكة”,
“activity”: “النشاط”,
“open”: “فتح →”,
“back_home”: “← العودة للرئيسية”,
“add_watchlist”: “🔖 إضافة للقائمة”,
“in_watchlist”: “✅ في القائمة”,
“recommendations”: “✅ توصيات”,
“rate_review”: “⭐ تقييم ومراجعة”,
“your_rating”: “تقييمك”,
“save_rating”: “💾 حفظ التقييم”,
“write_review”: “كتابة مراجعة”,
“your_name”: “اسمك”,
“stars”: “نجوم”,
“review_placeholder”: “شارك أفكارك…”,
“submit_review”: “📝 إرسال المراجعة”,
“no_reviews”: “لا مراجعات بعد. كن الأول! 🎬”,
“similar_movies”: “🔎 أفلام مشابهة”,
“more_genre”: “🎭 المزيد من هذا النوع”,
“mood_title”: “🎯 موصي بناءً على المزاج”,
“mood_subtitle”: “كيف تشعر اليوم؟ سنجد الأفلام المثالية لك.”,
“pick”: “اختر”,
“watchlist_title”: “🔖 قائمة مشاهدتي”,
“watchlist_empty”: “قائمة المشاهدة فارغة”,
“watchlist_hint”: “افتح أي فيلم → انقر 🔖”,
“clear_watchlist”: “🗑️ مسح القائمة”,
“view”: “عرض”,
“grid”: “شبكة”,
“list”: “قائمة”,
“added”: “أضيف”,
“analytics_title”: “📊 لوحة التحليلات”,
“movies_rated”: “الأفلام المقيّمة”,
“reviews”: “المراجعات”,
“avg_rating”: “متوسط التقييم”,
“ratings_dist”: “⭐ توزيع التقييمات”,
“genre_breakdown”: “🎭 توزيع الأنواع”,
“rate_to_see”: “قيّم الأفلام لرؤية الرسم البياني”,
“add_to_see”: “أضف أفلاماً لرؤية توزيع الأنواع”,
“trending”: “📈 الأفلام الرائجة”,
“simulated”: “شعبية تقديرية”,
“recent_reviews”: “📝 أحدث المراجعات”,
“no_reviews_yet”: “لا مراجعات بعد.”,
“profile_title”: “👤 ملفي الشخصي”,
“member_since”: “عضو منذ”,
“rated”: “مقيّم”,
“top_rated”: “🏆 الأعلى تقييماً”,
“no_ratings”: “قيّم الأفلام لبناء ملفك الشخصي!”,
“wrong_credentials”: “اسم المستخدم أو كلمة المرور خاطئة.”,
“enter_username”: “أدخل اسم المستخدم.”,
“username_taken”: “اسم المستخدم مأخوذ.”,
“passwords_no_match”: “كلمات المرور غير متطابقة.”,
“password_short”: “كلمة المرور قصيرة جداً.”,
“enter_name”: “أدخل اسمك.”,
“write_something”: “اكتب شيئاً.”,
“review_submitted”: “تم إرسال المراجعة! 🎉”,
“rating_saved”: “تم الحفظ”,
“min”: “دقيقة”,
“votes”: “أصوات”,
“language”: “اللغة”,
“search_results”: “نتائج”,
“movie_explorer”: “مستكشف الأفلام”,
“no_movie_selected”: “لم يتم اختيار فيلم.”,
},
}

# =============================

# STYLES

# =============================

st.markdown(”””

<style>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@400;700;900&family=DM+Sans:wght@300;400;500&display=swap');
:root {
    --bg: #0a0a0f; --surface: #12121a; --surface2: #1a1a26;
    --border: rgba(255,255,255,0.07); --accent: #e8b84b;
    --text: #f0ece4; --muted: #7a7590; --star: #f5c518;
}
html, body, [data-testid="stAppViewContainer"] { background: var(--bg) !important; color: var(--text) !important; font-family: 'DM Sans', sans-serif; }
[data-testid="stHeader"] { background: transparent !important; }
[data-testid="stSidebar"] { background: var(--surface) !important; border-right: 1px solid var(--border); }
.block-container { padding-top: 1.5rem; padding-bottom: 2rem; max-width: 1400px; }
h1,h2,h3 { font-family: 'Playfair Display', serif !important; color: var(--text) !important; }
.site-title { font-family: 'Playfair Display', serif; font-size: 2.4rem; font-weight: 900; background: linear-gradient(135deg,#e8b84b,#f0ece4,#c0392b); -webkit-background-clip: text; -webkit-text-fill-color: transparent; margin:0; }
.site-sub { color: var(--muted); font-size: 0.82rem; letter-spacing: 2.5px; text-transform: uppercase; margin-top:2px; }
.movie-title { font-size: 0.82rem; font-weight: 500; color: var(--text); line-height: 1.2rem; height: 2.4rem; overflow: hidden; margin-top: 6px; }
.stars { color: var(--star); font-size: 0.85rem; }
.rating-badge { display:inline-flex;align-items:center;gap:4px;background:rgba(245,197,24,0.12);border:1px solid rgba(245,197,24,0.25);border-radius:20px;padding:3px 10px;font-size:0.82rem;color:var(--star);font-weight:600; }
.vote-count { color:var(--muted);font-size:0.75rem; }
.genre-pill { display:inline-block;background:rgba(232,184,75,0.1);border:1px solid rgba(232,184,75,0.2);border-radius:20px;padding:2px 10px;font-size:0.76rem;color:var(--accent);margin:2px; }
.review-card { background:var(--surface2);border:1px solid var(--border);border-radius:12px;padding:16px;margin-bottom:12px; }
.reviewer-name { font-weight:600;color:var(--text);font-size:0.9rem; }
.review-date { color:var(--muted);font-size:0.78rem; }
.review-text { color:#c8c4be;font-size:0.88rem;line-height:1.5;margin-top:8px; }
.metric-card { background:var(--surface);border:1px solid var(--border);border-radius:14px;padding:18px 20px;text-align:center; }
.metric-value { font-family:'Playfair Display',serif;font-size:2rem;font-weight:700;color:var(--accent); }
.metric-label { color:var(--muted);font-size:0.8rem;text-transform:uppercase;letter-spacing:1px; }
.mood-card { background:var(--surface2);border:2px solid var(--border);border-radius:16px;padding:20px 16px;text-align:center;transition:border-color 0.2s; }
.mood-card:hover { border-color: rgba(232,184,75,0.4); }
.mood-emoji { font-size:2.6rem;margin-bottom:10px; }
.mood-label { font-family:'Playfair Display',serif;font-size:1rem;color:var(--text); }
.mood-desc { color:var(--muted);font-size:0.76rem;margin-top:4px; }
.mood-selected { border-color:#e8b84b !important; background: rgba(232,184,75,0.07) !important; }
.wl-title { font-size:0.92rem;color:var(--text);font-weight:500; }
.wl-meta { color:var(--muted);font-size:0.78rem;margin-top:2px; }
.profile-avatar { width:72px;height:72px;border-radius:50%;background:linear-gradient(135deg,#e8b84b,#c0392b);display:flex;align-items:center;justify-content:center;font-size:2rem;font-family:'Playfair Display',serif;color:#0a0a0f;font-weight:700; }
[data-testid="stTabs"] button { font-family:'DM Sans',sans-serif !important; color:var(--muted) !important; }
[data-testid="stTabs"] button[aria-selected="true"] { color:var(--accent) !important; border-bottom:2px solid var(--accent) !important; }
[data-testid="stTextInput"] input { background:var(--surface) !important;border:1px solid var(--border) !important;border-radius:10px !important;color:var(--text) !important; }
[data-testid="stSelectbox"] > div > div { background:var(--surface) !important;border:1px solid var(--border) !important;color:var(--text) !important; }
.stButton > button { background:transparent !important;border:1px solid var(--border) !important;color:var(--text) !important;border-radius:8px !important;font-family:'DM Sans',sans-serif !important;transition:all 0.2s !important; }
.stButton > button:hover { border-color:var(--accent) !important;color:var(--accent) !important; }
hr { border-color:var(--border) !important; }
.login-wrap { max-width:420px;margin:60px auto;background:var(--surface);border:1px solid var(--border);border-radius:20px;padding:40px; }
.profile-stat-card { background:var(--surface2);border:1px solid var(--border);border-radius:14px;padding:16px;text-align:center; }
.lang-badge { display:inline-block;background:rgba(232,184,75,0.12);border:1px solid rgba(232,184,75,0.25);border-radius:20px;padding:4px 14px;font-size:0.8rem;color:var(--accent);margin:2px;cursor:pointer; }
</style>

“””, unsafe_allow_html=True)

# =============================

# SESSION STATE

# =============================

defaults = {
“view”: “home”, “selected_tmdb_id”: None,
“reviews”: {}, “user_ratings”: {},
“watchlist”: [], “logged_in”: False,
“username”: “”, “mood_selected”: None,
“language”: “English”,
“movie_title_cache”: {},
}
for k, v in defaults.items():
if k not in st.session_state:
st.session_state[k] = v

def T(key):
lang = st.session_state.get(“language”, “English”)
return LANG_STRINGS.get(lang, LANG_STRINGS[“English”]).get(key, LANG_STRINGS[“English”].get(key, key))

USERS = {“sana”: “1234”, “demo”: “demo”, “admin”: “admin”}

qp_view = st.query_params.get(“view”)
qp_id   = st.query_params.get(“id”)
if qp_view in (“home”,“details”,“analytics”,“watchlist”,“mood”,“profile”):
st.session_state.view = qp_view
if qp_id:
try:
st.session_state.selected_tmdb_id = int(qp_id)
st.session_state.view = “details”
except:
pass

def goto(view, tmdb_id=None):
st.session_state.view = view
st.query_params[“view”] = view
if tmdb_id:
st.session_state.selected_tmdb_id = int(tmdb_id)
st.query_params[“id”] = str(int(tmdb_id))
elif “id” in st.query_params:
del st.query_params[“id”]
st.rerun()

# =============================

# LOGIN GATE

# =============================

if not st.session_state.logged_in:
# Language selector on login page
lang_col1, lang_col2 = st.columns([3,1])
with lang_col2:
selected_lang = st.selectbox(“🌐”, list(LANG_STRINGS.keys()), index=list(LANG_STRINGS.keys()).index(st.session_state.language), label_visibility=“collapsed”)
if selected_lang != st.session_state.language:
st.session_state.language = selected_lang
st.rerun()

```
st.markdown("<div class='login-wrap'>", unsafe_allow_html=True)
st.markdown(
    "<div style='font-family:Playfair Display,serif;font-size:1.8rem;color:#f0ece4;margin-bottom:4px'>🎬 CineScope</div>"
    f"<div style='color:#7a7590;font-size:0.85rem;margin-bottom:28px'>{T('site_sub')}</div>",
    unsafe_allow_html=True,
)
tab_in, tab_up = st.tabs([T("sign_in"), T("sign_up")])

with tab_in:
    uname = st.text_input(T("username"), placeholder="e.g. demo", key="li_u")
    pwd   = st.text_input(T("password"), type="password", key="li_p")
    if st.button(T("sign_in_btn"), use_container_width=True):
        if uname in USERS and USERS[uname] == pwd:
            st.session_state.logged_in = True
            st.session_state.username  = uname
            st.rerun()
        else:
            st.error(T("wrong_credentials"))
    st.markdown(f"<div style='color:#7a7590;font-size:0.8rem;margin-top:10px'>{T('demo_hint')}</div>", unsafe_allow_html=True)

with tab_up:
    nu = st.text_input(T("username"), key="su_u")
    np1 = st.text_input(T("password"), type="password", key="su_p1")
    np2 = st.text_input(T("confirm_password"), type="password", key="su_p2")
    if st.button(T("create_account"), use_container_width=True):
        if not nu.strip():
            st.warning(T("enter_username"))
        elif nu in USERS:
            st.error(T("username_taken"))
        elif np1 != np2:
            st.error(T("passwords_no_match"))
        elif len(np1) < 3:
            st.warning(T("password_short"))
        else:
            USERS[nu] = np1
            st.session_state.logged_in = True
            st.session_state.username  = nu
            st.rerun()

st.markdown("</div>", unsafe_allow_html=True)
st.stop()
```

# =============================

# API HELPERS

# =============================

@st.cache_data(ttl=30)
def api_get_json(path: str, params: dict | None = None):
try:
r = requests.get(f”{API_BASE}{path}”, params=params, timeout=25)
if r.status_code >= 400:
return None, f”HTTP {r.status_code}: {r.text[:300]}”
return r.json(), None
except Exception as e:
return None, f”Request failed: {e}”

# =============================

# RATING HELPERS

# =============================

def stars_html(rating: float, max_rating: float = 10.0) -> str:
n = (rating / max_rating) * 5
full = int(n); half = 1 if (n - full) >= 0.5 else 0; empty = 5 - full - half
return f”<span class='stars'>{‘★’*full}{‘½’ if half else ‘’}{‘☆’*empty}</span>”

def rating_badge_html(rating, vote_count=0):
vc = f”<span class='vote-count' style='margin-left:6px'>{vote_count:,} {T(‘votes’)}</span>” if vote_count else “”
return f”<span class='rating-badge'>⭐ {rating:.1f}/10</span>{vc}”

def render_rating_bars(rating):
bars = [(“10”, int(rating*3)), (“8”, int(rating*6)), (“6”, int(rating*4)), (“4”, int(rating*2)), (“2”, max(0,int(rating-5)))]
mx = max(v for _,v in bars) or 1
html = “”
for label, val in bars:
pct = int((val/mx)*100)
html += (f”<div style='display:flex;align-items:center;gap:8px;margin:4px 0'>”
f”<span style='color:#7a7590;font-size:0.78rem;width:20px'>{label}</span>”
f”<div style='background:#1a1a26;border-radius:4px;height:8px;flex:1'>”
f”<div style='background:linear-gradient(90deg,#e8b84b,#f5c518);border-radius:4px;height:8px;width:{pct}%'></div></div>”
f”<span style='color:#7a7590;font-size:0.75rem;width:24px'>{val}</span></div>”)
st.markdown(html, unsafe_allow_html=True)

# =============================

# WATCHLIST HELPERS

# =============================

def in_watchlist(tmdb_id):
return any(w[“tmdb_id”] == tmdb_id for w in st.session_state.watchlist)

def add_to_watchlist(tmdb_id, title, poster_url, genres=””):
if not in_watchlist(tmdb_id):
st.session_state.watchlist.append({
“tmdb_id”: tmdb_id, “title”: title, “poster_url”: poster_url,
“genres”: genres, “added_on”: datetime.now().strftime(”%b %d, %Y”),
})
st.session_state.movie_title_cache[tmdb_id] = title

def remove_from_watchlist(tmdb_id):
st.session_state.watchlist = [w for w in st.session_state.watchlist if w[“tmdb_id”] != tmdb_id]

# =============================

# POSTER GRID

# =============================

def poster_grid(cards, cols=6, key_prefix=“grid”, show_rating=False):
if not cards:
st.info(“No movies to show.”)
return
rows = (len(cards) + cols - 1) // cols
idx = 0
for r in range(rows):
colset = st.columns(cols)
for c in range(cols):
if idx >= len(cards): break
m = cards[idx]; idx += 1
tmdb_id = m.get(“tmdb_id”); title = m.get(“title”,“Untitled”)
poster = m.get(“poster_url”); rating = m.get(“vote_average”) or m.get(“rating”)
with colset[c]:
if poster:
st.image(poster, use_column_width=True)
else:
st.markdown(”<div style='background:#1a1a26;border-radius:8px;height:180px;display:flex;align-items:center;justify-content:center;color:#7a7590;font-size:2rem'>🎬</div>”, unsafe_allow_html=True)
st.markdown(f”<div class='movie-title'>{title}</div>”, unsafe_allow_html=True)
if show_rating and rating:
st.markdown(f”<div style='color:#f5c518;font-size:0.78rem'>⭐ {float(rating):.1f}</div>”, unsafe_allow_html=True)
if st.button(T(“open”), key=f”{key_prefix}*{r}*{c}*{idx}*{tmdb_id}”):
if tmdb_id:
st.session_state.movie_title_cache[tmdb_id] = title
goto(“details”, tmdb_id)

def to_cards_from_tfidf(items):
cards = []
for x in items or []:
t = x.get(“tmdb”) or {}
if t.get(“tmdb_id”):
cards.append({“tmdb_id”: t[“tmdb_id”], “title”: t.get(“title”) or x.get(“title”,“Untitled”), “poster_url”: t.get(“poster_url”), “vote_average”: t.get(“vote_average”)})
return cards

def parse_search_to_cards(data, keyword, limit=24):
keyword_l = keyword.strip().lower()
if isinstance(data, dict) and “results” in data:
raw = [{“tmdb_id”: int(m[“id”]), “title”: (m.get(“title”) or “”).strip(),
“poster_url”: f”{TMDB_IMG}{m[‘poster_path’]}” if m.get(“poster_path”) else None,
“release_date”: m.get(“release_date”,””), “vote_average”: m.get(“vote_average”)}
for m in data.get(“results”,[]) if m.get(“title”) and m.get(“id”)]
elif isinstance(data, list):
raw = [{“tmdb_id”: int(m.get(“tmdb_id”) or m.get(“id”,0)), “title”: (m.get(“title”) or “”).strip(),
“poster_url”: m.get(“poster_url”), “release_date”: m.get(“release_date”,””), “vote_average”: m.get(“vote_average”)}
for m in data if (m.get(“title”) and (m.get(“tmdb_id”) or m.get(“id”)))]
else:
return [], []
matched = [x for x in raw if keyword_l in x[“title”].lower()] or raw
suggestions = [(f”{x[‘title’]} ({x[‘release_date’][:4]})” if x.get(“release_date”) else x[“title”], x[“tmdb_id”]) for x in matched[:10]]
cards = [{“tmdb_id”: x[“tmdb_id”], “title”: x[“title”], “poster_url”: x[“poster_url”], “vote_average”: x.get(“vote_average”)} for x in matched[:limit]]
return suggestions, cards

# =============================

# MOOD CONFIG  — extended with multiple search queries

# =============================

MOODS = [
{
“emoji”: “😂”,
“label”: “Feel-Good”,
“desc”: {“English”: “Comedy & fun”, “हिन्दी”: “कॉमेडी और मस्ती”, “తెలుగు”: “కామెడీ & వినోదం”, “العربية”: “كوميديا وترفيه”},
“genres”: [“Comedy”,“Animation”,“Family”],
“queries”: [“funny comedy movie”, “family comedy film”, “animated comedy”],
“color”: “#f5c518”,
},
{
“emoji”: “😱”,
“label”: “Thriller”,
“desc”: {“English”: “Edge-of-seat suspense”, “हिन्दी”: “रोमांचक सस्पेंस”, “తెలుగు”: “థ్రిల్లర్ సస్పెన్స్”, “العربية”: “توتر وإثارة”},
“genres”: [“Thriller”,“Horror”,“Mystery”],
“queries”: [“thriller suspense movie”, “horror mystery film”, “psychological thriller”],
“color”: “#c0392b”,
},
{
“emoji”: “❤️”,
“label”: “Romantic”,
“desc”: {“English”: “Love stories”, “हिन्दी”: “प्रेम कहानियां”, “తెలుగు”: “ప్రేమ కథలు”, “العربية”: “قصص حب”},
“genres”: [“Romance”,“Drama”],
“queries”: [“romance love story”, “romantic drama film”, “love movie”],
“color”: “#e84393”,
},
{
“emoji”: “🚀”,
“label”: “Adventure”,
“desc”: {“English”: “Action & epic journeys”, “हिन्दी”: “एक्शन और महाकाव्य”, “తెలుగు”: “యాక్షన్ & సాహసాలు”, “العربية”: “أكشن ومغامرات”},
“genres”: [“Action”,“Adventure”,“Sci-Fi”],
“queries”: [“action adventure movie”, “epic journey film”, “action blockbuster”],
“color”: “#e8b84b”,
},
{
“emoji”: “😢”,
“label”: “Emotional”,
“desc”: {“English”: “Tear-jerkers”, “हिन्दी”: “भावुक फिल्में”, “తెలుగు”: “భావోద్వేగ చిత్రాలు”, “العربية”: “أفلام مؤثرة”},
“genres”: [“Drama”,“History”,“War”],
“queries”: [“emotional drama film”, “tearjerker movie”, “moving drama”],
“color”: “#9b59b6”,
},
{
“emoji”: “🧠”,
“label”: “Mind-Bending”,
“desc”: {“English”: “Twists & sci-fi”, “हिन्दी”: “दिमाग घुमाने वाली”, “తెలుగు”: “మైండ్ బెండింగ్”, “العربية”: “خيال علمي وغموض”},
“genres”: [“Science Fiction”,“Mystery”,“Thriller”],
“queries”: [“mind bending sci-fi”, “complex plot twist movie”, “cerebral science fiction”],
“color”: “#1abc9c”,
},
]

def get_mood_desc(mood):
lang = st.session_state.get(“language”,“English”)
return mood[“desc”].get(lang, mood[“desc”][“English”])

def get_mood_label(mood):
# mood label stays the same (used as key), desc is translated
return mood[“label”]

# =============================

# SIDEBAR

# =============================

with st.sidebar:
uname = st.session_state.username
initial = uname[0].upper() if uname else “?”
st.markdown(
f”<div style='display:flex;align-items:center;gap:12px;margin-bottom:16px'>”
f”<div class='profile-avatar'>{initial}</div>”
f”<div><div style='color:#f0ece4;font-weight:600'>{uname}</div>”
f”<div style='color:#7a7590;font-size:0.75rem'>{T(‘movie_explorer’)}</div></div></div>”,
unsafe_allow_html=True,
)
st.divider()

```
# Language selector
st.markdown(f"<div style='color:#7a7590;font-size:0.75rem;text-transform:uppercase;letter-spacing:1px;margin-bottom:6px'>🌐 {T('language')}</div>", unsafe_allow_html=True)
lang_options = list(LANG_STRINGS.keys())
selected_lang = st.selectbox("Lang", lang_options, index=lang_options.index(st.session_state.language), label_visibility="collapsed")
if selected_lang != st.session_state.language:
    st.session_state.language = selected_lang
    st.rerun()

st.divider()
for icon, label_key, vkey in [("🏠","home","home"),("🎯","mood_pick","mood"),("🔖","watchlist","watchlist"),("📊","analytics","analytics"),("👤","profile","profile")]:
    if st.button(f"{icon}  {T(label_key)}", key=f"nav_{vkey}", use_container_width=True):
        goto(vkey)
st.divider()
st.markdown(f"<div style='color:#7a7590;font-size:0.78rem;text-transform:uppercase;letter-spacing:1px;margin-bottom:8px'>{T('home_feed')}</div>", unsafe_allow_html=True)
home_category = st.selectbox(T("category"), ["trending","popular","top_rated","now_playing","upcoming"], index=0, label_visibility="collapsed")
grid_cols = st.slider(T("grid_cols"), 4, 8, 6)
st.divider()
st.markdown(
    f"<div style='color:#7a7590;font-size:0.75rem'>{T('activity')}</div>"
    f"<div style='color:#e8b84b;font-size:0.92rem;font-weight:600;margin-top:4px'>"
    f"🔖 {len(st.session_state.watchlist)} &nbsp;|&nbsp; ⭐ {len(st.session_state.user_ratings)} &nbsp;|&nbsp; 📝 {sum(len(v) for v in st.session_state.reviews.values())}</div>",
    unsafe_allow_html=True,
)
st.divider()
if st.button(f"🚪 {T('sign_out')}", use_container_width=True):
    st.session_state.logged_in = False
    st.session_state.username = ""
    st.rerun()
```

# =============================

# HEADER

# =============================

st.markdown(”<p class='site-title'>CineScope</p>”, unsafe_allow_html=True)
st.markdown(f”<p class='site-sub'>{T(‘site_sub’)}</p>”, unsafe_allow_html=True)
st.divider()

# ==========================================================

# VIEW: PROFILE  — shows all ratings, reviews, watchlist

# ==========================================================

if st.session_state.view == “profile”:
uname = st.session_state.username
total_rated = len(st.session_state.user_ratings)
total_rev   = sum(len(v) for v in st.session_state.reviews.values())
avg_r = round(sum(st.session_state.user_ratings.values()) / total_rated, 1) if total_rated else 0

```
st.markdown(f"<div style='font-family:Playfair Display,serif;font-size:1.6rem;color:#f0ece4;margin-bottom:20px'>{T('profile_title')}</div>", unsafe_allow_html=True)

left, right = st.columns([1, 2], gap="large")
with left:
    st.markdown(
        f"<div style='background:var(--surface);border:1px solid var(--border);border-radius:20px;padding:32px;text-align:center'>"
        f"<div class='profile-avatar' style='margin:0 auto 16px auto'>{uname[0].upper()}</div>"
        f"<div style='font-family:Playfair Display,serif;font-size:1.4rem;color:#f0ece4'>{uname}</div>"
        f"<div style='color:#7a7590;font-size:0.82rem;margin-top:4px'>{T('member_since')} {datetime.now().strftime('%b %Y')}</div>"
        f"<div style='margin-top:20px;display:flex;justify-content:space-around'>"
        f"<div><div style='color:#e8b84b;font-size:1.3rem;font-weight:700'>{total_rated}</div><div style='color:#7a7590;font-size:0.75rem'>{T('rated')}</div></div>"
        f"<div><div style='color:#e8b84b;font-size:1.3rem;font-weight:700'>{total_rev}</div><div style='color:#7a7590;font-size:0.75rem'>{T('reviews')}</div></div>"
        f"<div><div style='color:#e8b84b;font-size:1.3rem;font-weight:700'>{len(st.session_state.watchlist)}</div><div style='color:#7a7590;font-size:0.75rem'>{T('watchlist')}</div></div>"
        f"</div></div>",
        unsafe_allow_html=True,
    )

with right:
    ptab1, ptab2, ptab3 = st.tabs([T("top_rated"), T("recent_reviews"), T("watchlist")])

    with ptab1:
        if st.session_state.user_ratings:
            for rank, (mid, score) in enumerate(sorted(st.session_state.user_ratings.items(), key=lambda x: x[1], reverse=True), 1):
                movie_title = st.session_state.movie_title_cache.get(mid, f"Movie ID {mid}")
                col_a, col_b = st.columns([5,1])
                with col_a:
                    st.markdown(
                        f"<div style='display:flex;align-items:center;gap:12px;padding:10px 0;border-bottom:1px solid rgba(255,255,255,0.05)'>"
                        f"<span style='color:#e8b84b;font-family:Playfair Display,serif;width:26px'>#{rank}</span>"
                        f"<span style='color:#f0ece4;font-size:0.9rem'>{movie_title}</span>"
                        f"<span style='color:#f5c518;margin-left:auto'>{'★'*int(score)}{'☆'*(5-int(score))} {score}/5</span></div>",
                        unsafe_allow_html=True,
                    )
                with col_b:
                    if st.button("Open", key=f"prof_open_{mid}"):
                        goto("details", mid)
        else:
            st.markdown(f"<div style='color:#7a7590;padding:20px 0'>{T('no_ratings')}</div>", unsafe_allow_html=True)

    with ptab2:
        all_revs = [(mid, rev) for mid, revs in st.session_state.reviews.items() for rev in revs]
        if all_revs:
            for mid, rev in reversed(all_revs):
                movie_title = st.session_state.movie_title_cache.get(mid, f"Movie ID {mid}")
                st.markdown(
                    f"<div class='review-card'>"
                    f"<div style='display:flex;justify-content:space-between;align-items:center'>"
                    f"<span style='color:#e8b84b;font-size:0.85rem;font-weight:600'>{movie_title}</span>"
                    f"<span style='color:#f5c518'>{'★'*rev['rating']}{'☆'*(5-rev['rating'])}</span></div>"
                    f"<div class='review-date'>{rev['date']}</div>"
                    f"<div class='review-text'>{rev['text']}</div></div>",
                    unsafe_allow_html=True,
                )
        else:
            st.markdown(f"<div style='color:#7a7590;padding:20px 0'>{T('no_reviews_yet')}</div>", unsafe_allow_html=True)

    with ptab3:
        if st.session_state.watchlist:
            for w in st.session_state.watchlist:
                c1, c2, c3 = st.columns([1,5,1])
                with c1:
                    if w.get("poster_url"):
                        st.image(w["poster_url"], width=50)
                with c2:
                    genres_pills = "".join(f"<span class='genre-pill'>{g.strip()}</span>" for g in (w.get("genres","")).split(",") if g.strip())
                    st.markdown(f"<div class='wl-title'>{w['title']}</div><div style='margin-top:4px'>{genres_pills}</div><div class='wl-meta'>{T('added')} {w.get('added_on','')}</div>", unsafe_allow_html=True)
                with c3:
                    if st.button("Open", key=f"prof_wl_{w['tmdb_id']}"):
                        goto("details", w["tmdb_id"])
                st.markdown("<hr style='border-color:rgba(255,255,255,0.04);margin:6px 0'>", unsafe_allow_html=True)
        else:
            st.markdown(f"<div style='color:#7a7590;padding:20px 0'>{T('watchlist_empty')}</div>", unsafe_allow_html=True)
```

# ==========================================================

# VIEW: MOOD RECOMMENDER  — enhanced with instant fetch

# ==========================================================

elif st.session_state.view == “mood”:
st.markdown(f”<div style='font-family:Playfair Display,serif;font-size:1.6rem;color:#f0ece4;margin-bottom:4px'>{T(‘mood_title’)}</div>”, unsafe_allow_html=True)
st.markdown(f”<div style='color:#7a7590;font-size:0.88rem;margin-bottom:24px'>{T(‘mood_subtitle’)}</div>”, unsafe_allow_html=True)

```
cols = st.columns(6)
for i, mood in enumerate(MOODS):
    with cols[i]:
        selected = st.session_state.mood_selected == mood["label"]
        bc = mood["color"] if selected else "rgba(255,255,255,0.07)"
        bg = f"rgba({int(mood['color'][1:3],16)},{int(mood['color'][3:5],16)},{int(mood['color'][5:7],16)},0.08)" if selected else "var(--surface2)"
        st.markdown(
            f"<div class='mood-card' style='border-color:{bc};background:{bg}'>"
            f"<div class='mood-emoji'>{mood['emoji']}</div>"
            f"<div class='mood-label'>{mood['label']}</div>"
            f"<div class='mood-desc'>{get_mood_desc(mood)}</div></div>",
            unsafe_allow_html=True,
        )
        if st.button(T("pick"), key=f"mood_{i}", use_container_width=True):
            st.session_state.mood_selected = mood["label"]
            st.rerun()

if st.session_state.mood_selected:
    mood_obj = next((m for m in MOODS if m["label"] == st.session_state.mood_selected), None)
    if mood_obj:
        st.divider()
        st.markdown(
            f"<div style='display:flex;align-items:center;gap:12px;margin-bottom:12px'>"
            f"<span style='font-size:2.2rem'>{mood_obj['emoji']}</span>"
            f"<div><div style='font-family:Playfair Display,serif;font-size:1.4rem;color:#f0ece4'>{mood_obj['label']}</div>"
            f"<div style='color:#7a7590;font-size:0.85rem'>{get_mood_desc(mood_obj)}</div></div></div>",
            unsafe_allow_html=True,
        )
        st.markdown("".join(f"<span class='genre-pill'>{g}</span>" for g in mood_obj["genres"]), unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)

        # Fetch from all queries and merge results
        all_cards = []
        seen_ids = set()
        with st.spinner("Finding perfect movies for your mood..."):
            for query in mood_obj["queries"]:
                data, err = api_get_json("/tmdb/search", params={"query": query})
                if not err and data:
                    _, cards = parse_search_to_cards(data, query, limit=12)
                    for card in cards:
                        if card["tmdb_id"] not in seen_ids:
                            seen_ids.add(card["tmdb_id"])
                            all_cards.append(card)

        if all_cards:
            st.markdown(f"<div style='color:#7a7590;font-size:0.85rem;margin-bottom:12px'>Found <b style='color:#e8b84b'>{len(all_cards)}</b> movies for your mood</div>", unsafe_allow_html=True)
            poster_grid(all_cards, cols=grid_cols, key_prefix=f"mood_{mood_obj['label']}", show_rating=True)
        else:
            st.info("No movies found. Try another mood!")
```

# ==========================================================

# VIEW: WATCHLIST  — with genre tags and improved list view

# ==========================================================

elif st.session_state.view == “watchlist”:
st.markdown(f”<div style='font-family:Playfair Display,serif;font-size:1.6rem;color:#f0ece4;margin-bottom:4px'>{T(‘watchlist_title’)}</div>”, unsafe_allow_html=True)
st.markdown(f”<div style='color:#7a7590;font-size:0.88rem;margin-bottom:20px'>{len(st.session_state.watchlist)} movies saved</div>”, unsafe_allow_html=True)

```
if not st.session_state.watchlist:
    st.markdown(
        f"<div style='text-align:center;padding:60px 0'>"
        f"<div style='font-size:3rem'>🎬</div>"
        f"<div style='font-family:Playfair Display,serif;font-size:1.2rem;color:#f0ece4;margin-top:12px'>{T('watchlist_empty')}</div>"
        f"<div style='color:#7a7590;font-size:0.88rem;margin-top:8px'>{T('watchlist_hint')}</div></div>",
        unsafe_allow_html=True,
    )
else:
    wl_view = st.radio(T("view"), [T("grid"), T("list")], horizontal=True, label_visibility="collapsed")

    if wl_view == T("grid"):
        poster_grid(st.session_state.watchlist, cols=grid_cols, key_prefix="wl_grid")
        st.divider()
        if st.button(T("clear_watchlist")):
            st.session_state.watchlist = []
            st.rerun()
    else:
        # Enhanced list view with genre tags and date
        for i, w in enumerate(st.session_state.watchlist):
            c1, c2, c3 = st.columns([1, 5, 1])
            with c1:
                if w.get("poster_url"):
                    st.image(w["poster_url"], width=70)
                else:
                    st.markdown("<div style='width:70px;height:95px;background:#1a1a26;border-radius:8px;display:flex;align-items:center;justify-content:center;color:#7a7590;font-size:1.5rem'>🎬</div>", unsafe_allow_html=True)
            with c2:
                # Genre pills
                genre_list = [g.strip() for g in (w.get("genres","")).split(",") if g.strip()]
                genre_html = "".join(f"<span class='genre-pill'>{g}</span>" for g in genre_list) if genre_list else ""
                st.markdown(
                    f"<div class='wl-title'>{w['title']}</div>"
                    f"<div style='margin:5px 0'>{genre_html}</div>"
                    f"<div class='wl-meta'>📅 {T('added')}: {w.get('added_on','')}</div>",
                    unsafe_allow_html=True,
                )
            with c3:
                if st.button(T("open"), key=f"wl_o_{i}"):
                    goto("details", w["tmdb_id"])
                if st.button("✕", key=f"wl_r_{i}"):
                    remove_from_watchlist(w["tmdb_id"]); st.rerun()
            st.markdown("<hr style='margin:6px 0;border-color:rgba(255,255,255,0.05)'>", unsafe_allow_html=True)

        st.divider()
        if st.button(T("clear_watchlist")):
            st.session_state.watchlist = []
            st.rerun()
```

# ==========================================================

# VIEW: ANALYTICS

# ==========================================================

elif st.session_state.view == “analytics”:
st.markdown(f”<div style='font-family:Playfair Display,serif;font-size:1.6rem;color:#f0ece4;margin-bottom:20px;border-left:3px solid #e8b84b;padding-left:12px'>{T(‘analytics_title’)}</div>”, unsafe_allow_html=True)

```
total_rated = len(st.session_state.user_ratings)
total_rev   = sum(len(v) for v in st.session_state.reviews.values())
avg_r       = round(sum(st.session_state.user_ratings.values()) / total_rated, 1) if total_rated else 0
wl_count    = len(st.session_state.watchlist)

m1, m2, m3, m4 = st.columns(4)
for col, val, label in [(m1,total_rated,T("movies_rated")),(m2,total_rev,T("reviews")),(m3,f"{avg_r}★",T("avg_rating")),(m4,wl_count,T("watchlist"))]:
    with col:
        st.markdown(f"<div class='metric-card'><div class='metric-value'>{val}</div><div class='metric-label'>{label}</div></div>", unsafe_allow_html=True)

st.divider()
cl, cr = st.columns(2, gap="large")

with cl:
    st.markdown(f"#### {T('ratings_dist')}")
    if total_rated > 0:
        import pandas as pd
        buckets = {1:0,2:0,3:0,4:0,5:0}
        for v in st.session_state.user_ratings.values():
            buckets[min(5,max(1,round(v)))] += 1
        df = pd.DataFrame({"Stars": [f"{'★'*s}" for s in range(1,6)], "Count": [buckets[s] for s in range(1,6)]})
        st.bar_chart(df.set_index("Stars"), color="#e8b84b", height=220)
    else:
        st.markdown(f"<div style='color:#7a7590;padding:40px 0;text-align:center'>{T('rate_to_see')}</div>", unsafe_allow_html=True)

with cr:
    st.markdown(f"#### {T('genre_breakdown')}")
    if st.session_state.watchlist:
        import pandas as pd
        gc: dict = {}
        for w in st.session_state.watchlist:
            for g in (w.get("genres") or "").split(","):
                g = g.strip()
                if g: gc[g] = gc.get(g,0) + 1
        if gc:
            df_g = pd.DataFrame({"Genre":list(gc.keys()),"Count":list(gc.values())}).sort_values("Count",ascending=False).head(8)
            st.bar_chart(df_g.set_index("Genre"), color="#c0392b", height=220)
        else:
            st.markdown(f"<div style='color:#7a7590;padding:40px 0;text-align:center'>{T('add_to_see')}</div>", unsafe_allow_html=True)
    else:
        st.markdown(f"<div style='color:#7a7590;padding:40px 0;text-align:center'>{T('add_to_see')}</div>", unsafe_allow_html=True)

st.divider()
st.markdown(f"#### {T('trending')}")
import pandas as pd, numpy as np
titles = ["Inception","Interstellar","Dark Knight","Avengers","Parasite","Dune","Oppenheimer","Avatar"]
days = ["Mon","Tue","Wed","Thu","Fri","Sat","Sun"]
np.random.seed(42)
df_trend = pd.DataFrame(
    {t: np.clip(np.cumsum(np.random.randint(-3,8,7)) + 65, 40, 100) for t in titles[:5]},
    index=days
)
st.line_chart(df_trend, height=240)
st.markdown(f"<div style='color:#7a7590;font-size:0.75rem'>{T('simulated')}</div>", unsafe_allow_html=True)

st.divider()
st.markdown(f"#### {T('recent_reviews')}")
all_revs = [(mid,rev) for mid,revs in st.session_state.reviews.items() for rev in revs]
if all_revs:
    for mid, rev in reversed(all_revs[-5:]):
        movie_title = st.session_state.movie_title_cache.get(mid, f"Movie ID {mid}")
        st.markdown(
            f"<div class='review-card'><div style='display:flex;justify-content:space-between;align-items:center'>"
            f"<span class='reviewer-name'>{rev['name']} — <span style='color:#e8b84b;font-size:0.82rem'>{movie_title}</span></span>"
            f"<span style='color:#f5c518'>{'★'*rev['rating']}{'☆'*(5-rev['rating'])}</span></div>"
            f"<div class='review-date'>{rev['date']}</div><div class='review-text'>{rev['text']}</div></div>",
            unsafe_allow_html=True,
        )
else:
    st.markdown(f"<div style='color:#7a7590'>{T('no_reviews_yet')}</div>", unsafe_allow_html=True)
```

# ==========================================================

# VIEW: HOME

# ==========================================================

elif st.session_state.view == “home”:
typed = st.text_input(“Search”, placeholder=T(“search_placeholder”), label_visibility=“collapsed”)
st.divider()

```
if typed.strip():
    if len(typed.strip()) < 2:
        st.caption("Type at least 2 characters.")
    else:
        data, err = api_get_json("/tmdb/search", params={"query": typed.strip()})
        if err or data is None:
            st.error(f"Search failed: {err}")
        else:
            suggestions, cards = parse_search_to_cards(data, typed.strip(), limit=24)
            if suggestions:
                labels = ["-- Select a movie --"] + [s[0] for s in suggestions]
                sel = st.selectbox("Suggestions", labels, index=0, label_visibility="collapsed")
                if sel != "-- Select a movie --":
                    chosen_id = {s[0]: s[1] for s in suggestions}[sel]
                    st.session_state.movie_title_cache[chosen_id] = sel.split(" (")[0]
                    goto("details", chosen_id)
            else:
                st.info("No suggestions found.")
            st.markdown(f"<div style='color:#7a7590;font-size:0.85rem;margin-bottom:12px'>Found <b style='color:#e8b84b'>{len(cards)}</b> {T('search_results')} <b style='color:#f0ece4'>\"{typed}\"</b></div>", unsafe_allow_html=True)
            poster_grid(cards, cols=grid_cols, key_prefix="search", show_rating=True)
    st.stop()

st.markdown(f"<div style='font-family:Playfair Display,serif;font-size:1.3rem;color:#f0ece4;margin-bottom:16px'>{home_category.replace('_',' ').title()}</div>", unsafe_allow_html=True)
home_cards, err = api_get_json("/home", params={"category": home_category, "limit": 24})
if err or not home_cards:
    st.error(f"Home feed failed: {err or 'Unknown error'}")
    st.stop()
poster_grid(home_cards, cols=grid_cols, key_prefix="home_feed", show_rating=True)
```

# ==========================================================

# VIEW: DETAILS

# ==========================================================

elif st.session_state.view == “details”:
tmdb_id = st.session_state.selected_tmdb_id
if not tmdb_id:
st.warning(T(“no_movie_selected”))
if st.button(“← Back”): goto(“home”)
st.stop()

```
if st.button(T("back_home")): goto("home")

data, err = api_get_json(f"/movie/id/{tmdb_id}")
if err or not data:
    st.error(f"Could not load: {err or 'Unknown error'}")
    st.stop()

left, right = st.columns([1, 2.5], gap="large")

with left:
    if data.get("poster_url"):
        st.image(data["poster_url"], use_container_width=True)
    else:
        st.markdown("<div style='background:#1a1a26;border-radius:12px;height:380px;display:flex;align-items:center;justify-content:center;color:#7a7590;font-size:3rem'>🎬</div>", unsafe_allow_html=True)

with right:
    title    = data.get("title","Untitled")
    release  = (data.get("release_date") or "")[:4]
    vote_avg = data.get("vote_average") or 0
    vote_cnt = data.get("vote_count") or 0
    runtime  = data.get("runtime")
    genres   = data.get("genres", [])
    overview = data.get("overview") or "No overview available."
    genre_str = ", ".join(g["name"] for g in genres)

    # Cache movie title
    st.session_state.movie_title_cache[tmdb_id] = title

    st.markdown(f"<h1 style='margin-bottom:4px'>{title} <span style='color:#7a7590;font-size:1.1rem;font-weight:400'>({release})</span></h1>", unsafe_allow_html=True)
    if genres:
        st.markdown("".join(f"<span class='genre-pill'>{g['name']}</span>" for g in genres), unsafe_allow_html=True)
    if vote_avg:
        st.markdown(f"<div style='margin:12px 0'>{rating_badge_html(vote_avg, vote_cnt)}<div style='margin-top:6px'>{stars_html(vote_avg)}</div></div>", unsafe_allow_html=True)
        render_rating_bars(vote_avg)
    if runtime:
        st.markdown(f"<div style='color:#7a7590;font-size:0.85rem;margin-top:8px'>🕐 {runtime} {T('min')}</div>", unsafe_allow_html=True)
    st.markdown("---")
    st.markdown(f"<div style='color:#c8c4be;font-size:0.95rem;line-height:1.65'>{overview}</div>", unsafe_allow_html=True)
    st.markdown("<div style='margin-top:16px'>", unsafe_allow_html=True)
    wl_label = T("in_watchlist") if in_watchlist(tmdb_id) else T("add_watchlist")
    if st.button(wl_label, key="wl_toggle"):
        if in_watchlist(tmdb_id):
            remove_from_watchlist(tmdb_id)
        else:
            add_to_watchlist(tmdb_id, title, data.get("poster_url"), genre_str)
        st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)

if data.get("backdrop_url"):
    st.image(data["backdrop_url"], use_column_width=True)

st.divider()
tab1, tab2 = st.tabs([T("recommendations"), T("rate_review")])

with tab1:
    title_str = (data.get("title") or "").strip()
    if title_str:
        bundle, err2 = api_get_json("/movie/search", params={"query": title_str, "tfidf_top_n": 12, "genre_limit": 12})
        if not err2 and bundle:
            st.markdown(f"<div style='font-family:Playfair Display,serif;font-size:1.1rem;color:#e8b84b;margin-bottom:12px'>{T('similar_movies')}</div>", unsafe_allow_html=True)
            poster_grid(to_cards_from_tfidf(bundle.get("tfidf_recommendations")), cols=grid_cols, key_prefix="tfidf", show_rating=True)
            st.markdown(f"<div style='font-family:Playfair Display,serif;font-size:1.1rem;color:#e8b84b;margin:20px 0 12px'>{T('more_genre')}</div>", unsafe_allow_html=True)
            poster_grid(bundle.get("genre_recommendations",[]), cols=grid_cols, key_prefix="genre", show_rating=True)
        else:
            genre_only, err3 = api_get_json("/recommend/genre", params={"tmdb_id": tmdb_id, "limit": 18})
            if not err3 and genre_only:
                poster_grid(genre_only, cols=grid_cols, key_prefix="genre_fb", show_rating=True)
            else:
                st.warning("No recommendations available right now.")

with tab2:
    col_rate, col_review = st.columns([1, 1.6], gap="large")

    with col_rate:
        st.markdown(f"<div style='font-family:Playfair Display,serif;font-size:1.1rem;color:#f0ece4;margin-bottom:12px'>{T('your_rating')}</div>", unsafe_allow_html=True)
        cur = float(st.session_state.user_ratings.get(tmdb_id, 0.0))
        user_score = st.slider("Rate", 0.0, 5.0, cur, 0.5, label_visibility="collapsed")
        filled = int(user_score); half = 1 if (user_score-filled)==0.5 else 0; empty = 5-filled-half
        st.markdown(f"<div style='color:#f5c518;font-size:1.8rem;letter-spacing:3px;margin:8px 0'>{'★'*filled}{'½' if half else ''}{'☆'*empty}</div><div style='color:#7a7590;font-size:0.85rem'>{user_score}/5.0</div>", unsafe_allow_html=True)
        if st.button(T("save_rating"), use_container_width=True):
            st.session_state.user_ratings[tmdb_id] = user_score
            st.success(f"{T('rating_saved')}: {user_score}/5 ⭐")
        if vote_avg:
            st.markdown(f"<div style='margin-top:16px;padding:12px;background:#1a1a26;border-radius:10px;border:1px solid rgba(255,255,255,0.06)'><div style='color:#7a7590;font-size:0.75rem;text-transform:uppercase;letter-spacing:1px'>TMDB Average</div><div style='color:#f5c518;font-size:1.4rem;font-weight:600'>{vote_avg:.1f}/10</div><div style='color:#7a7590;font-size:0.78rem'>{vote_cnt:,} {T('votes')}</div></div>", unsafe_allow_html=True)

    with col_review:
        st.markdown(f"<div style='font-family:Playfair Display,serif;font-size:1.1rem;color:#f0ece4;margin-bottom:12px'>{T('write_review')}</div>", unsafe_allow_html=True)
        rev_name  = st.text_input(T("your_name"), value=st.session_state.username, key=f"rname_{tmdb_id}")
        rev_stars = st.select_slider(T("stars"), [1,2,3,4,5], value=3, format_func=lambda x: "★"*x+"☆"*(5-x), key=f"rstars_{tmdb_id}")
        rev_text  = st.text_area(T("rate_review"), placeholder=T("review_placeholder"), height=110, key=f"rtext_{tmdb_id}", label_visibility="collapsed")
        if st.button(T("submit_review"), use_container_width=True, key=f"rsub_{tmdb_id}"):
            if not rev_name.strip():
                st.warning(T("enter_name"))
            elif not rev_text.strip():
                st.warning(T("write_something"))
            else:
                st.session_state.reviews.setdefault(tmdb_id,[]).append({
                    "name": rev_name.strip(), "rating": rev_stars,
                    "text": rev_text.strip(), "date": datetime.now().strftime("%b %d, %Y")
                })
                st.success(T("review_submitted"))
                st.rerun()

    movie_reviews = st.session_state.reviews.get(tmdb_id, [])
    if movie_reviews:
        st.markdown("---")
        avg_u = sum(r["rating"] for r in movie_reviews) / len(movie_reviews)
        st.markdown(f"<div style='color:#f5c518;font-size:1rem;margin-bottom:12px'>{'★'*round(avg_u)}{'☆'*(5-round(avg_u))} <span style='color:#7a7590;font-size:0.85rem'>{avg_u:.1f} avg · {len(movie_reviews)} review(s)</span></div>", unsafe_allow_html=True)
        for rev in reversed(movie_reviews):
            st.markdown(
                f"<div class='review-card'><div style='display:flex;justify-content:space-between;align-items:center'>"
                f"<span class='reviewer-name'>{rev['name']}</span><span style='color:#f5c518'>{'★'*rev['rating']}{'☆'*(5-rev['rating'])}</span></div>"
                f"<div class='review-date'>{rev['date']}</div><div class='review-text'>{rev['text']}</div></div>",
                unsafe_allow_html=True,
            )
    else:
        st.markdown(f"<div style='color:#7a7590;font-size:0.88rem;margin-top:16px'>{T('no_reviews')}</div>", unsafe_allow_html=True)
```
