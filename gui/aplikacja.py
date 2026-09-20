import tkinter as tk
import pandas as pd
import matplotlib.pyplot as plt
from tkinter import messagebox

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

# Konfiguracja nowoczesnego stylu interfejsu
styl = ttk.Style()
styl.theme_use('clam')  # Użycie nowoczesnego motywu

# Stworzenie głównej ramki na górne elementy sterujące (filtry)
ramka_gorna = ttk.Frame(okno, padding="10")
ramka_gorna.pack(fill="x", padx=10, pady=10)

# Etykieta informacyjna dla panelu sterowania
etykieta_wykres = ttk.Label(ramka_gorna, text="Wybierz typ wykresu:")
etykieta_wykres.pack(side="left", padx=5)

# Lista rozwijana do wyboru typu wykresu
wybor_grupy = ttk.Combobox(
    ramka_gorna,
    values=["Wiek a ból", "Rozkład poziomu bólu", "Korelacja cech", "Średnia wg grupy"],
    state="readonly"
)

wybor_grupy.set("Wszyscy")
wybor_grupy.pack(side="left", padx=5)

# Etykieta i lista rozwijana do filtrowania danych pacjentów
etykieta_grupa = ttk.Label(ramka_gorna, text="Lokalizacja:")
etykieta_grupa.pack(side="left", padx=(15, 5)) # Dodajemy większy odstęp z lewej strony (15px), żeby oddzielić filtry

# Lista rozwijana do filtrowania po odcinku kręgosłupa
# 1. Tworzenie listy rozwijanej
wybor_grupy = ttk.Combobox(
    ramka_gorna,
    values=["Wszyscy", "szyjny", "piersiowy", "lędźwiowy"],
    state="readonly"
)


wybor_grupy.set("Wszyscy")  # Domyślny wybór przy starcie
wybor_grupy.pack(side="left", padx=5)  # Umieszcza element w oknie (lub użyj .grid(), jeśli tak układasz resztę)


# 1. Najpierw definiujemy funkcję eksportu:
def eksportuj_dane():
    if grupa == "Ćwiczą regularnie":
        dane_f = df[df['Regularne_Cwiczenia'] == 'Tak']
    elif grupa == "Nie ćwiczą":
        dane_f = df[df['Regularne_Cwiczenia'] == 'Nie']
    else:
        dane_f = df

    dane_eksport.to_csv("raport_z_analizy.csv", index=False)
    etykieta_status.config(text="Status: Wyeksportowano dane do pliku CSV!")
    print("Zapisano dane do pliku raport_z_analizy.csv!")

def resetuj_filtry():
    wybor_wykresu.current(0)
    wybor_grupy.current(0)
    rysuj_wykres()
    etykieta_status.config(text="Status: Zresetowano filtry")

def pokaz_informacje():
    messagebox.showinfo("O programie", "Aplikacja do analizy danych pacjentów z bólem pleców.\nProjekt inżynierski / zaliczeniowy.")
    etykieta_status.config(text="Status: Wyświetlono informacje o programie")


