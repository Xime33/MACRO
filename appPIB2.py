import streamlit as st
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import numpy as np
import pandas as pd


# =======================
#   LOAD PIB DATA
# =======================
pib_df = pd.read_csv("pib_mexico.csv")  # or use st.file_uploader if uploading in app
pib_df["TIME_PERIOD"] = pib_df["TIME_PERIOD"].astype(int)
pib_df["OBS_VALUE"] = pib_df["OBS_VALUE"].astype(float)
pib_fijo = dict(zip(pib_df["TIME_PERIOD"], pib_df["OBS_VALUE"]))

# Convert to millions of pesos
pib_fijo_millones = {year: value / 1e6 for year, value in pib_fijo.items()}


# =======================
#   DEFAULT PARAMETERS
# =======================
default_values = {
    "C_t_a": 4, "C_t_ct": 0.8, "Yt": 5,
    "C_k_b": 1, "C_k_ck": 0.2, "pik": 5,
    "I_h": 3, "I_i": 0.4, "pi": 5,
    "G_d": 2, "G_g": 0.4, "Rf": 5,
    "X_e": 2, "X_x": 0.2, "Yeu": 5,
    "M_f": 1, "M_m": 0.2, "Ymex": 5
}

lista = [0, 1, 2, 3, 2, 1, 2, 4, 5, 4, 3, 2, 3, 4, 5]  # Economic cycle
years = list(range(2011, 2026))


# =======================
#   FUNCTIONS
# =======================
def calcular_Ct(a, ct, Yt): return a + ct * Yt
def calcular_Ck(b, ck, pik): return b + ck * pik
def calcular_I(h, i_val, pi): return h + i_val * pi
def calcular_G(d, g, Rf): return d + g * Rf
def calcular_X(e, x_val, Yeu): return e + x_val * Yeu
def calcular_M(f, m, Ymex): return f + m * Ymex

def ciclo_Ct(a, ct): return [a + ct * i for i in lista]
def ciclo_Ck(b, ck): return [b + ck * i for i in lista]
def ciclo_I(h, i_val): return [h + i_val * i for i in lista]
def ciclo_G(d, g): return [d + g * i for i in lista]
def ciclo_X(e, x_val): return [e + x_val * i for i in lista]
def ciclo_M(f, m): return [f + m * i for i in lista]


# =======================
#   STREAMLIT UI
# =======================
st.title("Macroeconomía - PIB y Funciones")


# --- Sidebar Parameters ---
with st.sidebar.expander("Consumo (C)"):
    a = st.number_input("C_t - a", value=default_values["C_t_a"])
    ct = st.number_input("C_t - ct", value=default_values["C_t_ct"])
    b = st.number_input("C_k - b", value=default_values["C_k_b"])
    ck = st.number_input("C_k - ck", value=default_values["C_k_ck"])

with st.sidebar.expander("Inversión (I)"):
    h = st.number_input("I - h", value=default_values["I_h"])
    i_val = st.number_input("I - i", value=default_values["I_i"])

with st.sidebar.expander("Gasto Público (G)"):
    d = st.number_input("G - d", value=default_values["G_d"])
    g_val = st.number_input("G - g", value=default_values["G_g"])

with st.sidebar.expander("Comercio Exterior"):
    e = st.number_input("X - e", value=default_values["X_e"])
    x_val = st.number_input("X - x", value=default_values["X_x"])
    f = st.number_input("M - f", value=default_values["M_f"])
    m_val = st.number_input("M - m", value=default_values["M_m"])


# --- Ranges ---
st.sidebar.subheader("Rango de variables independientes")

def get_range(name, default_start=0, default_end=5, default_step=1):
    start = st.sidebar.number_input(f"{name} start", value=default_start)
    end = st.sidebar.number_input(f"{name} end", value=default_end)
    step = st.sidebar.number_input(f"{name} step", value=default_step)
    return np.arange(start, end + step, step)

Yt_range = get_range("Yt")
pik_range = get_range("pik")
pi_range = get_range("pi")
Rf_range = get_range("Rf")
Yeu_range = get_range("Yeu")
Ymex_range = get_range("Ymex")


# --- Calculate PIB Components ---
CT = calcular_Ct(a, ct, Yt_range[-1])
CK = calcular_Ck(b, ck, pik_range[-1])
I_val = calcular_I(h, i_val, pi_range[-1])
G_val = calcular_G(d, g_val, Rf_range[-1])
X_val = calcular_X(e, x_val, Yeu_range[-1])
M_val = calcular_M(f, m_val, Ymex_range[-1])
PIB_final = CT + CK + I_val + G_val + (X_val - M_val)


# --- Display Summary ---
st.subheader("PIB Final y Componentes")
col1, col2, col3 = st.columns(3)
col1.metric("Consumo C_t", f"{CT:.2f}")
col1.metric("Consumo C_k", f"{CK:.2f}")
col2.metric("Inversión I", f"{I_val:.2f}")
col2.metric("Gasto Público G", f"{G_val:.2f}")
col3.metric("Exportaciones X", f"{X_val:.2f}")
col3.metric("Importaciones M", f"{M_val:.2f}")
st.metric("Exportaciones Netas (X-M)", f"{X_val - M_val:.2f}")
st.subheader(f"PIB Final (calculado): **{PIB_final:.2f}**")


# =======================
#   DYNAMIC PIB STORAGE
# =======================
if "pib_dinamico" not in st.session_state:
    st.session_state["pib_dinamico"] = {2024: None, 2025: None}

col_year, col_store = st.columns([1, 1])
with col_year:
    year_selected_pib = st.selectbox("Año a modificar (PIB)", [2024, 2025], key="selectbox_pib_final")
with col_store:
    if st.button("Guardar PIB calculado", key="guardar_pib_final"):
        st.session_state["pib_dinamico"][year_selected_pib] = PIB_final


# =======================
#   PIB HISTORICAL PLOT
# =======================
years_plot = sorted(set(list(pib_fijo_millones.keys()) + list(st.session_state["pib_dinamico"].keys())))
values_plot = [
    st.session_state["pib_dinamico"].get(y, pib_fijo_millones.get(y, np.nan))
    for y in years_plot
]

fig_pib, ax_pib = plt.subplots(figsize=(8, 4))
ax_pib.plot(years_plot, values_plot, marker="o", color="blue", linestyle="-", label="PIB (base 2018)")

# Highlight dynamic years (2024–2025)
for year in [2024, 2025]:
    if st.session_state["pib_dinamico"].get(year) is not None:
        ax_pib.scatter(year, st.session_state["pib_dinamico"][year],
                       color="red", s=100, zorder=5)
# Shade recent projection period
ax_pib.axvspan(2023.5, 2025.5, color="gray", alpha=0.1, label="Proyecciones recientes")

# Format axis
ax_pib.set_xticks(years_plot)
ax_pib.set_xticklabels(years_plot, rotation=45)
ax_pib.set_xlabel("Año")
ax_pib.set_ylabel("PIB (millones de pesos, base 2018)")
ax_pib.set_title("Evolución del PIB de México (millones de pesos, base 2018)")
ax_pib.grid(True)
ax_pib.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"{x:,.0f}"))
ax_pib.legend()
st.pyplot(fig_pib, clear_figure=True)
