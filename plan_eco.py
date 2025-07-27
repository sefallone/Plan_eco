import streamlit as st
import pandas as pd
import altair as alt
from datetime import datetime, timedelta
import numpy as np

# --- 1. Carga y Preparación de Datos ---
# Datos reales transcritos de las imágenes del archivo de Excel (Oct 2025 - Dic 2027).
def load_data():
    data = {
        'Fecha': [
            'oct-25', 'nov-25', 'dic-25', 'ene-26', 'feb-26', 'mar-26', 'abr-26', 'may-26', 
            'jun-26', 'jul-26', 'ago-26', 'sep-26', 'oct-26', 'nov-26', 'dic-26',
            'ene-27', 'feb-27', 'mar-27', 'abr-27', 'may-27', 'jun-27',
            'jul-27', 'ago-27', 'sep-27', 'oct-27', 'nov-27', 'dic-27'
        ],
        'Total Facturación': [
            100000, 120000, 140000, 200000, 210000, 210000, 260000, 260000,
            360000, 360000, 360000, 370000, 370000, 370000, 380000,
            390000, 400000, 410000, 420000, 430000, 440000,
            450000, 460000, 470000, 480000, 490000, 500000
        ],
        'Facturación CCEE VITHAS': [
            10000, 12000, 14000, 20000, 21000, 21000, 26000, 26000,
            36000, 36000, 36000, 37000, 37000, 37000, 38000,
            39000, 40000, 41000, 42000, 43000, 44000,
            45000, 46000, 47000, 48000, 49000, 50000
        ],
        'Facturación CCEE OSA (80%)': [
            8000, 9600, 11200, 16000, 16800, 16800, 20800, 20800,
            28800, 28800, 28800, 29600, 29600, 29600, 30400,
            31200, 32000, 32800, 33600, 34400, 35200,
            36000, 36800, 37600, 38400, 39200, 40000
        ],
        'No. De Pacientes CCEE': [
            500, 600, 700, 1000, 1050, 1050, 1300, 1300,
            1800, 1800, 1800, 1850, 1850, 1850, 1900,
            1950, 2000, 2050, 2100, 2150, 2200,
            2250, 2300, 2350, 2400, 2450, 2500
        ],
        'Pacientes x Módulo (Cada 15 min)': [
            2.00, 2.00, 2.00, 2.00, 2.00, 2.00, 2.00, 2.00,
            2.00, 2.00, 2.00, 2.00, 2.00, 2.00, 2.00,
            2.10, 2.10, 2.10, 2.10, 2.10, 2.10,
            2.10, 2.10, 2.10, 2.10, 2.10, 2.10
        ],
        'Días x mes CCEE': [
            20, 20, 20, 20, 20, 20, 20, 20,
            20, 20, 20, 20, 20, 20, 20,
            21, 21, 21, 21, 21, 21,
            21, 21, 21, 21, 21, 21
        ],
        'Módulos Totales x día': [
            1.00, 1.00, 1.00, 1.00, 1.00, 1.00, 4.00, 4.00,
            4.00, 4.00, 4.00, 4.00, 4.00, 4.00, 4.00,
            5.00, 5.00, 5.00, 5.00, 5.00, 5.00,
            5.00, 5.00, 5.00, 5.00, 5.00, 5.00
        ],
        'Módulos Mañana': [
            1.00, 1.00, 1.00, 1.00, 1.00, 1.00, 2.00, 2.00,
            2.00, 2.00, 2.00, 2.00, 2.00, 2.00, 2.00,
            2.50, 2.50, 2.50, 2.50, 2.50, 2.50,
            2.50, 2.50, 2.50, 2.50, 2.50, 2.50
        ],
        'Módulos Tarde': [
            1.00, 1.00, 1.00, 1.00, 1.00, 1.00, 2.00, 2.00,
            2.00, 2.00, 2.00, 2.00, 2.00, 2.00, 2.00,
            2.50, 2.50, 2.50, 2.50, 2.50, 2.50,
            2.50, 2.50, 2.50, 2.50, 2.50, 2.50
        ],
        'Precio Medio Consultas CCEE': [
            20.00, 20.00, 20.00, 20.00, 20.00, 20.00, 20.00, 20.00,
            20.00, 20.00, 20.00, 20.00, 20.00, 20.00, 20.00,
            21.00, 21.00, 21.00, 21.00, 21.00, 21.00,
            21.00, 21.00, 21.00, 21.00, 21.00, 21.00
        ],
        'Precio HHMM 80% Consultas': [
            20.00, 20.00, 20.00, 20.00, 20.00, 20.00, 20.00, 20.00,
            20.00, 20.00, 20.00, 20.00, 20.00, 20.00, 20.00,
            21.00, 21.00, 21.00, 21.00, 21.00, 21.00,
            21.00, 21.00, 21.00, 21.00, 21.00, 21.00
        ],
        'Facturación Quirúrgico VITHAS': [
            20.00, 20.00, 20.00, 20.00, 20.00, 20.00, 20.00, 20.00,
            20.00, 20.00, 20.00, 20.00, 20.00, 20.00, 20.00,
            50.00, 50.00, 50.00, 50.00, 50.00, 50.00,
            50.00, 50.00, 50.00, 50.00, 50.00, 50.00
        ],
        'Facturación Quirúrgico OSA (90%)': [
            20.00, 20.00, 20.00, 20.00, 20.00, 20.00, 20.00, 20.00,
            20.00, 20.00, 20.00, 20.00, 20.00, 20.00, 20.00,
            45.00, 45.00, 45.00, 45.00, 45.00, 45.00,
            45.00, 45.00, 45.00, 45.00, 45.00, 45.00
        ],
        'No. De Intervenciones Quirúrgicas': [
            20.00, 20.00, 20.00, 20.00, 20.00, 20.00, 20.00, 20.00,
            20.00, 20.00, 20.00, 20.00, 20.00, 20.00, 20.00,
            50.00, 50.00, 50.00, 50.00, 50.00, 50.00,
            50.00, 50.00, 50.00, 50.00, 50.00, 50.00
        ],
        'Precio Medio HHMM Quirúrgicas': [
            20.00, 20.00, 20.00, 20.00, 20.00, 20.00, 20.00, 20.00,
            20.00, 20.00, 20.00, 20.00, 20.00, 20.00, 20.00,
            50.00, 50.00, 50.00, 50.00, 50.00, 50.00,
            50.00, 50.00, 50.00, 50.00, 50.00, 50.00
        ],
        'Facturación Urgencias OSA (50% )': [
            17500, 17500, 17500, 17500, 17500, 17500, 17500, 17500,
            17500, 17500, 17500, 17500, 17500, 17500, 17500,
            18000, 18000, 18000, 18000, 18000, 18000,
            18000, 18000, 18000, 18000, 18000, 18000
        ],
        'Facturación Urgencias VITHAS': [
            8750, 8750, 8750, 8750, 8750, 8750, 8750, 8750,
            8750, 8750, 8750, 8750, 8750, 8750, 8750,
            9000, 9000, 9000, 9000, 9000, 9000,
            9000, 9000, 9000, 9000, 9000, 9000
        ],
        'No. Urgencias Mes': [
            300, 300, 300, 300, 300, 300, 300, 300,
            300, 300, 300, 300, 300, 300, 300,
            350, 350, 350, 350, 350, 350,
            350, 350, 350, 350, 350, 350
        ],
        'Días x Mes Urgencias': [
            30, 30, 30, 30, 30, 30, 30, 30,
            30, 30, 30, 30, 30, 30, 30,
            30, 30, 30, 30, 30, 30,
            30, 30, 30, 30, 30, 30
        ],
        'Urgencias días Trauma (15%)': [
            3.00, 3.00, 3.00, 3.00, 3.00, 3.00, 3.00, 3.00,
            3.00, 3.00, 3.00, 3.00, 3.00, 3.00, 3.00,
            3.50, 3.50, 3.50, 3.50, 3.50, 3.50,
            3.50, 3.50, 3.50, 3.50, 3.50, 3.50
        ],
        'Urgencias días totales Vitha': [
            5.00, 5.00, 5.00, 5.00, 5.00, 5.00, 5.00, 5.00,
            5.00, 5.00, 5.00, 5.00, 5.00, 5.00, 5.00,
            6.00, 6.00, 6.00, 6.00, 6.00, 6.00,
            6.00, 6.00, 6.00, 6.00, 6.00, 6.00
        ],
        'Precio Medio Urgencias': [
            60.00, 60.00, 60.00, 60.00, 60.00, 60.00, 60.00, 60.00,
            60.00, 60.00, 60.00, 60.00, 60.00, 60.00, 60.00,
            65.00, 65.00, 65.00, 65.00, 65.00, 65.00,
            65.00, 65.00, 65.00, 65.00, 65.00, 65.00
        ]
    }
    df = pd.DataFrame(data)
    
    # Convert 'Fecha' to datetime objects
    df['Fecha'] = pd.to_datetime(df['Fecha'], format='%b-%y')

    # Calcular columnas derivadas necesarias para KPIs y gráficos
    df['Total Facturación CCEE'] = df['Facturación CCEE VITHAS'] + df['Facturación CCEE OSA (80%)']
    df['Total Facturación Quirúrgico'] = df['Facturación Quirúrgico VITHAS'] + df['Facturación Quirúrgico OSA (90%)']
    df['Total Facturación Urgencias'] = df['Facturación Urgencias OSA (50% )'] + df['Facturación Urgencias VITHAS']
    
    # Suma de todas las facturaciones por tipo para un "Total Ingresos" más general si se desea
    df['Total Ingresos General'] = df['Total Facturación CCEE'] + df['Total Facturación Quirúrgico'] + df['Total Facturación Urgencias']
    
    return df

