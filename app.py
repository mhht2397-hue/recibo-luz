import streamlit as st
import pandas as pd

# Configuración visual de la página
st.set_page_config(page_title="Control de Energía", page_icon="⚡", layout="centered")

# Estilos visuales optimizados para dispositivos móviles y tarjetas de colores
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

# ==========================================
# 📊 BASE DE DATOS INICIAL (HISTORIAL)
# ==========================================
if "registro_historico" not in st.session_state:
    st.session_state.registro_historico = {
        "Octubre 2026": {
            "monto_total": 94.00, "kwh_total": 116.0,
            "periodo": "17/09/2026 al 17/10/2026",
            "nora_kwh": 57.56, "jesus_kwh": 58.44,
            "nora_pago": 46.64, "jesus_pago": 47.36
        },
        "Setiembre 2026": {
            "monto_total": 88.00, "kwh_total": 110.0,
            "periodo": "16/08/2026 al 17/09/2026",
            "nora_kwh": 54.20, "jesus_kwh": 55.80,
            "nora_pago": 43.36, "jesus_pago": 44.64
        }
    }

st.title("⚡ Control de Luz")

# ==========================================
# 🔑 LOGIN DE USUARIOS
# ==========================================
st.sidebar.header("🔑 Selector de Usuario")
usuario = st.sidebar.selectbox("¿Quién ingresa?", ["Página Principal (Resumen)", "Administrador", "Inquilino: Nora", "Inquilino: Jesús"])

# Pines o claves sencillas de acceso
if usuario == "Administrador":
    pin = st.sidebar.text_input("Ingresa tu PIN de Admin:", type="password")
    if pin != "marc0":
        st.warning("🔒 Por favor, ingresa el PIN correcto en la barra lateral para ver tus opciones.")
        st.stop()
elif usuario == "Inquilino: Nora":
    pin = st.sidebar.text_input("Ingresa tu PIN (Nora):", type="password")
    if pin != "1111":
        st.warning("🔒 Ingresa tu PIN de inquilino para acceder a tu historial privado.")
        st.stop()
elif usuario == "Inquilino: Jesús":
    pin = st.sidebar.text_input("Ingresa tu PIN (Jesús):", type="password")
    if pin != "2222":
        st.warning("🔒 Ingresa tu PIN de inquilino para acceder a tu historial privado.")
        st.stop()

# Listas auxiliares para armar el historial de forma limpia
lista_meses = list(st.session_state.registro_historico.keys())

