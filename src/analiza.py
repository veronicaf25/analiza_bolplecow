# Importujemy 'pandas' - to specjalna biblioteka narzędzi do pracy z tabelami.
import pandas as pd

# 1. WSKAZANIE PLIKU
# Ścieżka "wyjdź wyżej i wejdź do data"
sciezka_do_pliku = "../data/dane_pacjenci_bol_plecow.csv"

# 2. WCZYTANIE DANYCH
df = pd.read_csv(sciezka_do_pliku)

# 3. WYŚWIETLENIE WYNIKU
print("Udało się! Oto pierwszych 5 pacjentów w naszej bazie:")
print(df.head())

# 4. PIERWSZA ANALIZA
# Wyciągamy z tabeli tylko tych pacjentów, którzy mają pracę siedzącą
pacjenci_siedzacy = df[df['Praca_Siedzaca'] == 'Tak']

# Wyliczamy średnią z ich skali bólu
sredni_bol = pacjenci_siedzacy['Skala_Bolu_1_10'].mean()

# Wyświetlamy wynik na ekranie (znacznik :.2f zaokrągla wynik do dwóch miejsc po przecinku)
print("\n--- WYNIKI ANALIZY ---")
print(f"Średni ból pleców u pacjentów z pracą siedzącą wynosi: {sredni_bol:.2f}")

# Importujemy dodatkowe narzędzie do rysowania wykresów
import matplotlib.pyplot as plt

# 5. WIZUALIZACJA DANYCH
print("Generowanie wykresu...")

# Grupujemy pacjentów (Praca_Siedzaca: Tak / Nie) i wyliczamy dla nich średni ból
sredni_bol_grupy = df.groupby('Praca_Siedzaca')['Skala_Bolu_1_10'].mean()

# Tworzymy wykres słupkowy (bar). Kolory: 'skyblue' i 'salmon' dla lepszego efektu
sredni_bol_grupy.plot(kind='bar', color=['skyblue', 'salmon'], edgecolor='black')

# Dodajemy opisy osi i tytuł, żeby na obronie nikt nie miał wątpliwości, co widzi
plt.title('Średni ból pleców a praca siedząca', fontsize=14)
plt.xlabel('Czy praca jest siedząca?', fontsize=12)
plt.ylabel('Średnia skala bólu (1-10)', fontsize=12)

# Poprawiamy kąt napisów na osi X, żeby 'Tak' i 'Nie' były prosto
plt.xticks(rotation=0)

# Pokazujemy gotowy wykres w nowym oknie
plt.show()

# 7. HISTOGRAM WIEKU PACJENTÓW
print("Generowanie histogramu wieku...")

# Tworzymy histogram dla kolumny 'Wiek'.
# 'bins=10' oznacza, że dzielimy pacjentów na 10 koszyków (przedziałów wiekowych).
plt.hist(df['Wiek'], bins=10, color='lightgreen', edgecolor='black', alpha=0.7)

# Opisy osi i tytuł
plt.title('Rozkład wieku pacjentów z bólem pleców', fontsize=14)
plt.xlabel('Wiek (lata)', fontsize=12)
plt.ylabel('Liczba pacjentów', fontsize=12)

# Wyświetlenie wykresu
plt.show()