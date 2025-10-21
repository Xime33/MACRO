import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
import re

from style50 import StyleCheck, Style50


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
    a = st.number_input("C_t - a", value=default_values["C_t_a"])
    ct = st.number_input("C_t - ct", value=default_values["C_t_ct"])
    b = st.number_input("C_k - b", value=default_values["C_k_b"])
    ck = st.number_input("C_k - ck", value=default_values["C_k_ck"])

with st.sidebar.expander("Inversión (I)"):
    h = st.number_input("I - h", value=default_values["I_h"])
    i_val = st.number_input("I - i", value=default_values["I_i"])
    pi_val = st.number_input("π", value=default_values["pi"])

with st.sidebar.expander("Gasto Público (G)"):
    d = st.number_input("G - d", value=default_values["G_d"])
    g_val = st.number_input("G - g", value=default_values["G_g"])
    Rf = st.number_input("Rf", value=default_values["Rf"])

with st.sidebar.expander("Comercio Exterior"):
    e = st.number_input("X - e", value=default_values["X_e"])
    x_val = st.number_input("X - x", value=default_values["X_x"])
    f = st.number_input("M - f", value=default_values["M_f"])
    m_val = st.number_input("M - m", value=default_values["M_m"])
    Yeu = st.number_input("Yeu", value=default_values["Yeu"])
    Ymex = st.number_input("Ymex", value=default_values["Ymex"])

# Sidebar ranges
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


CT = calcular_Ct(a, ct, Yt_range[-1])
CK = calcular_Ck(b, ck, pik_range[-1])
I = calcular_I(h, i_val, pi_range[-1])
G = calcular_G(d, g_val, Rf_range[-1])
X = calcular_X(e, x_val, Yeu_range[-1])
M = calcular_M(f, m_val, Ymex_range[-1])
PIB_final = CT + CK + I + G + (X - M)


st.subheader("PIB Final y Componentes")
col1, col2, col3 = st.columns(3)
col1.metric("Consumo C_t", f"{CT:.2f}")
col1.metric("Consumo C_k", f"{CK:.2f}")
col2.metric("Inversión I", f"{I:.2f}")
col2.metric("Gasto Público G", f"{G:.2f}")
col3.metric("Exportaciones X", f"{X:.2f}")
col3.metric("Importaciones M", f"{M:.2f}")
st.metric("Exportaciones Netas (X-M)", f"{X-M:.2f}")
st.subheader(f"PIB Final (calculado): **{PIB_final:.2f}**")


funcs = {
    "C_t": (calcular_Ct, a, ct, Yt_range, "Yt", ciclo_Ct),
    "C_k": (calcular_Ck, b, ck, pik_range, "pik", ciclo_Ck),
    "I": (calcular_I, h, i_val, pi_range, "π", ciclo_I),
    "G": (calcular_G, d, g_val, Rf_range, "Rf", ciclo_G),
    "X": (calcular_X, e, x_val, Yeu_range, "Yeu", ciclo_X),
    "M": (calcular_M, f, m_val, Ymex_range, "Ymex", ciclo_M)
}

if "funciones_historial" not in st.session_state:
    st.session_state["funciones_historial"] = {name: [] for name in funcs}
if "ultimos_parametros" not in st.session_state:
    st.session_state["ultimos_parametros"] = {name: None for name in funcs}
if "stored_year_values" not in st.session_state:
    st.session_state["stored_year_values"] = {2024: {}, 2025: {}}


col_reset, col_year, col_store = st.columns([1, 1, 1])
with col_reset:
    if st.button("Reset History"):
        st.session_state["funciones_historial"] = {name: [] for name in funcs}
        st.session_state["ultimos_parametros"] = {name: None for name in funcs}
        st.session_state["stored_year_values"] = {2024: {}, 2025: {}}
        st.rerun()
with col_year:
    year_selected = st.selectbox("Año a modificar", [2024, 2025])
with col_store:
    store_clicked = st.button("Guardar Valor del Año")

independent_ranges = {
    "C_t": (Yt_range, default_values["Yt"]),
    "C_k": (pik_range, default_values["pik"]),
    "I": (pi_range, default_values["pi"]),
    "G": (Rf_range, default_values["Rf"]),
    "X": (Yeu_range, default_values["Yeu"]),
    "M": (Ymex_range, default_values["Ymex"])
}

default_cycle_params = {
    "C_t": (default_values["C_t_a"], default_values["C_t_ct"]),
    "C_k": (default_values["C_k_b"], default_values["C_k_ck"]),
    "I": (default_values["I_h"], default_values["I_i"]),
    "G": (default_values["G_d"], default_values["G_g"]),
    "X": (default_values["X_e"], default_values["X_x"]),
    "M": (default_values["M_f"], default_values["M_m"])
}


for name, (func, p1, p2, x_vals, xlabel, ciclo_func) in funcs.items():
    st.markdown(f"### {name}")
    parametros_actuales = (p1, p2, tuple(x_vals))
    
    if st.session_state["ultimos_parametros"][name] != parametros_actuales:
        y_vals = [func(p1, p2, x) for x in x_vals]
        st.session_state["funciones_historial"][name].append((x_vals, y_vals))
        st.session_state["ultimos_parametros"][name] = parametros_actuales

    col_plot1, col_plot2 = st.columns(2)
    
    # Historical ranges plot
    with col_plot1:
        fig, ax = plt.subplots(figsize=(5, 3))
        colors = plt.cm.viridis(np.linspace(
            0, 1, len(st.session_state["funciones_historial"][name])))
        for idx, (x_h, y_h) in enumerate(st.session_state["funciones_historial"][name]):
            ax.plot(x_h, y_h, marker="o", color=colors[idx], linewidth=2, alpha=0.7)
        ax.set_xlabel(xlabel)
        ax.set_ylabel(name)
        ax.grid(True)
        st.pyplot(fig)
    
    # Economic cycle plot
    with col_plot2:
        default_p1, default_p2 = default_cycle_params[name]
        full_cycle = ciclo_func(default_p1, default_p2)
        if len(full_cycle) < len(years):
            full_cycle += [full_cycle[-1]] * (len(years) - len(full_cycle))

        # Get stored or current values
        current_val = independent_ranges[name][0][-1]
        val_2024_current = func(p1, p2, current_val)
        val_2025_current = func(p1, p2, current_val)
        
        val_2024_plot = st.session_state["stored_year_values"][2024].get(
            name, full_cycle[years.index(2024)])
        val_2025_plot = st.session_state["stored_year_values"][2025].get(
            name, full_cycle[years.index(2025)])
        
        if store_clicked:
            st.session_state["stored_year_values"][year_selected][name] = val_2024_current if year_selected == 2024 else val_2025_current
            val_2024_plot = st.session_state["stored_year_values"][2024].get(name, val_2024_plot)
            val_2025_plot = st.session_state["stored_year_values"][2025].get(name, val_2025_plot)

        full_cycle[years.index(2024)] = val_2024_plot
        full_cycle[years.index(2025)] = val_2025_plot

        fig2, ax2 = plt.subplots(figsize=(5, 3))
        ax2.plot(years, full_cycle, marker="o", color="orange",
                  linewidth=2, alpha=0.7, label="Ciclo económico")
        ax2.scatter([2024, 2025], [val_2024_plot, val_2025_plot], color="red", s=80,
                     label=[f'2024: {val_2024_plot:.2f}', f'2025: {val_2025_plot:.2f}'])
        ax2.set_xlabel("Año")
        ax2.set_ylabel(name)
        ax2.grid(True)
        ax2.legend()
        st.pyplot(fig2)
