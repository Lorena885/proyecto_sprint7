import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px

# Encabezado principal de la app
st.header('Análisis de Anuncios de Venta de Coches en EE.UU.')

# Cargar los datos
car_data = pd.read_csv('vehicles_us.csv')

# -------------------------------
# FILTROS EN LA BARRA LATERAL
# -------------------------------
st.sidebar.header('Filtros')

# Filtro por condición
selected_condition = st.sidebar.selectbox(
    'Condición del vehículo',
    options=['Todas'] + sorted(car_data['condition'].dropna().unique())
)

# Filtro por año del modelo
selected_year = st.sidebar.selectbox(
    'Año del modelo',
    options=['Todos'] + sorted(car_data['model_year'].dropna().unique())
)

# Filtro por odómetro
max_km = st.sidebar.slider(
    'Máximo odómetro (km)',
    0,
    int(car_data['odometer'].max()),
    100000
)

# Checkboxes para visualizaciones
st.sidebar.header('Visualizaciones')
build_histogram = st.sidebar.checkbox('Histograma del odómetro')
build_scatter = st.sidebar.checkbox('Dispersión precio vs odómetro')
build_bar = st.sidebar.checkbox('Barras por tipo de coche')

# -------------------------------
# APLICAR FILTROS
# -------------------------------
filtered_data = car_data.copy()

if selected_condition != 'Todas':
    filtered_data = filtered_data[filtered_data['condition'] == selected_condition]

if selected_year != 'Todos':
    filtered_data = filtered_data[filtered_data['model_year'] == selected_year]

filtered_data = filtered_data[filtered_data['odometer'] <= max_km]

# -------------------------------
# MOSTRAR RESULTADOS FILTRADOS
# -------------------------------
st.subheader('Resultados filtrados:')
st.dataframe(filtered_data)

# -------------------------------
# VISUALIZACIONES
# -------------------------------
if build_histogram:
    st.subheader('Histograma del Odómetro')
    fig = go.Figure(data=[go.Histogram(x=filtered_data['odometer'])])
    fig.update_layout(title='Distribución del Odómetro')
    st.plotly_chart(fig, use_container_width=True)

if build_scatter:
    st.subheader('Dispersión Precio vs Odómetro')
    fig = go.Figure(data=[go.Scatter(
        x=filtered_data['odometer'],
        y=filtered_data['price'],
        mode='markers',
        marker=dict(color='green', opacity=0.5)
    )])
    fig.update_layout(
        title='Precio vs Odómetro',
        xaxis_title='Odómetro',
        yaxis_title='Precio'
    )
    st.plotly_chart(fig, use_container_width=True)

if build_bar:
    st.subheader('Cantidad de anuncios por tipo de coche')
    type_counts = filtered_data['type'].value_counts().reset_index()
    type_counts.columns = ['type', 'count']
    fig = px.bar(
        type_counts,
        x='type',
        y='count',
        labels={'type': 'Tipo de vehículo', 'count': 'Cantidad'},
        title='Cantidad de anuncios por tipo de coche'
    )
    st.plotly_chart(fig, use_container_width=True)

# -------------------------------
# ESTADÍSTICAS BÁSICAS
# -------------------------------
st.subheader('Estadísticas del conjunto de datos filtrado:')
st.write(f'Número total de anuncios: {len(filtered_data)}')
st.write(f'Precio medio: ${round(filtered_data["price"].mean(), 2)}')
st.write(f'Odómetro promedio: {round(filtered_data["odometer"].mean(), 2)} km')
