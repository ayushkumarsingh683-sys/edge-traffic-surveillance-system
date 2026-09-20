import os
import glob
import pandas as pd
import streamlit as st
from PIL import Image

# Page Configuration
st.set_page_config(
    page_title="Edge AI Traffic Surveillance SOC",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Paths Configuration
LOG_PATH = os.path.join("exports", "telemetry_log.csv")
VIOLATIONS_DIR = os.path.join("exports", "violations")

# Custom Dark Glassmorphism CSS
st.markdown("""
<style>
    /* Global Background & Font */
    .stApp {
        background: radial-gradient(circle at 50% 0%, #171d2b 0%, #0c1017 60%, #07090e 100%);
        color: #f1f5f9;
        font-family: 'Segoe UI', -apple-system, sans-serif;
    }

    /* Metric Card Design */
    .metric-card {
        background: rgba(22, 27, 34, 0.75);
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 12px;
        padding: 18px 20px;
        box-shadow: 0 8px 24px rgba(0, 0, 0, 0.35);
        transition: transform 0.2s ease, border-color 0.2s ease;
    }
    .metric-card:hover {
        transform: translateY(-3px);
        border-color: rgba(56, 189, 248, 0.4);
    }
    .metric-title {
        color: #94a3b8;
        font-size: 0.85rem;
        text-transform: uppercase;
        letter-spacing: 0.08em;
        font-weight: 600;
        margin-bottom: 6px;
    }
    .metric-val {
        font-size: 2.1rem;
        font-weight: 700;
        color: #f8fafc;
        margin-bottom: 4px;
        font-family: monospace;
    }
    .metric-sub {
        font-size: 0.82rem;
        font-weight: 500;
    }
    .sub-green { color: #34d399; }
    .sub-red { color: #f87171; }
    .sub-blue { color: #38bdf8; }

    /* Live Pulse Badge */
    .status-badge {
        display: inline-flex;
        align-items: center;
        gap: 8px;
        background: rgba(16, 185, 129, 0.15);
        border: 1px solid rgba(16, 185, 129, 0.3);
        padding: 6px 14px;
        border-radius: 30px;
        font-size: 0.8rem;
        color: #34d399;
        font-weight: 600;
        letter-spacing: 0.05em;
    }
    .pulse-dot {
        width: 8px;
        height: 8px;
        background: #10b981;
        border-radius: 50%;
        box-shadow: 0 0 10px #10b981;
        animation: pulse 1.8s infinite;
    }
    @keyframes pulse {
        0% { transform: scale(0.9); opacity: 0.8; }
        50% { transform: scale(1.3); opacity: 1; }
        100% { transform: scale(0.9); opacity: 0.8; }
    }

    /* Evidence Image Card */
    .image-card {
        background: rgba(22, 27, 34, 0.85);
        border: 1px solid rgba(239, 68, 68, 0.3);
        border-radius: 10px;
        padding: 10px;
        margin-bottom: 15px;
        transition: transform 0.2s ease;
    }
    .image-card:hover {
        transform: scale(1.02);
        border-color: rgba(239, 68, 68, 0.8);
        box-shadow: 0 0 15px rgba(239, 68, 68, 0.25);
    }

    /* Tabs Customization */
    .stTabs [data-baseweb="tab-list"] {
        gap: 15px;
        border-bottom: 1px solid rgba(255, 255, 255, 0.1);
    }
    .stTabs [data-baseweb="tab"] {
        background: transparent !important;
        border: none !important;
        color: #94a3b8 !important;
        font-weight: 600 !important;
        padding: 10px 18px !important;
    }
    .stTabs [aria-selected="true"] {
        color: #38bdf8 !important;
        border-bottom: 2px solid #38bdf8 !important;
    }
</style>
""", unsafe_allow_html=True)

# Top Bar / Navigation Header
col_brand, col_action = st.columns([4, 1.2])

with col_brand:
    st.markdown("""
        <div style="display: flex; align-items: center; gap: 15px; margin-bottom: 8px;">
            <h2 style="margin: 0; color: #ffffff; font-weight: 700; letter-spacing: -0.02em;">
                ⚡ Smart Highway Surveillance & E-Challan SOC
            </h2>
            <div class="status-badge">
                <span class="pulse-dot"></span> EDGE GPU ACTIVE
            </div>
        </div>
        <p style="color: #64748b; margin: 0; font-size: 0.95rem;">
            Real-time multi-class tracking, tripwire speed profiling, and automated violation evidence logs.
        </p>
    """, unsafe_allow_html=True)

with col_action:
    st.write("")
    if st.button("🔄 Sync Live Telemetry", use_container_width=True):
        st.rerun()

st.markdown("<hr style='border: none; height: 1px; background: rgba(255, 255, 255, 0.08); margin: 20px 0;'>", unsafe_allow_html=True)

# Load Telemetry Logs
if os.path.exists(LOG_PATH) and os.path.getsize(LOG_PATH) > 0:
    df = pd.read_csv(LOG_PATH)
else:
    df = pd.DataFrame(columns=[
        'timestamp', 'track_id', 'vehicle_class', 
        'speed_kmh', 'status', 'travel_time_sec', 'snapshot_path'
    ])

# Top Executive KPI Cards
total_vehicles = len(df)
violations_count = len(df[df['status'] == 'OVERSPEED_VIOLATION']) if total_vehicles > 0 else 0
compliance_rate = round(((total_vehicles - violations_count) / total_vehicles) * 100, 1) if total_vehicles > 0 else 100.0
avg_speed = round(df['speed_kmh'].mean(), 1) if total_vehicles > 0 else 0.0

c1, c2, c3, c4 = st.columns(4)

with c1:
    st.markdown(f"""
        <div class="metric-card">
            <div class="metric-title">Fleet Processed</div>
            <div class="metric-val">{total_vehicles}</div>
            <div class="metric-sub sub-blue">Total Tracked Vehicles</div>
        </div>
    """, unsafe_allow_html=True)

with c2:
    st.markdown(f"""
        <div class="metric-card" style="border-left: 4px solid #ef4444;">
            <div class="metric-title">Violations Logged</div>
            <div class="metric-val" style="color: #f87171;">{violations_count}</div>
            <div class="metric-sub sub-red">⚡ E-Challans Triggered (>80 km/h)</div>
        </div>
    """, unsafe_allow_html=True)

with c3:
    st.markdown(f"""
        <div class="metric-card" style="border-left: 4px solid #10b981;">
            <div class="metric-title">Compliance Index</div>
            <div class="metric-val" style="color: #34d399;">{compliance_rate}%</div>
            <div class="metric-sub sub-green">Adherence to Highway Limit</div>
        </div>
    """, unsafe_allow_html=True)

with c4:
    st.markdown(f"""
        <div class="metric-card">
            <div class="metric-title">Average Flow Speed</div>
            <div class="metric-val">{avg_speed} <span style="font-size: 1.1rem; color: #64748b;">km/h</span></div>
            <div class="metric-sub sub-blue">Dynamic Segment Velocity</div>
        </div>
    """, unsafe_allow_html=True)

st.write("")

# Main Interface Tabs
tab_telemetry, tab_gallery = st.tabs(["📊 Live Telemetry Stream", "🚨 E-Challan Evidence Vault"])

# Tab 1: Telemetry Data Table
with tab_telemetry:
    if df.empty:
        st.info("No telemetry recorded yet. Start processing video via `python src/pipeline.py`.")
    else:
        f1, f2 = st.columns([1.5, 2.5])
        with f1:
            status_filter = st.selectbox("Enforcement Status", ["All", "OVERSPEED_VIOLATION", "COMPLIANT"])
        with f2:
            class_filter = st.multiselect(
                "Vehicle Categories", 
                options=df['vehicle_class'].unique(), 
                default=df['vehicle_class'].unique()
            )

        filtered_df = df.copy()
        if status_filter != "All":
            filtered_df = filtered_df[filtered_df['status'] == status_filter]
        if class_filter:
            filtered_df = filtered_df[filtered_df['vehicle_class'].isin(class_filter)]

        def style_violations(row):
            if row['status'] == 'OVERSPEED_VIOLATION':
                return ['background-color: rgba(239, 68, 68, 0.18); color: #fca5a5; font-weight: 500;'] * len(row)
            return ['color: #cbd5e1;'] * len(row)

        st.dataframe(
            filtered_df.style.apply(style_violations, axis=1),
            use_container_width=True,
            height=430
        )

# Tab 2: Captured Violation Evidence
with tab_gallery:
    challan_images = sorted(glob.glob(os.path.join(VIOLATIONS_DIR, "*.jpg")), key=os.path.getmtime, reverse=True)

    if not challan_images:
        st.info("No violation snapshots captured yet. Images will automatically populate when speeding is detected.")
    else:
        st.markdown(f"<p style='color: #94a3b8; font-size: 0.95rem;'>Displaying <b>{len(challan_images)}</b> cryptographic speed-violation captures</p>", unsafe_allow_html=True)
        cols = st.columns(3)

        for idx, img_path in enumerate(challan_images):
            file_name = os.path.basename(img_path)
            col = cols[idx % 3]
            try:
                img = Image.open(img_path)
                with col:
                    st.markdown('<div class="image-card">', unsafe_allow_html=True)
                    st.image(img, use_container_width=True)
                    st.markdown(f"<span style='font-family: monospace; font-size: 0.78rem; color: #94a3b8;'>📁 {file_name}</span>", unsafe_allow_html=True)
                    st.markdown('</div>', unsafe_allow_html=True)
            except Exception:
                pass