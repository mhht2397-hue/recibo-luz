import streamlit as st
import pandas as pd
from datetime import datetime

# Configuración de página optimizada
st.set_page_config(page_title="LuzNet - Control de Luz", page_icon="⚡", layout="centered")

st.markdown("""
    <style>
    .main { background-color: #f8f9fa; }
    .card-nora { background-color: #ffe6eb; padding: 20px; border-radius: 15px; border-left: 8px solid #ff4b72; margin-bottom: 15px; }
    .card-jesus { background-color: #e6f0ff; padding: 20px; border-radius: 15px; border-left: 8px solid #1e88e5; margin-bottom: 15px; }
    .card-resumen { background-color: #f1f5f9; padding: 18px; border-radius: 12px; border-left: 5px solid #64748b; margin-bottom: 15px; }
    h3 { margin-top: 0px !important; color: #0f172a; font-size: 20px; }
    h4 { margin-top: 0px !important; color: #0f172a; font-size: 18px; }
    .monto-grande { font-size: 30px; font-weight: bold; margin-top: 5px; }
    </style>
""", unsafe_allow_html=True)

# URL DE TU GOOGLE SHEETS (Reemplaza los números por los tuyos)
# Asegúrate de mantener el "/export?format=csv" al final para que cargue volando
# Pega tu enlace COMPLETO de Google Sheets aquí adentro de las comillas:
LINK_COMPLETO = "https://docs.google.com/spreadsheets/d/1yJeU6zTkOqc0kwR8rV8Q0wjl7NomX3R_RqcW4zKoYPg/edit?gid=0#gid=0"

# El código se encarga de limpiarlo automáticamente para el servidor
URL_EXCEL = "https://docs.google.com/spreadsheets/d/1yJeU6zTkOqc0kwR8rV8Q0wjl7NomX3R_RqcW4zKoYPg/edit?gid=0#gid=0.split("/edit")[0] + "/export?format=csv"


st.title("⚡ LuzNet - Control de Luz")

# Lector ultra-rápido de Google Sheets sin librerías pesadas
@st.cache_data(ttl=10) # Guarda en caché por 10 segundos para no saturar
def cargar_datos(url):
    try:
        df = pd.read_csv(url)
        df = df.dropna(subset=["mes"]).set_index("mes")
        return df
    except:
        # Datos de respaldo por si el enlace no está listo
        return pd.DataFrame([{
            "mes": "Octubre 2026", "periodo": "17/09/2026 al 17/10/2026",
            "monto_total": 94.0, "kwh_total": 116.0, "nora_kwh": 57.56,
            "jesus_kwh": 58.44, "nora_pago": 46.64, "jesus_pago": 47.36
        }]).set_index("mes")

df_historico = cargar_datos(URL_EXCEL)
lista_meses = list(df_historico.index)
mes_reciente = lista_meses[0] if len(lista_meses) > 0 else ""

# Selector de usuario lateral
st.sidebar.header("🔑 Selector de Usuario")
usuario = st.sidebar.selectbox("¿Quién ingresa?", ["Página Principal (Resumen)", "Administrador", "Inquilino: Nora", "Inquilino: Jesús"])

# Control de PINs de acceso
if usuario == "Administrador":
    pin = st.sidebar.text_input("Ingresa tu PIN de Admin:", type="password")
    if pin != "1234":
        st.warning("🔒 Por favor, ingresa el PIN de administrador.")
        st.stop()
elif usuario == "Inquilino: Nora":
    pin = st.sidebar.text_input("Ingresa tu PIN (Nora):", type="password")
    if pin != "1111":
        st.warning("🔒 Ingresa tu PIN para visualizar tu historial.")
        st.stop()
elif usuario == "Inquilino: Jesús":
    pin = st.sidebar.text_input("Ingresa tu PIN (Jesús):", type="password")
    if pin != "2222":
        st.warning("🔒 Ingresa tu PIN para visualizar tu historial.")
        st.stop()

# --- PÁGINA PRINCIPAL ---
if usuario == "Página Principal (Resumen)":
    st.write("Aquí puedes ver de forma rápida el último recibo calculado.")
    if mes_reciente:
        datos_mes = df_historico.loc[mes_reciente]
        st.subheader(f"📌 Último Mes: {mes_reciente}")
        st.markdown(f"""
            <div class="card-resumen">
                <strong>Recibo General:</strong> S/. {float(datos_mes['monto_total']):.2f} | Consumo: {float(datos_mes['kwh_total']):.0f} kWh <br>
                <span style='color:#64748b; font-size:14px;'>Período: {datos_mes['periodo']}</span>
            </div>
        """, unsafe_allow_html=True)
        col1, col2 = st.columns(2)
        with col1:
            st.markdown(f"""<div class="card-nora" style="padding:15px;"><h4>👩‍🦰 Sra. Nora</h4><div style="font-size:20px; font-weight:bold; color:#be123c;">S/. {float(datos_mes['nora_pago']):.2f}</div><span style="font-size:13px; color:#475569;">Consumo: {float(datos_mes['nora_kwh']):.2f} kWh</span></div>""", unsafe_allow_html=True)
        with col2:
            st.markdown(f"""<div class="card-jesus" style="padding:15px;"><h4>👨‍🦱 Jesús</h4><div style="font-size:20px; font-weight:bold; color:#1d4ed8;">S/. {float(datos_mes['jesus_pago']):.2f}</div><span style="font-size:13px; color:#475569;">Consumo: {float(datos_mes['jesus_kwh']):.2f} kWh</span></div>""", unsafe_allow_html=True)

