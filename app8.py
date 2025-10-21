import streamlit as st
import matplotlib.pyplot as plt
import numpy as np

# =====================
# 🎯 Default Parameters
# =====================
default_values = {
    "C_t_a": 4, "C_t_ct": 0.8, "Yt": 5,
    "C_k_b": 1, "C_k_ck": 0.2, "pik": 5,
    "I_h": 3, "I_i": 0.4, "pi": 5,
    "G_d": 2, "G_g": 0.4, "Rf": 5,
    "X_e": 2, "X_x": 0.2, "Yeu": 5,
    "M_f": 1, "M_m": 0.2, "Ymex": 5
}

years = list(range(2011, 2026))
lista = [0, 1, 2, 3, 2, 1, 2, 4, 5, 4, 3, 2, 3, 4, 5]

# =====================
# 🧮 Core Calculations
# =====================
def calcular_Ct(a, ct, Yt): return a + ct * Yt
def calcular_Ck(b, ck, pik): return b + ck * pik
def calcular_I(h, i_val, pi): return h + i_val * pi
def calcular_G(d, g, Rf): return d + g * Rf
def calcular_X(e, x_val, Yeu): return e + x_val * Yeu
def calcular_M(f, m, Ymex): return f + m * Ymex

def ciclo_func(param1, param2):
    return [param1 + param2 * i for i in lista]

# =====================
# 🖥️ Streamlit UI Setup
# =====================
st.title("📊 Macroeconomía - PIB y Funciones")

st.sidebar.header("🔧 Parámetros")
st.sidebar.caption("Ajusta los valores de las funciones macroeconómicas")

# --- Sidebar Sections ---
def sidebar_section(title, inputs):
    with st.sidebar.expander(title):
        values = {}
        for label, key in inputs:
            values[key] = st.number_input(label, value=default_values[key])
        return values

consumo = sidebar_section("Consumo (C)", [
    ("C_t - a", "C_t_a"), ("C_t - ct", "C_t_ct"),
    ("C_k - b", "C_k_b"), ("C_k - ck", "C_k_ck")
])
inversion = sidebar_section("Inversión (I)", [
    ("I - h", "I_h"), ("I - i", "I_i"), ("π", "pi")
])
gasto = sidebar_section("Gasto Público (G)", [
    ("G - d", "G_d"), ("G - g", "G_g"), ("Rf", "Rf")
])
comercio = sidebar_section("Comercio Exterior", [
    ("X - e", "X_e"), ("X - x", "X_x"),
    ("M - f", "M_f"), ("M - m", "M_m")
])

# --- Ranges ---
def range_slider(name, default):
    return np.arange(
        *st.sidebar.slider(f"{name} range", 0, 10, (0, default), 1)
    )

Yt_range = range_slider("Yt", default_values["Yt"])
pik_range = range_slider("pik", default_values["pik"])
pi_range = range_slider("pi", default_values["pi"])
Rf_range = range_slider("Rf", default_values["Rf"])
Yeu_range = range_slider("Yeu", default_values["Yeu"])
Ymex_range = range_slider("Ymex", default_values["Ymex"])

# =====================
# 🧾 Calculate Components
# =====================
CT = calcular_Ct(consumo["C_t_a"], consumo["C_t_ct"], Yt_range[-1])
CK = calcular_Ck(consumo["C_k_b"], consumo["C_k_ck"], pik_range[-1])
I = calcular_I(inversion["I_h"], inversion["I_i"], pi_range[-1])
G = calcular_G(gasto["G_d"], gasto["G_g"], Rf_range[-1])
X = calcular_X(comercio["X_e"], comercio["X_x"], Yeu_range[-1])
M = calcular_M(comercio["M_f"], comercio["M_m"], Ymex_range[-1])
PIB_final = CT + CK + I + G + (X - M)

