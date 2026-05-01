import streamlit as st
import numpy as np
import pandas as pd
import pickle
import os

# ── Page config ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Concrete Strength Predictor",
    page_icon="🏗️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Custom CSS ────────────────────────────────────────────────────────────────
st.markdown("""
<style>
    .main-header {
        font-size: 2.4rem;
        font-weight: 700;
        color: #1a3c6e;
        margin-bottom: 0.2rem;
    }
    .sub-header {
        font-size: 1rem;
        color: #555;
        margin-bottom: 2rem;
    }
    .metric-card {
        background: linear-gradient(135deg, #1a3c6e 0%, #2d6cbe 100%);
        border-radius: 12px;
        padding: 1.2rem 1.5rem;
        color: white;
        text-align: center;
    }
    .metric-card h2 { margin: 0; font-size: 2rem; }
    .metric-card p  { margin: 0; font-size: 0.85rem; opacity: 0.85; }
    .result-box {
        background: linear-gradient(135deg, #e8f5e9, #c8e6c9);
        border-left: 5px solid #2e7d32;
        border-radius: 8px;
        padding: 1.5rem 2rem;
        margin-top: 1rem;
    }
    .result-box h3 { color: #1b5e20; margin: 0 0 0.4rem; font-size: 1.1rem; }
    .result-box h1 { color: #2e7d32; margin: 0; font-size: 3rem; }
    .stSlider > div { padding-top: 0.3rem; }
    section[data-testid="stSidebar"] { background-color: #f0f4fa; }
</style>
""", unsafe_allow_html=True)

# ── Load model ────────────────────────────────────────────────────────────────
MODEL_PATH = os.path.join(os.path.dirname(__file__), "model_bundle.pkl")

@st.cache_resource
def load_model():
    with open(MODEL_PATH, "rb") as f:
        return pickle.load(f)

bundle = load_model()
model      = bundle["model"]
transformer = bundle["transformer"]
features   = bundle["features"]
r2         = bundle["r2"]
rmse       = bundle["rmse"]
y_min      = bundle["y_min"]
y_max      = bundle["y_max"]
y_mean     = bundle["y_mean"]

# ── Sidebar ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.image("https://img.icons8.com/color/96/000000/concrete-mixer.png", width=80)
    st.markdown("## ⚙️ Input Parameters")
    st.markdown("Adjust the mix design and curing conditions below:")
    st.markdown("---")

    cement     = st.slider("🪨 Cement (kg/m³)",        102.0, 540.0, 300.0, 1.0)
    blast_slag = st.slider("🔩 Blast Furnace Slag (kg/m³)", 0.0, 360.0, 100.0, 1.0)
    fly_ash    = st.slider("🌫️ Fly Ash (kg/m³)",        0.0, 200.0,  50.0, 1.0)
    water      = st.slider("💧 Water (kg/m³)",          121.0, 247.0, 185.0, 1.0)
    superp     = st.slider("🧪 Superplasticizer (kg/m³)",  0.0,  32.0,   6.0, 0.1)
    coarse_agg = st.slider("🪵 Coarse Aggregate (kg/m³)", 801.0,1145.0, 972.0, 1.0)
    fine_agg   = st.slider("🏖️ Fine Aggregate (kg/m³)",   594.0, 992.0, 773.0, 1.0)
    age        = st.slider("📅 Age (days)",                1,   365,   28,   1)

    st.markdown("---")
    predict_btn = st.button("🔍 Predict Strength", use_container_width=True, type="primary")

# ── Main area ─────────────────────────────────────────────────────────────────
st.markdown('<div class="main-header">🏗️ Concrete Compressive Strength Predictor</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-header">Predict the compressive strength of concrete (MPa) using an XGBoost model trained on 1,030 samples.</div>', unsafe_allow_html=True)

# Model metrics row
col1, col2, col3 = st.columns(3)
with col1:
    st.markdown(f'<div class="metric-card"><p>Model R² Score</p><h2>{r2:.2%}</h2></div>', unsafe_allow_html=True)
