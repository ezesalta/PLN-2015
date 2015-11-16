Corpus
------
El corpus lo saque de http://www.lllf.uam.es/ESP/Corlec.html
básicamente son conversaciones en distintos ambientes y originalmente tiene
muchos archivos por carpeta, cada carpeta representa el ambiente de la
charla (por ej: Administrativas).
Yo junte todas las charlas en un solo archivo (corpus.txt) por problemas
con el PlaintextCorpusReader para leer multiples archivos :/



Generación de Texto
-------------------

Unigramas
---------
    ngram:
        1: 'sabedor constitucionales impuestos esfuercen planetas hacerme ignorantes
           Definimos colgar ponte servidor somatiza reivindicaré idénticos teléfono'
    addone:
        1: 'recordaré locos magníficos restituírsela rescatarse fantásticas R mojé
            convergencia Demuestra ELE Juego aprobado Paseo asociales'
    interpolated:
        1: 'produciría Ecce prestadas Fraguas tubería influido Kea laurel Fanta
            ingresarlas actas mira deseaban Barragán fumadora'
    backoff:
        1: 'ganancia astronautas sincera renueven plasma galerías Toros biscuit
            dale pulsando meneadas Morton Véndelas navajita Gandía'

Bigramas
--------
    ngram:
        1: 'Atención , orientales ... estable ... allí le haya sucedido es'
    addone:
        1: 'Llamen ustedes los caballeros y efectivamente cuando se vayan
            creciendo etcétera etcétera y lleguen a'
    interpolated:
        1: 'Todas las dimensiones de tomar las chicas ... vigente todavía
            te iba con pesetas'
    backoff:
        1: 'Acaba el tiempo ya les diré lo que pasa un besito , Sálix alba ,'

Trigramas
---------
    ngram:
        1: 'Pues a. . . recibirte al aeropuerto , se formó ese comité , luego cayó'
    addone:
        1: 'Sí hombre Sí , está enterrado en la realidad , no libré ningún domingo ,'
    interpolated:
        1: 'Presión extenuante de los presupuestos que ,'
    backoff:
        1: 'Incapaz de beber de una ocasión me dijo , pero inevitablemente'

Cuatrigramas
------------
    ngram:
        1: 'Pero no ha requerido aquí previamente al representante legal ?'
    addone:
        1: 'Es testigo de crear maraña , directa o indirectamente , Almudena
            ha dicho que es'
    interpolated:
        1: 'cuando la veías en el cine ese de Juan Bravo , no'
        2: 'Veintitantas le ha costado , en el caso que yo tengo visto es eh ...'
    backoff:
        1: 'es imposible , si nadie me filmó en vídeo , nunca'
        2: 'no puedo , éticamente , no me lo han dicho ya'
        3: 'Gran fábrica de muebles " Franmobel "'
        4: 'Venían de Madrid . Y digo pero porqué va a tenerlo ?'


Se puede ver una evidente mejora en las oraciones generadas a medida que
incrementa el N, las oraciones más interesantes fueron conseguidas con el modelo
backoff con N=4.


Evaluación de Modelos de Lenguaje
---------------------------------

Resultados Perplexity
---------------------
n                1         2          3           4
AddOne           778.04    2368.47    16453.33    32007.21
Interpolation    777.79    373.61     519.19      483.34
Back-off         777.79    287.37     272.12      266.60

