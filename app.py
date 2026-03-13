import requests
import streamlit as st
import json
import os
from datetime import datetime
import pandas as pd
 
# =============================
# CONFIG
# =============================
API_BASE = "https://movie-recommender-1-eopi.onrender.com" or "http://127.0.0.1:8005"
TMDB_IMG = "https://image.tmdb.org/t/p/w500"
RATINGS_FILE = "ratings.json"
 
st.set_page_config(page_title="Movie Recommender", page_icon="🎬", layout="wide")
 
# =============================
# STYLES
# =============================
st.markdown(
    """
<style>
.block-container { padding-top: 1rem; padding-bottom: 2rem; max-width: 1400px; }
.small-muted { color:#6b7280; font-size: 0.92rem; }
.movie-title { font-size: 0.9rem; line-height: 1.15rem; height: 2.3rem; overflow: hidden; }
.card { border: 1px solid rgba(0,0,0,0.08); border-radius: 16px; padding: 14px; background: rgba(255,255,255,0.7); }
.mood-btn { border-radius: 20px; padding: 6px 14px; font-size: 0.85rem; }
.rating-star { font-size: 1.4rem; cursor: pointer; }
.stat-card { border: 1px solid rgba(0,0,0,0.1); border-radius: 12px; padding: 16px; text-align: center; background: linear-gradient(135deg, rgba(99,102,241,0.08), rgba(168,85,247,0.08)); }
.stat-number { font-size: 2rem; font-weight: 700; color: #6366f1; }
.stat-label { font-size: 0.85rem; color: #6b7280; }
</style>
""",
    unsafe_allow_html=True,
)
 
# =============================
# MOOD → GENRE MAPPING
# =============================
MOOD_GENRES = {
    "😊 Happy": ["Comedy", "Animation", "Family", "Musical"],
    "😱 Thrilling": ["Thriller", "Horror", "Mystery", "Crime"],
    "💕 Romantic": ["Romance", "Drama"],
    "🚀 Adventure": ["Action", "Adventure", "Science Fiction", "Fantasy"],
    "😢 Emotional": ["Drama", "History", "War"],
    "🤣 Fun": ["Comedy", "Animation"],
    "🔍 Mind-bending": ["Science Fiction", "Mystery", "Thriller"],
    "🌍 World Cinema": ["Foreign", "Documentary"],
}
 
YEAR_RANGES = {
    "All Time": (1900, 2025),
    "Classic (before 1980)": (1900, 1979),
    "80s–90s": (1980, 1999),
    "2000s": (2000, 2009),
    "2010s": (2010, 2019),
    "Recent (2020+)": (2020, 2025),
}
 
LANGUAGES = ["All", "English", "Hindi", "Korean", "French", "Japanese", "Spanish", "Tamil", "Telugu"]
 
# =============================
# RATINGS STORAGE
# =============================
def load_ratings():
    if os.path.exists(RATINGS_FILE):
        try:
            with open(RATINGS_FILE, "r") as f:
                return json.load(f)
        except:
            return {}
    return {}
 
def save_ratings(ratings):
    with open(RATINGS_FILE, "w") as f:
        json.dump(ratings, f, indent=2)
 
def add_rating(tmdb_id: int, title: str, rating: int, review: str = ""):
    ratings = load_ratings()
    key = str(tmdb_id)
    if key not in ratings:
        ratings[key] = {"title": title, "ratings": [], "reviews": []}
    ratings[key]["ratings"].append(rating)
    if review.strip():
        ratings[key]["reviews"].append({
            "text": review.strip(),
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M"),
            "rating": rating
        })
    save_ratings(ratings)
 
def get_movie_rating(tmdb_id: int):
    ratings = load_ratings()
    key = str(tmdb_id)
    if key in ratings and ratings[key]["ratings"]:
        avg = sum(ratings[key]["ratings"]) / len(ratings[key]["ratings"])
        count = len(ratings[key]["ratings"])
        return round(avg, 1), count
    return None, 0
 
# =============================
# STATE + ROUTING
# =============================
if "view" not in st.session_state:
    st.session_state.view = "home"
if "selected_tmdb_id" not in st.session_state:
    st.session_state.selected_tmdb_id = None
if "active_mood" not in st.session_state:
    st.session_state.active_mood = None
 
