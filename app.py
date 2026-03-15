import requests
import streamlit as st
from datetime import datetime
import json

# =============================
# CONFIG
# =============================
API_BASE = "https://movie-recommender-1-eopi.onrender.com" or "http://127.0.0.1:8005"
TMDB_IMG = "https://image.tmdb.org/t/p/w500"

st.set_page_config(page_title="CineScope", page_icon="🎬", layout="wide")

# =============================
# MODERN CINEMATIC STYLES
# =============================
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@400;700;900&family=DM+Sans:wght@300;400;500&display=swap');

:root {
    --bg: #0a0a0f;
    --surface: #12121a;
    --surface2: #1a1a26;
    --border: rgba(255,255,255,0.07);
    --accent: #e8b84b;
    --accent2: #c0392b;
    --text: #f0ece4;
    --muted: #7a7590;
    --star: #f5c518;
}

html, body, [data-testid="stAppViewContainer"] {
    background: var(--bg) !important;
    color: var(--text) !important;
    font-family: 'DM Sans', sans-serif;
}

[data-testid="stHeader"] { background: transparent !important; }
[data-testid="stSidebar"] {
    background: var(--surface) !important;
    border-right: 1px solid var(--border);
}
.block-container { padding-top: 1.5rem; padding-bottom: 2rem; max-width: 1400px; }