df = load_data()

# --- 2. Configuración de la Página Streamlit ---
st.set_page_config(
    page_title="Dashboard Financiero y Operacional",
    page_icon="📈",
    layout="wide"
)

st.title("📊 Dashboard: Análisis Financiero y Operacional")
st.markdown("---")

# --- 3. Filtros Globales ---
st.sidebar.header("Filtros")
selected_year = st.sidebar.selectbox("Seleccionar Año", options=sorted(df['Fecha'].dt.year.unique(), reverse=True))

df_filtered = df[df['Fecha'].dt.year == selected_year]

if df_filtered.empty:
    st.warning(f"No hay datos disponibles para el año {selected_year}. Por favor, ajusta el archivo de datos o selecciona otro año.")
    st.stop()

# --- 4. Definición y Visualización de KPIs (10 KPIs) ---
st.header(f"📈 Resumen Anual ({selected_year})")

# Calculando KPIs para el año filtrado
kpis = {
    "Total Facturación General": df_filtered['Total Facturación'].sum(),
    "Facturación CCEE Total": df_filtered['Total Facturación CCEE'].sum(),
    "Facturación Quirúrgico Total": df_filtered['Total Facturación Quirúrgico'].sum(),
    "Facturación Urgencias Total": df_filtered['Total Facturación Urgencias'].sum(),
    "Total Pacientes CCEE": df_filtered['No. De Pacientes CCEE'].sum(),
    "Total Intervenciones Quirúrgicas": df_filtered['No. De Intervenciones Quirúrgicas'].sum(),
    "Total Urgencias (Nº)": df_filtered['No. Urgencias Mes'].sum(),
    "Precio Medio Consultas CCEE (Promedio)": df_filtered['Precio Medio Consultas CCEE'].mean(),
    "Precio Medio Urgencias (Promedio)": df_filtered['Precio Medio Urgencias'].mean(),
    "Productividad Módulos (Promedio Pacientes/Módulo)": df_filtered['Pacientes x Módulo (Cada 15 min)'].mean()
}

