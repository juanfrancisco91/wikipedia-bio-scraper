import pandas as pd
from conexion import conexion
import os

listas_urls = []
entrada = '917110'
i = 0
# Bucle para recibir todas las urls, si es 0 se acabo
while entrada != '0':
    entrada = input(f'Ingrese la Url (Presiona el "0" Finalizar): ')
    # Condicional para evaluar si la entrada empieza con el protocolo https o http.
    if not entrada.startswith(('http:', 'https:')):
        print('No es una url (Necesita https o http)')
    else:
        if '0' in entrada:
            continue
        else:
            i += 1
            listas_urls.append(entrada)
            print(f'Numero de Urls ({i})')
# IGNORAR URLS DE PRUEBA -------------------------------------------------------------
'''listas_urls = ['https://es.wikipedia.org/wiki/Jesse_Helms',
               'https://es.wikipedia.org/wiki/Charles_Bukowski',
               'https://es.wikipedia.org/wiki/Giovanni_Battista_Lombardi',
               'https://es.wikipedia.org/wiki/Igal_Al%C3%B3n',
               'https://es.wikipedia.org/wiki/Jorge_Montenegro_(escritor)']'''
# IGNORAR URLS DE PRUEBA -------------------------------------------------------------

# CONDICIONAL PARA VERIFICAR QUE SISTEMA OPERATIVO POSEE EL USUARIO Y ASI PODER COLOCARLE SU USER-AGENT RESPECTIVO
system_os = os.uname().sysname
if system_os == 'Linux':
    agente = 'Mozilla/5.0 (X11; Linux x86_64; rv:60.0) Gecko/20100101 Firefox/81.0'
elif system_os == 'Mac':
    agente = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36'
elif system_os == 'Windows':
    agente = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:124.0) Gecko/20100101 Firefox/124.0.'

lista_dict = [] # LISTA PARA GUARDAR EL DICCIONARIO
# BUCLE PARA ITERAR SOBRE LA LISTAS DE URLS
if listas_urls:
    for i in listas_urls:

        dict_values = {}

        # LLAMADA A LA LIBRERIA CONEXION QUE CREAMOS Y A LA FUNCION conexion
        # PARA PASARLE POR PARAMETROS CADA URL Y EL REPECTIVO AGENTE A UTILIZAR
        soup = conexion(i, agente)

        # LE PONEMOS EL TITULO A CADA PAGINA QUE LLEVE
        dict_values['Titulo'] = soup.title.string

        # BUSCAMOS DENTRO DEL TBODY QUE ES DONDE SE ALMACENAN LOS DATOS QUE NOS INTERESAN
        # EN ESTE CASO LOS tr QUE A SU VEZ LLEVAN DENTRO LOS th y td QUE SON LOS QUE GUARDAN LA INFORMACION
        # th SIENDO LA QUE CONTIENE  'titulos' Y td EL CUERPO QUE ESTAMOS BUSCADO
        # th = Nacimiento
        # th = 18 de Julio
        for z in soup.tbody.find_all('tr'):
            th = z.find('th')
            td = z.find('td')

            # DECLARAMOS UNA BUSQUEDA SEPARADA PARA SABER SI ESTAS APARECEN AMBAS EN LA ETIQUETA
            # DE NO SER ASI INDICAMOS QUE NO CONTIENE ATRIBUTOS Y PASAMOS AL SIGUIENTE tr

            # SI LOS CONTIENEN PASAMOS A UN CONDICIONAL QUE NOS APARTA LOS DATOS QUE QUEREMOS ENCONTRAR,
            # NACIMIENTO, FALLECIMIENTO, CAUSA DE MUERTE
            if th is not None and td is not None:
                if 'Nacimiento' in th.text:
                    dict_values['Nacimiento'] = td.text.strip()

                elif 'Fallecimiento' in th.text:
                    dict_values['Fallecimiento'] = td.text.strip()

                elif 'Causa de muerte' in th.text:
                    dict_values['Causa de muerte'] = td.text.strip()
            else:
                print('No contiene el atributo td y th')
        # AGREGAMOS EL DICCIONARIO A UNA LISTA
        lista_dict.append(dict_values)

    # CONVERTIMOS A UN DATA FRAME CON PANDAS
    df = pd.DataFrame(lista_dict)

    # EXPORTAMOS EL ARCHIVO PARA SU MANIPULACION
    df.to_csv('_urls.csv', index=False)
    print(f'{10*'*'} ARCHIVO CREADO {10*'*'}')

else:
    print(f'{10*'x'} LISTA DE URLS VACIAS {10*'x'}')