def rysuj_wykres():
        typ = wybor_wykresu.get()
        grupa = wybor_grupy.get()

        # Filtrowanie danych w zależności od wyboru w liście rozwijanej
        if grupa == "szyjny":
            dane_f = df[df['Odcinek'] == 'szyjny']
        elif grupa == "piersiowy":
            dane_f = df[df['Odcinek'] == 'piersiowy']
        elif grupa == "lędźwiowy":
            dane_f = df[df['Odcinek'] == 'lędźwiowy']
        else:
            dane_f = df  # Wszyscy

        liczba_pacjentow = len(dane_f)
        sredni_wiek = dane_f['Wiek'].mean() if liczba_pacjentow > 0 else 0

        etykieta_liczba_pacjentow.config(text=f"Liczba pacjentów: {liczba_pacjentow}")
        etykieta_sredni_wiek.config(text=f"Średni wiek: {sredni_wiek:.1f}")

        ax.clear()

        # 4 różne typy wykresów zgodnie z wytycznymi
        if typ == "Wiek a ból":
        # Tworzymy przedziały wiekowe, żeby wykres pudełkowy był czytelny
            dane_f['Przedzial_Wiekowy'] = pd.cut(dane_f['Wiek'], bins=[0, 30, 40, 50, 60, 100],
                                             labels=['<30', '30-40', '41-50', '51-60', '60+'])

        # Rysujemy wykres pudełkowy poziomu bólu w podziale na grupy wiekowe
            dane_f.boxplot(column='Skala_Bolu_1_10', by='Przedzial_Wiekowy', ax=ax, grid=False)
            ax.set_title("Rozkład bólu w grupach wiekowych")
            ax.set_xlabel("Grupa wiekowa")
            ax.set_ylabel("Skala bólu (1-10)")
           # Ukrywamy domyślny, brzydki podpis generowany automatycznie przez pandas nad wykresem
            plt.suptitle("")
        elif typ == "Rozkład poziomo bólu":
            ax.hist(dane_f['Skala_Bolu_1_10'], bins=8, color='teal', edgecolor='black')
            ax.set_title("Rozkład poziomu bólu")
            ax.set_xlabel("Skala bólu")
            ax.set_ylabel("Liczba pacjentów")
        elif typ == "Korelacja cech":
            ax.scatter(dane_f['Wiek'], dane_f['Skala_Bolu_1_10'], c=dane_f['Skala_Bolu_1_10'], cmap='viridis',
                       alpha=0.8, s=60)
            ax.set_title("Korelacja wieku a poziomu bólu")
            ax.set_xlabel("Wiek pacjenta")
            ax.set_ylabel("Skala bólu (1-10)")
        elif typ == "Średnia wg grupy":
            srednie = df.groupby('Odcinek')['Skala_Bolu_1_10'].mean()
            srednie.plot(kind='bar', ax=ax, color=['#3498db', '#e74c3c', '#2ecc71'], edgecolor='black', rot=0)
            ax.set_title("Średni poziom bólu w zależności od odcinka kręgosłupa")
            ax.set_xlabel("Odcinek kręgosłupa")
            ax.set_ylabel("Średnia skala bólu")
        else:
            ax.text(0.5, 0.5, "Wybierz poprawny wykres", horizontalalignment='center', verticalalignment='center')

        canvas.draw()

# Ramka na wykres w środkowej części okna
ramka_srodek = ttk.Frame(okno, padding="10")
ramka_srodek.pack(fill="both", expand=True, padx=10, pady=5)

fig, ax = plt.subplots(figsize=(6, 4), dpi=100)
canvas = FigureCanvasTkAgg(fig, master=ramka_srodek)
canvas.get_tk_widget().pack(fill="both", expand=True)

# Dolna ramka na statystyki
ramka_dolna = ttk.LabelFrame(okno, text="Podsumowanie statystyczne", padding="10")
ramka_dolna.pack(fill="x", padx=10, pady=10)

etykieta_status = ttk.Label(ramka_dolna, text="Status: Gotowy do pracy", font=("Arial", 9, "italic"))
etykieta_status.pack(side="right", padx=15)

etykieta_liczba_pacjentow = ttk.Label(ramka_dolna, text="Liczba pacjentów: -", font=("Arial", 10, "bold"))
etykieta_liczba_pacjentow.pack(side="left", padx=15)

etykieta_sredni_wiek = ttk.Label(ramka_dolna, text="Średni wiek: -", font=("Arial", 10))
etykieta_sredni_wiek.pack(side="left", padx=15)


przycisk_aktualizuj = ttk.Button(ramka_gorna, text="Generuj wykres")
przycisk_aktualizuj.pack(side="left", padx=10)


przycisk_aktualizuj.config(command=rysuj_wykres)


def zamknij_aplikacje():
        print("Zamykanie aplikacji...")
        okno.destroy()

okno.protocol("WM_DELETE_WINDOW", zamknij_aplikacje)
okno.mainloop()

