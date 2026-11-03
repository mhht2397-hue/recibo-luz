import streamlit as st
import pandas as pd
from datetime import datetime

st.set_page_config(page_title="Control de Recibo de Luz", page_icon="⚡", layout="wide")

st.title("⚡ Calculador Interactivo de Recibo de Luz")
st.write("Ingresa los datos del recibo y las lecturas mensuales para calcular la división exacta.")

# --- BARRA LATERAL: DATOS DEL RECIBO GENERAL ---
st.sidebar.header("📋 1. Datos del Recibo General")
monto_recibo = st.sidebar.number_input("Monto Total del Recibo (S/.)", min_value=0.0, value=94.0, step=0.10, format="%.2f")
kwh_recibo = st.sidebar.number_input("Consumo Total del Recibo (kWh)", min_value=1.0, value=116.0, step=1.0)

fecha_ini = st.sidebar.date_input("Fecha Inicio Recibo", value=datetime(2026, 9, 17))
fecha_fin = st.sidebar.date_input("Fecha Fin Recibo", value=datetime(2026, 10, 17))

# --- CUERPO PRINCIPAL: INGRESO DE LECTURAS DE NORA ---
st.subheader("📸 2. Historial de Lecturas (Medidor de Nora)")
st.write("Modifica o añade nuevas filas según vayas tomando las lecturas del medidor interno.")

datos_iniciales = pd.DataFrame([
    {"Fecha": datetime(2026, 8, 16).date(), "Lectura (kWh)": 0.0},
    {"Fecha": datetime(2026, 9, 6).date(), "Lectura (kWh)": 36.4},
    {"Fecha": datetime(2026, 9, 29).date(), "Lectura (kWh)": 81.3},
    {"Fecha": datetime(2026, 10, 19).date(), "Lectura (kWh)": 124.4}
])

tabla_editable = st.data_editor(
    datos_iniciales, 
    num_rows="dynamic", 
    use_container_width=True,
    column_config={
        "Fecha": st.column_config.DateColumn("Fecha de Lectura", format="DD/MM/YYYY", required=True),
        "Lectura (kWh)": st.column_config.NumberColumn("Lectura del Medidor (kWh)", min_value=0.0, format="%.1f", required=True)
    }
)

df_lecturas = pd.DataFrame(tabla_editable).dropna().sort_values(by="Fecha").reset_index(drop=True)

if len(df_lecturas) >= 2:
    tramos = []
    for i in range(len(df_lecturas) - 1):
        f1 = df_lecturas.loc[i, "Fecha"]
        f2 = df_lecturas.loc[i+1, "Fecha"]
        dias = (f2 - f1).days
        kwh = df_lecturas.loc[i+1, "Lectura (kWh)"] - df_lecturas.loc[i, "Lectura (kWh)"]
        promedio = kwh / dias if dias > 0 else 0
        tramos.append({"inicio": f1, "fin": f2, "promedio": promedio, "dias": dias, "kwh": kwh})

    rango_recibo = pd.date_range(start=fecha_ini, end=fecha_fin)
    kwh_nora_total = 0.0

    for d in range(len(rango_recibo) - 1):
        dia_actual = rango_recibo[d].date()
        for tramo in tramos:
            if tramo["inicio"] <= dia_actual < tramo["fin"]:
                kwh_nora_total += tramo["promedio"]
                break

    kwh_jesus_total = max(0.0, kwh_recibo - kwh_nora_total)
    pct_nora = min(1.0, kwh_nora_total / kwh_recibo) if kwh_recibo > 0 else 0
    pago_nora = monto_recibo * pct_nora
    pago_jesus = monto_recibo * (1.0 - pct_nora)

    st.markdown("---")
    st.subheader("💵 División de la Cuenta del Mes")
    df_cuentas = pd.DataFrame({
        "Persona / Departamento": ["👩‍🦰 Nora", "👨‍🦱 Jesús"],
        "Consumo Estimado": [f"{kwh_nora_total:.2f} kWh", f"{kwh_jesus_total:.2f} kWh"],
        "Porcentaje del Total": [f"{pct_nora*100:.2f}%", f"{(1.0 - pct_nora)*100:.2f}%"],
        "Monto Justo a Pagar": [f"S/. {pago_nora:.2f}", f"S/. {pago_jesus:.2f}"]
    })
    st.dataframe(df_cuentas, hide_index=True, use_container_width=True)

    st.subheader("📊 Historial de Métricas de Gasto")
    df_tramos = pd.DataFrame([{
        "Período Evaluado": f"Del {t['inicio'].strftime('%d/%m/%Y')} al {t['fin'].strftime('%d/%m/%Y')}",
        "Días del Tramo": t["dias"],
        "Consumo en el Tramo": f"{t['kwh']:.1f} kWh",
        "Ritmo de Gasto Diario": f"{t['promedio']:.2f} kWh/día"
    } for t in tramos])
    st.dataframe(df_tramos, hide_index=True, use_container_width=True)
else:
    st.info("💡 Por favor, ingresa al menos 2 filas en la tabla superior.")
