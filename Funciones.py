import pytesseract as tess
tess.pytesseract.tesseract_cmd=r"C:\Users\zuly.buitrago\AppData\Local\Programs\Tesseract-OCR\tesseract.exe"

import re
import cv2
import numpy as np
import pytesseract
from pdf2image import convert_from_path
import streamlit as st
import tempfile
import os

# Transformación del archivo en texto
def obtener_texto_fecha(file):
    # Guardar temporalmente el archivo en el sistema de archivos local
    with tempfile.NamedTemporaryFile(delete=False) as tmp_file:
        tmp_file.write(file.read())
        tmp_path = tmp_file.name

    pages = convert_from_path(tmp_path, 500) # 500 dpi
    img = np.array(pages[0])[:, :, ::-1]  # Convertir PIL.Image a ndarray de OpenCV

    # Aplica técnicas de procesamiento de imágenes para detectar la fecha
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)  # Convierte la imagen a escala de grises
    gray = cv2.medianBlur(gray, 3)  # Aplica un filtro de mediana para reducir el ruido
    edges = cv2.Canny(gray, 50, 150, apertureSize=3)  # Detecta los bordes de la imagen
    lines = cv2.HoughLines(edges, 1, np.pi / 180, 200)  # Detecta las líneas en la imagen
    for rho, theta in lines[0]:
        a = np.cos(theta)
        b = np.sin(theta)
        x0 = a * rho
        y0 = b * rho
        x1 = int(x0 + 1000 * (-b))
        y1 = int(y0 + 1000 * (a))
        x2 = int(x0 - 1000 * (-b))
        y2 = int(y0 - 1000 * (a))
        cv2.line(gray, (x1, y1), (x2, y2), (0, 0, 255), 2)  # Dibuja las líneas detectadas en la imagen

    # Extrae la fecha de la imagen utilizando OCR (reconocimiento óptico de caracteres)
    #text = pytesseract.image_to_string(gray, lang='eng', config='--psm 11').lower()
    text =pytesseract.image_to_string(gray, lang="eng").lower()
    # Eliminar el archivo temporal
    os.remove(tmp_path)
    # Imprime la fecha extraída
    return text
# Asunto del documento
palabras_clave_asunto = ['constancia', 'acuse de movimiento']


def obtener_asunto_imagen(texto):
    contexto=[]
    # Buscar la palabra clave en el texto
    for key in palabras_clave_asunto:
        inicio = texto.find(key)
        if inicio != -1:
            # Obtener el contexto de la palabra clave
            #contexto = texto[inicio:inicio + len(palabra_clave) + 20]  # Se obtienen 20 caracteres después de la palabra clave
            # Obtener el contexto de la palabra clave hasta el siguiente salto de línea
            fin = texto.find('\n', inicio)
            resultado= texto[inicio:fin].strip()
            contexto.append(resultado)
    return contexto
## Formatos de fecha 

expresiones_regulares = [
    r'\d{1,2}/\d{1,2}/\d{4}',        # Formato dd/mm/aaaa
    r'\d{1,2}-\d{1,2}-\d{4}',        # Formato dd-mm-aaaa
    r'\d{4}/\d{1,2}/\d{1,2}',        # Formato aaaa/mm/dd
    r'\d{1,2}\s+de\s+\w+\s+de\s+\d{4}',    # Formato dd de mes de aaaa
    r'\d{1,2}\s+de\s+\w+\s+\d{4}', # Formato dd de mes  aaaa
    r'\w+\s+\d{1,2},\s+\d{4}'         # Formato mes dd, aaaa
]

palabras_clave=['vencimiento','fecha del aviso']
def buscar_fechas_palabras_clave(texto):    
    fechas_encontradas = []
    
    for palabra in palabras_clave:
        inicio = texto.find(palabra)
        if inicio != -1:
            for expresion in expresiones_regulares:
                #coincidencias = re.findall(expresion_regular + r'.*' + expresion + r'.*' + expresion_regular, texto, re.IGNORECASE)
                coincidencias = texto[inicio:inicio + len(palabra) + 100]  # Se obtienen 20 caracteres después de la palabra clave
                #print('coincidencia*-*-',coincidencias)
                coincidencia=re.findall(expresion,coincidencias)
                fechas_encontradas.extend(coincidencia)
    
    return fechas_encontradas

