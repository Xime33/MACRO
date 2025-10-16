default_values = { "C_t_a": 4, "C_t_ct": 0.8, "Yt": 5, "C_k_b": 1, "C_k_ck": 0.2,"pik": 5, "I_h": 3, "I_i": 0.4, "pi": 5, "G_d": 2, "G_g": 0.4, "Rf": 5, "X_e": 2, "X_x": 0.2, "Yeu": 5, "M_f": 1, "M_m": 0.2, "Ymex": 5 } 
lista = [0,1,2,3,2,1,2,4,5]

def calcular_Ct(a, ct):
    resultados = []
    for i in lista:
        calculo = a + ct * i
        resultados.append(calculo)
    return resultados

print(calcular_Ct(4, 0.8))