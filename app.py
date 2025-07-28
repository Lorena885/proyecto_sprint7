import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px

# Encabezado principal de la app
st.header('Análisis de Anuncios de Venta de Coches en EE.UU.')

# Cargar los datos
car_data = pd.read_csv('vehicles_us.csv')

# Mostrar vista previa de los datos
st.write('Vista previa de los datos:')
st.dataframe(car_data.head())



# Casillas de verificación
build_histogram = st.checkbox('Mostrar histograma del odómetro')
build_scatter = st.checkbox('Mostrar dispersión precio vs odómetro')

if build_histogram:
    st.write('Creación de un histograma para el odómetro')
    fig = go.Figure(data=[go.Histogram(x=car_data['odometer'])])
    fig.update_layout(title='Distribución del Odómetro')
    st.plotly_chart(fig, use_container_width=True)

if build_scatter:
    st.write('Creación de un gráfico de dispersión para precio vs odómetro')
    fig = go.Figure(data=[go.Scatter(
        x=car_data['odometer'],
        y=car_data['price'],
        mode='markers',
        marker=dict(color='green', opacity=0.5)
    )])
    fig.update_layout(
        title='Precio vs Odómetro',
        xaxis_title='Odómetro',
        yaxis_title='Precio'
    )
    st.plotly_chart(fig, use_container_width=True)
    
    
    
# Filtros interactivos - Filtrar por condicion
# Menú desplegable para condición
selected_condition = st.selectbox(
    'Filtrar por condición',
    options=['Todas'] + sorted(car_data['condition'].dropna().unique())
)

# Menú desplegable para año del modelo
selected_year = st.selectbox(
    'Filtrar por año del modelo',
    options=['Todos'] + sorted(car_data['model_year'].dropna().unique())
)

# Aplicar filtros
filtered_data = car_data.copy()

if selected_condition != 'Todas':
    filtered_data = filtered_data[filtered_data['condition'] == selected_condition]

if selected_year != 'Todos':
    filtered_data = filtered_data[filtered_data['model_year'] == selected_year]

# Mostrar los datos filtrados
st.write('Resultados filtrados:')
st.dataframe(filtered_data)

    
    
# grafico de barras por tipo de carro
# Crear un DataFrame con los conteos por tipo
type_counts = car_data['type'].value_counts().reset_index()
type_counts.columns = ['type', 'count']  # Renombrar columnas para claridad

# Crear gráfico de barras
fig = px.bar(type_counts,
             x='type',
             y='count',
             labels={'type': 'Tipo de vehículo', 'count': 'Cantidad'},
             title='Cantidad de anuncios por tipo de coche')

st.plotly_chart(fig, use_container_width=True)

max_km = st.slider('Filtrar por máximo odómetro (km)', 0, int(car_data['odometer'].max()), 100000)
filtered_data = car_data[car_data['odometer'] <= max_km]
st.dataframe(filtered_data)


#Resumen de estaditicas basicas
st.write('Estadísticas del conjunto de datos:')
st.write(f'Número total de anuncios: {len(car_data)}')
st.write(f'Precio medio: ${round(car_data["price"].mean(), 2)}')
st.write(f'Odómetro promedio: {round(car_data["odometer"].mean(), 2)} km')