with col2:
    st.markdown(f'<div class="metric-card"><p>RMSE</p><h2>{rmse:.2f} MPa</h2></div>', unsafe_allow_html=True)
with col3:
    st.markdown(f'<div class="metric-card"><p>Algorithm</p><h2>XGBoost</h2></div>', unsafe_allow_html=True)

st.markdown("---")

# ── Prediction ────────────────────────────────────────────────────────────────
left, right = st.columns([1.2, 1])

with left:
    st.subheader("📋 Current Mix Design")
    input_data = {
        "Cement (kg/m³)":              cement,
        "Blast Furnace Slag (kg/m³)":  blast_slag,
        "Fly Ash (kg/m³)":             fly_ash,
        "Water (kg/m³)":               water,
        "Superplasticizer (kg/m³)":    superp,
        "Coarse Aggregate (kg/m³)":    coarse_agg,
        "Fine Aggregate (kg/m³)":      fine_agg,
        "Age (days)":                  age,
    }
    df_display = pd.DataFrame(input_data.items(), columns=["Parameter", "Value"])
    st.dataframe(df_display, use_container_width=True, hide_index=True)

with right:
    st.subheader("🎯 Prediction Result")

    if predict_btn:
        raw = np.array([[cement, blast_slag, fly_ash, water, superp, coarse_agg, fine_agg, age]], dtype=float)
        transformed = transformer.transform(raw + 0.000001)
        strength = float(model.predict(transformed)[0])
        strength = max(0.0, strength)  # clamp

        # Strength classification
        if strength < 20:
            grade, color, icon = "Low Strength", "#d32f2f", "⚠️"
        elif strength < 40:
            grade, color, icon = "Normal Strength", "#f57c00", "✅"
        elif strength < 60:
            grade, color, icon = "High Strength", "#388e3c", "💪"
        else:
            grade, color, icon = "Ultra-High Strength", "#1565c0", "🚀"

        st.markdown(f"""
        <div class="result-box">
            <h3>{icon} Predicted Compressive Strength</h3>
            <h1>{strength:.2f} MPa</h1>
            <p style="color:{color}; font-weight:600; margin-top:0.5rem; font-size:1rem;">{grade}</p>
        </div>
        """, unsafe_allow_html=True)

        # Progress bar relative to dataset range
        pct = min(1.0, (strength - y_min) / (y_max - y_min))
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown(f"**Strength relative to dataset range ({y_min:.1f} – {y_max:.1f} MPa)**")
        st.progress(pct)

        # Key ratios
        st.markdown("**Mix Design Insights**")
        wc_ratio = water / (cement + 1e-6)
        st.info(f"💧 Water-Cement Ratio: **{wc_ratio:.3f}** {'(low — good strength)' if wc_ratio < 0.5 else '(high — may reduce strength)'}")
    else:
        st.info("👈 Adjust the parameters on the left panel and click **Predict Strength**.")

# ── About section ─────────────────────────────────────────────────────────────
with st.expander("ℹ️ About this app"):
    st.markdown("""
    **Dataset:** UCI Concrete Compressive Strength dataset (1,030 samples)

    **Features used:**
    - Cement, Blast Furnace Slag, Fly Ash, Water, Superplasticizer, Coarse Aggregate, Fine Aggregate, Age

    **Pipeline:**
    1. Removed duplicates
    2. Applied **Box-Cox transformation** (PowerTransformer) for normality
    3. Trained an **XGBoost Regressor** (200 estimators)

    **Strength Classifications:**
    | Range | Grade |
    |---|---|
    | < 20 MPa | Low Strength |
    | 20–40 MPa | Normal Strength |
    | 40–60 MPa | High Strength |
    | > 60 MPa | Ultra-High Strength |

    **Original project by:** [codebyPabitraa](https://github.com/codebyPabitraa/Concrete_Strength_Prediction)
    """)

st.markdown("---")
st.caption("Built with Streamlit · XGBoost · scikit-learn")