/* ── HEADINGS ── */
h1, h2, h3 { font-family: 'Playfair Display', serif !important; color: var(--text) !important; }
.site-title {
    font-family: 'Playfair Display', serif;
    font-size: 2.6rem;
    font-weight: 900;
    letter-spacing: -0.5px;
    background: linear-gradient(135deg, #e8b84b 0%, #f0ece4 60%, #c0392b 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    margin: 0;
}
.site-sub {
    color: var(--muted);
    font-size: 0.88rem;
    letter-spacing: 2px;
    text-transform: uppercase;
    margin-top: 2px;
}

/* ── CARDS ── */
.card {
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 16px;
    padding: 20px;
    transition: border-color 0.2s;
}
.card:hover { border-color: rgba(232,184,75,0.3); }

.movie-title {
    font-size: 0.82rem;
    font-weight: 500;
    color: var(--text);
    line-height: 1.2rem;
    height: 2.4rem;
    overflow: hidden;
    margin-top: 6px;
}

/* ── STAR RATING ── */
.stars { color: var(--star); font-size: 0.85rem; letter-spacing: 1px; }
.rating-badge {
    display: inline-flex;
    align-items: center;
    gap: 4px;
    background: rgba(245,197,24,0.12);
    border: 1px solid rgba(245,197,24,0.25);
    border-radius: 20px;
    padding: 3px 10px;
    font-size: 0.82rem;
    color: var(--star);
    font-weight: 600;
}
.vote-count { color: var(--muted); font-size: 0.75rem; }

/* ── GENRE PILL ── */
.genre-pill {
    display: inline-block;
    background: rgba(232,184,75,0.1);
    border: 1px solid rgba(232,184,75,0.2);
    border-radius: 20px;
    padding: 2px 10px;
    font-size: 0.76rem;
    color: var(--accent);
    margin: 2px;
}

/* ── REVIEW CARD ── */
.review-card {
    background: var(--surface2);
    border: 1px solid var(--border);
    border-radius: 12px;
    padding: 16px;
    margin-bottom: 12px;
}
.reviewer-name { font-weight: 600; color: var(--text); font-size: 0.9rem; }
.review-date { color: var(--muted); font-size: 0.78rem; }
.review-text { color: #c8c4be; font-size: 0.88rem; line-height: 1.5; margin-top: 8px; }

/* ── METRIC CARD ── */
.metric-card {
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 14px;
    padding: 18px 20px;
    text-align: center;
}
.metric-value {
    font-family: 'Playfair Display', serif;
    font-size: 2rem;
    font-weight: 700;
    color: var(--accent);
}
.metric-label { color: var(--muted); font-size: 0.8rem; text-transform: uppercase; letter-spacing: 1px; }

/* ── TABS ── */
[data-testid="stTabs"] button {
    font-family: 'DM Sans', sans-serif !important;
    color: var(--muted) !important;
    border-radius: 8px 8px 0 0 !important;
}
[data-testid="stTabs"] button[aria-selected="true"] {
    color: var(--accent) !important;
    border-bottom: 2px solid var(--accent) !important;
}

/* ── INPUTS ── */
[data-testid="stTextInput"] input {
    background: var(--surface) !important;
    border: 1px solid var(--border) !important;
    border-radius: 10px !important;
    color: var(--text) !important;
    font-family: 'DM Sans', sans-serif;
}
[data-testid="stSelectbox"] > div > div {
    background: var(--surface) !important;
    border: 1px solid var(--border) !important;
    color: var(--text) !important;
}

/* ── BUTTONS ── */
.stButton > button {
    background: transparent !important;
    border: 1px solid var(--border) !important;
    color: var(--text) !important;
    border-radius: 8px !important;
    font-family: 'DM Sans', sans-serif !important;
    transition: all 0.2s !important;
}
.stButton > button:hover {
    border-color: var(--accent) !important;
    color: var(--accent) !important;
}

/* ── DIVIDER ── */
hr { border-color: var(--border) !important; }

/* ── PROGRESS BAR ── */
.rating-bar-wrap { margin: 4px 0; }
.rating-bar-label { color: var(--muted); font-size: 0.78rem; display: inline-block; width: 20px; }
.rating-bar-bg { background: var(--surface2); border-radius: 4px; height: 8px; display: inline-block; width: 140px; vertical-align: middle; margin: 0 8px; }
.rating-bar-fill { background: var(--star); border-radius: 4px; height: 8px; }
.rating-bar-count { color: var(--muted); font-size: 0.75rem; }

/* ── ANALYTICS ── */
.analytics-header {
    font-family: 'Playfair Display', serif;
    font-size: 1.5rem;
    color: var(--text);
    border-left: 3px solid var(--accent);
    padding-left: 12px;
    margin-bottom: 16px;
}

/* ── POSTER OPEN BTN ── */
.open-btn > button {
    width: 100% !important;
    font-size: 0.75rem !important;
    padding: 4px 0 !important;
}
</style>
""", unsafe_allow_html=True)

# =============================
# SESSION STATE
# =============================
if "view" not in st.session_state:
    st.session_state.view = "home"
if "selected_tmdb_id" not in st.session_state:
    st.session_state.selected_tmdb_id = None
if "reviews" not in st.session_state:
    st.session_state.reviews = {}   # {tmdb_id: [{name, rating, text, date}]}
if "user_ratings" not in st.session_state:
    st.session_state.user_ratings = {}  # {tmdb_id: float}

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


# =============================
# STAR HELPERS
# =============================
def stars_html(rating: float, max_rating: float = 10.0) -> str:
    """Convert TMDB 0-10 rating to 5-star HTML."""
    normalized = (rating / max_rating) * 5
    full = int(normalized)
    half = 1 if (normalized - full) >= 0.5 else 0
    empty = 5 - full - half
    return (
        "<span class='stars'>"
        + "★" * full
        + ("½" if half else "")
        + "☆" * empty
        + "</span>"
    )


def rating_badge_html(rating: float, vote_count: int = 0) -> str:
    return (
        f"<span class='rating-badge'>⭐ {rating:.1f}/10</span>"
        f"<span class='vote-count' style='margin-left:6px'>{vote_count:,} votes</span>"
        if vote_count
        else f"<span class='rating-badge'>⭐ {rating:.1f}/10</span>"
    )


def render_rating_bars(rating: float):
    """Show a visual breakdown bar for the rating."""
    # Simulate distribution bars (aesthetic only)
    bars = [
        ("10", int(rating * 3)),
        ("8", int(rating * 6)),
        ("6", int(rating * 4)),
        ("4", int(rating * 2)),
        ("2", max(0, int(rating - 5))),
    ]
    max_val = max(v for _, v in bars) or 1
    html = ""
    for label, val in bars:
        pct = int((val / max_val) * 100)
        html += (
            f"<div class='rating-bar-wrap'>"
            f"<span class='rating-bar-label'>{label}</span>"
            f"<span class='rating-bar-bg'><div class='rating-bar-fill' style='width:{pct}%'></div></span>"
            f"<span class='rating-bar-count'>{val}</span>"
            f"</div>"
        )
    st.markdown(html, unsafe_allow_html=True)


# =============================
# POSTER GRID
# =============================
def poster_grid(cards, cols=6, key_prefix="grid", show_rating=False):
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
            rating = m.get("vote_average") or m.get("rating")

            with colset[c]:
                if poster:
                    st.image(poster, use_column_width=True)
                else:
                    st.markdown(
                        "<div style='background:#1a1a26;border-radius:8px;height:180px;"
                        "display:flex;align-items:center;justify-content:center;"
                        "color:#7a7590;font-size:2rem'>🎬</div>",
                        unsafe_allow_html=True,
                    )

                st.markdown(
                    f"<div class='movie-title'>{title}</div>", unsafe_allow_html=True
                )

                if show_rating and rating:
                    st.markdown(
                        f"<div style='color:#f5c518;font-size:0.78rem;margin-top:2px'>⭐ {float(rating):.1f}</div>",
                        unsafe_allow_html=True,
                    )

                with st.container():
                    st.markdown("<div class='open-btn'>", unsafe_allow_html=True)
                    if st.button("Open →", key=f"{key_prefix}_{r}_{c}_{idx}_{tmdb_id}"):
                        if tmdb_id:
                            goto_details(tmdb_id)
                    st.markdown("</div>", unsafe_allow_html=True)


def to_cards_from_tfidf_items(tfidf_items):
    cards = []
    for x in tfidf_items or []:
        tmdb = x.get("tmdb") or {}
        if tmdb.get("tmdb_id"):
            cards.append({
                "tmdb_id": tmdb["tmdb_id"],
                "title": tmdb.get("title") or x.get("title") or "Untitled",
                "poster_url": tmdb.get("poster_url"),
                "vote_average": tmdb.get("vote_average"),
            })
    return cards


def parse_tmdb_search_to_cards(data, keyword: str, limit: int = 24):
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
            raw_items.append({
                "tmdb_id": int(tmdb_id),
                "title": title,
                "poster_url": f"{TMDB_IMG}{poster_path}" if poster_path else None,
                "release_date": m.get("release_date", ""),
                "vote_average": m.get("vote_average"),
            })
    elif isinstance(data, list):
        raw_items = []
        for m in data:
            tmdb_id = m.get("tmdb_id") or m.get("id")
            title = (m.get("title") or "").strip()
            if not title or not tmdb_id:
                continue
            raw_items.append({
                "tmdb_id": int(tmdb_id),
                "title": title,
                "poster_url": m.get("poster_url"),
                "release_date": m.get("release_date", ""),
                "vote_average": m.get("vote_average"),
            })
    else:
        return [], []

    matched = [x for x in raw_items if keyword_l in x["title"].lower()]
    final_list = matched if matched else raw_items

    suggestions = []
    for x in final_list[:10]:
        year = (x.get("release_date") or "")[:4]
        label = f"{x['title']} ({year})" if year else x["title"]
        suggestions.append((label, x["tmdb_id"]))

    cards = [
        {"tmdb_id": x["tmdb_id"], "title": x["title"],
         "poster_url": x["poster_url"], "vote_average": x.get("vote_average")}
        for x in final_list[:limit]
    ]
    return suggestions, cards


# =============================
# SIDEBAR
# =============================
with st.sidebar:
    st.markdown(
        "<div style='font-family:Playfair Display,serif;font-size:1.3rem;"
        "font-weight:700;color:#e8b84b;margin-bottom:4px'>🎬 CineScope</div>",
        unsafe_allow_html=True,
    )
    st.markdown(
        "<div style='color:#7a7590;font-size:0.75rem;letter-spacing:2px;"
        "text-transform:uppercase;margin-bottom:16px'>Navigation</div>",
        unsafe_allow_html=True,
    )

    if st.button("🏠  Home"):
        goto_home()
    if st.button("📊  Analytics"):
        goto_analytics()

    st.divider()
    st.markdown(
        "<div style='color:#7a7590;font-size:0.78rem;text-transform:uppercase;"
        "letter-spacing:1px;margin-bottom:8px'>Home Feed</div>",
        unsafe_allow_html=True,
    )
    home_category = st.selectbox(
        "Category",
        ["trending", "popular", "top_rated", "now_playing", "upcoming"],
        index=0,
        label_visibility="collapsed",
    )
    grid_cols = st.slider("Grid columns", 4, 8, 6)

    st.divider()
    # Mini stats
    total_rated = len(st.session_state.user_ratings)
    total_reviewed = sum(len(v) for v in st.session_state.reviews.values())
    st.markdown(
        f"<div style='color:#7a7590;font-size:0.78rem'>Your Activity</div>"
        f"<div style='color:#e8b84b;font-size:1.1rem;font-weight:600'>{total_rated} rated · {total_reviewed} reviews</div>",
        unsafe_allow_html=True,
    )


# =============================
# HEADER
# =============================
col_title, col_right = st.columns([3, 1])
with col_title:
    st.markdown("<p class='site-title'>CineScope</p>", unsafe_allow_html=True)
    st.markdown(
        "<p class='site-sub'>Discover · Rate · Review</p>", unsafe_allow_html=True
    )
st.divider()


# ==========================================================
# VIEW: ANALYTICS DASHBOARD
# ==========================================================
if st.session_state.view == "analytics":
    st.markdown(
        "<div class='analytics-header'>📊 Your Analytics Dashboard</div>",
        unsafe_allow_html=True,
    )

    # ── Metrics Row ──
    total_rated = len(st.session_state.user_ratings)
    total_reviewed = sum(len(v) for v in st.session_state.reviews.values())
    avg_rating = (
        round(sum(st.session_state.user_ratings.values()) / total_rated, 1)
        if total_rated > 0 else 0
    )
    top_score = (
        max(st.session_state.user_ratings.values()) if total_rated > 0 else 0
    )

    m1, m2, m3, m4 = st.columns(4)
    for col, val, label in [
        (m1, total_rated, "Movies Rated"),
        (m2, total_reviewed, "Reviews Written"),
        (m3, f"{avg_rating}★", "Avg Rating Given"),
        (m4, f"{top_score}★", "Highest Rating"),
    ]:
        with col:
            st.markdown(
                f"<div class='metric-card'>"
                f"<div class='metric-value'>{val}</div>"
                f"<div class='metric-label'>{label}</div>"
                f"</div>",
                unsafe_allow_html=True,
            )

    st.divider()

    col_left, col_right = st.columns([1, 1], gap="large")

    with col_left:
        st.markdown("#### ⭐ Your Ratings Distribution")
        if total_rated > 0:
            buckets = {1: 0, 2: 0, 3: 0, 4: 0, 5: 0}
            for v in st.session_state.user_ratings.values():
                bucket = min(5, max(1, round(v)))
                buckets[bucket] = buckets.get(bucket, 0) + 1

            for star in range(5, 0, -1):
                count = buckets.get(star, 0)
                pct = int((count / total_rated) * 100) if total_rated > 0 else 0
                bar_html = (
                    f"<div style='display:flex;align-items:center;gap:10px;margin:5px 0'>"
                    f"<span style='color:#f5c518;width:50px;font-size:0.85rem'>{'★'*star}</span>"
                    f"<div style='background:#1a1a26;border-radius:4px;height:10px;flex:1'>"
                    f"<div style='background:linear-gradient(90deg,#e8b84b,#f5c518);"
                    f"border-radius:4px;height:10px;width:{pct}%'></div></div>"
                    f"<span style='color:#7a7590;font-size:0.8rem;width:30px'>{count}</span>"
                    f"</div>"
                )
                st.markdown(bar_html, unsafe_allow_html=True)
        else:
            st.markdown(
                "<div style='color:#7a7590;padding:20px 0'>Rate some movies to see your distribution.</div>",
                unsafe_allow_html=True,
            )

    with col_right:
        st.markdown("#### 📝 Your Recent Reviews")
        all_reviews = []
        for mid, revs in st.session_state.reviews.items():
            for rev in revs:
                all_reviews.append({**rev, "tmdb_id": mid})
        all_reviews.sort(key=lambda x: x.get("date", ""), reverse=True)

        if all_reviews:
            for rev in all_reviews[:5]:
                st.markdown(
                    f"<div class='review-card'>"
                    f"<div style='display:flex;justify-content:space-between'>"
                    f"<span class='reviewer-name'>{rev.get('name','Anonymous')}</span>"
                    f"<span class='stars' style='font-size:0.8rem'>{'★'*int(rev.get('rating',0))}{'☆'*(5-int(rev.get('rating',0)))}</span>"
                    f"</div>"
                    f"<div class='review-date'>{rev.get('date','')}</div>"
                    f"<div class='review-text'>{rev.get('text','')}</div>"
                    f"</div>",
                    unsafe_allow_html=True,
                )
        else:
            st.markdown(
                "<div style='color:#7a7590;padding:20px 0'>No reviews yet. Open a movie and leave a review!</div>",
                unsafe_allow_html=True,
            )

    st.divider()
    st.markdown("#### 🏆 Your Top Rated Movies")
    if st.session_state.user_ratings:
        sorted_ratings = sorted(
            st.session_state.user_ratings.items(), key=lambda x: x[1], reverse=True
        )[:10]
        for rank, (mid, score) in enumerate(sorted_ratings, 1):
            st.markdown(
                f"<div style='display:flex;align-items:center;gap:12px;padding:8px 0;"
                f"border-bottom:1px solid rgba(255,255,255,0.05)'>"
                f"<span style='color:#e8b84b;font-family:Playfair Display,serif;"
                f"font-size:1.1rem;font-weight:700;width:28px'>#{rank}</span>"
                f"<span style='color:#f0ece4'>Movie ID: {mid}</span>"
                f"<span style='color:#f5c518;margin-left:auto'>{'★'*int(score)}{'☆'*(5-int(score))} {score}/5</span>"
                f"</div>",
                unsafe_allow_html=True,
            )
    else:
        st.markdown(
            "<div style='color:#7a7590'>Rate movies to see your top picks here.</div>",
            unsafe_allow_html=True,
        )

    st.stop()


# ==========================================================
# VIEW: HOME
# ==========================================================
if st.session_state.view == "home":
    typed = st.text_input(
        "Search by movie title",
        placeholder="🔍  Type: avengers, batman, love...",
        label_visibility="collapsed",
    )
    st.divider()

    if typed.strip():
        if len(typed.strip()) < 2:
            st.caption("Type at least 2 characters.")
        else:
            data, err = api_get_json("/tmdb/search", params={"query": typed.strip()})
            if err or data is None:
                st.error(f"Search failed: {err}")
            else:
                suggestions, cards = parse_tmdb_search_to_cards(data, typed.strip(), limit=24)

                if suggestions:
                    labels = ["-- Select a movie --"] + [s[0] for s in suggestions]
                    selected = st.selectbox("Suggestions", labels, index=0, label_visibility="collapsed")
                    if selected != "-- Select a movie --":
                        label_to_id = {s[0]: s[1] for s in suggestions}
                        goto_details(label_to_id[selected])
                else:
                    st.info("No suggestions found.")

                st.markdown(
                    f"<div style='color:#7a7590;font-size:0.85rem;margin-bottom:12px'>"
                    f"Found <b style='color:#e8b84b'>{len(cards)}</b> results for "
                    f"<b style='color:#f0ece4'>\"{typed}\"</b></div>",
                    unsafe_allow_html=True,
                )
                poster_grid(cards, cols=grid_cols, key_prefix="search", show_rating=True)
        st.stop()

    st.markdown(
        f"<div style='font-family:Playfair Display,serif;font-size:1.3rem;"
        f"color:#f0ece4;margin-bottom:16px'>"
        f"{home_category.replace('_',' ').title()}</div>",
        unsafe_allow_html=True,
    )

    home_cards, err = api_get_json("/home", params={"category": home_category, "limit": 24})
    if err or not home_cards:
        st.error(f"Home feed failed: {err or 'Unknown error'}")
        st.stop()

    poster_grid(home_cards, cols=grid_cols, key_prefix="home_feed", show_rating=True)


# ==========================================================
# VIEW: DETAILS
# ==========================================================
elif st.session_state.view == "details":
    tmdb_id = st.session_state.selected_tmdb_id
    if not tmdb_id:
        st.warning("No movie selected.")
        if st.button("← Back"):
            goto_home()
        st.stop()

    if st.button("← Back to Home"):
        goto_home()

    data, err = api_get_json(f"/movie/id/{tmdb_id}")
    if err or not data:
        st.error(f"Could not load details: {err or 'Unknown error'}")
        st.stop()

    # ── MAIN LAYOUT ──
    left, right = st.columns([1, 2.5], gap="large")

    with left:
        if data.get("poster_url"):
            st.image(data["poster_url"], use_container_width=True)
        else:
            st.markdown(
                "<div style='background:#1a1a26;border-radius:12px;height:380px;"
                "display:flex;align-items:center;justify-content:center;"
                "color:#7a7590;font-size:3rem'>🎬</div>",
                unsafe_allow_html=True,
            )

    with right:
        title = data.get("title", "Untitled")
        release = (data.get("release_date") or "")[:4]
        vote_avg = data.get("vote_average") or 0
        vote_cnt = data.get("vote_count") or 0
        runtime = data.get("runtime")
        genres = data.get("genres", [])
        overview = data.get("overview") or "No overview available."

        st.markdown(
            f"<h1 style='margin-bottom:4px'>{title}"
            f"<span style='color:#7a7590;font-size:1.2rem;font-weight:400;margin-left:10px'>({release})</span>"
            f"</h1>",
            unsafe_allow_html=True,
        )

        # Genres
        if genres:
            pills = "".join(
                f"<span class='genre-pill'>{g['name']}</span>"
                for g in genres
            )
            st.markdown(f"<div style='margin:8px 0'>{pills}</div>", unsafe_allow_html=True)

        # Rating badge + star display
        if vote_avg:
            st.markdown(
                f"<div style='margin:12px 0'>"
                f"{rating_badge_html(vote_avg, vote_cnt)}"
                f"<div style='margin-top:6px'>{stars_html(vote_avg)}</div>"
                f"</div>",
                unsafe_allow_html=True,
            )
            render_rating_bars(vote_avg)

        if runtime:
            st.markdown(
                f"<div style='color:#7a7590;font-size:0.85rem;margin-top:8px'>🕐 {runtime} min</div>",
                unsafe_allow_html=True,
            )

        st.markdown("---")
        st.markdown(
            f"<div style='color:#c8c4be;font-size:0.95rem;line-height:1.65'>{overview}</div>",
            unsafe_allow_html=True,
        )

    if data.get("backdrop_url"):
        st.markdown(
            "<div style='margin-top:24px;border-radius:12px;overflow:hidden'>",
            unsafe_allow_html=True,
        )
        st.image(data["backdrop_url"], use_column_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

    st.divider()

    # ── TABS: Recommendations | Rate & Review ──
    tab1, tab2 = st.tabs(["✅ Recommendations", "⭐ Rate & Review"])

    # ── TAB 1: Recommendations ──
    with tab1:
        title_str = (data.get("title") or "").strip()
        if title_str:
            bundle, err2 = api_get_json(
                "/movie/search",
                params={"query": title_str, "tfidf_top_n": 12, "genre_limit": 12},
            )
            if not err2 and bundle:
                st.markdown(
                    "<div style='font-family:Playfair Display,serif;font-size:1.15rem;"
                    "color:#e8b84b;margin-bottom:12px'>🔎 Similar Movies</div>",
                    unsafe_allow_html=True,
                )
                poster_grid(
                    to_cards_from_tfidf_items(bundle.get("tfidf_recommendations")),
                    cols=grid_cols,
                    key_prefix="tfidf",
                    show_rating=True,
                )
                st.markdown(
                    "<div style='font-family:Playfair Display,serif;font-size:1.15rem;"
                    "color:#e8b84b;margin:20px 0 12px'>🎭 More in Genre</div>",
                    unsafe_allow_html=True,
                )
                poster_grid(
                    bundle.get("genre_recommendations", []),
                    cols=grid_cols,
                    key_prefix="genre",
                    show_rating=True,
                )
            else:
                genre_only, err3 = api_get_json(
                    "/recommend/genre", params={"tmdb_id": tmdb_id, "limit": 18}
                )
                if not err3 and genre_only:
                    poster_grid(genre_only, cols=grid_cols, key_prefix="genre_fb", show_rating=True)
                else:
                    st.warning("No recommendations available right now.")

    # ── TAB 2: Rate & Review ──
    with tab2:
        col_rate, col_review = st.columns([1, 1.6], gap="large")

        with col_rate:
            st.markdown(
                "<div style='font-family:Playfair Display,serif;font-size:1.1rem;"
                "color:#f0ece4;margin-bottom:12px'>Your Rating</div>",
                unsafe_allow_html=True,
            )

            current_rating = st.session_state.user_ratings.get(tmdb_id, 0.0)

            user_score = st.slider(
                "Rate this movie",
                min_value=0.0,
                max_value=5.0,
                value=float(current_rating),
                step=0.5,
                label_visibility="collapsed",
            )

            # Live star preview
            filled = int(user_score)
            half = 1 if (user_score - filled) == 0.5 else 0
            empty = 5 - filled - half
            star_preview = "★" * filled + ("½" if half else "") + "☆" * empty
            st.markdown(
                f"<div style='color:#f5c518;font-size:1.8rem;letter-spacing:3px;"
                f"margin:8px 0'>{star_preview}</div>"
                f"<div style='color:#7a7590;font-size:0.85rem'>{user_score}/5.0</div>",
                unsafe_allow_html=True,
            )

            if st.button("💾 Save Rating", use_container_width=True):
                st.session_state.user_ratings[tmdb_id] = user_score
                st.success(f"Rating saved: {user_score}/5 ⭐")

            # TMDB rating comparison
            if vote_avg:
                st.markdown(
                    f"<div style='margin-top:16px;padding:12px;background:#1a1a26;"
                    f"border-radius:10px;border:1px solid rgba(255,255,255,0.06)'>"
                    f"<div style='color:#7a7590;font-size:0.75rem;text-transform:uppercase;"
                    f"letter-spacing:1px'>TMDB Average</div>"
                    f"<div style='color:#f5c518;font-size:1.4rem;font-weight:600'>{vote_avg:.1f}/10</div>"
                    f"<div style='color:#7a7590;font-size:0.78rem'>{vote_cnt:,} votes</div>"
                    f"</div>",
                    unsafe_allow_html=True,
                )

        with col_review:
            st.markdown(
                "<div style='font-family:Playfair Display,serif;font-size:1.1rem;"
                "color:#f0ece4;margin-bottom:12px'>Write a Review</div>",
                unsafe_allow_html=True,
            )

            reviewer_name = st.text_input("Your name", placeholder="Enter your name", key=f"name_{tmdb_id}")
            review_stars = st.select_slider(
                "Review rating",
                options=[1, 2, 3, 4, 5],
                value=3,
                format_func=lambda x: "★" * x + "☆" * (5 - x),
                key=f"rev_stars_{tmdb_id}",
            )
            review_text = st.text_area(
                "Your review",
                placeholder="Share your thoughts about this movie...",
                height=110,
                key=f"rev_text_{tmdb_id}",
            )

            if st.button("📝 Submit Review", use_container_width=True, key=f"submit_{tmdb_id}"):
                if not reviewer_name.strip():
                    st.warning("Please enter your name.")
                elif not review_text.strip():
                    st.warning("Please write something in your review.")
                else:
                    if tmdb_id not in st.session_state.reviews:
                        st.session_state.reviews[tmdb_id] = []
                    st.session_state.reviews[tmdb_id].append({
                        "name": reviewer_name.strip(),
                        "rating": review_stars,
                        "text": review_text.strip(),
                        "date": datetime.now().strftime("%b %d, %Y"),
                    })
                    st.success("Review submitted! 🎉")
                    st.rerun()

        # ── Existing reviews for this movie ──
        movie_reviews = st.session_state.reviews.get(tmdb_id, [])
        if movie_reviews:
            st.markdown("---")
            st.markdown(
                f"<div style='font-family:Playfair Display,serif;font-size:1.1rem;"
                f"color:#f0ece4;margin-bottom:12px'>"
                f"Community Reviews <span style='color:#7a7590;font-size:0.85rem'>"
                f"({len(movie_reviews)})</span></div>",
                unsafe_allow_html=True,
            )
            # Summary
            avg_user = sum(r["rating"] for r in movie_reviews) / len(movie_reviews)
            st.markdown(
                f"<div style='color:#f5c518;font-size:1.1rem;margin-bottom:12px'>"
                f"{'★'*round(avg_user)}{'☆'*(5-round(avg_user))} "
                f"<span style='color:#7a7590;font-size:0.85rem'>"
                f"{avg_user:.1f} avg from {len(movie_reviews)} review(s)</span></div>",
                unsafe_allow_html=True,
            )

            for rev in reversed(movie_reviews):
                stars_filled = "★" * rev["rating"] + "☆" * (5 - rev["rating"])
                st.markdown(
                    f"<div class='review-card'>"
                    f"<div style='display:flex;justify-content:space-between;align-items:center'>"
                    f"<span class='reviewer-name'>{rev['name']}</span>"
                    f"<span style='color:#f5c518;font-size:0.9rem'>{stars_filled}</span>"
                    f"</div>"
                    f"<div class='review-date'>{rev['date']}</div>"
                    f"<div class='review-text'>{rev['text']}</div>"
                    f"</div>",
                    unsafe_allow_html=True,
                )
        else:
            st.markdown(
                "<div style='color:#7a7590;font-size:0.88rem;margin-top:16px'>"
                "No reviews yet for this movie. Be the first! 🎬</div>",
                unsafe_allow_html=True,
            )
