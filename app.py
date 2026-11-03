import streamlit as st
import pandas as pd
from datetime import datetime

# Configuración visual de la página
st.set_page_config(page_title="Recibo de Luz Compartido", page_icon="⚡", layout="centered")

# Estilos personalizados para que se vea limpio y moderno en el celular
st.markdown("""
    <style>
    .main { background-color: #f8f9fa; }
    .stNumberInput, .stDateInput { background-color: #ffffff; border-radius: 10px; }
    div[data-testid="stMetricValue"] { font-size: 32px; font-weight: bold; color: #1e293b; }
    .card-nora { background-color: #ffe6eb; padding: 20px; border-radius: 15px; border-left: 8px solid #ff4b72; margin-bottom: 15px; }
    .card-jesus { background-color: #e6f0ff; padding: 20px; border-radius: 15px; border-left: 8px solid #1e88e5; margin-bottom: 15px; }
    .card-total { background-color: #f1f5f9; padding: 15px; border-radius: 12px; border-left: 5px solid #64748b; }
    h3 { margin-top: 0px !important; color: #0f172a; }
    </style>
""", unsafe_allow_html=True)

st.title("⚡ LuzNet - Control de Recibo")
st.write("Selecciona el mes actual para ver cuánto le corresponde pagar a cada departamento de forma justa.")

# --- BASE DE DATOS LOCAL (Aquí agregas los datos reales cada mes) ---
# Al guardarlos aquí, tus inquilinos solo tendrán que abrir la web y elegir el mes.
historial_meses = {
    "Octubre 2026": {
        "monto_total": 94.00,
        "kwh_total": 116.0,
        "fecha_ini": "17/09/2026",
        "fecha_fin": "17/10/2026",
        "lecturas_nora": [
            {"fecha": "16/08/2026", "lectura": 0.0},
            {"fecha": "06/09/2026", "lectura": 36.4},
            {"fecha": "29/09/2026", "lectura": 81.3},
            {"fecha": "19/10/2026", "lectura": 124.4}
        ]
    }
    # Cuando llegue noviembre, simplemente copias la estructura aquí abajo.
}

# --- SELECCIÓN DE MES PARA LOS INQUILINOS ---
mes_seleccionado = st.selectbox("📆 Selecciona el mes del recibo que deseas consultar:", list(historial_meses.keys()))

# Extraer datos del mes elegido
datos = historial_meses[mes_seleccionado]
monto_recibo = datos["monto_total"]
kwh_recibo = datos["kwh_total"]
fecha_ini = datetime.strptime(datos["fecha_ini"], "%d/%m/%Y")
fecha_fin = datetime.strptime(datos["fecha_fin"], "%d/%m/%Y")

# Convertir lecturas de Nora a formato fecha
tramos = []
lecturas = datos["lecturas_nora"]
for i in range(len(lecturas) - 1):
    f1 = datetime.strptime(lecturas[i]["fecha"], "%d/%m/%Y").date()
    f2 = datetime.strptime(lecturas[i+1]["fecha"], "%d/%m/%Y").date()
    dias = (f2 - f1).days
    kwh = lecturas[i+1]["lectura"] - lecturas[i]["lectura"]
    promedio = kwh / dias if dias > 0 else 0
    tramos.append({"inicio": f1, "fin": f2, "promedio": promedio})

# Calcular consumo de Nora en el rango del recibo
rango_recibo = pd.date_range(start=fecha_ini, end=fecha_fin)
kwh_nora_total = 0.0

for d in range(len(rango_recibo) - 1):
    dia_actual = rango_recibo[d].date()
    for tramo in tramos:
        if tramo["inicio"] <= dia_actual < tramo["fin"]:
            kwh_nora_total += tramo["promedio"]
            break

# Cálculos finales
kwh_jesus_total = max(0.0, kwh_recibo - kwh_nora_total)
pct_nora = min(1.0, kwh_nora_total / kwh_recibo) if kwh_recibo > 0 else 0

pago_nora = monto_recibo * pct_nora
pago_jesus = monto_recibo * (1.0 - pct_nora)

st.markdown("---")

# --- DISEÑO DE TARJETAS VISUALES ---

# Tarjeta de Nora (Color Rosado/Rojo)
st.markdown(f"""
    <div class="card-nora">
        <h3>👩‍🦰 Departamento Sra. Nora</h3>
        <p style='margin-bottom:5px; color:#475569;'>Consumo medido en el mes: <strong>{kwh_nora_total:.2f} kWh</strong> ({(pct_nora*100):.1f}%)</p>
        <p style='margin-top:0px; font-size: 14px; color: #64748b;'>Calculado según promedio exacto de sus lecturas de medidor.</p>
        <div style='font-size: 28px; font-weight: bold; color: #be123c;'>Monto a Pagar: S/. {pago_nora:.2f}</div>
    </div>
""", unsafe_allow_html=True)

# Tarjeta de Jesús (Color Azul)
st.markdown(f"""
    <div class="card-jesus">
        <h3>👨‍🦱 Departamento Jesús</h3>
        <p style='margin-bottom:5px; color:#475569;'>Consumo (Diferencia del total): <strong>{kwh_jesus_total:.2f} kWh</strong> ({((1.0 - pct_nora)*100):.1f}%)</p>
        <p style='margin-top:0px; font-size: 14px; color: #64748b;'>Calculado restando el medidor de Nora al medidor general.</p>
        <div style='font-size: 28px; font-weight: bold; color: #1d4ed8;'>Monto a Pagar: S/. {pago_jesus:.2f}</div>
    </div>
""", unsafe_allow_html=True)

# Información del recibo general abajo
st.markdown(f"""
    <div class="card-total">
        <span style='color:#475569; font-size:14px;'><strong>Datos del Recibo General:</strong> Monto Total S/. {monto_recibo:.2f} | Consumo Total: {kwh_recibo:.0f} kWh | Período: del {datos['fecha_ini']} al {datos['fecha_fin']}</span>
    </div>
""", unsafe_allow_html=True)

