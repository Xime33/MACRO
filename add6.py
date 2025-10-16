import streamlit as st
import matplotlib.pyplot as plt
import numpy as np

# Valores por defecto
default_values = {
    "C_t_a": 4, "C_t_ct": 0.8, "Yt": 5,
    "C_k_b": 1, "C_k_ck": 0.2,"pik": 5,
    "I_h": 3, "I_i": 0.4, "pi": 5,
    "G_d": 2, "G_g": 0.4, "Rf": 5,
    "X_e": 2, "X_x": 0.2, "Yeu": 5,
    "M_f": 1, "M_m": 0.2, "Ymex": 5
}

# Funciones
def calcular_Ct(a, ct, Yt): return a + ct * Yt
def calcular_Ck(b, ck, pik): return b + ck * pik
def calcular_I(h, i_val, pi): return h + i_val * pi
def calcular_G(d, g, Rf): return d + g * Rf
def calcular_X(e, x_val, Yeu): return e + x_val * Yeu
def calcular_M(f, m, Ymex): return f + m * Ymex

# Interfaz
st.title("📊 Macroeconomía - PIB y funciones")

st.sidebar.header("Parámetros")
a = st.sidebar.number_input("C_t - a", value=default_values["C_t_a"])
ct = st.sidebar.number_input("C_t - ct", value=default_values["C_t_ct"])
b = st.sidebar.number_input("C_k - b", value=default_values["C_k_b"])
ck = st.sidebar.number_input("C_k - ck", value=default_values["C_k_ck"])
h = st.sidebar.number_input("I - h", value=default_values["I_h"])
i_val = st.sidebar.number_input("I - i", value=default_values["I_i"])
d = st.sidebar.number_input("G - d", value=default_values["G_d"])
g_val = st.sidebar.number_input("G - g", value=default_values["G_g"])
e = st.sidebar.number_input("X - e", value=default_values["X_e"])
x_val = st.sidebar.number_input("X - x", value=default_values["X_x"])
f = st.sidebar.number_input("M - f", value=default_values["M_f"])
m_val = st.sidebar.number_input("M - m", value=default_values["M_m"])

# Variables independientes (rangos)
st.sidebar.subheader("Rango de variables independientes")
def get_range(name, default_start=0, default_end=5, default_step=1):
    start = st.sidebar.number_input(f"{name} start", value=default_start)
    end = st.sidebar.number_input(f"{name} end", value=default_end)
    step = st.sidebar.number_input(f"{name} step", value=default_step)
    return np.arange(start, end+step, step)

Yt_range = get_range("Yt")
pik_range = get_range("pik")
pi_range = get_range("pi")
Rf_range = get_range("Rf")
Yeu_range = get_range("Yeu")
Ymex_range = get_range("Ymex")

# Calcular métricas usando el **último valor de cada rango**
CT = calcular_Ct(a, ct, Yt_range[-1])
CK = calcular_Ck(b, ck, pik_range[-1])
I = calcular_I(h, i_val, pi_range[-1])
G = calcular_G(d, g_val, Rf_range[-1])
X = calcular_X(e, x_val, Yeu_range[-1])
M = calcular_M(f, m_val, Ymex_range[-1])
PIB_final = CT + CK + I + G + (X - M)

st.subheader(f"PIB Final (calculado): **{PIB_final:.2f}**")

# Breakdown
col1, col2, col3 = st.columns(3)
with col1:
    st.metric("Consumo (C_t)", f"{CT:.2f}")
    st.metric("Consumo (C_k)", f"{CK:.2f}")
with col2:
    st.metric("Inversión (I)", f"{I:.2f}")
    st.metric("Gasto Público (G)", f"{G:.2f}")
with col3:
    st.metric("Exportaciones (X)", f"{X:.2f}")
    st.metric("Importaciones (M)", f"{M:.2f}")
st.metric("**Exportaciones Netas (X-M)**", f"{X-M:.2f}")

# Funciones con historial
st.subheader("📈 Gráficas de las funciones")
funcs = {
    "C_t": (calcular_Ct, a, ct, Yt_range, "Yt"),
    "C_k": (calcular_Ck, b, ck, pik_range, "pik"),
    "I": (calcular_I, h, i_val, pi_range, "π"),
    "G": (calcular_G, d, g_val, Rf_range, "Rf"),
    "X": (calcular_X, e, x_val, Yeu_range, "Yeu"),
    "M": (calcular_M, f, m_val, Ymex_range, "Ymex")
}

# Inicializar sesión
if "funciones_historial" not in st.session_state:
    st.session_state["funciones_historial"] = {name: [] for name in funcs}
if "ultimos_parametros" not in st.session_state:
    st.session_state["ultimos_parametros"] = {name: None for name in funcs}

if st.button("🔄 Reset History"):
    st.session_state["funciones_historial"] = {name: [] for name in funcs}
    st.session_state["ultimos_parametros"] = {name: None for name in funcs}
    st.rerun()

# Graficar con historial
for name, (func, p1, p2, x_vals, xlabel) in funcs.items():
    st.markdown(f"### {name}")
    parametros_actuales = (p1, p2, tuple(x_vals))
    if st.session_state["ultimos_parametros"][name] != parametros_actuales:
        y_vals = [func(p1, p2, x) for x in x_vals]
        st.session_state["funciones_historial"][name].append((x_vals, y_vals))
        st.session_state["ultimos_parametros"][name] = parametros_actuales
    colors = plt.cm.viridis(np.linspace(0, 1, len(st.session_state["funciones_historial"][name])))
    fig, ax = plt.subplots(figsize=(5, 3))
    for idx, (x_h, y_h) in enumerate(st.session_state["funciones_historial"][name]):
        ax.plot(x_h, y_h, marker="o", label=f"{name} v{idx+1}", color=colors[idx], linewidth=2, alpha=0.7)
    ax.set_title(f"Función {name}")
    ax.set_xlabel(xlabel)
    ax.set_ylabel(name)
    ax.grid(True)
    ax.legend()
    st.pyplot(fig)
