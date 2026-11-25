
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import math

from data import SAMPLE_SUBJECTS, SAMPLE_STUDENTS

# Supports both graph_coloring.py and graph_colouring.py
try:
    from graph_coloring import build_conflict_graph, find_minimum_coloring
except ImportError:
    from graph_colouring import build_conflict_graph, find_minimum_coloring



st.set_page_config(
    page_title="EXAMFLOW | Smart Exam Scheduler",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)


if "subjects" not in st.session_state:
    st.session_state.subjects = SAMPLE_SUBJECTS.copy()

if "students" not in st.session_state:
    st.session_state.students = {
        name: enrolled.copy()
        for name, enrolled in SAMPLE_STUDENTS.items()
    }

if "page" not in st.session_state:
    st.session_state.page = "Overview"


subjects = st.session_state.subjects
students = st.session_state.students



conflict_graph = build_conflict_graph(subjects, students)

coloring, slot_count, attempts = find_minimum_coloring(
    conflict_graph
)

if coloring is None:
    coloring = {}
    slot_count = 0

schedule = {}

for subject, color in coloring.items():
    schedule.setdefault(color + 1, []).append(subject)

total_subjects = len(subjects)
total_students = len(students)

total_conflicts = sum(
    len(neighbours)
    for neighbours in conflict_graph.values()
) // 2

conflict_free = bool(coloring) or not subjects

COLORS = [
    "#9675FF",
    "#4C9EFF",
    "#24C8B5",
    "#F2AD59",
    "#E779B5",
    "#65B9E8",
    "#A6D66D",
    "#E47C75"
]



