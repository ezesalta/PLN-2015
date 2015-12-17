
Introducción
------------
Este sistema propone una forma fácil de conocer tu orientación partidaria de
manera imparcial ya que se basa solo en resultados de votaciones en la cámara
de diputados.
A través de una interfaz web donde solo tenes que responder algunas preguntas
para calcular el porcentaje de coincidencia con cada diputado y por lo tanto
con cada partido político.


Instalación y uso
-----------------
Este sistema es una instancia de IEPY, por lo tanto primero se deberá seguir las
instrucciones de instalación de IEPY (en las referencias), luego se deberán
realizar algunas modificaciones a la instalación de IEPY comentadas en detalle
mas abajo.

Para correr el sistema con los datos que estan cargados solo se debe iniciar el
servidor local de IEPY:

    python voting/bin/manage.py runserver

En un navegador ir a http://localhost:8000/webapp y seguir las instrucciones.


Corpus de datos
---------------
El sistema esta pensado para interpretar los documentos generados en la cámara
de diputados únicamente, estos son tablas que vienen en formato pdf (en las
referencias) se deben convertir a pdf utilizando pdftotext, luego buscar el
numero o números de expedientes de las leyes votadas en ese documento, en el
Boletín de Asuntos Tratados (en las referencias), copiar y agregarlas al final
del documento separadas con guiones (-).


Modificaciones de IEPY
----------------------
Se tuvo que editar la instalación de iepy para poder adaptarlo al sistema.
Detalle de modificaciones:

iepy/preprocess/pipeline.py
    Fue reportado como bug.

    Linea 41:
        BORRAR: docs = self.documents.get_documents_lacking_preprocess(runner.step)
        AGREGAR: docs = self.documents

iepy/preprocess/tokenize.py
    Bug corregido, se envio un pull request.

    Linea 23:
        BORRAR: def __init__(self, override=False, lang='en'):
        AGREGAR: def __init__(self, override=False, increment=False, lang='en'):
    Linea 30:
        AGREGAR DEBAJO: self.increment = increment


iepy/webui/webui/urls.py
    Se agrego la referencia a las urls del sistema

    Linea 9:
        AGREGAR DEBAJO: url(r'^webapp/', include('voting.webapp.urls', namespace='webapp')),


Referencias
-----------
http://iepy.machinalis.com/

https://github.com/ezesalta/PLN-2015/tree/practico4

http://www.diputados.gov.ar/secadmin/ds_electronicos/actas_votacion-portada.html

http://www.diputados.gov.ar/sesiones/bat.html
