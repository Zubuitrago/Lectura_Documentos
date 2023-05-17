import time
import pandas as pd
import numpy as np
import streamlit as st
import os
import base64
import Funciones
from PIL import Image

st.set_page_config(
    page_title="Herramienta de Documentos Regulatorios OXXO.",
    page_icon="🧊",
    layout="wide"
)

css = """
<style>
    iframe {
        border: 0px;
        padding: 0px;
    }
</style>
"""

# Agrega el CSS personalizado al cuerpo de la página
st.markdown(css, unsafe_allow_html=True)

def estilo_verde(val):
    color = '#55efc4'
    return f'background-color: {color}'

def pagina_1():
    # Leer la imagen como bytes
    with open('Banner.png', 'rb') as f:
        image_bytes = f.read()

    # Convertir la imagen a base64
    image_base64 = base64.b64encode(image_bytes).decode()


    # Título justificado
    st.markdown(
        """
        <h1 style="white-space: nowrap; overflow: hidden; text-overflow: ellipsis; font-size: 33px;">Herramienta De Identificación Automática De Fechas</h1>
        """,
        unsafe_allow_html=True
    )

    # Crear columnas para centrar la imagen
    col1, col2, col3 = st.columns([1, 2, 1])

    # Centrar la imagen en la columna central
    with col2:
        st.markdown(
            f'<div style="display: flex; justify-content: center;"><img src="data:image/png;base64,{image_base64}" style="width:100%;"></div>',
            unsafe_allow_html=True
        )


    #st.title('Herramienta de identificación automática de fechas.')
    #st.image('Banner.png', width=650)
    st.markdown('')
    st.markdown('#### Objetivo')
    st.write(
        """
        El objetivo de esta herramienta es simplificar y mejorar la gestión de los documentos reglamentarios necesarios para el funcionamiento de tiendas, brindando una visión clara de las fechas de vencimiento y ayudando a garantizar el cumplimiento de los requisitos legales de manera oportuna y eficiente.
        """, font_size=5
    )
dataframe = pd.read_excel('./data/Documentos regulatorios.xlsx', dtype=str)
print(dataframe.head())

# Inicializar el DataFrame global
if 'seleccion_dataframe' not in st.session_state:
    st.session_state.seleccion_dataframe = pd.DataFrame()  # DataFrame vacío inicial
if 'seleccion_dataframe_transpuesto' not in st.session_state:
    st.session_state.seleccion_dataframe_transpuesto = pd.DataFrame()  # DataFrame vacío inicial    
    
# Inicializar variables globales
if 'option_Zona' not in st.session_state:
    st.session_state.option_Zona = "A"
if 'option_Region' not in st.session_state:
    st.session_state.option_Region = "1"
if 'option_Plaza' not in st.session_state:
    st.session_state.option_Plaza = "I"
if 'option_Tienda' not in st.session_state:
    st.session_state.option_Tienda = "1A"
if 'selected_options' not in st.session_state:
    st.session_state['selected_options'] = {
    'option_Zona':  st.session_state.option_Zona ,
    'option_Region': st.session_state.option_Region ,
    'option_Plaza': st.session_state.option_Plaza ,
    'option_Tienda':st.session_state.option_Tienda 
} 
if 'path_tienda' not in st.session_state:
    st.session_state.path_tienda = None  # DataFrame vacío inicial
if "Documentos" not in st.session_state:
    st.session_state.Documentos = []
def pagina_2():
    st.title('Maestro de Documentos Regulatorios')
    st.markdown('#### Documentos Regulatorios')

    if len(dataframe) > 0:
        df_estilo = dataframe.style.applymap(estilo_verde)
        st.markdown(dataframe.head(3).style.hide(axis="index").to_html(), unsafe_allow_html=True)

    else:
        st.markdown(dataframe.head(3).style.hide(axis="index").to_html(), unsafe_allow_html=True)
    st.markdown('***')

    st.markdown('#### Seleccione  Zona, Región, Plaza y Tienda del documento')