st.markdown("""
<style>

@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800;900&display=swap');

:root {
    --bg: #080B16;
    --panel: #11182B;
    --panel2: #151D34;
    --border: rgba(151, 143, 220, 0.18);
    --purple: #9675FF;
    --blue: #4C9EFF;
    --muted: #929DB9;
    --white: #F5F6FF;
}

* {
    font-family: 'Inter', sans-serif;
}

.stApp {
    background:
        radial-gradient(ellipse at 75% 0%, rgba(100,70,190,.15), transparent 32%),
        radial-gradient(ellipse at 5% 60%, rgba(35,100,180,.10), transparent 30%),
        var(--bg);
    color: var(--white);
}

[data-testid="stHeader"] {
    background: transparent;
}

[data-testid="stToolbar"] {
    right: 1rem;
}

.block-container {
    padding-top: 1.8rem;
    padding-bottom: 2.5rem;
    max-width: 1550px;
}

/* ---------------- SIDEBAR ---------------- */

[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #10152A 0%, #0B1121 100%);
    border-right: 1px solid rgba(150,130,255,.20);
}

[data-testid="stSidebar"] .block-container {
    padding: 1.5rem 1rem;
}

.brand {
    padding: 12px 8px 28px;
}

.brand-icon {
    display: inline-flex;
    width: 43px;
    height: 43px;
    border-radius: 14px;
    align-items: center;
    justify-content: center;
    background: linear-gradient(135deg, #8A69F5, #397FDE);
    box-shadow: 0 7px 25px rgba(115,85,230,.35);
    font-size: 22px;
    margin-bottom: 15px;
}

.brand-name {
    color: white;
    font-size: 25px;
    font-weight: 900;
    letter-spacing: 1px;
}

.brand-tagline {
    color: #8994B3;
    font-size: 9px;
    letter-spacing: 2.1px;
    margin-top: 6px;
}

.menu-heading {
    color: #6F7C9D;
    font-size: 9px;
    font-weight: 800;
    letter-spacing: 2px;
    padding: 10px 9px;
}

[data-testid="stRadio"] > label {
    display: none !important;
}

[data-testid="stRadio"] > div {
    gap: 7px;
}

[data-testid="stRadio"] label {
    border: 1px solid transparent;
    border-radius: 12px;
    padding: 11px 12px;
    transition: .2s ease;
    cursor: pointer;
}

[data-testid="stRadio"] label:hover {
    background: #1A2340;
    border-color: #38466C;
}

[data-testid="stRadio"] label:has(input:checked) {
    background: linear-gradient(105deg, #493A91, #253D70);
    border: 1px solid #806AE2;
    box-shadow: 0 5px 20px rgba(105,80,220,.20);
}

[data-testid="stRadio"] label > div:first-child {
    display: none !important;
}

[data-testid="stRadio"] label p {
    color: #B5BED8;
    font-size: 12px;
    font-weight: 600;
}

[data-testid="stRadio"] label:has(input:checked) p {
    color: white;
}

.sidebar-status {
    margin-top: 30px;
    padding: 15px;
    border-radius: 14px;
    background: linear-gradient(135deg, #192744, #171B35);
    border: 1px solid #39476C;
}

.sidebar-status-title {
    color: #E6DEFF;
    font-size: 11px;
    font-weight: 800;
    letter-spacing: 1px;
}

.sidebar-status-text {
    color: #9AA9C8;
    font-size: 10px;
    line-height: 2;
    margin-top: 9px;
}

/* ---------------- TOP HEADER ---------------- */

.topbar {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 3px 2px 20px;
    border-bottom: 1px solid rgba(150,150,200,.13);
    margin-bottom: 25px;
}

.breadcrumb {
    color: #8490AE;
    font-size: 11px;
    letter-spacing: .5px;
}

.topbar-right {
    display: flex;
    gap: 10px;
    align-items: center;
}

.live-pill {
    border: 1px solid rgba(55,205,151,.30);
    background: rgba(33,174,125,.10);
    color: #64E4B2;
    border-radius: 30px;
    padding: 7px 12px;
    font-size: 10px;
    font-weight: 700;
}

.topbar-date {
    color: #929DB9;
    font-size: 10px;
}

/* ---------------- HERO ---------------- */

.hero {
    position: relative;
    overflow: hidden;
    border-radius: 23px;
    padding: 30px;
    min-height: 225px;
    background:
        radial-gradient(circle at 85% 25%, rgba(119,102,255,.42), transparent 27%),
        linear-gradient(112deg, #29215B 0%, #1B376C 55%, #172A4C 100%);
    border: 1px solid rgba(164,150,255,.35);
    box-shadow: 0 18px 45px rgba(0,0,0,.22);
}

.hero:after {
    content: "";
    position: absolute;
    width: 230px;
    height: 230px;
    border: 1px solid rgba(255,255,255,.12);
    border-radius: 50%;
    right: 7%;
    top: -85px;
    box-shadow:
        0 0 0 28px rgba(255,255,255,.025),
        0 0 0 58px rgba(255,255,255,.02);
}

.hero-kicker {
    color: #C8BBFF;
    font-size: 10px;
    letter-spacing: 2.2px;
    font-weight: 800;
}

.hero-title {
    color: white;
    font-size: 32px;
    font-weight: 900;
    letter-spacing: -.9px;
    margin-top: 14px;
    line-height: 1.2;
}

.hero-description {
    color: #D2D6F0;
    font-size: 12px;
    line-height: 1.9;
    max-width: 570px;
    margin-top: 12px;
}

.hero-label {
    display: inline-block;
    color: white;
    background: rgba(255,255,255,.12);
    border: 1px solid rgba(255,255,255,.18);
    padding: 7px 12px;
    border-radius: 8px;
    font-size: 10px;
    margin-top: 18px;
}

.hero-visual {
    min-height: 160px;
    display: flex;
    align-items: center;
    justify-content: center;
}

.hero-orbit {
    height: 145px;
    width: 145px;
    border-radius: 50%;
    border: 1px solid rgba(255,255,255,.22);
    display: flex;
    align-items: center;
    justify-content: center;
    box-shadow:
        0 0 0 15px rgba(255,255,255,.035),
        0 0 35px rgba(139,116,255,.25);
    font-size: 55px;
}

/* ---------------- KPI CARDS ---------------- */

.kpi {
    position: relative;
    overflow: hidden;
    background: linear-gradient(145deg, #19233D, #11192D);
    border: 1px solid var(--border);
    border-radius: 17px;
    padding: 19px;
    min-height: 145px;
    box-shadow: 0 8px 25px rgba(0,0,0,.14);
    transition: .2s ease;
}

.kpi:hover {
    transform: translateY(-3px);
    border-color: rgba(155,130,255,.55);
}

.kpi:after {
    content: "";
    position: absolute;
    right: -35px;
    top: -45px;
    width: 105px;
    height: 105px;
    border-radius: 50%;
    background: var(--glow, rgba(145,110,255,.15));
    filter: blur(8px);
}

.kpi-top {
    display: flex;
    align-items: center;
    justify-content: space-between;
}

.kpi-icon {
    width: 38px;
    height: 38px;
    border-radius: 12px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 19px;
    background: rgba(151,120,255,.15);
    border: 1px solid rgba(151,120,255,.23);
}

.kpi-tag {
    color: #8D9AB9;
    font-size: 9px;
    font-weight: 800;
    letter-spacing: 1px;
}

.kpi-value {
    color: white;
    font-size: 30px;
    font-weight: 900;
    margin-top: 17px;
}

.kpi-label {
    color: #9DA9C4;
    font-size: 10px;
    margin-top: 4px;
}

/* ---------------- PANELS ---------------- */

.section-head {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin: 29px 0 14px;
}

.section-title {
    color: #F1F1FF;
    font-size: 17px;
    font-weight: 800;
}

.section-subtitle {
    color: #818DAA;
    font-size: 10px;
    margin-top: 5px;
}

.panel {
    background: linear-gradient(145deg, rgba(24,33,57,.96), rgba(16,24,42,.96));
    border: 1px solid rgba(139,145,200,.17);
    border-radius: 17px;
    padding: 20px;
    box-shadow: 0 10px 28px rgba(0,0,0,.12);
}

.panel-title {
    color: #EDEEFF;
    font-size: 13px;
    font-weight: 800;
}

.panel-subtitle {
    color: #8996B2;
    font-size: 10px;
    margin-top: 5px;
}

.mini-label {
    color: #8C9AB9;
    font-size: 9px;
    letter-spacing: 1.2px;
    font-weight: 800;
}

.big-number {
    color: white;
    font-size: 29px;
    font-weight: 900;
    margin-top: 6px;
}

.muted {
    color: #98A3BD;
    font-size: 11px;
    line-height: 1.8;
}

.slot-card {
    background: linear-gradient(120deg, #1D2946, #17213A);
    border: 1px solid rgba(130,145,205,.20);
    border-left: 4px solid var(--slot-color);
    border-radius: 12px;
    padding: 14px 16px;
    margin-bottom: 10px;
}

.slot-number {
    color: var(--slot-color);
    font-size: 10px;
    font-weight: 800;
    letter-spacing: 1px;
}

.slot-subject {
    color: white;
    font-size: 13px;
    font-weight: 700;
    margin-top: 6px;
}

.slot-meta {
    color: #8E9AB7;
    font-size: 10px;
    margin-top: 6px;
}

.subject-chip {
    display: inline-block;
    padding: 7px 10px;
    border-radius: 8px;
    background: rgba(143,118,255,.12);
    border: 1px solid rgba(143,118,255,.24);
    color: #D8D0FF;
    font-size: 10px;
    margin: 4px 4px 4px 0;
}

.status-good {
    color: #61DFAE;
    font-size: 10px;
    font-weight: 800;
}

.status-warning {
    color: #F3B76C;
    font-size: 10px;
    font-weight: 800;
}

/* ---------------- BUTTONS AND INPUTS ---------------- */

.stButton > button,
.stDownloadButton > button {
    background: linear-gradient(105deg, #7158D8, #347FD4);
    color: white;
    border: 1px solid #8E7DE9;
    border-radius: 10px;
    min-height: 39px;
    font-size: 11px;
    font-weight: 700;
    transition: .2s ease;
}

.stButton > button:hover,
.stDownloadButton > button:hover {
    color: white;
    border-color: white;
    box-shadow: 0 0 18px rgba(120,100,235,.35);
}

.stTextInput input,
.stNumberInput input,
[data-baseweb="select"] > div {
    background: #141D33 !important;
    color: white !important;
    border-color: #394563 !important;
    border-radius: 9px !important;
}

[data-testid="stMultiSelect"] span {
    color: white;
}

.stTabs [data-baseweb="tab-list"] {
    gap: 8px;
    background: #111A2D;
    padding: 7px;
    border-radius: 12px;
}

.stTabs [data-baseweb="tab"] {
    color: #9DA9C5;
    border-radius: 8px;
}

.stTabs [aria-selected="true"] {
    background: #3C3674;
    color: white;
}

[data-testid="stDataFrame"] {
    border: 1px solid rgba(140,145,190,.20);
    border-radius: 12px;
    overflow: hidden;
}

div[data-testid="stMetric"] {
    background: #17223B;
    padding: 13px;
    border: 1px solid #343F61;
    border-radius: 12px;
}

div[data-testid="stMetric"] label {
    color: #9AA7C2 !important;
}

div[data-testid="stMetric"] [data-testid="stMetricValue"] {
    color: white !important;
}

hr {
    border-color: rgba(145,145,190,.17);
}

.footer {
    text-align: center;
    color: #65728F;
    font-size: 9px;
    letter-spacing: 1.5px;
    padding: 20px 0 5px;
}

</style>
""", unsafe_allow_html=True)