qp_view = st.query_params.get("view")
qp_id = st.query_params.get("id")
if qp_view in ("home", "details", "analytics"):
    st.session_state.view = qp_view
if qp_id:
    try:
        st.session_state.selected_tmdb_id = int(qp_id)
        st.session_state.view = "details"
    except:
        pass
 
 
def goto_home():
    st.session_state.view = "home"
    st.session_state.active_mood = None
    st.query_params["view"] = "home"
    if "id" in st.query_params:
        del st.query_params["id"]
    st.rerun()
 
 
def goto_details(tmdb_id: int):
    st.session_state.view = "details"
    st.session_state.selected_tmdb_id = int(tmdb_id)
    st.query_params["view"] = "details"
    st.query_params["id"] = str(int(tmdb_id))
    st.rerun()
 
 
def goto_analytics():
    st.session_state.view = "analytics"
    st.query_params["view"] = "analytics"
    if "id" in st.query_params:
        del st.query_params["id"]
    st.rerun()
 
 
# =============================
# API HELPERS
# =============================
@st.cache_data(ttl=30)
def api_get_json(path: str, params: dict | None = None):
    try:
        r = requests.get(f"{API_BASE}{path}", params=params, timeout=25)
        if r.status_code >= 400:
            return None, f"HTTP {r.status_code}: {r.text[:300]}"
        return r.json(), None
    except Exception as e:
        return None, f"Request failed: {e}"
 
 
def poster_grid(cards, cols=6, key_prefix="grid"):
    if not cards:
        st.info("No movies to show.")
        return
 
    rows = (len(cards) + cols - 1) // cols
    idx = 0
    for r in range(rows):
        colset = st.columns(cols)
        for c in range(cols):
            if idx >= len(cards):
                break
            m = cards[idx]
            idx += 1
 
            tmdb_id = m.get("tmdb_id")
            title = m.get("title", "Untitled")
            poster = m.get("poster_url")
            year = (m.get("release_date") or "")[:4]
            rating_avg, rating_count = get_movie_rating(tmdb_id) if tmdb_id else (None, 0)
 
            with colset[c]:
                if poster:
                    st.image(poster, use_column_width=True)
                else:
                    st.write("🖼️ No poster")
 
                if st.button("Open", key=f"{key_prefix}_{r}_{c}_{idx}_{tmdb_id}"):
                    if tmdb_id:
                        goto_details(tmdb_id)
 
                st.markdown(
                    f"<div class='movie-title'>{title}</div>", unsafe_allow_html=True
                )
                if year:
                    st.markdown(f"<div class='small-muted'>{year}</div>", unsafe_allow_html=True)
                if rating_avg:
                    stars = "⭐" * int(round(rating_avg))
                    st.markdown(f"<div class='small-muted'>{stars} {rating_avg}/5 ({rating_count})</div>", unsafe_allow_html=True)
 
 
def to_cards_from_tfidf_items(tfidf_items):
    cards = []
    for x in tfidf_items or []:
        tmdb = x.get("tmdb") or {}
        if tmdb.get("tmdb_id"):
            cards.append(
                {
                    "tmdb_id": tmdb["tmdb_id"],
                    "title": tmdb.get("title") or x.get("title") or "Untitled",
                    "poster_url": tmdb.get("poster_url"),
                    "release_date": tmdb.get("release_date", ""),
                }
            )
    return cards
 
 
