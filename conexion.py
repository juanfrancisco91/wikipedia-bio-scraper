# IMPORTACION DE LIBRERIAS PARA HACER LA PETICION A LA PAGINA
import requests
from bs4 import BeautifulSoup

# CREACION DE FUNCION PARA ESTABLECER CONEXION, RECIBIENDO LA URL DEL SITIO QUE DEBE SER DE WIKIPEDIA
# Y RECIBIENDO EL USER-AGENT QUE SE UTILIZARA
def conexion(url,user_agent):
    url = url
    cabecera = {
        "User-Agent": user_agent}
    path = requests.get(url, headers=cabecera)

    # CONDICIONAL PARA SABER CUANDO FALLE LA CONEXION
    if path.status_code == 200:
        soup = BeautifulSoup(path.text, 'html.parser')
        print(path.status_code)
        print('La Conexion a sido un Exito')
        return soup
    else:
        return print('Conexion Fallida')