def section(title, subtitle=""):
    st.markdown(f"""
    <div class="section-head">
        <div>
            <div class="section-title">{title}</div>
            <div class="section-subtitle">{subtitle}</div>
        </div>
    </div>
    """, unsafe_allow_html=True)


def kpi(icon, tag, value, label, glow="rgba(145,110,255,.18)"):
    st.markdown(f"""
    <div class="kpi" style="--glow:{glow}">
        <div class="kpi-top">
            <div class="kpi-icon">{icon}</div>
            <div class="kpi-tag">{tag}</div>
        </div>
        <div class="kpi-value">{value}</div>
        <div class="kpi-label">{label}</div>
    </div>
    """, unsafe_allow_html=True)


def panel_title(title, subtitle=""):
    st.markdown(f"""
    <div class="panel-title">{title}</div>
    <div class="panel-subtitle">{subtitle}</div>
    """, unsafe_allow_html=True)


def chart_style(fig, height=330):
    fig.update_layout(
        height=height,
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(
            color="#C3CBE0",
            family="Inter",
            size=10
        ),
        margin=dict(l=15, r=15, t=30, b=15),
        xaxis=dict(
            gridcolor="rgba(130,145,190,.13)",
            zerolinecolor="rgba(130,145,190,.13)"
        ),
        yaxis=dict(
            gridcolor="rgba(130,145,190,.13)",
            zerolinecolor="rgba(130,145,190,.13)"
        ),
        legend=dict(
            bgcolor="rgba(0,0,0,0)",
            font=dict(color="#B9C4DD")
        )
    )
    return fig


def make_timetable_dataframe():
    rows = []

    for slot, items in sorted(schedule.items()):
        for subject in items:
            enrolled_count = sum(
                subject in enrolled
                for enrolled in students.values()
            )

            rows.append({
                "Exam Slot": f"Slot {slot}",
                "Subject": subject,
                "Enrolled Students": enrolled_count,
                "Status": "Conflict Free"
            })

    return pd.DataFrame(rows)