# ==========================================
# 🏠 ESCENARIO 1: PÁGINA PRINCIPAL (RESUMEN)
# ==========================================
if usuario == "Página Principal (Resumen)":
    st.write("Bienvenido al sistema. Aquí puedes ver de forma rápida el último recibo calculado.")
    
    mes_reciente = lista_meses[0]
    datos_mes = st.session_state.registro_historico[mes_reciente]
    
    st.subheader(f"📌 Último Mes Calculado: {mes_reciente}")
    
    st.markdown(f"""
        <div class="card-resumen">
            <strong>Recibo General de la Casa:</strong> S/. {datos_mes['monto_total']:.2f} | Consumo: {datos_mes['kwh_total']:.0f} kWh <br>
            <span style='color: #64748b; font-size: 14px;'>Facturado durante el período: {datos_mes['periodo']}</span>
        </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    with col1:
        st.markdown(f"""
            <div class="card-nora" style="padding:15px;">
                <h4>👩‍🦰 Sra. Nora</h4>
                <div style="font-size:20px; font-weight:bold; color:#be123c;">S/. {datos_mes['nora_pago']:.2f}</div>
                <span style="font-size:13px; color:#475569;">Consumo: {datos_mes['nora_kwh']:.2f} kWh</span>
            </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown(f"""
            <div class="card-jesus" style="padding:15px;">
                <h4>👨‍🦱 Jesús</h4>
                <div style="font-size:20px; font-weight:bold; color:#1d4ed8;">S/. {datos_mes['jesus_pago']:.2f}</div>
                <span style="font-size:13px; color:#475569;">Consumo: {datos_mes['jesus_kwh']:.2f} kWh</span>
            </div>
        """, unsafe_allow_html=True)
        
    st.info("💡 Inquilinos: Para revisar el historial completo de meses anteriores o detalles de su medidor, seleccionen su nombre en la barra de la izquierda.")

# ==========================================
# 🔐 ESCENARIO 2: ADMINISTRADOR (INGRESO)
# ==========================================
elif usuario == "Administrador":
    st.subheader("🛠️ Panel de Control - Administrador")
    st.write("Desde aquí puedes ingresar los datos mensuales. Al guardar, se actualizarán los paneles de tus inquilinos.")
    
    with st.form("formulario_mes"):
        nombre_mes = st.text_input("Nombre del Mes a Facturar:", placeholder="Noviembre 2026")
        periodo_txt = st.text_input("Período de fechas del recibo:", placeholder="17/10/2026 al 17/11/2026")
        
        col_ad1, col_ad2 = st.columns(2)
        with col_ad1:
            monto_in = st.number_input("Costo del Recibo General (S/.)", min_value=0.0, value=94.0)
            nora_kwh_in = st.number_input("kWh calculados para Nora este mes:", min_value=0.0, value=57.5)
        with col_ad2:
            kwh_in = st.number_input("Consumo General de la casa (kWh)", min_value=1.0, value=116.0)
            
        boton_guardar = st.form_submit_button("💾 Procesar y Publicar Cuentas", type="primary")
        
        if boton_guardar:
            if not nombre_mes or not periodo_txt:
                st.error("⚠️ Llena el nombre del mes y el período de fechas.")
            else:
                jesus_kwh_calc = max(0.0, kwh_in - nora_kwh_in)
                pct_nora_calc = nora_kwh_in / kwh_in if kwh_in > 0 else 0
                
                pago_nora_calc = monto_in * pct_nora_calc
                pago_jesus_calc = monto_in * (1.0 - pct_nora_calc)
                
                nuevo_registro = {
                    nombre_mes: {
                        "monto_total": float(monto_in), "kwh_total": float(kwh_in),
                        "periodo": periodo_txt,
                        "nora_kwh": round(nora_kwh_in, 2), "jesus_kwh": round(jesus_kwh_calc, 2),
                        "nora_pago": round(pago_nora_calc, 2), "jesus_pago": round(pago_jesus_calc, 2)
                    }
                }
                st.session_state.registro_historico = {**nuevo_registro, **st.session_state.registro_historico}
                st.success(f"🎉 ¡El mes de '{nombre_mes}' ha sido añadido al historial!")
                st.rerun()

# ==========================================
# 👩‍🦰 ESCENARIO 3: USUARIO NORA (SOLO LO SUYO)
# ==========================================
elif usuario == "Inquilino: Nora":
    st.subheader("👩‍🦰 Historial de Consumos - Sra. Nora")
    
    # Extraer los datos actuales destacados de Nora
    mes_reciente = lista_meses[0]
    act = st.session_state.registro_historico[mes_reciente]
    
    st.markdown(f"""
        <div class="card-nora">
            <h3>📌 Monto del Período Actual ({mes_reciente})</h3>
            <p style="margin:0; color:#475569;">Rango de días: {act['periodo']}</p>
            <p style="margin:0; color:#475569;">Su consumo de energía: <strong>{act['nora_kwh']:.2f} kWh</strong></p>
            <div class="monto-grande" style="color:#be123c;">Total a pagar: S/. {act['nora_pago']:.2f}</div>
        </div>
    """, unsafe_allow_html=True)
    
    # Armar la tabla histórica
    tabla_nora = []
    for m in lista_meses:
        info = st.session_state.registro_historico[m]
        tabla_nora.append({
            "Mes": m, "Período Facturado": info["periodo"], 
            "Su Consumo": f"{info['nora_kwh']:.2f} kWh", "Total a Pagar": f"S/. {info['nora_pago']:.2f}"
        })
    
    st.subheader("📚 Historial de Meses Anteriores")
    st.dataframe(pd.DataFrame(tabla_nora), hide_index=True, use_container_width=True)

# ==========================================
# 👨‍🦱 ESCENARIO 4: USUARIO JESÚS (SOLO LO SUYO)
# ==========================================
elif usuario == "Inquilino: Jesús":
    st.subheader("👨‍🦱 Historial de Consumos - Jesús")
    
    # Extraer los datos actuales destacados de Jesús
    mes_reciente = lista_meses[0]
    act = st.session_state.registro_historico[mes_reciente]
    
    st.markdown(f"""
        <div class="card-jesus">
            <h3>📌 Monto del Período Actual ({mes_reciente})</h3>
            <p style="margin:0; color:#475569;">Rango de días: {act['periodo']}</p>
            <p style="margin:0; color:#475569;">Tu consumo de energía (Diferencia): <strong>{act['jesus_kwh']:.2f} kWh</strong></p>
            <div class="monto-grande" style="color:#1d4ed8;">Total a pagar: S/. {act['jesus_pago']:.2f}</div>
        </div>
    """, unsafe_allow_html=True)
    
    # Armar la tabla histórica
    tabla_jesus = []
    for m in lista_meses:
        info = st.session_state.registro_historico[m]
        tabla_jesus.append({
            "Mes": m, "Período Facturado": info["periodo"], 
            "Tu Consumo": f"{info['jesus_kwh']:.2f} kWh", "Total a Pagar": f"S/. {info['jesus_pago']:.2f}"
        })
    
    st.subheader("📚 Historial de Meses Anteriores")
    st.dataframe(pd.DataFrame(tabla_jesus), hide_index=True, use_container_width=True)