# --- ADMINISTRADOR ---
elif usuario == "Administrador":
    st.subheader("🛠️ Panel de Control - Administrador")
    st.info("Para subir los nuevos datos de forma permanente, agrégalos directamente en tu archivo de Google Sheets. El sistema se actualizará al instante de forma ligera.")
    st.write("👉 [Abre tu Google Sheets aquí](https://google.com)")
    
    # Formulario interactivo auxiliar para cálculo rápido en pantalla
    st.write("🧮 **Calculadora rápida de apoyo (Ver en pantalla):**")
    nombre_mes = st.text_input("Nombre del Mes:", value="Noviembre 2026")
    col_f1, col_f2 = st.columns(2)
    fecha_inicio_cal = col_f1.date_input("Inicio del Recibo:", value=datetime.today())
    fecha_fin_cal = col_f2.date_input("Fin del Recibo:", value=datetime.today())
    
    col_ad1, col_ad2 = st.columns(2)
    monto_in = col_ad1.number_input("Costo del Recibo (S/.)", min_value=0.0, value=94.0)
    nora_kwh_in = col_ad1.number_input("kWh de Nora:", min_value=0.0, value=57.5)
    kwh_in = col_ad2.number_input("Consumo Total Casa (kWh)", min_value=1.0, value=116.0)
    
    if st.button("🧮 Calcular montos en pantalla"):
        periodo_txt = f"{fecha_inicio_cal.strftime('%d/%m/%Y')} al {fecha_fin_cal.strftime('%d/%m/%Y')}"
        j_kwh = max(0.0, kwh_in - nora_kwh_in)
        p_nora = (nora_kwh_in / kwh_in) if kwh_in > 0 else 0
        st.code(f"Copiar esta fila a tu Excel:\n{nombre_mes},{periodo_txt},{monto_in},{kwh_in},{nora_kwh_in},{j_kwh},{monto_in*p_nora:.2f},{monto_in*(1-p_nora):.2f}")

# --- NORA ---
elif usuario == "Inquilino: Nora" and mes_reciente:
    st.subheader("👩‍🦰 Historial - Sra. Nora")
    act = df_historico.loc[mes_reciente]
    st.markdown(f"""<div class="card-nora"><h3>📌 Período Actual ({mes_reciente})</h3><p style="margin:0; color:#475569;">Período: {act['periodo']}</p><p style="margin:0; color:#475569;">Su consumo: <strong>{float(act['nora_kwh']):.2f} kWh</strong></p><div class="monto-grande" style="color:#be123c;">Total a pagar: S/. {float(act['nora_pago']):.2f}</div></div>""", unsafe_allow_html=True)
    
    tabla_nora = [{"Mes": m, "Período": df_historico.loc[m]["periodo"], "Su Consumo": f"{float(df_historico.loc[m]['nora_kwh']):.2f} kWh", "Total a Pagar": f"S/. {float(df_historico.loc[m]['nora_pago']):.2f}"} for m in lista_meses]
    st.dataframe(pd.DataFrame(tabla_nora), hide_index=True, use_container_width=True)

# --- JESÚS ---
elif usuario == "Inquilino: Jesús" and mes_reciente:
    st.subheader("👨‍🦱 Historial - Jesús")
    act = df_historico.loc[mes_reciente]
    st.markdown(f"""<div class="card-jesus"><h3>📌 Período Actual ({mes_reciente})</h3><p style="margin:0; color:#475569;">Período: {act['periodo']}</p><p style="margin:0; color:#475569;">Tu consumo: <strong>{float(act['jesus_kwh']):.2f} kWh</strong></p><div class="monto-grande" style="color:#1d4ed8;">Total a pagar: S/. {float(act['jesus_pago']):.2f}</div></div>""", unsafe_allow_html=True)
    
    tabla_jesus = [{"Mes": m, "Período": df_historico.loc[m]["periodo"], "Tu Consumo": f"{float(df_historico.loc[m]['jesus_kwh']):.2f} kWh", "Total a Pagar": f"S/. {float(df_historico.loc[m]['jesus_pago']):.2f}"} for m in lista_meses]
    st.dataframe(pd.DataFrame(tabla_jesus), hide_index=True, use_container_width=True)
