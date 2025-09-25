import streamlit as st
import matplotlib.pyplot as plt

# =====================
# Valores por defecto
# =====================
default_values = {
    "C_t_a": 4, "C_t_ct": 0.8, "Yt": 5,
    "C_k_b": 1, "C_k_ck": 0.2, "Yk": 5,
    "I_h": 3, "I_i": 0.4, "pi": 5,
    "G_d": 2, "G_g": 0.4, "Rf": 5,
    "X_e": 2, "X_x": 0.2, "Yeu": 5,
    "M_f": 1, "M_m": 0.2, "Ymex": 5
}

# =====================
# Funciones
# =====================
def calcular_Ct(a, ct, Yt): return a + ct*Yt
def calcular_Ck(b, ck, Yk): return b + ck*Yk
def calcular_I(h, i_val, pi): return h + i_val*pi
def calcular_G(d, g, Rf): return d + g*Rf
def calcular_X(e, x_val, Yeu): return e + x_val*Yeu
def calcular_M(f, m, Ymex): return f + m*Ymex

# =====================
# Interfaz Streamlit
# =====================
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

# Variables independientes (constantes)
Yt, Yk, pi, Rf, Yeu, Ymex = (
    default_values["Yt"],
    default_values["Yk"],
    default_values["pi"],
    default_values["Rf"],
    default_values["Yeu"],
    default_values["Ymex"],
)

# Calcular valores
CT = calcular_Ct(a, ct, Yt)
CK = calcular_Ck(b, ck, Yk)
I = calcular_I(h, i_val, pi)
G = calcular_G(d, g_val, Rf)
X = calcular_X(e, x_val, Yeu)
M = calcular_M(f, m_val, Ymex)

PIB_final = CT + CK + I + G + (X - M)

st.subheader(f"PIB Final (calculado): **{PIB_final:.2f}**")

# =====================
# Gráfica del PIB fija
# =====================
pib_fijo = {
    2011: 20,
    2012: 21,
    2013: 21.5,
    2014: 22,
    2015: 21,
    2016: 20.5,
    2017: 20,
    2018: 19,
    2019: 19.5,
    2020: 18,
    2021: 19.5,
    2022: 20.5,
    2023: 20,
    2024: 19.5,
    2025: 20
}

st.subheader("📈 Evolución histórica del PIB (fija)")
fig, ax = plt.subplots(figsize=(8, 4))
years = sorted(pib_fijo.keys())
values = [pib_fijo[y] for y in years]
ax.plot(years, values, marker="o", color="blue", linestyle="-")
ax.set_xlabel("Año")
ax.set_ylabel("PIB (B)")
ax.set_title("Evolución histórica del PIB")
ax.grid(True)
st.pyplot(fig)

# =====================
# Gráficas de funciones con historial SOLO si cambian parámetros
# =====================
st.subheader("📈 Gráficas de las funciones")

# Diccionario con funciones y parámetros
funcs = {
    "C_t": (calcular_Ct, a, ct, Yt, "Yt"),
    "C_k": (calcular_Ck, b, ck, Yk, "Yk"),
    "I": (calcular_I, h, i_val, pi, "π"),
    "G": (calcular_G, d, g_val, Rf, "Rf"),
    "X": (calcular_X, e, x_val, Yeu, "Yeu"),
    "M": (calcular_M, f, m_val, Ymex, "Ymex")
}

# Inicializar almacenamiento si no existe
if "funciones_historial" not in st.session_state:
    st.session_state["funciones_historial"] = {name: [] for name in funcs}
if "ultimos_parametros" not in st.session_state:
    st.session_state["ultimos_parametros"] = {name: None for name in funcs}

# Generar gráficas independientes
for name, (func, p1, p2, y_var, xlabel) in funcs.items():
    st.markdown(f"### {name}")

    # Definir parámetros actuales como tupla (para detectar cambios)
    parametros_actuales = (p1, p2, y_var)

    # Solo agregar nueva curva si los parámetros cambiaron
    if st.session_state["ultimos_parametros"][name] != parametros_actuales:
        x_vals = [0, 1, 2, 3, 4, 5]
        y_vals = [func(p1, p2, Y) for Y in x_vals]
        st.session_state["funciones_historial"][name].append((x_vals, y_vals))
        st.session_state["ultimos_parametros"][name] = parametros_actuales

    # Graficar todas las curvas guardadas
    fig, ax = plt.subplots(figsize=(5, 3))
    for idx, (x_h, y_h) in enumerate(st.session_state["funciones_historial"][name]):
        ax.plot(x_h, y_h, marker="o", label=f"{name} v{idx+1}")
    ax.set_title(f"Función {name}")
    ax.set_xlabel(xlabel)
    ax.set_ylabel(name)
    ax.grid(True)
    ax.legend()
    st.pyplot(fig)
