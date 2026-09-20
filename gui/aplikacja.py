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
    values=["Wszyscy", "Praca siedząca", "Praca niesiedziąca"],
    state="readonly"
)
wybor_grupy.pack(side="left", padx=5)
wybor_grupy.current(0)

# 1. Najpierw definiujemy funkcję eksportu:
def eksportuj_dane():
    grupa = wybor_grupy.get()
    if grupa == "Praca siedząca":
        dane_eksport = df[df['Grupa'] == 'A']
    elif grupa == "Praca niesiedząca":
        dane_eksport = df[df['Grupa'] == 'B']
    else:
        dane_eksport = df

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

        # Filtrowanie danych dla pracy siedzącej (A) i niesiedzącej (B)
        if grupa == "Praca siedząca":
            dane_f = df[df['Grupa'] == 'A']  # Praca siedząca
        elif grupa == "Praca niesiedząca":
            dane_f = df[df['Grupa'] == 'B']  # Praca niesiedząca
        else:
            dane_f = df

        liczba_pacjentow = len(dane_f)
        sredni_wiek = dane_f['Wiek'].mean() if liczba_pacjentow > 0 else 0

        etykieta_liczba_pacjentow.config(text=f"Liczba pacjentów: {liczba_pacjentow}")
        etykieta_sredni_wiek.config(text=f"Średni wiek: {sredni_wiek:.1f}")

        ax.clear()

        # 4 różne typy wykresów zgodnie z wytycznymi
        if typ == "Wiek a ból":
            ax.scatter(dane_f['Wiek'], dane_f['Skala_Bolu_1_10'], color='purple', alpha=0.7, s=50)
            ax.set_title("Zależność wieku od poziomu bólu")
            ax.set_xlabel("Wiek pacjenta")
            ax.set_ylabel("Skala bólu (1-10)")
        elif typ == "Rozkład bólów":
            ax.hist(dane_f['Skala_Bolu_1_10'], bins=8, color='teal', edgecolor='black')
            ax.set_title("Rozkład poziomu bólu")
            ax.set_xlabel("Skala bólu")
            ax.set_ylabel("Liczba pacjentów")
        elif typ == "Korelacja cech":
            dane_f.boxplot(column='Wiek', by='Skala_Bolu_1_10', ax=ax, grid=False)
            ax.set_title("Rozkład wieku dla poziomów bólu")
            ax.set_xlabel("Skala bólu")
            ax.set_ylabel("Wiek")
        elif typ == "Średnia wg grupy":
            srednie = dane_f.groupby('Grupa')['Skala_Bolu_1_10'].mean() if 'Grupa' in dane_f.columns else pd.Series()
            srednie.plot(kind='bar', ax=ax, color=['#3498db', '#e74c3c'], edgecolor='black', rot=0)
            ax.set_title("Średni poziom bólu: Siedząca (A) vs Niesiedząca (B)")
            ax.set_xlabel("Grupa (A - siedząca, B - niesiedząca)")
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
rysuj_wykres()

def zamknij_aplikacje():
        print("Zamykanie aplikacji...")
        okno.destroy()

okno.protocol("WM_DELETE_WINDOW", zamknij_aplikacje)
okno.mainloop()