# Mostrar los KPIs en columnas
col_kpi1, col_kpi2, col_kpi3, col_kpi4, col_kpi5 = st.columns(5)

with col_kpi1:
    st.metric("Total Facturación General", f"${kpis['Total Facturación General']:,.0f}")
    st.metric("Facturación CCEE Total", f"${kpis['Facturación CCEE Total']:,.0f}")
with col_kpi2:
    st.metric("Facturación Quirúrgico Total", f"${kpis['Facturación Quirúrgico Total']:,.0f}")
    st.metric("Facturación Urgencias Total", f"${kpis['Facturación Urgencias Total']:,.0f}")
with col_kpi3:
    st.metric("Total Pacientes CCEE", f"{kpis['Total Pacientes CCEE']:,.0f}")
    st.metric("Total Intervenciones QX", f"{kpis['Total Intervenciones Quirúrgicas']:,.0f}")
with col_kpi4:
    st.metric("Total Urgencias (Nº)", f"{kpis['Total Urgencias (Nº)']:.0f}")
    st.metric("Precio Medio Consultas CCEE", f"${kpis['Precio Medio Consultas CCEE (Promedio)']:.2f}")
with col_kpi5:
    st.metric("Precio Medio Urgencias", f"${kpis['Precio Medio Urgencias (Promedio)']:.2f}")
    st.metric("Productividad Módulos", f"{kpis['Productividad Módulos (Promedio Pacientes/Módulo)']:.2f} Px/Mód")

