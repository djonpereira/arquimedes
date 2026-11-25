import streamlit as st


def load_styles() -> None:
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=DM+Serif+Display&display=swap');

    :html, body, [class*="css"] { font-family: 'DM Sans', sans-serif; }
    .stApp { background: #f5f7f3; }
    [data-testid="stSidebar"] { background: #17211d; }
    [data-testid="stSidebar"] * { color: #edf3ec; }
    [data-testid="stSidebar"] [role="radiogroup"] label { border-radius: 12px; padding: 10px 12px; }
    [data-testid="stSidebar"] [role="radiogroup"] label:has(input:checked) { background: #2b3b34; }
    .brand-mark { width: 42px; height: 42px; border: 1px solid #91aaa0; border-radius: 50%; display:grid; place-items:center; font: 25px 'DM Serif Display'; margin: 10px 0 8px; }
    .brand-name { letter-spacing: .18em; font-weight: 700; font-size: 13px; }
    .hero { min-height: 290px; border-radius: 24px; overflow:hidden; position:relative; padding: 54px 48px; background: linear-gradient(115deg, rgba(16,40,33,.92), rgba(16,40,33,.22)), radial-gradient(circle at 75% 40%, #c4d8aa 0 12%, #6f9781 13% 28%, #233f35 29% 54%, #0d211a 55%); }
    .court-hero { background: linear-gradient(115deg, rgba(20,48,39,.96), rgba(20,48,39,.42)), url("app/static/court.svg") center/cover no-repeat; }
    .hero h1 { color: white; font: 58px 'DM Serif Display', serif; max-width: 620px; line-height:.98; margin:0 0 18px; }
    .hero p { color: #dfe9e2; max-width: 520px; font-size:18px; }
    .eyebrow { color:#769489; font-size:12px; font-weight:800; letter-spacing:.16em; text-transform:uppercase; }
    .card { background:white; border:1px solid #dde5dc; border-radius:18px; padding:22px; height:100%; box-shadow: 0 8px 28px rgba(23,33,29,.05); }
    .card h3 { font: 25px 'DM Serif Display', serif; margin:8px 0; }
    .card p { color:#5d695f; }
    .coach-card { display:grid; grid-template-columns:120px 1fr; align-items:center; gap:18px; background:white; border:1px solid #dde5dc; border-radius:18px; padding:14px; min-height:190px; box-shadow: 0 8px 28px rgba(23,33,29,.05); }
    .coach-card img { width:100%; height:160px; object-fit:cover; border-radius:13px; }
    [data-testid="stImage"] img { object-fit: contain !important; border-radius:14px; }
    .coach-card h3 { font:26px 'DM Serif Display', serif; margin:7px 0; }
    .coach-card p { color:#5d695f; }
    .mission-card { min-height: 170px; transition: transform .2s ease, box-shadow .2s ease; }
    .mission-card:hover { transform: translateY(-4px); box-shadow: 0 14px 32px rgba(23,33,29,.10); }
    .mission-top { display:flex; justify-content:space-between; align-items:center; }
    .mission-number { display:grid; place-items:center; width:36px; height:36px; border-radius:50%; background:#e8efe9; color:#315844; font-weight:800; }
    .duration { font-size:12px; color:#7d8a82; }
    .lesson-title { font: 36px 'DM Serif Display', serif; }
    .quiz-card { background:white; border:1px solid #dde5dc; border-radius:20px; padding:28px; margin:8px 0 20px; box-shadow: 0 8px 28px rgba(23,33,29,.05); }
    .quiz-card h2 { font: 30px 'DM Serif Display', serif; margin:12px 0 8px; }
    .rank-track { display:flex; align-items:center; gap:8px; overflow-x:auto; margin:14px 0 4px; padding:10px 12px; border:1px solid #dde5dc; border-radius:999px; background:#fff; }
    .rank-track span { white-space:nowrap; font-size:11px; font-weight:800; letter-spacing:.08em; color:#769489; }
    .rank-track i { width:38px; min-width:38px; height:3px; border-radius:99px; background:#cfdbd1; }
    [data-testid="stAppViewContainer"] > .main { padding-top: 1.4rem; }
    .stButton > button { border-radius: 999px; border: 1px solid #9aac9f; font-weight:700; min-height:44px; }
    .stButton > button[kind="primary"] { background:#0f766e; border-color:#0f766e; }
    .shot-stage { height:260px; position:relative; overflow:hidden; border-radius:20px; background:linear-gradient(180deg,#dceae4 0 73%,#bd8050 74% 100%); border:1px solid #dde5dc; }
    .hoop { position:absolute; right:28px; top:54px; width:82px; height:44px; display:grid; place-items:center; border:7px solid #bc6d3b; border-top-width:10px; border-radius:8px 8px 50% 50%; color:#fff; font-size:11px; font-weight:900; background:#eae8dc; }
    .ball { position:absolute; left:40%; bottom:44px; width:52px; height:52px; display:grid; place-items:center; border-radius:50%; background:#c96f33; border:5px solid #75452c; color:transparent; box-shadow:0 8px 10px #603c2933; }
    .shot-made { animation:shot 1.15s cubic-bezier(.2,.7,.3,1) both; }
    @keyframes shot { 0%{left:40%;bottom:44px;transform:rotate(0)} 55%{left:63%;bottom:185px;transform:rotate(260deg)} 100%{left:75%;bottom:116px;transform:rotate(520deg);opacity:.25} }
    .shot-floor { position:absolute; left:-10%; bottom:-45px; width:120%; height:130px; border:4px solid #f4ead9; border-radius:50%; }
    .encourage-card { display:flex; justify-content:space-between; align-items:center; border-radius:14px; padding:14px 16px; margin:12px 0; }
    .encourage-card span { font-size:13px; }
    .encourage-card.made { background:#dff3df; border:1px solid #9fcda4; color:#315844; }
    .encourage-card.missed { background:#fff0dc; border:1px solid #dfbd83; color:#75562d; }
    .finish-card { border-radius:24px; padding:34px; margin:10px 0 18px; background:linear-gradient(135deg,#17382e,#315844); color:#fff; }
    .finish-card span { color:#e4c873; font-size:12px; font-weight:900; letter-spacing:.16em; }
    .finish-card h2 { font:36px 'DM Serif Display',serif; margin:8px 0; }
    .finish-card p { color:#dceae4; }
    .structure-map { border-radius:22px; background:#17382e; color:#fff; padding:24px; margin:16px 0 24px; text-align:center; }
    .structure-main { border:1px solid #719285; border-radius:16px; padding:16px; }
    .structure-main span { display:block; color:#e4c873; letter-spacing:.14em; font-size:12px; font-weight:900; }
    .structure-main b { display:block; font:28px 'DM Serif Display',serif; margin-top:4px; }
    .structure-arrow { color:#a9c4ba; font-size:28px; margin:4px 0; }
    .structure-options { display:grid; grid-template-columns:1fr 1fr; gap:12px; }
    .structure-options > div { background:#fff; color:#17382e; border-radius:14px; padding:16px; }
    .structure-options span { display:block; color:#769489; font-size:12px; font-weight:900; letter-spacing:.08em; }
    .structure-options b { display:block; margin:4px 0; }
    .structure-options small { color:#6a756f; }

    .study-card { border-radius:16px; padding:16px 18px; margin:8px 0 12px; border-left:6px solid; }
    .study-card h3 { margin:0 0 5px !important; font-size:19px !important; }
    .study-card p { margin:0; }
    .study-card.green { background:#e3f1e6; border-color:#609a68; }
    .study-card.orange { background:#fff0dc; border-color:#d38a3f; }
    .study-card.blue { background:#dfeaf5; border-color:#5d86a8; }
    .study-card.purple { background:#eee5f5; border-color:#80649a; }
    .study-card.pink { background:#f6e3e8; border-color:#b86a7d; }

    .example-card { background:#fff; border:1px solid #dde5dc; border-radius:14px; padding:16px; margin:8px 0 12px; box-shadow:0 5px 16px #17211d0d; }
    .example-card span { color:#80649a; font-weight:800; }
    .example-card mark { background:#f5dda1; border-radius:5px; padding:1px 5px; color:#17382e; }

    .dependency-map { display:grid; grid-template-columns:1fr 100px 1fr; align-items:center; gap:10px; margin:16px 0 24px; }
    .principal-node,.subordinate-node { min-height:120px; display:grid; place-items:center; text-align:center; border-radius:18px; padding:18px; }
    .principal-node { background:#17382e; color:#fff; }
    .subordinate-node { background:#dfeaf5; color:#315844; border:2px solid #91aabd; }
    .dependency-arrow { text-align:center; color:#769489; font-weight:800; }

    .game-token { min-height:58px; display:grid; place-items:center; text-align:center; background:#fff; border:1px solid #dde5dc; border-radius:14px; padding:10px 14px; box-shadow:0 5px 16px #17211d0d; font-weight:700; }
    .puzzle-objective,.scenario-card { background:#fff6df; border:1px solid #dfbd83; border-radius:16px; padding:16px 18px; margin:12px 0 18px; }
    .puzzle-piece { min-height:58px; display:grid; place-items:center; text-align:center; border-radius:12px; background:#dfeaf5; color:#315844; border:2px solid #91aabd; font-size:12px; font-weight:800; }

    .session-scoreboard { position:sticky; top:.5rem; z-index:20; background:rgba(245,247,243,.96); border:1px solid #dde5dc; border-radius:14px; padding:8px; margin:0 0 12px; box-shadow:0 6px 18px #17211d12; backdrop-filter:blur(8px); }
    .quarter-board { background:#fff; border:1px solid #e2e8df; border-radius:10px; padding:7px 9px; }
    .quarter-header { display:flex; justify-content:space-between; align-items:center; }
    .quarter-header b { color:#315844; font-size:12px; }
    .quarter-header small { color:#769489; font-size:9px; font-weight:800; }
    .quarter-dots { display:flex; gap:5px; margin-top:7px; }
    .score-dot { width:11px; height:11px; border-radius:50%; background:#fff; border:2px solid #aebbb2; }
    .score-dot.done { background:#5d9d6b; border-color:#5d9d6b; }

    @media (max-width: 700px) { .hero { min-height:250px; padding:36px 24px; } .hero h1 { font-size:42px; } .lesson-title { font-size:30px; } .coach-card { grid-template-columns:95px 1fr; } .structure-options { grid-template-columns:1fr; } .dependency-map { grid-template-columns:1fr; } .dependency-arrow { transform:rotate(90deg); } }
    </style>
    """, unsafe_allow_html=True)
