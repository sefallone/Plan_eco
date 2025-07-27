import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime
import locale
import os

# Configuración del locale para español (soluciona el error)
try:
    locale.setlocale(locale.LC_TIME, 'es_ES.UTF-8')
except:
    try:
        locale.setlocale(locale.LC_TIME, 'spanish')
    except:
        st.warning("No se pudo configurar el locale en español, los meses aparecerán en inglés")

# Configuración de la página
st.set_page_config(layout="wide", page_title="Dashboard Proyección Financiera")
st.title("📊 Dashboard de Proyección Financiera 2025-2027")

# --- Función para cargar datos ---
@st.cache_data
def load_data(uploaded_file):
    try:
        df = pd.read_excel(uploaded_file, sheet_name="Proyeccion 2025-26-27")
        
        # Limpieza de datos
        df['Fecha'] = pd.to_datetime(df['Fecha'])
        df['Año'] = df['Fecha'].dt.year
        
        # Extraer nombre del mes (en español si el locale funciona, sino en inglés)
        try:
            df['Mes'] = df['Fecha'].dt.strftime('%B')
        except:
            df['Mes'] = df['Fecha'].dt.month_name()
        
        return df
    except Exception as e:
        st.error(f"Error al cargar el archivo: {str(e)}")
        return None

# --- Carga del archivo ---
uploaded_file = st.file_uploader("Sube tu archivo Excel (Proyeccion 3.xlsx)", type="xlsx")

if not uploaded_file:
    st.warning("Por favor, sube un archivo Excel para continuar.")
    st.stop()

df = load_data(uploaded_file)

if df is None:
    st.error("No se pudieron cargar los datos. Verifica el formato del archivo.")
    st.stop()

# --- Sidebar con filtros ---
st.sidebar.header("Filtros")
selected_year = st.sidebar.selectbox("Selecciona el año", options=sorted(df['Año'].unique()))
df_filtered = df[df['Año'] == selected_year]

# --- Sección de KPIs ---
st.header("🔍 KPIs Clave")

# Calculamos los KPIs
total_facturacion = df_filtered["Total Facturación"].sum() / 1000  # En miles
facturacion_quirurgico = df_filtered["Facturación Quirúrgico VITHAS"].sum() / 1000
pacientes_totales = df_filtered["No. De Pacientes CCEE"].sum()
intervenciones = df_filtered["No. De Intervenciones Quirúrgicas"].sum()
modulos_promedio = df_filtered["Módulos Totales x día"].mean()
urgencias_mes = df_filtered["No. Urgencias Mes"].sum()
precio_medio_consultas = df_filtered["Precio Medio Consultas CCEE"].mean()
precio_medio_quirurgico = df_filtered["Precio Medio HHMM Quirúrgicas"].mean()

# Cálculo de crecimiento anual (solo si hay datos del año anterior)
if selected_year > min(df['Año']):
    crecimiento_anual = ((df[df['Año'] == selected_year]["Total Facturación"].sum() / 
                         df[df['Año'] == (selected_year - 1)]["Total Facturación"].sum() - 1) * 100)
else:
    crecimiento_anual = "N/A"

# Mostramos los KPIs en columnas
col1, col2, col3 = st.columns(3)
with col1:
    st.metric("Facturación Total (Miles €)", f"{total_facturacion:,.0f}K")
    st.metric("Pacientes Totales CCEE", f"{pacientes_totales:,.0f}")
    st.metric("Módulos Diarios Promedio", f"{modulos_promedio:.1f}")

with col2:
    st.metric("Facturación Quirúrgico (Miles €)", f"{facturacion_quirurgico:,.0f}K")
    st.metric("Intervenciones Quirúrgicas", f"{intervenciones:,.0f}")
    st.metric("Urgencias Totales", f"{urgencias_mes:,.0f}")

with col3:
    st.metric("Crecimiento Anual (%)", f"{crecimiento_anual if isinstance(crecimiento_anual, str) else f'{crecimiento_anual:.1f}%'}")
    st.metric("Precio Medio Consultas (€)", f"{precio_medio_consultas:,.0f}")
    st.metric("Precio Medio Quirúrgico (€)", f"{precio_medio_quirurgico:,.0f}")

# --- Gráficos ---
st.header("📈 Visualizaciones Clave")

# Gráfico 1: Facturación por áreas
fig1 = px.bar(df_filtered, 
              x="Mes", 
              y=["Facturación CCEE VITHAS", "Facturación Quirúrgico VITHAS", "Facturación Urgencias VITHAS"],
              title=f"Facturación por Área ({selected_year})",
              labels={"value": "Facturación (€)", "variable": "Área"})
st.plotly_chart(fig1, use_container_width=True)

# Resto de gráficos (igual que antes)...
# [Aquí irían los otros 5 gráficos del código original]

# --- Mostrar datos ---
if st.checkbox("Mostrar datos crudos"):
    st.dataframe(df_filtered)