st.markdown("---")

# --- 5. Visualización de Gráficos (10 Gráficos) ---
st.header("📊 Análisis Detallado y Tendencias")

# Preparar datos para gráficos mensuales
df_monthly = df_filtered.copy()
df_monthly['Mes'] = df_monthly['Fecha'].dt.strftime('%Y-%m') # Formato para ordenar cronológicamente

# Gráfico 1: Tendencia Mensual de Facturación Total
st.subheader("1. Tendencia Mensual de Facturación Total")
chart1 = alt.Chart(df_monthly).mark_line(point=True).encode(
    x=alt.X('Mes:O', title='Mes'),
    y=alt.Y('Total Facturación:Q', title='Facturación ($)'),
    tooltip=[alt.Tooltip('Mes'), alt.Tooltip('Total Facturación', format='$,.0f')]
).properties(
    title='Facturación Total Mensual'
).interactive()
st.altair_chart(chart1, use_container_width=True)

# Gráfico 2: Tendencia Mensual de Facturación por Tipo de Servicio
st.subheader("2. Tendencia Mensual: Facturación por Tipo de Servicio")
df_facturacion_tipos = df_monthly.melt(
    id_vars=['Mes'],
    value_vars=['Total Facturación CCEE', 'Total Facturación Quirúrgico', 'Total Facturación Urgencias'],
    var_name='Tipo de Facturación',
    value_name='Valor'
)
chart2 = alt.Chart(df_facturacion_tipos).mark_line(point=True).encode(
    x=alt.X('Mes:O', title='Mes'),
    y=alt.Y('Valor:Q', title='Facturación ($)'),
    color='Tipo de Facturación:N',
    tooltip=['Mes', 'Tipo de Facturación', alt.Tooltip('Valor', format='$,.0f')]
).properties(
    title='Facturación Mensual por Tipo de Servicio'
).interactive()
st.altair_chart(chart2, use_container_width=True)

# Gráfico 3: Tendencia Mensual: Nº Pacientes CCEE vs Nº Intervenciones Quirúrgicas
st.subheader("3. Tendencia Mensual: Nº Pacientes y Nº Intervenciones QX")
df_pacientes_qx_melted = df_monthly.melt(
    id_vars=['Mes'], 
    value_vars=['No. De Pacientes CCEE', 'No. De Intervenciones Quirúrgicas'],
    var_name='Métrica', 
    value_name='Cantidad'
)
chart3 = alt.Chart(df_pacientes_qx_melted).mark_line(point=True).encode(
    x=alt.X('Mes:O', title='Mes'),
    y=alt.Y('Cantidad:Q', title='Cantidad'),
    color='Métrica:N',
    tooltip=['Mes', 'Métrica', 'Cantidad']
).properties(
    title='Tendencia Mensual de Pacientes CCEE e Intervenciones QX'
).interactive()
st.altair_chart(chart3, use_container_width=True)

# Gráfico 4: Tendencia Mensual: Nº Urgencias Mes
st.subheader("4. Tendencia Mensual: Nº Urgencias Mes")
chart4 = alt.Chart(df_monthly).mark_line(point=True, color='orange').encode(
    x=alt.X('Mes:O', title='Mes'),
    y=alt.Y('No. Urgencias Mes:Q', title='Número de Urgencias'),
    tooltip=['Mes', 'No. Urgencias Mes']
).properties(
    title='Número de Urgencias Mensual'
).interactive()
st.altair_chart(chart4, use_container_width=True)

# Gráfico 5: Comparación Mensual: Precios Medios (Consultas CCEE vs Urgencias)
st.subheader("5. Comparación Mensual: Precios Medios")
df_precios_medios_melted = df_monthly.melt(
    id_vars=['Mes'],
    value_vars=['Precio Medio Consultas CCEE', 'Precio Medio Urgencias'],
    var_name='Tipo de Precio Medio',
    value_name='Precio'
)
chart5 = alt.Chart(df_precios_medios_melted).mark_line(point=True).encode(
    x=alt.X('Mes:O', title='Mes'),
    y=alt.Y('Precio:Q', title='Precio ($)'),
    color='Tipo de Precio Medio:N',
    tooltip=['Mes', 'Tipo de Precio Medio', alt.Tooltip('Precio', format='$,.2f')]
).properties(
    title='Tendencia Mensual de Precios Medios'
).interactive()
st.altair_chart(chart5, use_container_width=True)