with st.sidebar:

    st.markdown("""
    <div class="brand">
        <div class="brand-icon">🎓</div>
        <div class="brand-name">
            EXAM<span style="color:#A18BFF">FLOW</span>
        </div>
        <div class="brand-tagline">INTELLIGENT SCHEDULING SYSTEM</div>
    </div>

    <div class="menu-heading">WORKSPACE</div>
    """, unsafe_allow_html=True)

    navigation = {
        "🏠   Overview": "Overview",
        "📅   Timetable": "Timetable",
        "👨‍🎓   Students": "Students",
        "📚   Subjects": "Subjects",
        "🔗   Conflict Network": "Conflict Network",
        "📊   Analytics": "Analytics",
        "⚙️   Manage Data": "Manage Data"
    }

    labels = list(navigation.keys())
    values = list(navigation.values())

    current_index = (
        values.index(st.session_state.page)
        if st.session_state.page in values else 0
    )

    selected = st.radio(
        "Navigation",
        labels,
        index=current_index,
        label_visibility="collapsed",
        key="main_navigation"
    )

    page = navigation[selected]
    st.session_state.page = page

    st.markdown("""
    <div class="sidebar-status">
        <div class="sidebar-status-title">✦ SYSTEM HEALTH</div>
        <div class="sidebar-status-text">
            🟢 Scheduler Engine Online<br>
            🟢 Graph Coloring Ready<br>
            🟢 Backtracking Active<br>
            🟢 Data Connection Stable
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div style="padding:22px 8px 5px;color:#64718E;font-size:9px;line-height:2;">
        EXAMFLOW V2.0<br>
        SMART ACADEMIC WORKSPACE
    </div>
    """, unsafe_allow_html=True)



st.markdown(f"""
<div class="topbar">
    <div class="breadcrumb">
        WORKSPACE&nbsp;&nbsp; / &nbsp;&nbsp;{page.upper()}
    </div>
    <div class="topbar-right">
        <div class="live-pill">● SYSTEM LIVE</div>
        <div class="topbar-date">EXAMFLOW 2.0</div>
    </div>
</div>
""", unsafe_allow_html=True)




