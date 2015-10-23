STATS
-----

sents: 17379
occ words: 517268
words: 46482
tags: 48

#   tag     frec        % total     most freccuent words for tag
1   nc      92002       0.18        ['años', 'presidente', 'millones', 'equipo', 'partido']
2   sp      79904       0.15        ['de', 'en', 'a', 'del', 'con']
3   da      54552       0.11        ['la', 'el', 'los', 'las', 'El']
4   vm      50609       0.10        ['está', 'tiene', 'dijo', 'puede', 'hace']
5   aq      33904       0.07        ['pasado', 'gran', 'mayor', 'nuevo', 'próximo']
6   fc      30148       0.06        [',']
7   np      29113       0.06        ['Gobierno', 'España', 'PP', 'Barcelona', 'Madrid']
8   fp      21157       0.04        ['.', '(', ')']
9   rg      15333       0.03        ['más', 'hoy', 'también', 'ayer', 'ya']
10  cc      15023       0.03        ['y', 'pero', 'o', 'Pero', 'e']

Descripción:
nc: Nombre Común                Ej: gato, chico
sp: Adposición Preposicion      Ej: al, del
da: Determinante Articulo       Ej: el, los, las
vm: Verbo Principal.            Ej: cantar, ser
aq: Adjetivo Calificativo       Ej: alegre, malo
fc: Puntuacion Coma.            Ej: ,
np: Nombre Propio.              Ej: Pedro, Juan
fp: Puntuacion Punto.           Ej: .
rg: Advervio General.           Ej: despacio, ahora
cc: Conjuncion Coordinada.      Ej: mas, pero

                Frec    %Total
Unambiguous:    44109   94.89%
Ambiguous 2-9:  2373    5.11%
        1 tags: 2194    4.72%
        2 tags: 153     0.33%
        3 tags: 19      0.04%
        4 tags: 4       0.01%
        5 tags: 3       0.01%

5 most freccuent words:
#       Word    Frec    %Total
1       ,       30148   64.86%
2       de      28478   61.27%
3       la      18100   38.94%
4       .       17520   37.69%
5       que     15391   33.11%


Time lapsed: 21.31s
--------------------------------------------------------------------------------


Cuando evalue MEMM con MultinomialNB tardo mucho en terminar y ademas
dio valores muy por debajo del baseline. Los demas valores obtenidos estan
dentro de lo esperado.

BASELINE
--------
Accuracy:           89.04%
Accuracy known:     95.35%
Accuracy unknown:   31.80%
Time:               5.00s
---------------------------------------------------------------

MLHMM
-----
N                   1           2           3           4
Accuracy:           89.01%      92.72%      93.06%      92.98%
Accuracy known:     95.32%      97.61%      97.61%      97.37%
Accuracy unknown:   31.80%      48.42%      51.78%      53.15%
Time:               20.21s      43.06s      158.12s     693.69s
---------------------------------------------------------------

MEMM
----

Logistic Regresion
------------------
N                   1           2           3           4
Accuracy:           92.72%      91.99%      92.18%      92.22%
Accuracy known:     95.29%      94.55%      94.71%      94.72%
Accuracy unknown:   69.36%      68.75%      69.18%      69.62%
Time:               62.50s      68.98s      73.48s      75.83s
--------------------------------------------------------------

Multinomial NB
--------------
N                   1           2           3           4
Accuracy:           81.27%      76.02%      70.97%      67.95%
Accuracy known:     84.74%      79.64%      74.55%      71.06%
Accuracy unknown:   49.89%      43.25%      38.51%      39.83%
Time:               2376.78s    2306.70s    2356.35s    2426.56s
----------------------------------------------------------------

Linear SVC
----------
N                   1           2           3           4
Accuracy:           94.43%      94.29%      94.39%      94.45%
Accuracy known:     97.04%      96.91%      96.93%      96.95%
Accuracy unknown:   70.82%      70.57%      71.36%      71.79%
Time:               62.17s      70.39s      79.54s      80.58s
--------------------------------------------------------------
