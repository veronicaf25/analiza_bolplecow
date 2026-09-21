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
    values=["Wiek a ból", "Rozkład poziomu bólu", "Korelacja cech", "Średnia wg grupy"],
    state="readonly"
)

wybor_wykresu.set("Wszyscy")
wybor_wykresu.pack(side="left", padx=5)

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


def rysuj_wykres(event=None):
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
              dane_f['Przedzial_Wiekowy'] = pd.cut(
            dane_f['Wiek'],
            bins=[0, 30, 40, 50, 60, 100],
            labels=['<30', '30-40', '41-50', '51-60', '60+']
        )

        if not dane_f.empty:
            grupy_danych = [g_df['Skala_Bolu_1_10'].dropna().values for _, g_df in
                            dane_f.groupby('Przedzial_Wiekowy', observed=True)]
            etykiety = [str(nazwa) for nazwa, _ in dane_f.groupby('Przedzial_Wiekowy', observed=True)]

            ax.boxplot(grupy_danych, tick_labels=etykiety)
            ax.set_title("Rozkład poziomu bólu w grupach wiekowych")
            ax.set_xlabel("Grupa wiekowa")
            ax.set_ylabel("Skala bólu (1-10)")
            ax.grid(True, linestyle='--', alpha=0.6)
        else:
            ax.text(0.5, 0.5, "Brak danych dla wybranego filtra", horizontalalignment='center',
                    verticalalignment='center', transform=ax.transAxes)

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

wybor_wykresu.bind("<<ComboboxSelected>>", rysuj_wykres)
wybor_grupy.bind("<<ComboboxSelected>>", rysuj_wykres)


def zamknij_aplikacje():
        print("Zamykanie aplikacji...")
        okno.destroy()

okno.protocol("WM_DELETE_WINDOW", zamknij_aplikacje)
okno.mainloop()

