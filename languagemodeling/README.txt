Corpus:
El corpus lo saque de http://www.lllf.uam.es/ESP/Corlec.html
basicamente son conversaciones en distintos ambientes y originalmente tiene
muchos archivos por carpeta, cada carpeta representa el ambiente de la
charla (por ej: Administrativas).
Yo junte todas las charlas en un solo archivo (corpus.txt) por problemas
con el PlaintextCorpusReader para leer multiples archivos :/

Modelo de n-gramas:
pass

Generación de Texto:

Unigramas:
    ['hogares', 'drama', 'Mikel', 'auge', 'tipificar', 'creativas', 'virado',
    'cóctel', 'parabrisas', 'parlamentarias', 'fuer', 'perderán', 'fijaban',
    'videntes', 'Abadi', 'sufre', 'lamentos', 'define', 'cerrando', 'incidirían',
    'reducidas', 'espectacular', 'Corto', 'ingenia', 'exportadora', 'prosa', 'Viviane',
    'nombraron', 'campeó', 'modernizarse', 'Hídrica', 'atenuar', 'cuele', 'revertir',
    'cuáles', 'afiliados', 'extraía', 'Rockboer', 'sorprendidos', 'baldío', 'favorito',
    'mosquito', 'parcialidad', 'equinoterapia', 'Seeber', 'altísimo', 'vitalidad', 'Colapsado',
    'anteproyecto', 'resolverlo', '334', 'involucrada', 'impreso', 'Presupuestarios', 'UEPC',
    'curso', 'idénticas', 'Azar', 'funcionando', 'inexorable', 'relativa', 'mayoritariamente',
    'molesto', 'venia', 'Calamuchitana', 'cunden', 'conozco', 'espacial', 'suena', 'lotes',
    'lesionado', 'Prematuro', 'catarata', '159', '0800', 'gamma', 'Britos', 'albergar',
    'estrépito', 'interpretamos', 'semen', 'imaginaron', 'Moyano', 'Vidal', 'acólitos', '2010',
    'zarpazo', 'transponen', 'recurrir', 'pontificado', 'exclusivamente', 'concejal', 'stands',
    'galpón', 'estudié', 'indocumentados', 'escuden', 'narrativas', 'Acosta', 'imponga']

Bigramas:
    ['un', 'discurso', 'insistiendo', 'una', 'cama', ',', 'repetimos', ',', 'místico', ',',
    'dejadle', 'a', 'llamarle', 'imbécil', 'no', 'se', 'funciona', 'muy', 'razonable']

    ['se', 'encienden', ',', 'predomina', 'la', 'opinión', 'pública']

    ['en', 'español', 'publicado', ',', 'intestino', 'irritable', ',', 'aguantando', 'bola',
    'vaya', 'recogiendo']

Trigramas:
    ['a', 'la', 'derecha', 'y', 'su', 'discurso', 'insistiendo', 'una', 'vez', 'más']

    [':', 'Déjale', ',', 'no', 'pediste', 'un', 'a', 'una', 'cosa', 'política', 'de', 'Íñigo',
    'Cavero', 'ha', 'tenido', 'intención', 'de', 'voto']

Cuatrigramas:
    ['se', 'ilustrar', 'eja', 'ríodos', 'convienen', 'necesite', 'vasallaje', 'pronunciamiento',
    'rgar', 'diferenciar', 'moderando', 'debiera', 'hojaldre', 'esclavitud', '325', 'modernizar',
    'evita', 'encontrasen', 'micrófonos', 'Estadística', 'gerente', 'micro', 'contemplado', 'prefabricadas',
    'áeme', 'Época', 'científicas', 'Comunidad', 'complico', 'alfabético', 'enfermedades', 'rgas', 'cortársela',
    'identificando', 'desembolsar', 'úblico', 'comportamos', 'experimentó', 'derrumba', 'urgentemente', 'plátano',
    'riodista', 'desapareciera', 'desempaquetar', 'neutralizaciones', 'sillita', 'aportarle', 'comprendemos',
    'mandéis', 'instalar', 'arrugas', 'negros', 'campamento', 'guarros', 'Sofia', 'dedicarle', 'bipolar', 'puerro',
    'tuercas', 'scientos', 'Opinas', 'marcial', 'reflejo', 'afecte', 'erpo', 'Mejía', 'Quién', 'contén', 'amoniaco',
    'estudiaba', 'ccon019a', 'prolegómenos', 'protocolarias', 'despues', 'Parroquia', 'encalado', 'cdeb001b',
    'lventa', 'define', 'máximos', 'dijimos', 'etiene', 'encontraron', 'estrés', 'nen', 'corpúsculo', 'Pone',
    'labor', 'aprende', 'genotipos', 'sentarnos', 'ofrecimiento', 'Brevemente', 'diciembre', 'julio', 'encauzada',
    'lapamiento', 'asientos', 'Existía']

Se puede ver que las oraciones que tienen mas sentido son las de los bigramas y trigramas, he generado muchas
oraciones con unigramas y cuatrigramas y son todas muy parecidas, bastante largas y sin sentido.


Evaluación de Modelos de Lenguaje:

Resultados Perplexity
n               |       1            |       2           |       3            |       4
AddOne          | 756.2122431514837  | 2315.836399041006 | 14550.806335145406 | 29730.972152043785
Interpolation   | 699.099521447562   | 327.193472545306  | 442.118093330896   | 443.48049425779266
Back-off        | 756.6594355395407  | inf               | inf                | inf


Suavizado por Back-Off con Discounting:

Tuve problemas con este punto, a pesar de que pasa todos los test y no veo claramente donde puede estar el problema,
algunas probabilidades condicionales me dan negativas, por eso la perplexity me da inf.
Lo parche devolviendo 10**-3 en los casos donde la probabilidad condicional me da negativa.
