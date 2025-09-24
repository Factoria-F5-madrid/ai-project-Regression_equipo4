import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime


# Configuración de la página
st.set_page_config(
    page_title="Buscador de Coches Usados",
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
st.title("🚗 Buscador de Coches Usados")
st.markdown("Encuentra el coche perfecto filtrando por marca, año y precio")

# --- INFORMACIÓN ADICIONAL ---
st.markdown("---")
st.subheader("ℹ️ Cómo usar esta aplicación")

st.markdown("""
1. **Selecciona una marca** en el menú desplegable
2. **Elige el rango de años** que te interesa
3. **Ajusta el precio máximo y mínimo** con el deslizador
4. **Usa los filtros adicionales** para refinar tu búsqueda
5. **Explora los resultados** en tabla o tarjetas
""")

# Datos de ejemplo (en un caso real, esto vendría de una base de datos)
@st.cache_data
def cargar_datos_ejemplo():
    """Carga datos de ejemplo de coches"""
    marcas = ['Toyota', 'Honda', 'Ford', 'BMW', 'Mercedes', 'Audi', 'Volkswagen', 'Nissan', 'Hyundai', 'Kia']
    modelos = {
        'Toyota': ['Corolla', 'Camry', 'RAV4', 'Prius', 'Highlander'],
        'Honda': ['Civic', 'Accord', 'CR-V', 'Pilot', 'HR-V'],
        'Ford': ['Focus', 'Fiesta', 'Mustang', 'Explorer', 'Escape'],
        'BMW': ['Serie 3', 'Serie 5', 'X3', 'X5', 'Serie 1'],
        'Mercedes': ['Clase A', 'Clase C', 'Clase E', 'GLC', 'GLE'],
        'Audi': ['A3', 'A4', 'A6', 'Q3', 'Q5'],
        'Volkswagen': ['Golf', 'Passat', 'Tiguan', 'Polo', 'T-Roc'],
        'Nissan': ['Qashqai', 'Juke', 'Leaf', 'X-Trail', 'Micra'],
        'Hyundai': ['Tucson', 'i30', 'Kona', 'Santa Fe', 'i20'],
        'Kia': ['Sportage', 'Ceed', 'Niro', 'Sorento', 'Picanto']
    }
    
    # Generar datos de ejemplo
    np.random.seed(42)
    datos = []
    
    for _ in range(1000):
        marca = np.random.choice(marcas)
        modelo = np.random.choice(modelos[marca])
        año = np.random.randint(2010, 2024)
        precio = np.random.randint(5000, 35000)
        kilometraje = np.random.randint(10000, 150000)
        combustible = np.random.choice(['Gasolina', 'Diésel', 'Híbrido', 'Eléctrico'])
        transmision = np.random.choice(['Manual', 'Automática'])
        
        datos.append({
            'marca': marca,
            'modelo': modelo,
            'año': año,
            'precio': precio,
            'kilometraje': kilometraje,
            'combustible': combustible,
            'transmision': transmision
        })
    
    return pd.DataFrame(datos)

# Cargar datos
df_coches = cargar_datos_ejemplo()

# --- SIDEBAR CON FILTROS ---
st.sidebar.header("🔍 Filtros de Búsqueda")

# 1. Selector de Marca
marcas_disponibles = ['Todas'] + sorted(df_coches['marca'].unique().tolist())
marca_seleccionada = st.sidebar.selectbox(
    "Selecciona la marca:",
    options=marcas_disponibles,
    index=0
)

# 2. Selector de Año (con rango)
st.sidebar.markdown("---")
año_minimo = int(df_coches['año'].min())
año_maximo = int(df_coches['año'].max())

año_seleccionado = st.sidebar.slider(
    "Selecciona el año:",
    min_value=año_minimo,
    max_value=año_maximo,
    value=(2018, 2023),  # Valor por defecto
    step=1
)

# 3. Barra de deslizamiento para Precio
st.sidebar.markdown("---")
precio_minimo = int(df_coches['precio'].min())
precio_maximo = int(df_coches['precio'].max())

precio_seleccionado = st.sidebar.slider(
    "Rango de precio (€):",
    min_value=precio_minimo,
    max_value=precio_maximo,
    value=(10000, 25000),  # Valor por defecto
    step=1000
)

# 4. Filtros adicionales (opcionales)
st.sidebar.markdown("---")
st.sidebar.subheader("🎛️ Filtros Adicionales")

# Combustible
combustibles = ['Todos'] + sorted(df_coches['combustible'].unique().tolist())
combustible_seleccionado = st.sidebar.selectbox(
    "Tipo de combustible:",
    options=combustibles,
    index=0
)

# Transmisión
transmisiones = ['Todas'] + sorted(df_coches['transmision'].unique().tolist())
transmision_seleccionada = st.sidebar.selectbox(
    "Transmisión:",
    options=transmisiones,
    index=0
)

# Kilometraje
kilometraje_maximo = st.sidebar.slider(
    "Kilometraje máximo:",
    min_value=0,
    max_value=200000,
    value=100000,
    step=10000
)

# --- APLICAR FILTROS ---
df_filtrado = df_coches.copy()

# Aplicar filtros
if marca_seleccionada != 'Todas':
    df_filtrado = df_filtrado[df_filtrado['marca'] == marca_seleccionada]

# Filtro de año
df_filtrado = df_filtrado[
    (df_filtrado['año'] >= año_seleccionado[0]) & 
    (df_filtrado['año'] <= año_seleccionado[1])
]

# Filtro de precio
df_filtrado = df_filtrado[
    (df_filtrado['precio'] >= precio_seleccionado[0]) & 
    (df_filtrado['precio'] <= precio_seleccionado[1])
]

# Filtros adicionales
if combustible_seleccionado != 'Todos':
    df_filtrado = df_filtrado[df_filtrado['combustible'] == combustible_seleccionado]

if transmision_seleccionada != 'Todas':
    df_filtrado = df_filtrado[df_filtrado['transmision'] == transmision_seleccionada]

# Filtro de kilometraje
df_filtrado = df_filtrado[df_filtrado['kilometraje'] <= kilometraje_maximo]

# --- MOSTRAR RESULTADOS ---
st.markdown("---")

# Métricas principales
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("Coches encontrados", len(df_filtrado))

with col2:
    if len(df_filtrado) > 0:
        precio_promedio = f"€{df_filtrado['precio'].mean():,.0f}"
    else:
        precio_promedio = "N/A"
    st.metric("Precio promedio", precio_promedio)

with col3:
    if len(df_filtrado) > 0:
        año_promedio = f"{df_filtrado['año'].mean():.0f}"
    else:
        año_promedio = "N/A"
    st.metric("Año promedio", año_promedio)

with col4:
    if len(df_filtrado) > 0:
        km_promedio = f"{df_filtrado['kilometraje'].mean():,.0f} km"
    else:
        km_promedio = "N/A"
    st.metric("Km promedio", km_promedio)

# Mostrar resultados
if len(df_filtrado) > 0:
    st.subheader(f"🎯 {len(df_filtrado)} coches encontrados")
    
    # Opciones de visualización
    vista = st.radio(
        "Tipo de vista:",
        ["Tabla"],
        horizontal=True
    )
    
    if vista == "Tabla":
        # Mostrar como tabla
        st.dataframe(
            df_filtrado.sort_values('precio'),
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
        # Mostrar como tarjetas con padding mejorado
        cols = st.columns(3)
        for idx, (_, coche) in enumerate(df_filtrado.iterrows()):
            with cols[idx % 3]:
                with st.container():
                    st.markdown(f"""
                    <div style='
                        border: 1px solid #ddd;
                        border-radius: 10px;
                        padding: 20px;
                        margin: 10px 0;
                        background-color: #f9f9f9;
                        display: flex;
                        flex-direction: column;
                        gap: 5px;
                    '>
                        <h4 style='margin-bottom: 0;'>🚗 {coche['marca']} {coche['modelo']}</h4>
                        <p style='margin: 0;'><strong>Año:</strong> {coche['año']}</p>
                        <p style='margin: 0;'><strong>Precio:</strong> €{coche['precio']:,}</p>
                        <p style='margin: 0;'><strong>Km:</strong> {coche['kilometraje']:,}</p>
                        <p style='margin: 0;'><strong>Combustible:</strong> {coche['combustible']}</p>
                        <p style='margin: 0;'><strong>Transmisión:</strong> {coche['transmision']}</p>
                    </div>
                    """, unsafe_allow_html=True)
    
    # Gráficos adicionales
    with st.expander("📊 Ver estadísticas y gráficos"):
        col1, col2 = st.columns(2)
        
        with col1:
            # Distribución de precios
            st.bar_chart(df_filtrado['precio'].value_counts().head(10))
            st.caption("Distribución de precios")
        
        with col2:
            # Marcas más populares
            st.bar_chart(df_filtrado['marca'].value_counts().head(5))
            st.caption("Marcas más comunes")
        
else:
    st.warning("⚠️ No se encontraron coches con los filtros seleccionados.")
    st.info("💡 Prueba a ampliar el rango de precio o año.")


# Footer
st.markdown("---")
st.caption("✨ Desarrollado con Streamlit | Datos de ejemplo generados automáticamente")

# --- SECCIÓN OCULTA PARA DESARROLLO ---
with st.expander("🔧 Información para desarrolladores"):
    st.write("**Datos del dataset:**")
    st.write(f"- Total de coches: {len(df_coches)}")
    st.write(f"- Marcas disponibles: {len(df_coches['marca'].unique())}")
    st.write(f"- Rango de años: {df_coches['año'].min()} - {df_coches['año'].max()}")
    st.write(f"- Rango de precios: €{df_coches['precio'].min():,} - €{df_coches['precio'].max():,}")
    
    if st.button("Mostrar datos crudos"):
        st.dataframe(df_coches.head(10))