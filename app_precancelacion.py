# app_precancelacion_v3.py
import streamlit as st
from scipy.optimize import fsolve

st.title("Calculadora de Precancelación - Crédito Prendario")

# Inputs del usuario
capital = st.number_input("Capital Financiado (AR$)", min_value=1.0, value=500000.0)
cuotas_totales = st.number_input("Cantidad total de Cuotas", min_value=1, value=12)
valor_cuota = st.number_input("Valor de Cuota Mensual (AR$)", min_value=1.0, value=45000.0)
cuotas_pendientes = st.number_input("Cuotas pendientes (incluyendo la vigente)", min_value=1, value=12)

# Checkbox: si la cuota vigente ya está pagada
cuota_vigente_pagada = st.checkbox("La cuota vigente ya está cancelada", value=False)

# Ajustar número de cuotas según el checkbox
if cuota_vigente_pagada:
    cuotas_a_precancelar = cuotas_pendientes - 1  # no contamos la cuota vigente
else:
    cuotas_a_precancelar = cuotas_pendientes      # contamos la cuota vigente

# Botón para calcular
if st.button("Calcular Precancelación"):
    
    # 1️⃣ Calcular tasa mensual aproximada
    def ecuacion(i):
        return capital * (i*(1+i)**cuotas_totales)/((1+i)**cuotas_totales - 1) - valor_cuota
    
    tasa_mensual = fsolve(ecuacion, 0.01)[0]
    
    # 2️⃣ Calcular saldo para precancelación
    saldo_precancelar = valor_cuota * (1 - (1 + tasa_mensual)**(-cuotas_a_precancelar)) / tasa_mensual
    
    # Resultados
    st.markdown(f"**Tasa mensual aproximada:** {tasa_mensual*100:.2f}%")
    st.markdown(f"**Monto para precancelar (AR$):** {saldo_precancelar:,.2f}")
    st.markdown(f"**Cuotas consideradas para precancelación:** {cuotas_a_precancelar}")