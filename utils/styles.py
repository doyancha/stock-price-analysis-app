import streamlit as st


def inject_css():
    st.markdown("""
    <style>
    /* ── Google Fonts ── */
    @import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@300;400;500;600;700&family=Space+Grotesk:wght@400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap');

    /* ── Root palette ── */
    :root {
        --navy:   #060d1f;
        --navy2:  #0b1630;
        --panel:  #0f1e3d;
        --card:   #132040;
        --border: #1e3058;
        --cyan:   #00e5ff;
        --cyan2:  #38bdf8;
        --purple: #a78bfa;
        --green:  #34d399;
        --red:    #f87171;
        --amber:  #fbbf24;
        --text1:  #e2e8f0;
        --text2:  #94a3b8;
        --text3:  #64748b;
    }

    /* ── Base ── */
    html, body, [data-testid="stAppViewContainer"] {
        background: var(--navy) !important;
        font-family: 'DM Sans', sans-serif;
        color: var(--text1);
    }
    [data-testid="stSidebar"] {
        background: var(--navy2) !important;
        border-right: 1px solid var(--border);
    }
    [data-testid="stSidebar"] > div:first-child { padding-top: 0; }

    /* ── Hide default decorations ── */
    #MainMenu, footer { visibility: hidden; }
    [data-testid="stDecoration"] { display: none; }
    header[data-testid="stHeader"] {
        background: transparent !important;
        height: 0 !important;
    }
    [data-testid="collapsedControl"] {
        display: flex !important;
        visibility: visible !important;
        position: fixed;
        top: 0.85rem;
        left: 0.85rem;
        z-index: 1000;
        background: var(--card) !important;
        border: 1px solid var(--border) !important;
        border-radius: 10px;
        box-shadow: 0 8px 24px rgba(0,0,0,0.25);
    }
    [data-testid="collapsedControl"] button {
        color: var(--text1) !important;
    }
    .block-container { padding-top: 1.5rem; padding-bottom: 2rem; max-width: 1280px; }

    /* ── Scrollbar ── */
    ::-webkit-scrollbar { width: 6px; }
    ::-webkit-scrollbar-track { background: var(--navy2); }
    ::-webkit-scrollbar-thumb { background: var(--border); border-radius: 3px; }

    /* ─────────────────────────────────────────────────────────
       SIDEBAR CARDS
    ───────────────────────────────────────────────────────── */
    .sb-project-card {
        background: linear-gradient(135deg, #0a1628 0%, #0e2347 60%, #0d1f3c 100%);
        border: 1px solid var(--border);
        border-top: 2px solid var(--cyan);
        border-radius: 12px;
        padding: 18px 16px 14px;
        margin: 0 0 6px 0;
        box-shadow: 0 0 20px rgba(0,229,255,0.08);
        text-align: center;
    }
    .sb-project-badge {
        display: inline-block;
        background: rgba(0,229,255,0.12);
        border: 1px solid rgba(0,229,255,0.3);
        border-radius: 20px;
        padding: 3px 10px;
        font-size: 0.68rem;
        color: var(--cyan);
        letter-spacing: 1.5px;
        text-transform: uppercase;
        font-family: 'JetBrains Mono', monospace;
        margin-bottom: 8px;
    }
    .sb-project-title {
        font-family: 'Space Grotesk', sans-serif;
        font-size: 1.1rem;
        font-weight: 700;
        color: var(--text1);
        margin: 4px 0 3px;
        letter-spacing: 0.3px;
    }
    .sb-project-tag {
        font-size: 0.72rem;
        color: var(--text2);
        line-height: 1.4;
    }

    .sb-contact-card {
        background: linear-gradient(180deg, rgba(10,22,40,0.98) 0%, rgba(12,26,49,0.98) 100%);
        border: 1px solid var(--border);
        border-radius: 14px;
        padding: 12px;
        margin: 6px 0 4px 0;
        box-shadow: 0 12px 24px rgba(0,0,0,0.16);
    }
    .sb-contact-title {
        font-size: 0.62rem;
        color: var(--text3);
        text-transform: uppercase;
        letter-spacing: 1.6px;
        font-family: 'JetBrains Mono', monospace;
        margin-bottom: 10px;
        text-align: left;
    }
    .sb-contact-head {
        display: flex;
        align-items: center;
        gap: 10px;
        text-align: left;
        margin-bottom: 12px;
    }
    .sb-contact-photo {
        width: 44px;
        height: 44px;
        object-fit: cover;
        object-position: center 18%;
        border-radius: 50%;
        border: 1px solid rgba(0,229,255,0.24);
        box-shadow: 0 8px 18px rgba(0,0,0,0.2);
        margin-bottom: 0;
        background: rgba(255,255,255,0.05);
        flex-shrink: 0;
    }
    .sb-contact-meta {
        min-width: 0;
    }
    .sb-contact-name {
        font-family: 'Space Grotesk', sans-serif;
        font-size: 0.84rem;
        font-weight: 700;
        color: var(--text1);
        margin-bottom: 2px;
        line-height: 1.2;
    }
    .sb-contact-role {
        font-size: 0.68rem;
        color: var(--text2);
        font-family: 'JetBrains Mono', monospace;
        letter-spacing: 0.4px;
    }
    .sb-contact-status {
        margin-top: 7px;
        display: inline-flex;
        align-items: center;
        gap: 6px;
        padding: 3px 8px;
        border-radius: 999px;
        background: rgba(0,229,255,0.06);
        border: 1px solid rgba(0,229,255,0.16);
        color: var(--cyan);
        font-size: 0.6rem;
        font-family: 'JetBrains Mono', monospace;
        letter-spacing: 0.7px;
        text-transform: uppercase;
    }
    .sb-contact-status-dot {
        width: 6px;
        height: 6px;
        border-radius: 50%;
        background: var(--cyan);
        box-shadow: 0 0 8px rgba(0,229,255,0.6);
    }
    .sb-contact-grid {
        display: flex;
        flex-direction: column;
        gap: 6px;
    }
    .sb-contact-link {
        display: flex;
        align-items: center;
        justify-content: space-between;
        gap: 8px;
        min-height: 36px;
        padding: 7px 10px;
        border-radius: 9px;
        color: var(--text2) !important;
        font-size: 0.74rem;
        font-weight: 600;
        text-decoration: none !important;
        transition: all 0.2s ease;
        margin-bottom: 0;
        border: 1px solid rgba(30,48,88,0.78);
        background: rgba(255,255,255,0.03);
    }
    .sb-contact-link:hover {
        transform: translateY(-1px);
        background: rgba(255,255,255,0.06);
        color: var(--text1) !important;
    }
    .sb-contact-link.github { border-left: 2px solid var(--cyan); }
    .sb-contact-link.linkedin { border-left: 2px solid var(--purple); }
    .sb-contact-link.email { border-left: 2px solid var(--green); }
    .sb-contact-link.repo { border-left: 2px solid var(--amber); }
    .sb-contact-link-main {
        display: inline-flex;
        align-items: center;
        gap: 8px;
    }
    .sb-contact-icon {
        font-size: 0.68rem;
        width: 18px;
        height: 18px;
        display: inline-flex;
        align-items: center;
        justify-content: center;
        border-radius: 50%;
        background: rgba(255,255,255,0.06);
        text-align: center;
        opacity: 0.95;
    }
    .sb-contact-arrow {
        color: var(--text3);
        font-size: 0.8rem;
        line-height: 1;
    }

    /* ─────────────────────────────────────────────────────────
       NAV MENU
    ───────────────────────────────────────────────────────── */
    .nav-section-label {
        font-size: 0.62rem;
        color: var(--text3);
        text-transform: uppercase;
        letter-spacing: 2px;
        font-family: 'JetBrains Mono', monospace;
        padding: 12px 4px 4px;
    }

    /* ─────────────────────────────────────────────────────────
       HERO BANNERS
    ───────────────────────────────────────────────────────── */
    .hero {
        background: linear-gradient(135deg, #060d1f 0%, #0b1a3d 50%, #071630 100%);
        border: 1px solid var(--border);
        border-left: 3px solid var(--cyan);
        border-radius: 16px;
        padding: 36px 40px 32px;
        margin-bottom: 28px;
        position: relative;
        overflow: hidden;
        text-align: center;
        display: flex;
        flex-direction: column;
        align-items: center;
    }
    .hero::before {
        content: '';
        position: absolute; top: 0; right: 0;
        width: 300px; height: 300px;
        background: radial-gradient(circle, rgba(0,229,255,0.04) 0%, transparent 70%);
        pointer-events: none;
    }
    .hero-eyebrow {
        display: block;
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.68rem;
        color: var(--cyan);
        letter-spacing: 2.5px;
        text-transform: uppercase;
        margin-bottom: 10px;
        text-align: center;
    }
    .hero h1 {
        font-family: 'Space Grotesk', sans-serif;
        font-size: 2.2rem;
        font-weight: 700;
        color: var(--text1);
        margin: 0 auto 10px;
        max-width: 700px;
        line-height: 1.15;
        text-align: center;
    }
    .hero h1 span { color: var(--cyan); }
    .hero-sub {
        font-size: 1rem;
        color: var(--text2);
        max-width: 900px;
        line-height: 1.6;
        margin-left: auto;
        margin-right: auto;
        margin-bottom: 18px;
        text-align: center;
        text-wrap: balance;
    }
    .hero-badges { display: flex; gap: 8px; flex-wrap: wrap; justify-content: center; align-items: center; }
    .hero-badge {
        background: rgba(255,255,255,0.05);
        border: 1px solid var(--border);
        border-radius: 20px;
        padding: 4px 12px;
        font-size: 0.72rem;
        color: var(--text2);
        font-family: 'JetBrains Mono', monospace;
    }
    .hero-badge.cyan  { border-color: rgba(0,229,255,0.3);  color: var(--cyan);   background: rgba(0,229,255,0.07); }
    .hero-badge.purple{ border-color: rgba(167,139,250,0.3); color: var(--purple); background: rgba(167,139,250,0.07); }
    .hero-badge.green { border-color: rgba(52,211,153,0.3);  color: var(--green);  background: rgba(52,211,153,0.07); }
    .hero-badge.amber { border-color: rgba(251,191,36,0.3);  color: var(--amber);  background: rgba(251,191,36,0.07); }
    .hero-badge.red   { border-color: rgba(248,113,113,0.3); color: var(--red);    background: rgba(248,113,113,0.07); }

    /* ─────────────────────────────────────────────────────────
       KPI CARDS
    ───────────────────────────────────────────────────────── */
    .kpi-grid { display: grid; gap: 14px; }
    .kpi-card {
        background: var(--card);
        border: 1px solid var(--border);
        border-radius: 12px;
        padding: 18px 20px;
        position: relative;
        overflow: hidden;
        transition: transform 0.2s, box-shadow 0.2s;
        text-align: center;
        min-height: 164px;
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
        gap: 4px;
    }
    .kpi-card:hover { transform: translateY(-2px); box-shadow: 0 8px 24px rgba(0,0,0,0.3); }
    .kpi-card::after {
        content: '';
        position: absolute; top: 0; left: 0; right: 0;
        height: 2px;
    }
    .kpi-card.cyan::after   { background: var(--cyan); box-shadow: 0 0 8px var(--cyan); }
    .kpi-card.purple::after { background: var(--purple); box-shadow: 0 0 8px var(--purple); }
    .kpi-card.green::after  { background: var(--green); box-shadow: 0 0 8px var(--green); }
    .kpi-card.amber::after  { background: var(--amber); box-shadow: 0 0 8px var(--amber); }
    .kpi-card.red::after    { background: var(--red); box-shadow: 0 0 8px var(--red); }
    .kpi-icon { font-size: 1.4rem; margin-bottom: 6px; }
    .kpi-label { font-size: 0.7rem; color: var(--text3); text-transform: uppercase; letter-spacing: 1.2px; font-family: 'JetBrains Mono', monospace; }
    .kpi-value { font-family: 'Space Grotesk', sans-serif; font-size: 1.6rem; font-weight: 700; color: var(--text1); line-height: 1.1; margin: 4px 0 2px; }
    .kpi-delta { font-size: 0.75rem; color: var(--text2); min-height: 1.2em; }
    .kpi-delta.up   { color: var(--green); }
    .kpi-delta.down { color: var(--red); }

    /* ─────────────────────────────────────────────────────────
       INSIGHT / CALLOUT BOXES
    ───────────────────────────────────────────────────────── */
    .insight-box {
        border-radius: 12px;
        padding: 18px 20px;
        margin: 16px 0;
        border-left: 3px solid;
    }
    .insight-box.cyan   { background: rgba(0,229,255,0.05);   border-color: var(--cyan);   }
    .insight-box.purple { background: rgba(167,139,250,0.05); border-color: var(--purple); }
    .insight-box.green  { background: rgba(52,211,153,0.05);  border-color: var(--green);  }
    .insight-box.amber  { background: rgba(251,191,36,0.05);  border-color: var(--amber);  }
    .insight-box.red    { background: rgba(248,113,113,0.05); border-color: var(--red);    }
    .insight-box-label {
        font-size: 0.65rem;
        text-transform: uppercase;
        letter-spacing: 1.5px;
        font-family: 'JetBrains Mono', monospace;
        margin-bottom: 6px;
    }
    .insight-box.cyan   .insight-box-label { color: var(--cyan); }
    .insight-box.purple .insight-box-label { color: var(--purple); }
    .insight-box.green  .insight-box-label { color: var(--green); }
    .insight-box.amber  .insight-box-label { color: var(--amber); }
    .insight-box.red    .insight-box-label { color: var(--red); }
    .insight-box p { font-size: 0.88rem; color: var(--text2); margin: 0; line-height: 1.6; }

    /* ─────────────────────────────────────────────────────────
       CHART CONTAINERS
    ───────────────────────────────────────────────────────── */
    .chart-card {
        background: var(--card);
        border: 1px solid var(--border);
        border-radius: 14px;
        padding: 22px 20px 12px;
        margin-bottom: 20px;
        text-align: center;
    }
    .chart-title {
        font-family: 'Space Grotesk', sans-serif;
        font-size: 0.9rem;
        font-weight: 600;
        color: var(--text1);
        margin-bottom: 4px;
        text-align: center;
    }
    .chart-sub {
        font-size: 0.75rem;
        color: var(--text3);
        margin-bottom: 16px;
        font-family: 'JetBrains Mono', monospace;
        text-align: center;
    }

    /* ─────────────────────────────────────────────────────────
       SECTION DIVIDER
    ───────────────────────────────────────────────────────── */
    .section-divider {
        border: none;
        border-top: 1px solid var(--border);
        margin: 28px 0;
    }

    /* ─────────────────────────────────────────────────────────
       GLOWING BUTTONS  (injected via HTML/markdown)
    ───────────────────────────────────────────────────────── */
    .glow-btn {
        display: inline-flex;
        align-items: center;
        gap: 7px;
        padding: 9px 20px;
        border-radius: 8px;
        font-size: 0.82rem;
        font-weight: 600;
        font-family: 'DM Sans', sans-serif;
        text-decoration: none !important;
        cursor: pointer;
        transition: all 0.2s;
    }
    .glow-btn.cyan {
        background: rgba(0,229,255,0.1);
        border: 1px solid rgba(0,229,255,0.4);
        color: var(--cyan) !important;
        box-shadow: 0 0 10px rgba(0,229,255,0.15);
    }
    .glow-btn.cyan:hover {
        background: rgba(0,229,255,0.18);
        box-shadow: 0 0 18px rgba(0,229,255,0.3);
    }
    .glow-btn.purple {
        background: rgba(167,139,250,0.1);
        border: 1px solid rgba(167,139,250,0.4);
        color: var(--purple) !important;
        box-shadow: 0 0 10px rgba(167,139,250,0.15);
    }
    .glow-btn.purple:hover {
        background: rgba(167,139,250,0.18);
        box-shadow: 0 0 18px rgba(167,139,250,0.3);
    }
    .glow-btn.green {
        background: rgba(52,211,153,0.1);
        border: 1px solid rgba(52,211,153,0.4);
        color: var(--green) !important;
        box-shadow: 0 0 10px rgba(52,211,153,0.12);
    }
    .glow-btn.green:hover {
        background: rgba(52,211,153,0.18);
        box-shadow: 0 0 18px rgba(52,211,153,0.28);
    }
    .btn-row { display: flex; gap: 10px; flex-wrap: wrap; margin-top: 6px; }

    /* ─────────────────────────────────────────────────────────
       DATA TABLE
    ───────────────────────────────────────────────────────── */
    [data-testid="stDataFrame"] { border: 1px solid var(--border) !important; border-radius: 10px !important; overflow: hidden; }
    .stDataFrame table { background: var(--card) !important; }

    /* ─────────────────────────────────────────────────────────
       SELECTBOX / MULTISELECT / SLIDER
    ───────────────────────────────────────────────────────── */
    [data-testid="stSelectbox"] > div > div,
    [data-testid="stMultiSelect"] > div > div {
        background: var(--panel) !important;
        border-color: var(--border) !important;
        color: var(--text1) !important;
    }

    /* ─────────────────────────────────────────────────────────
       DISCLAIMER BOX
    ───────────────────────────────────────────────────────── */
    .disclaimer {
        background: rgba(251,191,36,0.05);
        border: 1px solid rgba(251,191,36,0.2);
        border-radius: 10px;
        padding: 12px 16px;
        font-size: 0.78rem;
        color: var(--text2);
        line-height: 1.5;
        margin-top: 12px;
    }
    .disclaimer strong { color: var(--amber); }

    /* ─────────────────────────────────────────────────────────
       METRIC OVERRIDE
    ───────────────────────────────────────────────────────── */
    [data-testid="stMetric"] {
        background: var(--card);
        border: 1px solid var(--border);
        border-radius: 12px;
        padding: 14px 18px !important;
        text-align: center;
    }
    [data-testid="stMetricLabel"] { color: var(--text3) !important; font-size: 0.72rem !important; justify-content: center; }
    [data-testid="stMetricValue"] { color: var(--text1) !important; font-family: 'Space Grotesk', sans-serif !important; justify-content: center; }

    /* tabs */
    [data-testid="stTabs"] [data-baseweb="tab"] {
        color: var(--text2);
        font-size: 0.85rem;
    }
    [data-testid="stTabs"] [aria-selected="true"] {
        color: var(--cyan) !important;
        border-bottom-color: var(--cyan) !important;
    }

    /* expander */
    [data-testid="stExpander"] {
        background: var(--card) !important;
        border: 1px solid var(--border) !important;
        border-radius: 10px !important;
    }

    /* roadmap card */
    .roadmap-card {
        background: var(--card);
        border: 1px solid var(--border);
        border-radius: 12px;
        padding: 18px 20px;
        height: 100%;
        display: flex;
        flex-direction: column;
        justify-content: center;
    }
    .roadmap-card h4 {
        font-family: 'Space Grotesk', sans-serif;
        font-size: 0.9rem;
        font-weight: 600;
        color: var(--text1);
        margin: 0 0 6px;
        text-align: center;
    }
    .roadmap-card p {
        font-size: 0.8rem;
        color: var(--text2);
        margin: 0;
        line-height: 1.5;
    }
    .roadmap-tag {
        display: inline-block;
        background: rgba(167,139,250,0.1);
        border: 1px solid rgba(167,139,250,0.3);
        color: var(--purple);
        border-radius: 20px;
        padding: 2px 10px;
        font-size: 0.65rem;
        font-family: 'JetBrains Mono', monospace;
        margin-bottom: 8px;
        margin-left: auto;
        margin-right: auto;
        text-transform: uppercase;
        letter-spacing: 1px;
    }

    /* findings card */
    .finding-card {
        background: var(--card);
        border: 1px solid var(--border);
        border-radius: 12px;
        padding: 20px;
        height: 100%;
    }
    .finding-num {
        font-family: 'JetBrains Mono', monospace;
        font-size: 2rem;
        font-weight: 700;
        color: var(--border);
        line-height: 1;
        margin-bottom: 8px;
    }
    .finding-card h4 {
        font-family: 'Space Grotesk', sans-serif;
        font-size: 0.92rem;
        font-weight: 600;
        color: var(--text1);
        margin: 0 0 6px;
    }
    .finding-card p {
        font-size: 0.8rem;
        color: var(--text2);
        line-height: 1.55;
        margin: 0;
    }

    /* about tech pill */
    .tech-pill {
        display: inline-block;
        background: rgba(0,229,255,0.07);
        border: 1px solid rgba(0,229,255,0.2);
        border-radius: 20px;
        padding: 5px 14px;
        font-size: 0.75rem;
        color: var(--cyan2);
        font-family: 'JetBrains Mono', monospace;
        margin: 3px;
        text-decoration: none !important;
        transition: all 0.2s ease;
        cursor: pointer;
    }
    .tech-pill:hover {
        color: var(--text1);
        border-color: rgba(0,229,255,0.45);
        background: rgba(0,229,255,0.12);
    }

    .about-panel {
        background: var(--card);
        border: 1px solid var(--border);
        border-radius: 14px;
        padding: 28px 24px;
        min-height: 392px;
        height: 100%;
    }
    .about-panel.center {
        display: flex;
        flex-direction: column;
        justify-content: center;
        text-align: center;
    }
    .profile-photo {
        width: 118px;
        height: 118px;
        object-fit: cover;
        object-position: center 20%;
        border-radius: 50%;
        border: 3px solid rgba(0,229,255,0.28);
        box-shadow: 0 12px 28px rgba(0,0,0,0.25), 0 0 22px rgba(0,229,255,0.12);
        margin: 0 auto 14px;
        display: block;
        background: rgba(255,255,255,0.04);
    }
    .about-panel-title {
        font-family: 'Space Grotesk', sans-serif;
        font-size: 1rem;
        font-weight: 600;
        color: var(--text1);
        margin-bottom: 12px;
    }
    .about-panel-text {
        font-size: 0.85rem;
        color: var(--text2);
        line-height: 1.7;
        margin-bottom: 14px;
    }
    .about-panel-list {
        font-size: 0.82rem;
        color: var(--text2);
        line-height: 1.8;
    }

    </style>
    """, unsafe_allow_html=True)
