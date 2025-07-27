import streamlit as st
import pandas as pd
import plotly.express as px

# Cargar datos (ajusta la ruta)
df = pd.read_excel("Proyeccion 3.xlsx", sheet_name="Proyeccion 2025-26-27")

# Configurar página
st.set_page_config(layout="wide")
st.title("📊 Dashboard de Proyección Financiera 2025-2027")

# --- KPIs ---
st.header("🔍 KPIs Principales")
col1, col2, col3 = st.columns(3)
with col1:
    total_fact = df["Total Facturación"].sum() / 1000  # En miles
    st.metric("Facturación Total (Miles)", f"${total_fact:,.0f}K")

with col2:
    crecimiento = ((df[df["Fecha"].dt.year == 2027]["Total Facturación"].mean() / 
                   df[df["Fecha"].dt.year == 2025]["Total Facturación"].mean()) - 1) * 100
    st.metric("Crecimiento 2025-2027", f"{crecimiento:.1f}%")

with col3:
    avg_pacientes = df["No. De Pacientes CCEE"].mean()
    st.metric("Pacientes CCEE (Prom/Mes)", f"{avg_pacientes:,.0f}")

# --- Gráficos ---
st.header("📈 Visualizaciones")

# 1. Facturación por Área
fig1 = px.bar(df, x="Fecha", y=["Facturación CCEE VITHAS", "Facturación Quirúrgico VITHAS", "Facturación Urgencias VITHAS"],
              title="Facturación Mensual por Área (VITHAS)")
st.plotly_chart(fig1, use_container_width=True)

# 2. Evolución Total
fig2 = px.line(df, x="Fecha", y="Total Facturación", title="Evolución de Facturación Total")
st.plotly_chart(fig2, use_container_width=True)

# 3. Módulos vs Pacientes
fig3 = px.bar(df, x="Fecha", y=["Pacientes x Módulo (Cada 15 min)", "Módulos Totales x día"],
              barmode="group", title="Eficiencia de Módulos CCEE")
st.plotly_chart(fig3, use_container_width=True)

# --- Filtros Interactivos ---
st.sidebar.header("Filtros")
year = st.sidebar.selectbox("Año", [2025, 2026, 2027])
df_filtered = df[df["Fecha"].dt.year == year]

# Mostrar datos filtrados
st.write(f"Datos para {year}:", df_filtered)


