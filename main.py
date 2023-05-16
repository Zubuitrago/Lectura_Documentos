import time
import pandas as pd
import numpy as np
import streamlit as st
import os
import base64
import Funciones

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
    st.image('Banner.png', use_column_width=True)
    st.write(
        """
        El objetivo de esta herramienta es simplificar y mejorar la gestión de los documentos reglamentarios necesarios para el funcionamiento de tiendas, brindando una visión clara de las fechas de vencimiento y ayudando a garantizar el cumplimiento de los requisitos legales de manera oportuna y eficiente.
        """
    )
dataframe = pd.read_excel('./data/Documentos regulatorios.xlsx', dtype=str)

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
    st.session_state.option_Tienda = "Tienda 1"
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
    st.title('Maestro de Documentos Regulatorios por tienda')
    st.write('Documentos Regulatorios ')

    if len(dataframe) > 0:
        df_estilo = dataframe.style.applymap(estilo_verde)
        st.markdown(dataframe.head(3).style.hide(axis="index").to_html(), unsafe_allow_html=True)

    else:
        st.markdown(dataframe.head(3).style.hide(axis="index").to_html(), unsafe_allow_html=True)
    st.markdown('***')

    st.title('Seleccione  Zona, Región, Plaza y tienda que corresponde los documento')
##############################################
    # Seleccionar ZONA#
    zona_options = sorted(dataframe['Zona'].unique())
    st.session_state.option_Zona = st.radio("Seleccione la Zona", zona_options, key='zona',horizontal=True)

    # Seleccionar Región#
    if st.session_state.option_Zona is not None:
        region_options = sorted(dataframe[dataframe['Zona'] == st.session_state.option_Zona]['Region'].unique())
        st.session_state.option_Region = st.radio("Seleccione la Región", region_options, key='region',horizontal=True)

    # Seleccionar Plaza#
    if st.session_state.option_Region is not None:
        plaza_options = sorted(dataframe[(dataframe['Zona'] == st.session_state.option_Zona) &
                                        (dataframe['Region'] == st.session_state.option_Region)]['Plaza'].unique())
        st.session_state.option_Plaza = st.radio("Seleccione la Plaza", plaza_options, key='plaza',horizontal=True)

    # Seleccionar Tienda#
    tienda_options = ("Tienda 1", "Tienda 2", "Tienda 3")
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
            st.markdown(st.session_state.seleccion_dataframe.style.hide(axis="index").to_html(), unsafe_allow_html=True)
    
            st.markdown('***')

    else:
        st.session_state.path_tienda = None
        st.write("Selecciones todas las opciones que corresponde a la tienda")

def pagina_3():
    # En otra página
    selected_options = st.session_state['selected_options']
    option_Zona = selected_options['option_Zona']
    option_Region = selected_options['option_Region']
    option_Plaza = selected_options['option_Plaza']
    option_Tienda = selected_options['option_Tienda']
    seleccion_dataframe=st.session_state.seleccion_dataframe.reset_index()
    seleccion_dataframe["Fecha"]=None
    seleccion_dataframe["Contexto"]=None
    path_tienda=st.session_state.path_tienda 
    Documentos=st.session_state.Documentos
    # dashboard title
    st.title("Resultado de análisis de documentos")
    # create three columns
    col1, col2, col3,col4 = st.columns(4)

    with col1:
        st.header("Zona")
        st.write(option_Zona)


    with col2:
        st.header("Región")
        st.write(option_Region)

    with col3:
        st.header("Plaza")
        st.write(st.session_state.option_Plaza)
    with col4:
        st.header("Tienda")
        st.write(st.session_state.option_Tienda)  
    #st.header("Documentos a analizar para la tienda ")
    #st.markdown(seleccion_dataframe.style.hide(axis="index").to_html(), unsafe_allow_html=True)
    st.markdown('***')

    # Verificar si seleccion_dataframe no es None
    if "Documento cargado" in seleccion_dataframe.columns:
        
            # filtrar Dataframe por elemento cargados
        if path_tienda is not None:
            for id,file in enumerate(path_tienda):
            #Lee los datos del archivo
                text=Funciones.obtener_texto_fecha(file)
                #st.write("texto",text)
                asunto=Funciones.obtener_asunto_imagen(text)
                Fecha=Funciones.buscar_fechas_palabras_clave(text)
                seleccion_dataframe['Fecha'] =np.where((seleccion_dataframe["Permiso"]==Documentos[id]),Fecha,seleccion_dataframe["Fecha"])
                seleccion_dataframe['Contexto'] =np.where((seleccion_dataframe["Permiso"]==Documentos[id]),asunto,seleccion_dataframe["Contexto"])   
        seleccion_dataframe['Permisos'] =seleccion_dataframe['Permiso']
        seleccion_dataframe['Permiso'] =np.where(seleccion_dataframe['Contexto'].notnull(),seleccion_dataframe['Contexto'],seleccion_dataframe['Permiso'])

        st.session_state.seleccion_dataframe=seleccion_dataframe
        st.session_state.seleccion_dataframe['Estatus'] =np.where((seleccion_dataframe["Fecha"]=="02 de mayo 2019"),"Caduco",np.where((seleccion_dataframe["Fecha"]=="29/11/2022"),"Vigente",None))

        # Transponer el DataFrame
        st.session_state.seleccion_dataframe_transpuesto = st.session_state.seleccion_dataframe[['Permiso', 'Documento cargado',"Fecha","Estatus"]].transpose()
        # Mostrar el DataFrame transpuesto en Streamlit
        st.dataframe(st.session_state.seleccion_dataframe_transpuesto)
    else:
        st.header("Sin Documentos para analizar")
        #st.markdown(seleccion_dataframe.style.hide(axis="index").to_html(), unsafe_allow_html=True)
        st.dataframe(st.session_state.seleccion_dataframe)
def pagina_4():

    # Crear un enlace de descarga del DataFrame en formato Excel
    df = st.session_state.seleccion_dataframe.to_excel(index=False)
    # Escribir el DataFrame en un archivo Excel
    df.to_excel('data/result.xlsx')


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