##############################################
    # Seleccionar ZONA#
    zona_options = sorted(dataframe['Zona'].unique())

    col1, col2,col3,col4 = st.columns([1.3,1.3,1,1.3])
    with col1:
            st.session_state.option_Zona = st.radio('Seleccione la Zona', zona_options, key='zona',horizontal=True)
            # Set the font size using CSS
    with col2:
            if st.session_state.option_Zona is not None:
                region_options = sorted(dataframe[dataframe['Zona'] == st.session_state.option_Zona]['Region'].unique())
                st.session_state.option_Region = st.radio("Seleccione la Región", region_options, key='region',horizontal=True)
    with col3:
             # Seleccionar Plaza#
            if st.session_state.option_Region is not None:
                plaza_options = sorted(dataframe[(dataframe['Zona'] == st.session_state.option_Zona) &
                                                (dataframe['Region'] == st.session_state.option_Region)]['Plaza'].unique())
                st.session_state.option_Plaza = st.radio("Seleccione la Plaza", plaza_options, key='plaza',horizontal=True)
    with col4:
            # Seleccionar Tienda#
            tienda_options = ("1A", "2B", "3C")
            st.session_state.option_Tienda = st.radio("Seleccione la Tienda", tienda_options, key='tienda',horizontal=True)
    


    # Guardar las variables seleccionadas en el estado global
    st.session_state['selected_options'] = {
        'option_Zona':  st.session_state.option_Zona ,
        'option_Region': st.session_state.option_Region ,
        'option_Plaza': st.session_state.option_Plaza ,
        'option_Tienda':st.session_state.option_Tienda 
    }
    st.session_state.seleccion_dataframe=dataframe[(dataframe['Zona'] == st.session_state.option_Zona) &
                                        (dataframe['Region'] == st.session_state.option_Region)]

################################################

    if st.session_state.option_Zona is not None and st.session_state.option_Region is not None and st.session_state.option_Tienda is not None and st.session_state.option_Plaza is not None :
        # Agrega un widget de file_uploader a tu aplicación Streamlit
        st.session_state.path_tienda = st.file_uploader("Selecciones los PDF analizar", type="pdf", accept_multiple_files=True)
        # Verifica si se cargó un archivo
        if st.session_state.path_tienda is not None:
            archivos = [archivo.name for archivo in st.session_state.path_tienda]
            st.session_state.Documentos = [elemento.split('.')[0] for elemento in archivos]
            st.session_state.seleccion_dataframe['Documento cargado']=np.where(st.session_state.seleccion_dataframe["Permiso"].isin(st.session_state.Documentos),"Si","No")
            st.header("Documentos a analizar")
            print(st.session_state.seleccion_dataframe)
            st.markdown(st.session_state.seleccion_dataframe.style.hide(axis="index").to_html(), unsafe_allow_html=True)

            st.markdown('***')

    else:
        st.session_state.path_tienda = None
        st.write("Selecciones todas las opciones que corresponde a la tienda")

