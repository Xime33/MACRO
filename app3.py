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
# Inicializar almacenamiento
# =====================
if "pib_data" not in st.session_state:
    st.session_state["pib_data"] = {}  # {año: valor_PIB}

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

st.subheader(f"PIB Final: **{PIB_final:.2f}**")

# =====================
# Guardar PIB por año con validaciones
# =====================
st.subheader("💾 Guardar PIB por año")
anio = st.number_input("Año", min_value=1900, max_value=2100, value=2025, step=1)

if st.button("Guardar PIB"):
    if anio in st.session_state["pib_data"]:
        if st.checkbox(f"⚠️ El año {anio} ya tiene un valor ({st.session_state['pib_data'][anio]:.2f}). ¿Quieres sobrescribirlo?"):
            st.session_state["pib_data"][anio] = PIB_final
            st.success(f"✅ PIB actualizado para {anio}: {PIB_final:.2f} B")
        else:
            st.warning("Selecciona la casilla si quieres sobrescribir el valor existente.")
    else:
        st.session_state["pib_data"][anio] = PIB_final
        st.success(f"✅ PIB del año {anio} guardado: {PIB_final:.2f} B")

# =====================
# Mostrar / Editar / Eliminar datos guardados
# =====================
if st.session_state["pib_data"]:
    st.subheader("📑 Historial de PIB guardado")
    for year, pib in sorted(st.session_state["pib_data"].items()):
        col1, col2, col3 = st.columns([2, 2, 1])
        with col1:
            nuevo_valor = st.number_input(f"PIB {year}", value=pib, key=f"edit_{year}")
        with col2:
            if st.button(f"Actualizar {year}"):
                st.session_state["pib_data"][year] = nuevo_valor
                st.success(f"PIB de {year} actualizado a {nuevo_valor}")
        with col3:
            if st.button(f"🗑️ Borrar {year}"):
                del st.session_state["pib_data"][year]
                st.warning(f"PIB de {year} eliminado")
                st.experimental_rerun()


# =====================
# Gráficas
# =====================
st.subheader("📈 Gráficas de las funciones")

fig, axes = plt.subplots(3, 2, figsize=(10, 8))
fig.tight_layout(pad=3.0)

axes = axes.flatten()

funcs = {
    "C_t": (calcular_Ct, a, ct, Yt, "blue"),
    "C_k": (calcular_Ck, b, ck, Yk, "green"),
    "I": (calcular_I, h, i_val, pi, "orange"),
    "G": (calcular_G, d, g_val, Rf, "red"),
    "X": (calcular_X, e, x_val, Yeu, "purple"),
    "M": (calcular_M, f, m_val, Ymex, "brown")
}

for ax, (name, (func, p1, p2, y_var, color)) in zip(axes, funcs.items()):
    x_vals = [0, 1, 2, 3, 4, 5]
    y_vals = [func(p1, p2, Y) for Y in x_vals]
    ax.plot(x_vals, y_vals, color=color, label=name)
    ax.set_title(name)
    ax.set_xlabel("Variable independiente")
    ax.set_ylabel(name)
    ax.grid(True)
    ax.legend()

st.pyplot(fig)
