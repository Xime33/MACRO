from tkinter import *
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

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
# Ventana principal
# =====================
window = Tk()
window.title("Macroeconomía")
window.geometry("650x600")
window.config(bg="DarkBlue")

Label(window, text="Ingresar parámetros de todas las funciones", 
      font=("Arial", 16, "bold"), fg="White", bg="DarkBlue").pack(pady=10)

# =====================
# Frame para entradas
# =====================
entries = {}
variables = [
    ("C_t","a"),("C_t","ct"),
    ("C_k","b"),("C_k","ck"),
    ("I","h"),("I","i"),
    ("G","d"),("G","g"),
    ("X","e"),("X","x"),
    ("M","f"),("M","m")
]

frame = Frame(window, bg="DarkBlue")
frame.pack(pady=10)

row = 0
for func, var in variables:
    Label(frame, text=f"{func} - {var}", bg="DarkBlue", fg="White").grid(row=row, column=0, padx=5, pady=5, sticky=W)
    entry = Entry(frame)
    entry.grid(row=row, column=1, padx=5, pady=5)
    key = f"{func}_{var}"
    entry.insert(0, str(default_values[key]))  # valor por defecto
    entries[key] = entry
    row += 1

# =====================
# Label para mostrar PIB
# =====================
pib_label = Label(window, text="PIB final: ", font=("Arial", 14), fg="White", bg="DarkBlue")
pib_label.pack(pady=10)

# =====================
# Función para graficar y calcular PIB
# =====================
def graficar_y_sumar():
    try:
        a = float(entries["C_t_a"].get())
        ct = float(entries["C_t_ct"].get())
        b = float(entries["C_k_b"].get())
        ck = float(entries["C_k_ck"].get())
        h = float(entries["I_h"].get())
        i_val = float(entries["I_i"].get())
        d = float(entries["G_d"].get())
        g_val = float(entries["G_g"].get())
        e = float(entries["X_e"].get())
        x_val = float(entries["X_x"].get())
        f = float(entries["M_f"].get())
        m_val = float(entries["M_m"].get())
    except ValueError:
        pib_label.config(text="Error: ingresa valores numéricos")
        return

    # Variables independientes
    Yt = default_values["Yt"]
    Yk = default_values["Yk"]
    pi = default_values["pi"]
    Rf = default_values["Rf"]
    Yeu = default_values["Yeu"]
    Ymex = default_values["Ymex"]

    # Calcular valores finales
    CT = calcular_Ct(a, ct, Yt)
    CK = calcular_Ck(b, ck, Yk)
    I = calcular_I(h, i_val, pi)
    G = calcular_G(d, g_val, Rf)
    X = calcular_X(e, x_val, Yeu)
    M = calcular_M(f, m_val, Ymex)

    PIB_final = CT + CK + I + G + (X - M)
    pib_label.config(text=f"PIB final: {PIB_final:.2f}")

    # Graficar todas las funciones en una sola ventana
    graf_window = Toplevel(window)
    graf_window.title("Funciones macroeconómicas")
    fig, axes = plt.subplots(3,2, figsize=(10,8))
    fig.tight_layout(pad=3.0)  # "pad" es la separación general entre subplots

    axes = axes.flatten()

    # Diccionario para graficar
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

    canvas = FigureCanvasTkAgg(fig, master=graf_window)
    canvas.get_tk_widget().pack(fill=BOTH, expand=True)
    canvas.draw()


# =====================
# Botón
# =====================
Button(window, text="Graficar y calcular PIB", command=graficar_y_sumar, bg="DarkBlue", fg="White").pack(pady=10)

window.mainloop()


"""
PIB = 20 B aprox

2025 20 B sumatoria del consumo + inversión + gasto + (exportaciones - importaciones)
CT = 6 
consumo de los trabajadores = 4
capitalistas = 2 = constante + .3 * ganancias
a = 4 
yt = 5
ct = .8
ck = .3

4 = ordenada al origen + ct * x (valor por debajo de 15 que de 4)

CT = 8
CK = 2
inversión = 5
gasto = 4
exportaciones = 3
importaciones = 2
20 = 10 + 5 + 4 + (3 - 2)


-----
suma 2024
19.5 B

-----
suma 2023
20 B

-------
suma 2022
20.5 B

---------
suma 2021
19.5 B

---------
suma 2020
18 B

----------
suma 2019

19.5 B
----
suma 2018
19 B
-------
2017
20 B
-------
2016
20.5 B
-------
2015
21 B
-------
2014
22 B
-------
2013
21.5 B
-------
2012
21 B
------- 
2011
20 B

programa economico de ingresos y gastos 2025 sep hacienda

pronostico PIB 2026-2028
"""

