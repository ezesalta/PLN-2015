Resultados
----------
horzMarkov = 0
--------------
Training time: 66.92s


horzMarkov = 1
--------------
Training time: 69.78s

horzMarkov = 2
--------------
Training Time: 70.49s
-----
con collapsePOS=False

100.0% (3491/3492) (P=41.10%, R=67.56%, F1=51.11%)
Parsed 1444 sentences
Discarded 2048 sentences
Labeled
    Precision: 41.10%
    Recall: 67.56%
    F1: 51.11%
Unlabeled
    Precision: 46.74%
    Recall: 76.84%
    F1: 58.12%
Time: 36542.78s = 609.05m = 10.15h
Averge time CKY parser: 25.29
--------------

con collapsePOS=True
Parsing...                                                                                                 100.0% (3491/3492) (P=96.53%, R=14.62%, F1=25.39%)
Parsed 1444 sentences
Discarded 2048 sentences
Labeled
    Precision: 96.53%
    Recall: 14.62%
    F1: 25.39%
Unlabeled
    Precision: 97.00%
    Recall: 14.69%
    F1: 25.52%
Time: 169.48s
Averge time CKY parser: 0.12





horzMarkov = 3
--------------
Training Time: 73.91s

horzMarkov = 4
--------------