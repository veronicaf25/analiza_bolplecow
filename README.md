Analiza pacjentów z bólem pleców

1. Opis projektu
Projekt polega na stworzeniu aplikacji desktopowej w języku Python, która umożliwia analizę danych pacjentów zgłaszających ból pleców.
Aplikacja pozwala analizować poziom bólu w zależności od wieku, płci, aktywności fizycznej, wykonywania pracy siedzącej oraz odcinka kręgosłupa. Wyniki są przedstawiane w formie wykresów, tabel i statystyk opisowych.
Do stworzenia aplikacji wykorzystano biblioteki Pandas, Matplotlib i Tkinter oraz bazę danych SQLite.

2. Lista funkcji aplikacji

Aplikacja oferuje następujące funkcjonalności:
* Wizualizacja danych - sześć rodzajów wykresów przedstawiających zależności między poziomem bólu a wybranymi cechami pacjentów.
* Filtrowanie danych - wybór odcinka kręgosłupa, aktywności fizycznej i wykonywania pracy siedzącej.
* Widok tabelaryczny - wyświetlanie danych pacjentów spełniających wybrane kryteria.
* Statystyki opisowe - obliczanie liczby pacjentów, średniego wieku, mediany wieku, średniego poziomu bólu, mediany bólu, odchylenia standardowego oraz wartości minimalnej i maksymalnej bólu.
* Automatyczny wniosek analityczny - generowanie podsumowania na podstawie aktualnie filtrowanych danych.
* Dodawanie pacjentów - formularz umożliwiający wprowadzanie nowych rekordów.
* Baza danych SQLite - przechowywanie i odczytywanie danych pacjentów.
* Import danych z CSV - możliwość inicjalizacji bazy na podstawie pliku CSV.
* Eksport danych do CSV - zapisywanie danych po zastosowaniu filtrów.
* Zapisywanie wykresów - eksport aktualnego wykresu do pliku PNG lub PDF.
* Kontrola jakości danych - sprawdzanie brakujących wartości i podstawowych zakresów logicznych.

3. Instrukcja instalacji i uruchomienia

Do uruchomienia aplikacji potrzebne są:
* Python 3.10 lub nowszy;
* biblioteki Pandas i Matplotlib;
* Tkinter;
* plik CSV z danymi wejściowymi.

Instalacja
1. Pobierz lub sklonuj repozytorium projektu z GitHub.
2. Otwórz projekt w PyCharm lub terminalu.
3. Zainstaluj wymagane biblioteki, wpisując w terminalu:

python -m pip install pandas matplotlib

Przygotowanie danych
Plik dane_pacjenci_bol_plecow.csv powinien znajdować się w folderze data.

Uruchomienie aplikacji
W terminalu, w głównym folderze projektu, wpisz:
python gui/aplikacja.py

Przy pierwszym uruchomieniu program spróbuje odczytać dane z bazy SQLite. Jeśli nie będzie to możliwe, podejmie próbę utworzenia bazy na podstawie pliku CSV.


4. Informacja o wykorzystaniu AI
Podczas realizacji projektu korzystałam z ChatGPT jako narzędzia wspierającego naukę programowania.
AI pomagało mi w:
* wyjaśnianiu działania kodu w Pythonie;
* analizowaniu i poprawianiu potencjalnych błędów;
* rozwijaniu funkcjonalności aplikacji, takich jak filtrowanie danych, statystyki i wizualizacja;
* zrozumieniu obsługi bazy danych SQLite;
* przygotowaniu dokumentacji projektu.

Proponowane rozwiązania analizowałam i dostosowywałam do własnego projektu. Korzystanie z AI miało na celu wsparcie procesu nauki i lepsze zrozumienie wykorzystywanych narzędzi.