# Gráfico 6: Distribución de Días por Mes (CCEE vs Urgencias)
st.subheader("6. Días de Actividad por Mes (CCEE vs Urgencias)")
df_dias_melted = df_monthly.melt(
    id_vars=['Mes'],
    value_vars=['Días x mes CCEE', 'Días x Mes Urgencias'],
    var_name='Tipo de Días',
    value_name='Días'
)
chart6 = alt.Chart(df_dias_melted).mark_bar().encode(
    x=alt.X('Mes:O', title='Mes'),
    y=alt.Y('Días:Q', title='Número de Días'),
    color='Tipo de Días:N',
    tooltip=['Mes', 'Tipo de Días', 'Días']
).properties(
    title='Días de Actividad Mensual'
).interactive()
st.altair_chart(chart6, use_container_width=True)

# Gráfico 7: Composición de Módulos (Mañana vs Tarde)
st.subheader("7. Composición Mensual de Módulos (Mañana vs Tarde)")
df_modulos_melted = df_monthly.melt(
    id_vars=['Mes'],
    value_vars=['Módulos Mañana', 'Módulos Tarde'],
    var_name='Turno',
    value_name='Número de Módulos'
)
chart7 = alt.Chart(df_modulos_melted).mark_bar().encode(
    x=alt.X('Mes:O', title='Mes'),
    y=alt.Y('Número de Módulos:Q', title='Módulos'),
    color='Turno:N',
    tooltip=['Mes', 'Turno', 'Número de Módulos']
).properties(
    title='Módulos Mensuales por Turno'
).interactive()
st.altair_chart(chart7, use_container_width=True)

# Gráfico 8: Relación: Pacientes x Módulo vs Módulos Totales x día
st.subheader("8. Relación: Pacientes por Módulo vs Módulos Totales por Día")
chart8 = alt.Chart(df_monthly).mark_circle().encode(
    x=alt.X('Módulos Totales x día:Q', title='Módulos Totales por Día'),
    y=alt.Y('Pacientes x Módulo (Cada 15 min):Q', title='Pacientes por Módulo'),
    tooltip=['Mes', 'Módulos Totales x día', 'Pacientes x Módulo (Cada 15 min)']
).properties(
    title='Relación entre Módulos y Productividad de Pacientes'
).interactive()
st.altair_chart(chart8, use_container_width=True)

# Gráfico 9: Tendencia Mensual: Precio HHMM 80% Consultas vs Precio Medio HHMM Quirúrgicas
st.subheader("9. Tendencia Mensual: Precios HHMM")
df_precio_hhmm_melted = df_monthly.melt(
    id_vars=['Mes'],
    value_vars=['Precio HHMM 80% Consultas', 'Precio Medio HHMM Quirúrgicas'],
    var_name='Tipo de Precio HHMM',
    value_name='Precio'
)
chart9 = alt.Chart(df_precio_hhmm_melted).mark_line(point=True).encode(
    x=alt.X('Mes:O', title='Mes'),
    y=alt.Y('Precio:Q', title='Precio ($)'),
    color='Tipo de Precio HHMM:N',
    tooltip=['Mes', 'Tipo de Precio HHMM', alt.Tooltip('Precio', format='$,.2f')]
).properties(
    title='Tendencia Mensual de Precios HHMM'
).interactive()
st.altair_chart(chart9, use_container_width=True)

# Gráfico 10: Tendencia Mensual: Urgencias días Trauma (15%) vs Urgencias días totales Vitha
st.subheader("10. Tendencia Mensual: Días de Urgencias (Trauma vs Totales Vitha)")
df_urgencias_dias_melted = df_monthly.melt(
    id_vars=['Mes'],
    value_vars=['Urgencias días Trauma (15%)', 'Urgencias días totales Vitha'],
    var_name='Tipo de Días de Urgencia',
    value_name='Días'
)
chart10 = alt.Chart(df_urgencias_dias_melted).mark_line(point=True).encode(
    x=alt.X('Mes:O', title='Mes'),
    y=alt.Y('Días:Q', title='Número de Días'),
    color='Tipo de Días de Urgencia:N',
    tooltip=['Mes', 'Tipo de Días de Urgencia', 'Días']
).properties(
    title='Tendencia Mensual de Días de Urgencias'
).interactive()
st.altair_chart(chart10, use_container_width=True)


st.markdown("---")
st.success("¡Dashboard actualizado con los datos proporcionados!")