# =====================
# 📈 Metrics Overview
# =====================
st.subheader("📊 PIB Final y Componentes")
col1, col2, col3 = st.columns(3)
col1.metric("C_t", f"{CT:.2f}")
col1.metric("C_k", f"{CK:.2f}")
col2.metric("Inversión I", f"{I:.2f}")
col2.metric("Gasto Público G", f"{G:.2f}")
col3.metric("Exportaciones X", f"{X:.2f}")
col3.metric("Importaciones M", f"{M:.2f}")
st.metric("Exportaciones Netas (X-M)", f"{X - M:.2f}")
st.subheader(f"📌 PIB Final Calculado: **{PIB_final:.2f}**")

# =====================
# 🧮 Funciones & Gráficas
# =====================
funcs = {
    "C_t": (calcular_Ct, consumo["C_t_a"], consumo["C_t_ct"], Yt_range, "Yt"),
    "C_k": (calcular_Ck, consumo["C_k_b"], consumo["C_k_ck"], pik_range, "pik"),
    "I": (calcular_I, inversion["I_h"], inversion["I_i"], pi_range, "π"),
    "G": (calcular_G, gasto["G_d"], gasto["G_g"], Rf_range, "Rf"),
    "X": (calcular_X, comercio["X_e"], comercio["X_x"], Yeu_range, "Yeu"),
    "M": (calcular_M, comercio["M_f"], comercio["M_m"], Ymex_range, "Ymex")
}

if "historial" not in st.session_state:
    st.session_state["historial"] = {k: [] for k in funcs}

tabs = st.tabs(list(funcs.keys()))

for tab, (name, (func, p1, p2, x_vals, xlabel)) in zip(tabs, funcs.items()):
    with tab:
        y_vals = [func(p1, p2, x) for x in x_vals]
        st.session_state["historial"][name].append((x_vals, y_vals))

        fig, ax = plt.subplots(figsize=(6, 3))
        for i, (x, y) in enumerate(st.session_state["historial"][name]):
            ax.plot(x, y, label=f"Run {i+1}", linewidth=2, alpha=0.7)
        ax.set_title(f"Función {name}")
        ax.set_xlabel(xlabel)
        ax.set_ylabel(name)
        ax.grid(True)
        ax.legend()
        st.pyplot(fig)

        # Ciclo Económico
        fig2, ax2 = plt.subplots(figsize=(6, 3))
        cycle = ciclo_func(p1, p2)
        ax2.plot(years, cycle[:len(years)], color="orange", marker="o")
        ax2.set_title(f"Ciclo Económico - {name}")
        ax2.set_xlabel("Año")
        ax2.set_ylabel(name)
        ax2.grid(True)
        st.pyplot(fig2)

# =====================
# 📊 PIB Histórico
# =====================
st.markdown("---")
st.subheader("📈 Evolución Histórica del PIB")

pib_fijo = {
    2011: 20, 2012: 21, 2013: 21.5, 2014: 22, 2015: 21,
    2016: 20.5, 2017: 20, 2018: 19, 2019: 19.5, 2020: 18,
    2021: 19.5, 2022: 20.5, 2023: 20, 2024: 19.5, 2025: 20
}

if "pib_dinamico" not in st.session_state:
    st.session_state["pib_dinamico"] = {2024: None, 2025: None}

col_year, col_store = st.columns([1, 1])
with col_year:
    year_sel = st.selectbox("Año para modificar", [2024, 2025])
with col_store:
    if st.button("Guardar PIB Actual"):
        st.session_state["pib_dinamico"][year_sel] = PIB_final

years_plot = sorted(pib_fijo.keys())
values_plot = [
    st.session_state["pib_dinamico"].get(y, pib_fijo[y]) for y in years_plot
]

fig_pib, ax_pib = plt.subplots(figsize=(8, 4))
ax_pib.plot(years_plot, values_plot, marker="o", linewidth=2)
for y in [2024, 2025]:
    val = st.session_state["pib_dinamico"][y]
    if val:
        ax_pib.scatter(y, val, color="red", s=100, label=f"PIB {y}: {val:.2f}")
ax_pib.set_xlabel("Año")
ax_pib.set_ylabel("PIB (B)")
ax_pib.set_title("Evolución Histórica del PIB")
ax_pib.grid(True)
ax_pib.legend()
st.pyplot(fig_pib)