def parse_tmdb_search_to_cards(data, keyword: str, limit: int = 24,
                                 year_range=None, min_rating=None, language=None):
    keyword_l = keyword.strip().lower()
 
    if isinstance(data, dict) and "results" in data:
        raw = data.get("results") or []
        raw_items = []
        for m in raw:
            title = (m.get("title") or "").strip()
            tmdb_id = m.get("id")
            poster_path = m.get("poster_path")
            if not title or not tmdb_id:
                continue
            raw_items.append(
                {
                    "tmdb_id": int(tmdb_id),
                    "title": title,
                    "poster_url": f"{TMDB_IMG}{poster_path}" if poster_path else None,
                    "release_date": m.get("release_date", ""),
                    "vote_average": m.get("vote_average", 0),
                    "original_language": m.get("original_language", ""),
                }
            )
    elif isinstance(data, list):
        raw_items = []
        for m in data:
            tmdb_id = m.get("tmdb_id") or m.get("id")
            title = (m.get("title") or "").strip()
            poster_url = m.get("poster_url")
            if not title or not tmdb_id:
                continue
            raw_items.append(
                {
                    "tmdb_id": int(tmdb_id),
                    "title": title,
                    "poster_url": poster_url,
                    "release_date": m.get("release_date", ""),
                    "vote_average": m.get("vote_average", 0),
                    "original_language": m.get("original_language", ""),
                }
            )
    else:
        return [], []
 
    matched = [x for x in raw_items if keyword_l in x["title"].lower()]
    final_list = matched if matched else raw_items
 
    # ---- ADVANCED FILTERS ----
    if year_range and year_range != (1900, 2025):
        y_min, y_max = year_range
        filtered = []
        for x in final_list:
            year_str = (x.get("release_date") or "")[:4]
            if year_str.isdigit():
                y = int(year_str)
                if y_min <= y <= y_max:
                    filtered.append(x)
        if filtered:
            final_list = filtered
 
    if min_rating and min_rating > 0:
        filtered = [x for x in final_list if (x.get("vote_average") or 0) >= min_rating]
        if filtered:
            final_list = filtered
 
    LANG_MAP = {
        "English": "en", "Hindi": "hi", "Korean": "ko", "French": "fr",
        "Japanese": "ja", "Spanish": "es", "Tamil": "ta", "Telugu": "te"
    }
    if language and language != "All":
        lang_code = LANG_MAP.get(language, "")
        if lang_code:
            filtered = [x for x in final_list if x.get("original_language") == lang_code]
            if filtered:
                final_list = filtered
 
    suggestions = []
    for x in final_list[:10]:
        year = (x.get("release_date") or "")[:4]
        label = f"{x['title']} ({year})" if year else x["title"]
        suggestions.append((label, x["tmdb_id"]))
 
    cards = [
        {
            "tmdb_id": x["tmdb_id"],
            "title": x["title"],
            "poster_url": x["poster_url"],
            "release_date": x.get("release_date", ""),
        }
        for x in final_list[:limit]
    ]
    return suggestions, cards
 
 
# =============================
# SIDEBAR
# =============================
with st.sidebar:
    st.markdown("## 🎬 Menu")
    if st.button("🏠 Home"):
        goto_home()
    if st.button("📊 Analytics"):
        goto_analytics()
 
    st.markdown("---")
 
    # Mood selector in sidebar
    st.markdown("### 🎭 Browse by Mood")
    mood_selected = st.selectbox(
        "Pick a mood",
        ["None"] + list(MOOD_GENRES.keys()),
        index=0,
        key="sidebar_mood"
    )
    if mood_selected != "None":
        st.session_state.active_mood = mood_selected
        st.session_state.view = "home"
        st.query_params["view"] = "home"
        st.rerun()
 
    st.markdown("---")
    st.markdown("### 🏠 Home Feed")
    home_category = st.selectbox(
        "Category",
        ["trending", "popular", "top_rated", "now_playing", "upcoming"],
        index=0,
    )
    grid_cols = st.slider("Grid columns", 4, 8, 6)
 
    st.markdown("---")
    st.markdown("### 🔍 Advanced Filters")
    year_label = st.selectbox("Year Range", list(YEAR_RANGES.keys()), index=0)
    selected_year_range = YEAR_RANGES[year_label]
    min_tmdb_rating = st.slider("Min TMDB Rating", 0.0, 10.0, 0.0, 0.5)
    selected_language = st.selectbox("Language", LANGUAGES, index=0)
 
# =============================
# HEADER
# =============================
st.title("🎬 Movie Recommender")
st.markdown(
    "<div class='small-muted'>Search · Filter by Mood · Rate Movies · View Analytics</div>",
    unsafe_allow_html=True,
)
st.divider()
 