if page == "Overview":

    # HERO
    hero_left, hero_right = st.columns([1.65, 0.75])

    with hero_left:
        st.markdown("""
        <div class="hero">
            <div class="hero-kicker">✦ INTELLIGENT EXAM MANAGEMENT</div>
            <div class="hero-title">
                Schedule smarter.<br>
                Work better.
            </div>
            <div class="hero-description">
                Welcome to EXAMFLOW — an intelligent examination
                scheduling platform that uses Graph Coloring and
                Backtracking to create conflict-free timetables.
            </div>
            <div class="hero-label">
                GRAPH COLORING &nbsp; • &nbsp; BACKTRACKING
            </div>
        </div>
        """, unsafe_allow_html=True)

    with hero_right:
        st.markdown("""
        <div class="hero hero-visual">
            <div class="hero-orbit">🎓</div>
        </div>
        """, unsafe_allow_html=True)

    # KPI ROW
    section("System Overview", "A live snapshot of your academic scheduling data")

    c1, c2, c3, c4 = st.columns(4)

    with c1:
        kpi("📚", "ACADEMIC DATA", total_subjects, "Total Subjects")

    with c2:
        kpi("👨‍🎓", "REGISTRATION", total_students, "Registered Students",
            "rgba(70,150,255,.20)")

    with c3:
        kpi("🕒", "OPTIMIZATION", slot_count, "Minimum Exam Slots",
            "rgba(30,205,180,.18)")

    with c4:
        kpi("🔗", "CONFLICT ANALYSIS", total_conflicts, "Subject Conflicts",
            "rgba(230,120,180,.17)")

    # MAIN WORKSPACE
    section("Scheduling Workspace", "Explore the generated timetable and algorithm insights")

    left, right = st.columns([1.45, 0.85], gap="large")

    with left:

        st.markdown('<div class="panel">', unsafe_allow_html=True)
        panel_title("Exam Slot Distribution",
                    "Number of subjects assigned to each examination slot")

        if schedule:
            chart_data = pd.DataFrame([
                {
                    "Slot": f"Slot {slot}",
                    "Subjects": len(items)
                }
                for slot, items in sorted(schedule.items())
            ])

            fig = px.bar(
                chart_data,
                x="Slot",
                y="Subjects",
                text="Subjects",
                color="Slot",
                color_discrete_sequence=COLORS
            )

            fig.update_traces(
                marker_line_width=0,
                textposition="outside",
                textfont=dict(color="white", size=12),
                marker_cornerradius=7
            )

            fig.update_layout(
                showlegend=False,
                yaxis_title="Number of Subjects",
                xaxis_title="Examination Slot"
            )

            st.plotly_chart(
                chart_style(fig, 290),
                use_container_width=True
            )
        else:
            st.info("Add subjects and students to generate a timetable.")

        st.markdown('</div>', unsafe_allow_html=True)

    with right:

        st.markdown('<div class="panel">', unsafe_allow_html=True)
        panel_title("Algorithm Performance",
                    "Live execution summary")

        st.markdown(f"""
        <div style="margin-top:22px">
            <div class="mini-label">MINIMUM SLOTS REQUIRED</div>
            <div class="big-number">{slot_count}</div>
        </div>
        <div style="margin-top:22px">
            <div class="mini-label">BACKTRACKING ATTEMPTS</div>
            <div class="big-number">{attempts:,}</div>
        </div>
        <div style="margin-top:22px">
            <div class="mini-label">TOTAL CONFLICT EDGES</div>
            <div class="big-number">{total_conflicts}</div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("---")

        if conflict_free:
            st.markdown(
                '<div class="status-good">● VALID SCHEDULE GENERATED</div>',
                unsafe_allow_html=True
            )
            st.caption("No conflicting subjects share an examination slot.")
        else:
            st.markdown(
                '<div class="status-warning">● SCHEDULE NOT AVAILABLE</div>',
                unsafe_allow_html=True
            )

        st.markdown('</div>', unsafe_allow_html=True)

    # TIMETABLE PREVIEW
    section("Generated Timetable", "Your automatically assigned examination slots")

    if schedule:

        slot_columns = st.columns(min(len(schedule), 4))

        for index, (slot, items) in enumerate(sorted(schedule.items())):

            with slot_columns[index % len(slot_columns)]:

                color = COLORS[(slot - 1) % len(COLORS)]

                html_subjects = "".join(
                    f'<div class="slot-subject">• {subject}</div>'
                    for subject in items
                )

                st.markdown(f"""
                <div class="slot-card" style="--slot-color:{color}">
                    <div class="slot-number">EXAMINATION SLOT {slot:02}</div>
                    {html_subjects}
                    <div class="slot-meta">
                        {len(items)} subject(s) assigned
                    </div>
                </div>
                """, unsafe_allow_html=True)

    else:
        st.info("No timetable available. Add subjects first.")

    # BOTTOM INFORMATION
    section("How EXAMFLOW Works", "The logic behind your smart timetable")

    x1, x2, x3 = st.columns(3)

    with x1:
        st.markdown("""
        <div class="panel">
            <div style="font-size:25px">🔗</div>
            <div class="panel-title" style="margin-top:12px">
                01. Conflict Graph
            </div>
            <div class="muted" style="margin-top:8px">
                Subjects sharing one or more students are connected
                through an edge in the graph.
            </div>
        </div>
        """, unsafe_allow_html=True)

    with x2:
        st.markdown("""
        <div class="panel">
            <div style="font-size:25px">🎨</div>
            <div class="panel-title" style="margin-top:12px">
                02. Graph Coloring
            </div>
            <div class="muted" style="margin-top:8px">
                Each subject receives a color. Connected subjects
                cannot receive the same color.
            </div>
        </div>
        """, unsafe_allow_html=True)

    with x3:
        st.markdown("""
        <div class="panel">
            <div style="font-size:25px">⚡</div>
            <div class="panel-title" style="margin-top:12px">
                03. Backtracking
            </div>
            <div class="muted" style="margin-top:8px">
                The algorithm searches for a valid assignment using
                the minimum possible number of slots.
            </div>
        </div>
        """, unsafe_allow_html=True)




elif page == "Timetable":

    section("Examination Timetable", "Your optimized, conflict-free examination plan")

    a, b, c = st.columns(3)

    with a:
        kpi("📚", "SUBJECTS", total_subjects, "Scheduled Subjects")

    with b:
        kpi("🕒", "EXAM SLOTS", slot_count, "Minimum Slots")

    with c:
        kpi("👨‍🎓", "STUDENTS", total_students, "Registered Students")

    if schedule:

        st.markdown('<div class="panel">', unsafe_allow_html=True)
        panel_title("Slot-by-Slot Schedule",
                    "Subjects are grouped by their assigned exam slot")

        for slot, items in sorted(schedule.items()):

            color = COLORS[(slot - 1) % len(COLORS)]

            st.markdown(f"""
            <div class="slot-card" style="--slot-color:{color};margin-top:15px">
                <div class="slot-number">EXAMINATION SLOT {slot:02}</div>
                <div style="margin-top:8px">
                    {''.join(f'<span class="subject-chip">{subject}</span>' for subject in items)}
                </div>
                <div class="slot-meta">
                    {len(items)} subject(s) &nbsp; • &nbsp; Conflict-free assignment
                </div>
            </div>
            """, unsafe_allow_html=True)

        st.markdown('</div>', unsafe_allow_html=True)

        st.markdown("")
        section("Export Your Timetable", "Download the generated schedule")

        timetable_df = make_timetable_dataframe()

        st.dataframe(
            timetable_df,
            use_container_width=True,
            hide_index=True
        )

        st.download_button(
            "⬇ Download Timetable CSV",
            timetable_df.to_csv(index=False).encode("utf-8"),
            "EXAMFLOW_Timetable.csv",
            "text/csv",
            use_container_width=False
        )

    else:
        st.warning("No valid timetable found. Please check your subject data.")




elif page == "Students":

    section("Student Directory", "View student registrations and enrolled subjects")

    a, b = st.columns(2)

    with a:
        kpi("👨‍🎓", "TOTAL REGISTRATION", total_students, "Registered Students")

    with b:
        average = (
            sum(len(x) for x in students.values()) / total_students
            if total_students else 0
        )
        kpi("📖", "ENROLLMENT", f"{average:.1f}", "Average Subjects per Student",
            "rgba(60,165,255,.18)")

    search = st.text_input(
        "Search student",
        placeholder="Enter student name..."
    )

    student_rows = []

    for name, enrolled in students.items():

        if search.lower() in name.lower():

            student_rows.append({
                "Student Name": name,
                "Enrolled Subjects": ", ".join(enrolled) if enrolled else "No subjects",
                "Total Subjects": len(enrolled)
            })

    section("Registration Records", "Student-wise enrollment details")

    if student_rows:
        st.dataframe(
            pd.DataFrame(student_rows),
            use_container_width=True,
            hide_index=True
        )
    else:
        st.info("No matching student found.")

    section("Enrollment Distribution", "Number of students in each subject")

    if subjects:

        enrollment_data = []

        for subject in subjects:
            count = sum(
                subject in enrolled
                for enrolled in students.values()
            )

            enrollment_data.append({
                "Subject": subject,
                "Students": count
            })

        fig = px.bar(
            pd.DataFrame(enrollment_data),
            x="Subject",
            y="Students",
            color="Subject",
            color_discrete_sequence=COLORS,
            text="Students"
        )

        fig.update_traces(textposition="outside")
        fig.update_layout(showlegend=False)

        st.plotly_chart(
            chart_style(fig, 330),
            use_container_width=True
        )


# =========================================================
# SUBJECTS
# =========================================================

elif page == "Subjects":

    section("Subject Management", "Explore all subjects and their assigned slots")

    a, b = st.columns(2)

    with a:
        kpi("📚", "SUBJECT CATALOG", total_subjects, "Total Subjects")

    with b:
        kpi("🔗", "GRAPH CONNECTIONS", total_conflicts, "Conflict Connections")

    subject_rows = []

    for subject in subjects:

        count = sum(
            subject in enrolled
            for enrolled in students.values()
        )

        subject_rows.append({
            "Subject": subject,
            "Enrolled Students": count,
            "Conflict Count": len(conflict_graph.get(subject, [])),
            "Exam Slot": (
                f"Slot {coloring[subject] + 1}"
                if subject in coloring else "Not Assigned"
            )
        })

    section("Subject Directory", "Enrollment and conflict information")

    if subject_rows:
        st.dataframe(
            pd.DataFrame(subject_rows),
            use_container_width=True,
            hide_index=True
        )
    else:
        st.info("No subjects have been added.")

    section("Subject Cards", "Quick view of your academic subjects")

    if subjects:

        cols = st.columns(3)

        for index, subject in enumerate(subjects):

            count = sum(
                subject in enrolled
                for enrolled in students.values()
            )

            conflict_count = len(conflict_graph.get(subject, []))

            with cols[index % 3]:

                color = COLORS[index % len(COLORS)]

                st.markdown(f"""
                <div class="panel" style="margin-bottom:13px;border-top:3px solid {color}">
                    <div class="mini-label">SUBJECT {index + 1:02}</div>
                    <div class="panel-title" style="margin-top:12px">
                        {subject}
                    </div>
                    <div style="display:flex;gap:25px;margin-top:17px">
                        <div>
                            <div class="mini-label">STUDENTS</div>
                            <div style="font-size:21px;font-weight:800;color:white">
                                {count}
                            </div>
                        </div>
                        <div>
                            <div class="mini-label">CONFLICTS</div>
                            <div style="font-size:21px;font-weight:800;color:white">
                                {conflict_count}
                            </div>
                        </div>
                    </div>
                </div>
                """, unsafe_allow_html=True)



elif page == "Conflict Network":

    section("Conflict Network", "Visual representation of shared student enrollments")

    a, b, c = st.columns(3)

    with a:
        kpi("🔵", "GRAPH NODES", total_subjects, "Subjects")

    with b:
        kpi("🔗", "GRAPH EDGES", total_conflicts, "Conflicting Pairs")

    with c:
        kpi("🎨", "COLOR GROUPS", slot_count, "Exam Slots")

    if subjects:

        # Create graph coordinates without requiring NetworkX.
        count = len(subjects)
        positions = {}

        for i, subject in enumerate(subjects):
            angle = 2 * math.pi * i / max(count, 1) - math.pi / 2
            positions[subject] = (
                math.cos(angle),
                math.sin(angle)
            )

        edge_x = []
        edge_y = []

        for subject, neighbours in conflict_graph.items():

            for neighbour in neighbours:

                if subjects.index(subject) < subjects.index(neighbour):

                    x0, y0 = positions[subject]
                    x1, y1 = positions[neighbour]

                    edge_x.extend([x0, x1, None])
                    edge_y.extend([y0, y1, None])

        edge_trace = go.Scatter(
            x=edge_x,
            y=edge_y,
            mode="lines",
            line=dict(
                color="rgba(144,130,220,.55)",
                width=2
            ),
            hoverinfo="none"
        )

        node_x = []
        node_y = []
        node_text = []
        node_colors = []
        hover_text = []

        for subject in subjects:

            x, y = positions[subject]

            node_x.append(x)
            node_y.append(y)
            node_text.append(subject)

            slot = coloring.get(subject, 0)
            node_colors.append(COLORS[slot % len(COLORS)])

            hover_text.append(
                f"<b>{subject}</b><br>"
                f"Exam Slot: {slot + 1 if subject in coloring else 'Not assigned'}"
                f"<br>Conflicts: {len(conflict_graph.get(subject, []))}"
            )

        node_trace = go.Scatter(
            x=node_x,
            y=node_y,
            mode="markers+text",
            text=node_text,
            textposition="bottom center",
            hovertext=hover_text,
            hoverinfo="text",
            marker=dict(
                size=31,
                color=node_colors,
                line=dict(color="#FFFFFF", width=1.5)
            ),
            textfont=dict(
                color="#E9E9FF",
                size=10
            )
        )

        fig = go.Figure([edge_trace, node_trace])

        fig.update_layout(
            height=560,
            showlegend=False,
            xaxis=dict(visible=False, range=[-1.5, 1.5]),
            yaxis=dict(visible=False, range=[-1.5, 1.5]),
            hovermode="closest"
        )

        st.markdown('<div class="panel">', unsafe_allow_html=True)
        panel_title("Subject Relationship Map",
                    "Each node represents a subject; each line represents a conflict")

        st.plotly_chart(
            chart_style(fig, 540),
            use_container_width=True
        )

        st.markdown("""
        <div class="muted">
            <b>How to read this graph:</b><br>
            • Connected subjects share at least one student.<br>
            • Different colors represent different examination slots.<br>
            • Two connected subjects must never share the same color.
        </div>
        """, unsafe_allow_html=True)

        st.markdown('</div>', unsafe_allow_html=True)

        section("Conflict Details", "Direct subject-to-subject relationships")

        conflict_rows = []

        for subject, neighbours in conflict_graph.items():

            for neighbour in neighbours:

                if subjects.index(subject) < subjects.index(neighbour):

                    conflict_rows.append({
                        "Subject 1": subject,
                        "Subject 2": neighbour,
                        "Slot 1": coloring.get(subject, -1) + 1,
                        "Slot 2": coloring.get(neighbour, -1) + 1,
                        "Status": "No Slot Conflict"
                    })

        if conflict_rows:
            st.dataframe(
                pd.DataFrame(conflict_rows),
                use_container_width=True,
                hide_index=True
            )
        else:
            st.success("No subject conflicts detected.")

    else:
        st.info("Add subjects to build the conflict network.")




elif page == "Analytics":

    section("Analytics & Performance", "Understand the efficiency of your scheduling algorithm")

    a, b, c = st.columns(3)

    with a:
        kpi("⚡", "SEARCH PROCESS", f"{attempts:,}", "Backtracking Attempts")

    with b:
        kpi("🕒", "OPTIMIZATION", slot_count, "Minimum Slots")

    with c:
        kpi("🔗", "GRAPH STRUCTURE", total_conflicts, "Conflict Edges")

    left, right = st.columns([1.15, 1], gap="large")

    with left:

        st.markdown('<div class="panel">', unsafe_allow_html=True)
        panel_title("Slot Composition", "Subject distribution across examination slots")

        if schedule:

            pie_data = pd.DataFrame([
                {
                    "Slot": f"Slot {slot}",
                    "Subjects": len(items)
                }
                for slot, items in sorted(schedule.items())
            ])

            fig = px.pie(
                pie_data,
                names="Slot",
                values="Subjects",
                hole=.64,
                color_discrete_sequence=COLORS
            )

            fig.update_traces(
                textposition="outside",
                textinfo="percent+label"
            )

            st.plotly_chart(
                chart_style(fig, 350),
                use_container_width=True
            )

        else:
            st.info("No slot data available.")

        st.markdown('</div>', unsafe_allow_html=True)

    with right:

        st.markdown('<div class="panel">', unsafe_allow_html=True)
        panel_title("Graph Statistics", "Structure of the conflict graph")

        if total_subjects > 1:
            max_edges = total_subjects * (total_subjects - 1) / 2
            density = total_conflicts / max_edges
        else:
            density = 0

        st.markdown(f"""
        <div style="margin-top:25px">
            <div class="mini-label">GRAPH DENSITY</div>
            <div class="big-number">{density * 100:.1f}%</div>
            <div class="muted">Percentage of possible subject connections that exist.</div>
        </div>
        <div style="margin-top:23px">
            <div class="mini-label">TOTAL SUBJECTS</div>
            <div class="big-number">{total_subjects}</div>
        </div>
        <div style="margin-top:23px">
            <div class="mini-label">TOTAL STUDENTS</div>
            <div class="big-number">{total_students}</div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown('</div>', unsafe_allow_html=True)

    section("Algorithm Explanation", "The computational approach used by EXAMFLOW")

    p1, p2 = st.columns(2)

    with p1:
        st.markdown("""
        <div class="panel">
            <div style="font-size:25px">🎨</div>
            <div class="panel-title" style="margin-top:10px">
                Graph Coloring
            </div>
            <div class="muted" style="margin-top:9px">
                The problem is modeled as a graph. Every subject is a
                vertex, and an edge connects subjects that share students.
                A color represents an examination slot.
            </div>
        </div>
        """, unsafe_allow_html=True)

    with p2:
        st.markdown("""
        <div class="panel">
            <div style="font-size:25px">↩️</div>
            <div class="panel-title" style="margin-top:10px">
                Backtracking
            </div>
            <div class="muted" style="margin-top:9px">
                The algorithm assigns colors while checking conflicts.
                If an assignment cannot lead to a valid solution, it
                backtracks and tries another assignment.
            </div>
        </div>
        """, unsafe_allow_html=True)




elif page == "Manage Data":

    section("Data Control Center", "Manage subjects, students and scheduler records")

    tab1, tab2, tab3 = st.tabs([
        "＋ Add Subject",
        "＋ Add Student",
        "⚙ Remove / Reset"
    ])

    # ADD SUBJECT
    with tab1:

        st.markdown('<div class="panel">', unsafe_allow_html=True)
        panel_title("Create a New Subject",
                    "Add a subject to the scheduling database")

        new_subject = st.text_input(
            "Subject Name",
            placeholder="Example: Artificial Intelligence",
            key="new_subject_input"
        )

        if st.button("＋ Add Subject", key="add_subject_button"):

            new_subject = new_subject.strip()

            if not new_subject:
                st.warning("Please enter a subject name.")

            elif new_subject in st.session_state.subjects:
                st.warning("This subject already exists.")

            else:
                st.session_state.subjects.append(new_subject)
                st.success(f"{new_subject} added successfully.")
                st.rerun()

        st.markdown('</div>', unsafe_allow_html=True)

    # ADD STUDENT
    with tab2:

        st.markdown('<div class="panel">', unsafe_allow_html=True)
        panel_title("Register a Student",
                    "Create a student record and assign enrolled subjects")

        new_student = st.text_input(
            "Student Name",
            placeholder="Example: Rahul Sharma",
            key="new_student_input"
        )

        enrolled_subjects = st.multiselect(
            "Select Enrolled Subjects",
            st.session_state.subjects,
            key="new_student_subjects"
        )

        if st.button("＋ Register Student", key="add_student_button"):

            new_student = new_student.strip()

            if not new_student:
                st.warning("Please enter the student's name.")

            elif new_student in st.session_state.students:
                st.warning("This student already exists.")

            else:
                st.session_state.students[new_student] = enrolled_subjects.copy()
                st.success(f"{new_student} registered successfully.")
                st.rerun()

        st.markdown('</div>', unsafe_allow_html=True)

    # REMOVE / RESET
    with tab3:

        st.markdown('<div class="panel">', unsafe_allow_html=True)
        panel_title("Remove Subject",
                    "Remove a subject and its student enrollment references")

        if st.session_state.subjects:

            remove_subject = st.selectbox(
                "Choose Subject",
                st.session_state.subjects,
                key="remove_subject_select"
            )

            if st.button("Remove Selected Subject", key="remove_subject_button"):

                st.session_state.subjects.remove(remove_subject)

                for student in st.session_state.students:
                    if remove_subject in st.session_state.students[student]:
                        st.session_state.students[student].remove(remove_subject)

                st.success("Subject removed successfully.")
                st.rerun()

        else:
            st.info("There are no subjects to remove.")

        st.markdown("---")

        panel_title("Remove Student", "Delete a student registration")

        if st.session_state.students:

            remove_student = st.selectbox(
                "Choose Student",
                list(st.session_state.students.keys()),
                key="remove_student_select"
            )

            if st.button("Remove Selected Student", key="remove_student_button"):

                del st.session_state.students[remove_student]
                st.success("Student removed successfully.")
                st.rerun()

        else:
            st.info("There are no students to remove.")

        st.markdown("---")

        panel_title("Restore Sample Data",
                    "Restore the original demonstration dataset")

        if st.button("↩ Restore Default Data", key="reset_data_button"):

            st.session_state.subjects = SAMPLE_SUBJECTS.copy()

            st.session_state.students = {
                name: enrolled.copy()
                for name, enrolled in SAMPLE_STUDENTS.items()
            }

            st.success("Sample data restored.")
            st.rerun()

        st.markdown('</div>', unsafe_allow_html=True)

    section("Current Database Summary", "Live records currently stored in this session")

    s1, s2 = st.columns(2)

    with s1:
        st.metric("Total Subjects", len(st.session_state.subjects))

    with s2:
        st.metric("Total Students", len(st.session_state.students))




st.markdown("""
<div class="footer">
    EXAMFLOW 2.0 &nbsp; • &nbsp; SMART EXAM SCHEDULER
    <br><br>
    POWERED BY GRAPH COLORING & BACKTRACKING
</div>
""", unsafe_allow_html=True)
