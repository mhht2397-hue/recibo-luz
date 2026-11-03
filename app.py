import streamlit as st
import pandas as pd
from datetime import datetime

# Configuración visual de la página
st.set_page_config(page_title="LuzNet - Control de Energía", page_icon="⚡", layout="centered")

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

# URL pública de tu hoja de cálculo (Asegúrate de pegar aquí tu enlace copiado)
URL_EXCEL = "AGREGAR_AQUÍ_TU_ENLACE_DE_SHARE"

st.title("⚡ LuzNet - Control de Luz")

# Conexión directa a Google Sheets usando el enlace
try:
    from streamlit_gsheets import GSheetsConnection
    conn = st.connection("gsheets", type=GSheetsConnection)
    df_historico = conn.read(spreadsheet=URL_EXCEL, ttl="10s")
    df_historico = df_historico.dropna(subset=["mes"]).set_index("mes")
except Exception as e:
    st.error("⚠️ Configuración inicial: Conecta el enlace de Google Sheets en la línea 22 del código.")
    st.stop()

# Menú lateral para roles
st.sidebar.header("🔑 Selector de Usuario")
usuario = st.sidebar.selectbox("¿Quién ingresa?", ["Página Principal (Resumen)", "Administrador", "Inquilino: Nora", "Inquilino: Jesús"])

# Control de llaves de acceso (PIN)
if usuario == "Administrador":
    pin = st.sidebar.text_input("Ingresa tu PIN de Admin:", type="password")
    if pin != "1234":
        st.warning("🔒 Por favor, ingresa el PIN de administrador en la barra lateral.")
        st.stop()
elif usuario == "Inquilino: Nora":
    pin = st.sidebar.text_input("Ingresa tu PIN (Nora):", type="password")
    if pin != "1111":
        st.warning("🔒 Ingresa tu PIN asignado para visualizar tu historial.")
        st.stop()
elif usuario == "Inquilino: Jesús":
    pin = st.sidebar.text_input("Ingresa tu PIN (Jesús):", type="password")
    if pin != "2222":
        st.warning("🔒 Ingresa tu PIN asignado para visualizar tu historial.")
        st.stop()

# Obtener los meses disponibles desde el Excel
lista_meses = list(df_historico.index)
mes_reciente = lista_meses[0] if len(lista_meses) > 0 else ""