# ==========================================================
# VIEW: ANALYTICS
# ==========================================================
if st.session_state.view == "analytics":
    col_back, _ = st.columns([1, 5])
    with col_back:
        if st.button("← Back to Home"):
            goto_home()
 
    st.markdown("## 📊 Analytics Dashboard")
    st.markdown("*Insights based on your ratings and searches*")
    st.divider()
 
    ratings = load_ratings()
 
    if not ratings:
        st.info("No ratings yet! Go rate some movies first to see analytics here.")
        st.stop()
 
    # ---- TOP STATS ----
    total_rated = len(ratings)
    total_reviews = sum(len(v.get("reviews", [])) for v in ratings.values())
    all_rating_vals = [r for v in ratings.values() for r in v.get("ratings", [])]
    avg_overall = round(sum(all_rating_vals) / len(all_rating_vals), 2) if all_rating_vals else 0
    top_rated_movie = max(ratings.items(),
                          key=lambda x: sum(x[1]["ratings"]) / len(x[1]["ratings"]) if x[1]["ratings"] else 0,
                          default=(None, {}))
 
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.markdown(f"""<div class='stat-card'>
            <div class='stat-number'>{total_rated}</div>
            <div class='stat-label'>Movies Rated</div>
        </div>""", unsafe_allow_html=True)
    with c2:
        st.markdown(f"""<div class='stat-card'>
            <div class='stat-number'>{total_reviews}</div>
            <div class='stat-label'>Reviews Written</div>
        </div>""", unsafe_allow_html=True)
    with c3:
        st.markdown(f"""<div class='stat-card'>
            <div class='stat-number'>{avg_overall}/5</div>
            <div class='stat-label'>Average Rating</div>
        </div>""", unsafe_allow_html=True)
    with c4:
        top_title = top_rated_movie[1].get("title", "N/A") if top_rated_movie[0] else "N/A"
        short_title = top_title[:14] + "…" if len(top_title) > 16 else top_title
        st.markdown(f"""<div class='stat-card'>
            <div class='stat-number' style='font-size:1.2rem'>{short_title}</div>
            <div class='stat-label'>Highest Rated</div>
        </div>""", unsafe_allow_html=True)
 
    st.markdown("---")
 
    # ---- CHARTS ----
    col_left, col_right = st.columns(2)
 
    with col_left:
        st.markdown("#### ⭐ Rating Distribution")
        dist = {1: 0, 2: 0, 3: 0, 4: 0, 5: 0}
        for v in ratings.values():
            for r in v.get("ratings", []):
                if r in dist:
                    dist[r] += 1
        df_dist = pd.DataFrame({
            "Stars": [f"{'⭐'*k} ({k})" for k in dist],
            "Count": list(dist.values())
        })
        st.bar_chart(df_dist.set_index("Stars"))
 
    with col_right:
        st.markdown("#### 🏆 Top 5 Rated Movies")
        sorted_movies = sorted(
            [(v["title"], round(sum(v["ratings"]) / len(v["ratings"]), 1), len(v["ratings"]))
             for v in ratings.values() if v.get("ratings")],
            key=lambda x: x[1], reverse=True
        )[:5]
        if sorted_movies:
            df_top = pd.DataFrame(sorted_movies, columns=["Movie", "Avg Rating", "# Ratings"])
            df_top.index = range(1, len(df_top) + 1)
            st.dataframe(df_top, use_container_width=True)
 
    st.markdown("---")
 
    # ---- REVIEWS TABLE ----
    all_reviews = []
    for v in ratings.values():
        for rev in v.get("reviews", []):
            all_reviews.append({
                "Movie": v.get("title", "Unknown"),
                "Rating": "⭐" * rev.get("rating", 0),
                "Review": rev.get("text", ""),
                "Date": rev.get("timestamp", ""),
            })
 
    if all_reviews:
        st.markdown("#### 📝 All Reviews")
        df_reviews = pd.DataFrame(all_reviews)
        st.dataframe(df_reviews, use_container_width=True)
 
    st.stop()
 
