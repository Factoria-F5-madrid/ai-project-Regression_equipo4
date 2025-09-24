import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime


# Configuración de la página
st.set_page_config(
    page_title="Predictor de precios de Coches Usados",
    page_icon="🚗",
    layout="wide"
)

# --- CSS personalizado para el sidebar y los sliders ---
st.markdown("""
<style>
/* Aumenta el ancho de la barra lateral y su padding */
.st-emotion-cache-1pxx5n7 {
    width: 350px !important;
    padding-left: 20px;
    padding-right: 20px;
}

/* Espacio entre los elementos de la barra lateral */
.st-emotion-cache-1pxx5n7 > div {
    margin-bottom: 20px;
}

/* Ajusta el espaciado interno del sidebar */
.st-emotion-cache-1pxx5n7 {
    padding-top: 2rem;
    padding-bottom: 2rem;
}

/* Ajusta el espaciado de los labels de los widgets */
label.st-emotion-cache-121bdns {
    margin-bottom: 0.5rem;
}

/* Aumenta el padding para los números del slider de precio y año */
.st-emotion-cache-1v41k89 { /* Este es un selector clave para el contenedor del slider */
    padding: 0 10px; 
}

/* Asegura que los valores de texto del slider no se corten */
.st-emotion-cache-14u4t2z {
    min-width: 50px;
    text-align: center;
}

/* Alinea los números del slider en la parte superior para evitar que se salgan */
.st-emotion-cache-1l09y6r {
    margin-top: 10px;
}

</style>
""", unsafe_allow_html=True)


# Título principal
st.title("🚗 Predictor de precios de Coches Usados")
st.markdown("Estima el precio de cualquier vehículo usado en función de sus características.")

# Cargar datos
df_coches = pd.read_csv('../datasets/predicted_prices_for_frontend.csv')

# --- SIDEBAR CON FILTROS ---
st.sidebar.header("🔍 Filtros de Búsqueda")

# 1. Selector de Marca
marcas_disponibles = ['Todas'] + sorted(df_coches['brand'].unique().tolist())
marca_seleccionada = st.sidebar.selectbox(
    "Escoge una marca:",
    options=marcas_disponibles,
    index=0
)

# 2. Selector de Año (con rango)
st.sidebar.markdown("---")
año_minimo = int(df_coches['age'].min())
año_maximo = int(df_coches['age'].max())

año_seleccionado = st.sidebar.slider(
    "Selecciona antigüedad del vehículo (en años):",
    min_value=año_minimo,
    max_value=año_maximo,
    value=(0, 51),  # Valor por defecto
    step=1
)

# 4. Filtros adicionales (opcionales)
st.sidebar.markdown("---")
st.sidebar.subheader("🎛️ Filtros Adicionales")

# Combustible
combustibles = ['Todos'] + sorted(df_coches['fuel_type'].unique().tolist())
combustible_seleccionado = st.sidebar.selectbox(
    "Tipo de combustible:",
    options=combustibles,
    index=0
)

# Transmisión
transmisiones = ['Todas'] + sorted(df_coches['transmission'].unique().tolist())
transmision_seleccionada = st.sidebar.selectbox(
    "Transmisión:",
    options=transmisiones,
    index=0
)

# Kilometraje
milage_minimo = int(df_coches['milage'].min())
milage_maximo = int(df_coches['milage'].max())
kilometraje_seleccionado = st.sidebar.slider(
    "Kilometraje:",
    min_value=milage_minimo,
    max_value=milage_maximo,
    value=(0, 500000),  # Valor por defecto
    step=10000
)

# --- APLICAR FILTROS ---
df_filtrado = df_coches.copy()

# Aplicar filtros
if marca_seleccionada != 'Todas':
    df_filtrado = df_filtrado[df_filtrado['brand'] == marca_seleccionada]

# Filtro de año
df_filtrado = df_filtrado[
    (df_filtrado['age'] >= año_seleccionado[0]) & 
    (df_filtrado['age'] <= año_seleccionado[1])
]

# Filtros adicionales
if combustible_seleccionado != 'Todos':
    df_filtrado = df_filtrado[df_filtrado['fuel_type'] == combustible_seleccionado]

if transmision_seleccionada != 'Todas':
    df_filtrado = df_filtrado[df_filtrado['transmission'] == transmision_seleccionada]

# Filtro de kilometraje
df_filtrado = df_filtrado[
    (df_filtrado['milage'] >= kilometraje_seleccionado[0]) &
    (df_filtrado['milage'] <= kilometraje_seleccionado[1])
]

# --- MOSTRAR RESULTADOS ---
st.markdown("---")

# Métricas principales
col = st.columns(1)[0]
with col:
    if len(df_filtrado) > 0:
        precio_promedio = f"€{df_filtrado['predicted_price'].mean():,.0f}"
    else:
        precio_promedio = "N/A"
    st.metric("Predicción de Precio promedio", precio_promedio)

# Mostrar resultados
if len(df_filtrado) > 0:
    
    # Mostrar como tabla
    st.subheader("Predicciones más específicas")
    columnas_ocultas = ['power_to_weight_ratio', 'Is_Luxury_Brand', 'Accident_Impact']
    columnas_a_mostrar = [col for col in df_filtrado.columns if col not in columnas_ocultas]
    st.dataframe(
        df_filtrado[columnas_a_mostrar].sort_values('predicted_price'),
        use_container_width=True,
        height=400
    )
    
    # Botón de descarga
    csv = df_filtrado.to_csv(index=False)
    st.download_button(
        label="📥 Descargar resultados CSV",
        data=csv,
        file_name=f"coches_filtrados_{datetime.now().strftime('%Y%m%d')}.csv",
        mime="text/csv"
    )
    
else:
    st.warning("⚠️ Rangos fuera del predictor!")
    st.info("💡 Prueba a cambiar los filtros")


# Footer
st.markdown("---")
st.caption("✨ Desarrollado con Streamlit | Datos de ejemplo generados automáticamente")

# --- SECCIÓN OCULTA PARA DESARROLLO ---
with st.expander("🔧 Información para desarrolladores"):
    st.write("**Datos del dataset:**")
    st.write(f"- Total de coches: {len(df_coches)}")
    st.write(f"- Marcas disponibles: {len(df_coches['brand'].unique())}")
    st.write(f"- Rango de antigüedad: {df_coches['age'].min()} - {df_coches['age'].max()}")
    st.write(f"- Rango de precios: €{df_coches['predicted_price'].min():,} - €{df_coches['predicted_price'].max():,}")
    
    if st.button("Mostrar datos crudos"):
        st.dataframe(df_coches.head(10))