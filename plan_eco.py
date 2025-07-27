import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime

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
        df['Mes'] = df['Fecha'].dt.month_name(locale='es')
        
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
selected_year = st.sidebar.selectbox("Selecciona el año", options=df['Año'].unique())
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
crecimiento_anual = ((df[df['Año'] == selected_year]["Total Facturación"].sum() / 
                     df[df['Año'] == (selected_year - 1)]["Total Facturación"].sum() - 1) * 100

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
    st.metric("Crecimiento Anual (%)", f"{crecimiento_anual:.1f}%")
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

# Gráfico 2: Evolución mensual
fig2 = px.line(df_filtered, 
               x="Fecha", 
               y="Total Facturación",
               title=f"Evolución Mensual de Facturación ({selected_year})")
st.plotly_chart(fig2, use_container_width=True)

# Gráfico 3: Distribución de facturación
fig3 = px.pie(df_filtered,
              names=["CCEE", "Quirúrgico", "Urgencias"],
              values=[df_filtered["Facturación CCEE VITHAS"].sum(), 
                      df_filtered["Facturación Quirúrgico VITHAS"].sum(),
                      df_filtered["Facturación Urgencias VITHAS"].sum()],
              title="Distribución de Facturación")
st.plotly_chart(fig3, use_container_width=True)

# Gráfico 4: Pacientes vs Módulos
fig4 = px.scatter(df_filtered,
                 x="No. De Pacientes CCEE",
                 y="Módulos Totales x día",
                 size="Total Facturación",
                 color="Mes",
                 title="Relación Pacientes vs Módulos")
st.plotly_chart(fig4, use_container_width=True)

# Gráfico 5: Intervenciones quirúrgicas
fig5 = px.bar(df_filtered,
             x="Mes",
             y="No. De Intervenciones Quirúrgicas",
             title=f"Intervenciones Quirúrgicas ({selected_year})")
st.plotly_chart(fig5, use_container_width=True)

# Gráfico 6: Urgencias
fig6 = px.area(df_filtered,
              x="Fecha",
              y="No. Urgencias Mes",
              title=f"Urgencias Mensuales ({selected_year})")
st.plotly_chart(fig6, use_container_width=True)

# --- Mostrar datos ---
if st.checkbox("Mostrar datos crudos"):
    st.dataframe(df_filtered)