# ==========================================================
# VIEW: HOME
# ==========================================================
if st.session_state.view == "home":
 
    # ---- MOOD BANNER ----
    if st.session_state.active_mood:
        mood = st.session_state.active_mood
        genres = MOOD_GENRES[mood]
        col_mood, col_clear = st.columns([4, 1])
        with col_mood:
            st.markdown(f"### {mood} — Showing: `{', '.join(genres)}`")
        with col_clear:
            if st.button("✕ Clear Mood"):
                st.session_state.active_mood = None
                st.rerun()
 
        mood_results, err = api_get_json("/home", params={"category": "popular", "limit": 24})
        if not err and mood_results:
            # Filter by genre client-side (if genre info available, else show all)
            poster_grid(mood_results, cols=grid_cols, key_prefix="mood_feed")
        else:
            st.error("Could not load movies for this mood.")
        st.stop()
 
    # ---- SEARCH ----
    typed = st.text_input(
        "🔍 Search by movie title", placeholder="Type: avenger, batman, love..."
    )
 
    # ---- MOOD BUTTONS ROW ----
    st.markdown("#### 🎭 Quick Mood Picker")
    mood_cols = st.columns(len(MOOD_GENRES))
    for i, (mood, genres) in enumerate(MOOD_GENRES.items()):
        with mood_cols[i]:
            if st.button(mood, key=f"mood_{i}", use_container_width=True):
                st.session_state.active_mood = mood
                st.rerun()
 
    st.divider()
 
    # SEARCH MODE
    if typed.strip():
        if len(typed.strip()) < 2:
            st.caption("Type at least 2 characters for suggestions.")
        else:
            data, err = api_get_json("/tmdb/search", params={"query": typed.strip()})
 
            if err or data is None:
                st.error(f"Search failed: {err}")
            else:
                suggestions, cards = parse_tmdb_search_to_cards(
                    data, typed.strip(), limit=24,
                    year_range=selected_year_range,
                    min_rating=min_tmdb_rating,
                    language=selected_language
                )
 
                # Active filter badges
                active_filters = []
                if year_label != "All Time":
                    active_filters.append(f"📅 {year_label}")
                if min_tmdb_rating > 0:
                    active_filters.append(f"⭐ Rating ≥ {min_tmdb_rating}")
                if selected_language != "All":
                    active_filters.append(f"🌐 {selected_language}")
                if active_filters:
                    st.markdown("**Active Filters:** " + " · ".join(active_filters))
 
                if suggestions:
                    labels = ["-- Select a movie --"] + [s[0] for s in suggestions]
                    selected = st.selectbox("Suggestions", labels, index=0)
 
                    if selected != "-- Select a movie --":
                        label_to_id = {s[0]: s[1] for s in suggestions}
                        goto_details(label_to_id[selected])
                else:
                    st.info("No suggestions found. Try another keyword or adjust filters.")
 
                result_count = len(cards)
                st.markdown(f"### Results ({result_count} movies)")
                poster_grid(cards, cols=grid_cols, key_prefix="search_results")
 
        st.stop()
 
    # HOME FEED MODE
    st.markdown(f"### 🏠 Home — {home_category.replace('_',' ').title()}")
 
    home_cards, err = api_get_json(
        "/home", params={"category": home_category, "limit": 24}
    )
    if err or not home_cards:
        st.error(f"Home feed failed: {err or 'Unknown error'}")
        st.stop()
 
    poster_grid(home_cards, cols=grid_cols, key_prefix="home_feed")
 
 
