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

## Przyjęte założenia

- scena jest wyeksportowana z Blender'a do formatu `.dae`
- plik sceny zawiera jedną kamerę perspektywiczną
- światła są obiektami emitującymi światło, nie obiektami typu światło
- interfejs konsolowy
- render do pliku + wyskakujące GUI z efektem