def pagina_3():
    selected_options = st.session_state['selected_options']
    option_Zona = selected_options['option_Zona']
    option_Region = selected_options['option_Region']
    option_Plaza = selected_options['option_Plaza']
    option_Tienda = selected_options['option_Tienda']
    seleccion_dataframe=st.session_state.seleccion_dataframe.reset_index()
    seleccion_dataframe["Vigencia"]=None
    seleccion_dataframe["Contexto"]=None
    path_tienda=st.session_state.path_tienda 
    Documentos=st.session_state.Documentos
    print(st.session_state.seleccion_dataframe)
    # dashboard title
    st.title("Resultado de análisis de documentos")
    # Definir opciones

    col1, col2, col3,col4  = st.columns([0.5,0.5,0.5,0.5])

    # Set the content for each column
    content1 = f"Zona: {option_Zona}"
    content2 = f"Región: {option_Region}"
    content3 = f"Plaza: {option_Plaza}"
    content4 = f"Tienda: {option_Tienda}"

    # Apply CSS styling to center-align the content in each column
    style = """
        <style>
            .column-content {
                display: flex;
                flex-direction: column;
                align-items: center;
                font-size: 22px;
                font-weight: bold;
            }
        </style>
    """
    st.markdown(style, unsafe_allow_html=True)

    # Display the content in each column
    col1.markdown(f"<div class='column-content'>{content1}</div>", unsafe_allow_html=True)
    col2.markdown(f"<div class='column-content'>{content2}</div>", unsafe_allow_html=True)
    col3.markdown(f"<div class='column-content'>{content3}</div>", unsafe_allow_html=True)
    col4.markdown(f"<div class='column-content'>{content4}</div>", unsafe_allow_html=True)

    # Define the legend with circles
    legend = "<div style='display:flex; align-items:center;'>" \
            "<div style='background-color:#f8a359; width:15px; height:15px; border-radius:50%;'></div>" \
            "<p style='margin:0 5px;'>Caduco</p>" \
            "<div style='background-color:#fde686; width:15px; height:15px; border-radius:50%;'></div>" \
            "<p style='margin:0 5px;'>Por Caducar</p>" \
            "<div style='background-color:#94eba9; width:15px; height:15px; border-radius:50%;'></div>" \
            "<p style='margin:0 5px;'>Vigente</p>" \
            "</div>"

    # Render the legend in Streamlit
    st.markdown(legend, unsafe_allow_html=True)
    st.markdown('')

   # Create a sample DataFrame
    data = {
        "Permiso": ["Permiso de uso de suelo", "Registro de marca y derechos de autor"],
        "Documento cargado": ["Sí", "Sí"],
        "Contexto": ["Constancia de Alimentos y Numero Oficial Comercial", "Acuse de movimientos de actualización de sitiación"],
        "Vigencia": ['02 DE MAYO 2019', '29/11/2022'],
        "Estatus": ["Caduco", "Vigente"]
    }

    df = pd.DataFrame(data)

    # Apply conditional formatting to the DataFrame
    def highlight_status(row):
        estatus = row['Estatus']
        background_color = ''
        if estatus == 'Caduco':
            background_color = '#f8a359'
        elif estatus == 'Por Caducar':
            background_color = '#fde686'
        elif estatus == 'Vigente':
            background_color = '#27ae60'
        
        return ['background-color: ' + background_color] * len(row)

    styled_df = df.style.apply(highlight_status, axis=1)

    # Apply CSS styling to align values to center
    styled_df = styled_df.set_table_styles([
        {"selector": "td", "props": [("text-align", "center")]}
    ])

    # Display the styled DataFrame in Streamlit
    #st.markdown(styled_df,unsafe_allow_html=True)
    col1, col2,col3 = st.columns([0.2,3,0.2])
    with col1:
        st.markdown('')
    with col2:
        st.markdown(styled_df.hide(axis="index").to_html(), unsafe_allow_html=True)
    with col3:
        st.markdown('')

    

st.markdown(
                        """
                    <style>
                    [data-testid="stSidebar"][aria-expanded="true"]{
                        min-width: 260px;
                        max-width: 270px;
                    }
                    """,
                        unsafe_allow_html=True,
                    )
imageLogoS = Image.open('img/LogoSimple.png')
st.sidebar.image(imageLogoS,width=10,use_column_width = 'auto')
st.sidebar.title('Menú')
if st.sidebar.button('Introducción', key='pagina1', use_container_width=True):
    st.experimental_set_query_params(pagina='1')
if st.sidebar.button('Cargar datos', key='pagina2', use_container_width=True):
    st.experimental_set_query_params(pagina='2')
if st.sidebar.button('Proceso de Lectura automática', key='pagina3', use_container_width=True):
    st.experimental_set_query_params(pagina='3')




pagina_actual = st.experimental_get_query_params().get("pagina", "1")

if pagina_actual[0] == '1':
    pagina_1()
elif pagina_actual[0] == '2':
    pagina_2()
elif pagina_actual[0] == '3':
    pagina_3()