# ==========================================================
# VIEW: DETAILS
# ==========================================================
elif st.session_state.view == "details":
    tmdb_id = st.session_state.selected_tmdb_id
    if not tmdb_id:
        st.warning("No movie selected.")
        if st.button("← Back to Home"):
            goto_home()
        st.stop()
 
    a, b = st.columns([3, 1])
    with a:
        st.markdown("### 📄 Movie Details")
    with b:
        if st.button("← Back to Home"):
            goto_home()
 
    data, err = api_get_json(f"/movie/id/{tmdb_id}")
    if err or not data:
        st.error(f"Could not load details: {err or 'Unknown error'}")
        st.stop()
 
    left, right = st.columns([1, 2.4], gap="large")
 
    with left:
        st.markdown("<div class='card'>", unsafe_allow_html=True)
        if data.get("poster_url"):
            st.image(data["poster_url"], use_container_width=True)
        else:
            st.write("🖼️ No poster")
 
        # Community rating display
        rating_avg, rating_count = get_movie_rating(tmdb_id)
        if rating_avg:
            stars_display = "⭐" * int(round(rating_avg))
            st.markdown(f"**Community Rating:** {stars_display}")
            st.markdown(f"<div class='small-muted'>{rating_avg}/5 from {rating_count} rating(s)</div>", unsafe_allow_html=True)
        else:
            st.markdown("<div class='small-muted'>No ratings yet — be the first!</div>", unsafe_allow_html=True)
 
        st.markdown("</div>", unsafe_allow_html=True)
 
    with right:
        st.markdown("<div class='card'>", unsafe_allow_html=True)
        st.markdown(f"## {data.get('title','')}")
        release = data.get("release_date") or "-"
        genres = ", ".join([g["name"] for g in data.get("genres", [])]) or "-"
        runtime = data.get("runtime")
        vote = data.get("vote_average")
 
        st.markdown(f"<div class='small-muted'>📅 Release: {release}</div>", unsafe_allow_html=True)
        st.markdown(f"<div class='small-muted'>🎭 Genres: {genres}</div>", unsafe_allow_html=True)
        if runtime:
            st.markdown(f"<div class='small-muted'>⏱ Runtime: {runtime} min</div>", unsafe_allow_html=True)
        if vote:
            st.markdown(f"<div class='small-muted'>⭐ TMDB Rating: {vote}/10</div>", unsafe_allow_html=True)
 
        st.markdown("---")
        st.markdown("### Overview")
        st.write(data.get("overview") or "No overview available.")
        st.markdown("</div>", unsafe_allow_html=True)
 
    if data.get("backdrop_url"):
        st.markdown("#### Backdrop")
        st.image(data["backdrop_url"], use_column_width=True)
 
    # ================================================================
    # ⭐ RATE THIS MOVIE SECTION
    # ================================================================
    st.divider()
    st.markdown("### ⭐ Rate This Movie")
 
    movie_title = data.get("title", "")
    rating_key = f"user_rating_{tmdb_id}"
    review_key = f"user_review_{tmdb_id}"
 
    rating_col, review_col = st.columns([1, 2])
    with rating_col:
        user_rating = st.radio(
            "Your Rating",
            options=[1, 2, 3, 4, 5],
            format_func=lambda x: "⭐" * x,
            horizontal=True,
            key=rating_key
        )
    with review_col:
        user_review = st.text_area(
            "Write a Review (optional)",
            placeholder="What did you think of this movie?",
            height=80,
            key=review_key
        )
 
    if st.button("✅ Submit Rating", type="primary"):
        add_rating(tmdb_id, movie_title, user_rating, user_review)
        st.success(f"Thanks! You rated **{movie_title}** {'⭐' * user_rating}")
        st.rerun()
 
    # Show existing reviews
    ratings_data = load_ratings()
    movie_reviews = ratings_data.get(str(tmdb_id), {}).get("reviews", [])
    if movie_reviews:
        st.markdown("#### 💬 Community Reviews")
        for rev in reversed(movie_reviews[-5:]):  # show last 5
            st.markdown(f"{'⭐' * rev.get('rating', 0)} — *{rev.get('text', '')}*")
            st.caption(rev.get("timestamp", ""))
 
    # ================================================================
    # RECOMMENDATIONS
    # ================================================================
    st.divider()
    st.markdown("### ✅ Recommendations")
 
    title = (data.get("title") or "").strip()
    if title:
        bundle, err2 = api_get_json(
            "/movie/search",
            params={"query": title, "tfidf_top_n": 12, "genre_limit": 12},
        )
 
        if not err2 and bundle:
            st.markdown("#### 🔎 Similar Movies (TF-IDF)")
            poster_grid(
                to_cards_from_tfidf_items(bundle.get("tfidf_recommendations")),
                cols=grid_cols,
                key_prefix="details_tfidf",
            )
 
            st.markdown("#### 🎭 More Like This (Genre)")
            poster_grid(
                bundle.get("genre_recommendations", []),
                cols=grid_cols,
                key_prefix="details_genre",
            )
        else:
            st.info("Showing Genre recommendations (fallback).")
            genre_only, err3 = api_get_json(
                "/recommend/genre", params={"tmdb_id": tmdb_id, "limit": 18}
            )
            if not err3 and genre_only:
                poster_grid(
                    genre_only, cols=grid_cols, key_prefix="details_genre_fallback"
                )
            else:
                st.warning("No recommendations available right now.")
    else:
        st.warning("No title available to compute recommendations.")
 
