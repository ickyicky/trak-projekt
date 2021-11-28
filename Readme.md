# Projekt nr. 9 TRAK - Badanie możliwości próbkowania

## Treść projektu

W ramach projektu należy stworzyć program, który będzie umożliwiał rendering z wykorzystaniem algorytmu śledzenia ścieżek wraz z różnymi algorytmami próbkowania.

W programie powinny znaleźć się m.in.:

1. obsługa mapy środowiska
2. interfejs konsolowy/graficzny, który umożliwi wczytanie sceny (modele wraz z materiałami oraz ich właściwościami) z pliku, podanie algorytmu próbkowania oraz wczytanie mapy środowiska
3. implementacja algorytmu śledzenia ścieżek
4. różne algorytmy próbkowania: całkowicie losowy, stratified sampling, multijittered sampling, szeregi małej rozbieżności (ang. low-discrepancy series)

## Wykorzystane technologie - propozycja

- język programowania: Python
- wczytanie sceny za pomocą [pycollada](https://github.com/pycollada/pycollada)
- wybór sceny z pliku i podanie algorytmu z interfesju konsolowego jako argumenty wywołania
- render sceny, jedno z poniższych:
	- wykorzystanie [PyOpenGL](https://pypi.org/project/PyOpenGL/)
	- render do pliku

## Przyjęte założenia

- scena jest wyeksportowana z Blender'a do formatu `.dae`
- kamera definiowana jest osobno, np. w specjalnym pliku TODO

## Algorytm śledzenia ścieżek

Algorytm można uogólnić do:

1. Z punktu, w którym znajduje się obserwator wypuszczane są promienie.
2. Jeśli promień trafi w jakiś obiekt, z punktu przecięcia (rekursywnie) wypuszczane są kolejne promienie (co najmniej jeden), przy czym kierunek nowych promieni jest losowy; od jakości funkcji losującej zależy jakość obrazu, a każdy obiekt może pochłaniać lub emitować światło.
3. Tworzenie pojedynczej ścieżki kończy się, gdy głębokość rekursji przekroczy pewien limit. Wówczas wyznacza się ostateczne natężenie światła, jakie dociera do obserwatora: składa się na nie natężenie światła pochodzące od obiektów emitujących, które następnie na ścieżce jest tłumione; tłumienie zależy od współczynnika pochłaniania światła dla każdego trafionego obiektu (funkcja BRDF) uwzględniające m.in. kąt pomiędzy promieniem padającym i odbitym.

## Opracowanie badanych algorytmów próbkowania

Większość algorytmów ma już swoją implementację w bibliotece Pythonowej [sklearn](https://scikit-learn.org/stable/index.html)

### Całkowicie losowy

### Stratified sampling

### Multijittered sampling

### Low-discrepancy series, szeregi małej rozbieżności
