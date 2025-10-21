import streamlit as st
import matplotlib.pyplot as plt
import numpy as np


default_values = {
    "C_t_a": 4, "C_t_ct": 0.8, "Yt": 5,
    "C_k_b": 1, "C_k_ck": 0.2,"pik": 5,
    "I_h": 3, "I_i": 0.4, "pi": 5,
    "G_d": 2, "G_g": 0.4, "Rf": 5,
    "X_e": 2, "X_x": 0.2, "Yeu": 5,
    "M_f": 1, "M_m": 0.2, "Ymex": 5
}

lista = [0, 1, 2, 3, 2, 1, 2, 4, 5, 4, 3, 2, 3, 4, 5]
years = list(range(2011, 2026))


def calcular_Ct(a, ct, Yt): return a + ct * Yt
def calcular_Ck(b, ck, pik): return b + ck * pik
def calcular_I(h, i_val, pi): return h + i_val * pi
def calcular_G(d, g, Rf): return d + g * Rf
def calcular_X(e, x_val, Yeu): return e + x_val * Yeu
def calcular_M(f, m, Ymex): return f + m * Ymex

def ciclo_Ct(a, ct): return [a + ct*i for i in lista]
def ciclo_Ck(b, ck): return [b + ck*i for i in lista]
def ciclo_I(h, i_val): return [h + i_val*i for i in lista]
def ciclo_G(d, g): return [d + g*i for i in lista]
def ciclo_X(e, x_val): return [e + x_val*i for i in lista]
def ciclo_M(f, m): return [f + m*i for i in lista]

st.title("Macroeconomía - PIB y Funciones")


with st.sidebar.expander("Consumo (C)"):
    a = st.number_input("C_t - a", value=default_values["C_t_a"], key="C_t_a")
    ct = st.number_input("C_t - ct", value=default_values["C_t_ct"], key="C_t_ct")
    b = st.number_input("C_k - b", value=default_values["C_k_b"], key="C_k_b")
    ck = st.number_input("C_k - ck", value=default_values["C_k_ck"], key="C_k_ck")

with st.sidebar.expander("Inversión (I)"):
    h = st.number_input("I - h", value=default_values["I_h"], key="I_h")
    i_val = st.number_input("I - i", value=default_values["I_i"], key="I_i")
    pi_val = st.number_input("π", value=default_values["pi"], key="pi")

with st.sidebar.expander("Gasto Público (G)"):
    d = st.number_input("G - d", value=default_values["G_d"], key="G_d")
    g_val = st.number_input("G - g", value=default_values["G_g"], key="G_g")
    Rf = st.number_input("Rf", value=default_values["Rf"], key="Rf")

with st.sidebar.expander("Comercio Exterior"):
    e = st.number_input("X - e", value=default_values["X_e"], key="X_e")
    x_val = st.number_input("X - x", value=default_values["X_x"], key="X_x")
    f = st.number_input("M - f", value=default_values["M_f"], key="M_f")
    m_val = st.number_input("M - m", value=default_values["M_m"], key="M_m")
    Yeu = st.number_input("Yeu", value=default_values["Yeu"], key="Yeu")
    Ymex = st.number_input("Ymex", value=default_values["Ymex"], key="Ymex")


st.sidebar.subheader("Rango de variables independientes")
def get_range(name, default_start=0, default_end=5, default_step=1):
    start = st.sidebar.number_input(f"{name} start", value=default_start, key=f"{name}_start")
    end = st.sidebar.number_input(f"{name} end", value=default_end, key=f"{name}_end")
    step = st.sidebar.number_input(f"{name} step", value=default_step, key=f"{name}_step")
    return np.arange(start, end+step, step)

Yt_range = get_range("Yt")
pik_range = get_range("pik")
pi_range = get_range("pi")
Rf_range = get_range("Rf")
Yeu_range = get_range("Yeu")
Ymex_range = get_range("Ymex")


funcs = {
    "C_t": (calcular_Ct, a, ct, Yt_range, "Yt", ciclo_Ct),
    "C_k": (calcular_Ck, b, ck, pik_range, "pik", ciclo_Ck),
    "I": (calcular_I, h, i_val, pi_range, "π", ciclo_I),
    "G": (calcular_G, d, g_val, Rf_range, "Rf", ciclo_G),
    "X": (calcular_X, e, x_val, Yeu_range, "Yeu", ciclo_X),
    "M": (calcular_M, f, m_val, Ymex_range, "Ymex", ciclo_M)
}

default_cycle_params = {
    "C_t": (default_values["C_t_a"], default_values["C_t_ct"]),
    "C_k": (default_values["C_k_b"], default_values["C_k_ck"]),
    "I": (default_values["I_h"], default_values["I_i"]),
    "G": (default_values["G_d"], default_values["G_g"]),
    "X": (default_values["X_e"], default_values["X_x"]),
    "M": (default_values["M_f"], default_values["M_m"])
}


if "funciones_historial" not in st.session_state:
    st.session_state["funciones_historial"] = {name: [] for name in funcs}
if "ultimos_parametros" not in st.session_state:
    st.session_state["ultimos_parametros"] = {name: None for name in funcs}
if "stored_year_values" not in st.session_state:
    st.session_state["stored_year_values"] = {2024: {}, 2025: {}}
if "pib_dinamico" not in st.session_state:
    st.session_state["pib_dinamico"] = {2024: None, 2025: None}


CT = calcular_Ct(a, ct, Yt_range[-1])
CK = calcular_Ck(b, ck, pik_range[-1])
I_val = calcular_I(h, i_val, pi_range[-1])
G_val = calcular_G(d, g_val, Rf_range[-1])
X_val = calcular_X(e, x_val, Yeu_range[-1])
M_val = calcular_M(f, m_val, Ymex_range[-1])
PIB_final = CT + CK + I_val + G_val + (X_val - M_val)

st.subheader(f"PIB Final (calculado): **{PIB_final:.2f}**")


col_year, col_store = st.columns([1,1])
with col_year:
    year_selected = st.selectbox("Año a modificar", [2024, 2025], key="selectbox_pib")
with col_store:
    store_clicked = st.button("Guardar PIB calculado", key="guardar_pib")
    if store_clicked:
        st.session_state["pib_dinamico"][year_selected] = PIB_final


pib_fijo = {
    2011: 20, 2012: 21, 2013: 21.5, 2014: 22, 2015: 21,
    2016: 20.5, 2017: 20, 2018: 19, 2019: 19.5, 2020: 18,
    2021: 19.5, 2022: 20.5, 2023: 20, 2024: 19.5, 2025: 20
}

years_plot = sorted(pib_fijo.keys())
values_plot = [st.session_state["pib_dinamico"].get(y, pib_fijo[y]) for y in years_plot]

fig, ax = plt.subplots(figsize=(8,4))
ax.plot(years_plot, values_plot, marker="o", color="blue", linestyle="-", label="PIB")
for year in [2024, 2025]:
    if st.session_state["pib_dinamico"][year] is not None:
        ax.scatter(year, st.session_state["pib_dinamico"][year], color="red", s=100, zorder=5, label=f"PIB {year} dinámico")
ax.set_xlabel("Año")
ax.set_ylabel("PIB (B)")
ax.set_title("Evolución histórica del PIB")
ax.grid(True)
ax.legend()
plt.tight_layout()
st.pyplot(fig)