# --- ESCENARIO 1: PÁGINA PRINCIPAL ---
if usuario == "Página Principal (Resumen)":
    st.write("Bienvenido al sistema conectado. Aquí puedes ver de forma rápida el último recibo calculado.")
    
    if mes_reciente:
        datos_mes = df_historico.loc[mes_reciente]
        st.subheader(f"📌 Último Mes Calculado: {mes_reciente}")
        
        st.markdown(f"""
            <div class="card-resumen">
                <strong>Recibo General de la Casa:</strong> S/. {float(datos_mes['monto_total']):.2f} | Consumo: {float(datos_mes['kwh_total']):.0f} kWh <br>
                <span style='color: #64748b; font-size: 14px;'>Facturado durante el período: {datos_mes['periodo']}</span>
            </div>
        """, unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        with col1:
            st.markdown(f"""
                <div class="card-nora" style="padding:15px;">
                    <h4>👩‍🦰 Sra. Nora</h4>
                    <div style="font-size:20px; font-weight:bold; color:#be123c;">S/. {float(datos_mes['nora_pago']):.2f}</div>
                    <span style="font-size:13px; color:#475569;">Consumo: {float(datos_mes['nora_kwh']):.2f} kWh</span>
                </div>
            """, unsafe_allow_html=True)
        with col2:
            st.markdown(f"""
                <div class="card-jesus" style="padding:15px;">
                    <h4>👨‍🦱 Jesús</h4>
                    <div style="font-size:20px; font-weight:bold; color:#1d4ed8;">S/. {float(datos_mes['jesus_pago']):.2f}</div>
                    <span style="font-size:13px; color:#475569;">Consumo: {float(datos_mes['jesus_hwh'] if 'jesus_hwh' in datos_mes else datos_mes['jesus_kwh']):.2f} kWh</span>
                </div>
            """, unsafe_allow_html=True)
    else:
        st.info("No hay meses registrados en el sistema.")

# --- ESCENARIO 2: ADMINISTRADOR (CON CALENDARIOS INTERACTIVOS) ---
elif usuario == "Administrador":
    st.subheader("🛠️ Panel de Control - Administrador")
    st.info("Usa los selectores de calendario para marcar las fechas de facturación con clics.")
    
    with st.form("formulario_mes"):
        nombre_mes = st.text_input("Nombre del Mes a Facturar:", placeholder="Noviembre 2026")
        
        # Calendarios interactivos en lugar de cajas de texto manuales
        col_f1, col_f2 = st.columns(2)
        with col_f1:
            fecha_inicio_cal = st.date_input("Fecha de Inicio del Recibo:", value=datetime.today())
        with col_f2:
            fecha_fin_cal = st.date_input("Fecha de Fin del Recibo:", value=datetime.today())
        
        st.markdown("---")
        col_ad1, col_ad2 = st.columns(2)
        with col_ad1:
            monto_in = st.number_input("Costo del Recibo General (S/.)", min_value=0.0, value=94.0, step=0.10)
            nora_kwh_in = st.number_input("kWh calculados para Nora este mes:", min_value=0.0, value=57.5, step=0.1)
        with col_ad2:
            kwh_in = st.number_input("Consumo General de la casa (kWh)", min_value=1.0, value=116.0, step=1.0)
            
        boton_guardar = st.form_submit_button("💾 Procesar y Publicar Cuentas", type="primary")
        
        if boton_guardar:
            if not nombre_mes:
                st.error("⚠️ Por favor, escribe un nombre identificador para el mes (ej: Noviembre 2026).")
            elif fecha_inicio_cal >= fecha_fin_cal:
                st.error("⚠️ La fecha de inicio no puede ser igual o posterior a la fecha de fin.")
            else:
                # Armar el texto del período automáticamente uniendo las dos fechas del calendario
                periodo_automatico = f"{fecha_inicio_cal.strftime('%d/%m/%Y')} al {fecha_fin_cal.strftime('%d/%m/%Y')}"
                
                jesus_kwh_calc = max(0.0, kwh_in - nora_kwh_in)
                pct_nora_calc = nora_kwh_in / kwh_in if kwh_in > 0 else 0
                
                pago_nora_calc = monto_in * pct_nora_calc
                pago_jesus_calc = monto_in * (1.0 - pct_nora_calc)
                
                # Fila estructurada para el Excel
                nueva_fila = pd.DataFrame([{
                    "mes": nombre_mes, 
                    "periodo": periodo_automatico,
                    "monto_total": float(monto_in), 
                    "kwh_total": float(kwh_in),
                    "nora_kwh": round(nora_kwh_in, 2), 
                    "jesus_kwh": round(jesus_kwh_calc, 2),
                    "nora_pago": round(pago_nora_calc, 2), 
                    "jesus_pago": round(pago_jesus_calc, 2)
                }])
                
                # Insertar los datos arriba en el historial
                df_actualizado = pd.concat([nueva_fila, df_historico.reset_index()], ignore_index=True)
                
                # Subir de forma permanente al Google Sheets
                conn.update(spreadsheet=URL_EXCEL, data=df_actualizado)
                st.success(f"🎉 ¡El mes de '{nombre_mes}' con período [{periodo_automatico}] se guardó correctamente en la nube!")
                st.rerun()

# --- ESCENARIO 3: NORA ---
elif usuario == "Inquilino: Nora" and mes_reciente:
    st.subheader("👩‍🦰 Historial de Consumos - Sra. Nora")
    act = df_historico.loc[mes_reciente]
    
    st.markdown(f"""
        <div class="card-nora">
            <h3>📌 Monto del Período Actual ({mes_reciente})</h3>
            <p style="margin:0; color:#475569;">Rango de días: {act['periodo']}</p>
            <p style="margin:0; color:#475569;">Su consumo de energía: <strong>{float(act['nora_kwh']):.2f} kWh</strong></p>
            <div class="monto-grande" style="color:#be123c;">Total a pagar: S/. {float(act['nora_pago']):.2f}</div>
        </div>
    """, unsafe_allow_html=True)
    
    tabla_nora = []
    for m in lista_meses:
        info = df_historico.loc[m]
        tabla_nora.append({
            "Mes": m, "Período Facturado": info["periodo"], 
            "Su Consumo": f"{float(info['nora_kwh']):.2f} kWh", "Total a Pagar": f"S/. {float(info['nora_pago']):.2f}"
        })
    st.subheader("📚 Historial de Meses Anteriores")
    st.dataframe(pd.DataFrame(tabla_nora), hide_index=True, use_container_width=True)

# --- ESCENARIO 4: JESÚS ---
elif usuario == "Inquilino: Jesús" and mes_reciente:
    st.subheader("👨‍🦱 Historial de Consumos - Jesús")
    act = df_historico.loc[mes_reciente]
    
    st.markdown(f"""
        <div class="card-jesus">
            <h3>📌 Monto del Período Actual ({mes_reciente})</h3>
            <p style="margin:0; color:#475569;">Rango de días: {act['periodo']}</p>
            <p style="margin:0; color:#475569;">Tu consumo de energía (Diferencia): <strong>{float(act['jesus_kwh'] if 'jesus_kwh' in act else act['jesus_hwh']):.2f} kWh</strong></p>
            <div class="monto-grande" style="color:#1d4ed8;">Total a pagar: S/. {float(act['jesus_pago']):.2f}</div>
        </div>
    """, unsafe_allow_html=True)
    
    tabla_jesus = []
    for m in lista_meses:
        info = df_historico.loc[m]
        tabla_jesus.append({
            "Mes": m, "Período Facturado": info["periodo"], 
            "Tu Consumo": f"{float(info['jesus_kwh'] if 'jesus_kwh' in info else info['jesus_hwh']):.2f} kWh", "Total a Pagar": f"S/. {float(info['jesus_pago']):.2f}"
        })
    st.subheader("📚 Historial de Meses Anteriores")
