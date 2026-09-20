import tkinter as tk
import pandas as pd
import matplotlib.pyplot as plt

from tkinter import ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# Wczytanie pliku z danymi pacjentów z zabezpieczeniem ścieżki
try:
    df = pd.read_csv('data/dane_pacjenci_bol_plecow.csv')
except FileNotFoundError:
    df = pd.read_csv('../data/dane_pacjenci_bol_plecow.csv')

# Stworzenie głównego okna aplikacji
okno = tk.Tk()
okno.title("Analiza pacjentów z bólem pleców")
okno.geometry("900x750")

# Stworzenie głównej ramki na górne elementy sterujące (filtry)
ramka_gorna = ttk.Frame(okno, padding="10")
ramka_gorna.pack(fill="x", padx=10, pady=10)

# Etykieta informacyjna dla panelu sterowania
etykieta_wykres = ttk.Label(ramka_gorna, text="Wybierz typ wykresu:")
etykieta_wykres.pack(side="left", padx=5)

# Lista rozwijana do wyboru typu wykresu
wybor_wykresu = ttk.Combobox(
    ramka_gorna,
    values=["Wiek a ból", "Rozkład bólów", "Korelacja cech", "Średnia wg grupy"],
    state="readonly"
)
wybor_wykresu.pack(side="left", padx=5)
wybor_wykresu.current(0) # Ustawienie domyślnego wyboru na pierwszy element

# Etykieta i lista rozwijana do filtrowania danych pacjentów
etykieta_grupa = ttk.Label(ramka_gorna, text="Grupa pacjentów:")
etykieta_grupa.pack(side="left", padx=(15, 5)) # Dodajemy większy odstęp z lewej strony (15px), żeby oddzielić filtry

wybor_grupy = ttk.Combobox(
    ramka_gorna,
    values=["Wszyscy", "Grupa A", "Grupa B"],
    state="readonly"
)
wybor_grupy.pack(side="left", padx=5)
wybor_grupy.current(0)

# Przycisk wyzwalający aktualizację i rysowanie wykresu
przycisk_aktualizuj = ttk.Button(ramka_gorna, text="Generuj wykres")
przycisk_aktualizuj.pack(side="left", padx=10)

# Ramka kontenerowa na wykres/tabelę w środkowej części okna
ramka_srodek = ttk.Frame(okno, padding="10")
ramka_srodek.pack(fill="both", expand=True, padx=10, pady=5)

# Inicjalizacja figury i osi wykresu biblioteki Matplotlib
fig, ax = plt.subplots(figsize=(6, 4), dpi=100)

# Osadzenie płótna wykresu Matplotlib w środkowej ramce aplikacji
canvas = FigureCanvasTkAgg(fig, master=ramka_srodek)
canvas.get_tk_widget().pack(fill="both", expand=True)

# Stworzenie dolnej ramki na podsumowanie statystyczne
ramka_dolna = ttk.LabelFrame(okno, text="Podsumowanie statystyczne", padding="10")
ramka_dolna.pack(fill="x", padx=10, pady=10)

# Etykiety tekstowe w dolnej ramce do wyświetlania dynamicznych statystyk
etykieta_liczba_pacjentow = ttk.Label(ramka_dolna, text="Liczba pacjentów: -", font=("Arial", 10, "bold"))
etykieta_liczba_pacjentow.pack(side="left", padx=15)

etykieta_sredni_wiek = ttk.Label(ramka_dolna, text="Średni wiek: -", font=("Arial", 10))
etykieta_sredni_wiek.pack(side="left", padx=15)

# Funkcja odpowiedzialna za generowanie wykresów na podstawie filtrów
def rysuj_wykres():
    # Pobranie wybranej opcji z list rozwijanych
    typ = wybor_wykresu.get()
    grupa = wybor_grupy.get()

    # Filtrowanie danych w zależności od wybranej grupy pacjentów
    if grupa == "Grupa A":
        dane_f = df[df['Grupa'] == 'A']
    elif grupa == "Grupa B":
        dane_f = df[df['Grupa'] == 'B']
    else:
        dane_f = df  # Wszyscy pacjenci

    # Wyczyszczenie poprzedniego wykresu z osi
    ax.clear()

    # Generowanie odpowiedniego wykresu w zależności od wyboru
    if typ == "Wiek a ból":
        ax.scatter(dane_f['Wiek'], dane_f['Bol_Plecow'], color='purple', alpha=0.7)
        ax.set_title("Zależność wieku od poziomu bólu")
        ax.set_xlabel("Wiek pacjenta")
        ax.set_ylabel("Skala bólu")
    elif typ == "Rozkład bólów":
        ax.hist(dane_f['Bol_Plecow'], bins=8, color='teal', edgecolor='black')
        ax.set_title("Rozkład poziomu bólu")
        ax.set_xlabel("Skala bólu")
        ax.set_ylabel("Liczba pacjentów")
    else:
        # Wykres domyślny dla pozostałych opcji
        ax.plot([1, 2, 3, 4], [10, 20, 15, 25], marker='o', color='orange')
        ax.set_title(f"Analiza: {typ}")
        ax.set_xlabel("Kategoria")
        ax.set_ylabel("Wartość")

    # Odświeżenie płótna, aby nowy wykres wyświetlił się w oknie
    canvas.draw()


# Powiązanie przycisku z funkcją rysującą
przycisk_aktualizuj.config(command=rysuj_wykres)

# Wywołanie funkcji rysującej od razu przy starcie aplikacji
rysuj_wykres()