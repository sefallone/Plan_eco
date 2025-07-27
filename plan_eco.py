import streamlit as st
import pandas as pd
import altair as alt
from datetime import datetime, timedelta
import numpy as np
import locale # Importar el módulo locale

# --- 1. Carga y Preparación de Datos ---
# Función para cargar datos directamente desde un archivo de Excel
def load_data_from_excel(uploaded_file):
    if uploaded_file is not None:
        try:
            # Leer el archivo de Excel en un DataFrame de pandas
            df = pd.read_excel(uploaded_file)
            
            # Limpiar espacios en blanco de los nombres de columna si existen
            df.columns = df.columns.str.strip()

            # Convertir 'Fecha' a objetos datetime, manejando errores y eliminando espacios
            if 'Fecha' in df.columns:
                # Establecer la configuración regional a español para que pd.to_datetime reconozca los nombres de los meses
                try:
                    locale.setlocale(locale.LC_TIME, 'es_ES.UTF-8')
                except locale.Error:
                    # Fallback para sistemas donde 'es_ES.UTF-8' no está disponible
                    locale.setlocale(locale.LC_TIME, 'es_ES')
                except Exception as e:
                    st.warning(f"Advertencia: No se pudo establecer la configuración regional para fechas: {e}. "
                               "Esto podría afectar la interpretación de los nombres de meses en español.")

                df['Fecha'] = df['Fecha'].astype(str).apply(lambda x: x.strip()) # Asegurar que es string y limpiar espacios
                df['Fecha'] = pd.to_datetime(df['Fecha'], format='%b-%y', errors='coerce')

                # Verificar si hay fechas que fallaron en la conversión
                if df['Fecha'].isnull().any():
                    st.warning("Advertencia: Algunas fechas en el archivo de Excel no pudieron ser convertidas. "
                               "Por favor, revisa el formato de la columna 'Fecha' en tu archivo. "
                               "Las filas afectadas pueden no aparecer en los gráficos.")
            else:
                st.error("Error: La columna 'Fecha' no se encontró en el archivo de Excel.")
                return pd.DataFrame() # Retorna un DataFrame vacío si falta la columna clave

            # Calcular columnas derivadas necesarias para KPIs y gráficos
            # Se asume que estas columnas existen en el Excel o se pueden derivar
            # Añade validaciones o un valor por defecto si alguna columna esperada no existe
            
            # Asegúrate de que todas las columnas necesarias para los cálculos existan
            required_cols = [
                'Total Facturación', 'Facturación CCEE VITHAS', 'Facturación CCEE OSA (80%)',
                'Facturación Quirúrgico VITHAS', 'Facturación Quirúrgico OSA (90%)',
                'Facturación Urgencias OSA (50% )', 'Facturación Urgencias VITHAS',
                'No. De Pacientes CCEE', 'No. De Intervenciones Quirúrgicas',
                'No. Urgencias Mes', 'Precio Medio Consultas CCEE', 'Precio Medio Urgencias',
                'Pacientes x Módulo (Cada 15 min)', 'Días x mes CCEE', 'Días x Mes Urgencias',
                'Módulos Totales x día', 'Módulos Mañana', 'Módulos Tarde',
                'Precio HHMM 80% Consultas', 'Precio Medio HHMM Quirúrgicas',
                'Urgencias días Trauma (15%)', 'Urgencias días totales Vitha'
            ]
            
            for col in required_cols:
                if col not in df.columns:
                    st.warning(f"Advertencia: La columna '{col}' no se encontró en el archivo de Excel. "
                               "Algunos cálculos y gráficos pueden verse afectados. Se usará 0 como valor por defecto.")
                    df[col] = 0 # Añade la columna con ceros si no existe para evitar errores
                # Intentar convertir a tipo numérico, forzando errores a NaN
                try:
                    df[col] = pd.to_numeric(df[col], errors='coerce')
                except Exception:
                    # Si no se puede convertir a numérico, no hacer nada o loggear
                    pass


            df['Total Facturación CCEE'] = df['Facturación CCEE VITHAS'] + df['Facturación CCEE OSA (80%)']
            df['Total Facturación Quirúrgico'] = df['Facturación Quirúrgico VITHAS'] + df['Facturación Quirúrgico OSA (90%)']
            df['Total Facturación Urgencias'] = df['Facturación Urgencias OSA (50% )'] + df['Facturación Urgencias VITHAS']
            
            df['Total Ingresos General'] = df['Total Facturación CCEE'] + df['Total Facturación Quirúrgico'] + df['Total Facturación Urgencias']
            
            return df

        except Exception as e:
            st.error(f"Error al leer el archivo de Excel: {e}. Asegúrate de que el archivo es un formato Excel válido y las columnas son correctas.")
            return pd.DataFrame() # Retorna un DataFrame vacío en caso de error
    else:
        return pd.DataFrame() # Retorna un DataFrame vacío si no hay archivo cargado

# --- 2. Configuración de la Página Streamlit ---
st.set_page_config(
    page_title="Dashboard Financiero y Operacional",
    page_icon="📈",
    layout="wide"
)

st.title("📊 Dashboard: Análisis Financiero y Operacional")
st.markdown("---")

# --- 3. Filtros Globales y Carga de Archivo ---
st.sidebar.header("Cargar Datos y Filtros")
uploaded_file = st.sidebar.file_uploader("Sube tu archivo de Excel (.xlsx, .xls)", type=["xlsx", "xls"])

df = load_data_from_excel(uploaded_file)

if df.empty:
    st.info("Por favor, sube un archivo de Excel para comenzar el análisis.")
    st.stop() # Detiene la ejecución si no hay datos

# Asegurarse de que 'Fecha' no tenga valores nulos después de la conversión
df = df.dropna(subset=['Fecha'])

# Filtro de año
selected_year = st.sidebar.selectbox(
    "Seleccionar Año", 
    options=sorted(df['Fecha'].dt.year.unique(), reverse=True)
)

df_filtered = df[df['Fecha'].dt.year == selected_year]

if df_filtered.empty:
    st.warning(f"No hay datos disponibles para el año {selected_year} después de aplicar los filtros. Por favor, revisa tu archivo o selecciona otro año.")
    st.stop()

# --- 4. Definición y Visualización de KPIs (10 KPIs) ---
st.header(f"📈 Resumen Anual ({selected_year})")

# Calculando KPIs para el año filtrado
# Se añaden .sum() o .mean() para asegurar que el cálculo se realiza sobre los datos filtrados
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
st.success("¡Sube tu archivo de Excel para visualizar los datos!")



