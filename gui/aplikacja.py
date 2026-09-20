import tkinter as tk
from tkinter import ttk
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# 1. Wczytanie danych pacjentów
try:
    df = pd.read_csv('data/dane_pacjenci_bol_plecow.csv')
except FileNotFoundError:
    df = pd.read_csv('../data/dane_pacjenci_bol_plecow.csv')

# 2. Tworzymy główne okno aplikacji
okno = tk.Tk()
okno.title("Projekt 2 - Analiza pacjentów (Weronika)")
okno.geometry("900x750")

# 3. Górna ramka z filtrami
ramka_gorna = tk.Frame(okno, bg="#f0f0f0", pady=10)
ramka_gorna.pack(fill=tk.X)

# Filtr grupy
tk.Label(ramka_gorna, text="Grupa:", font=("Arial", 9, "bold"), bg="#f0f0f0").pack(side=tk.LEFT, padx=5)
opcje_filtru = ["Wszyscy", "Tylko ćwiczący (Tak)", "Tylko niećwiczący (Nie)"]
wybor_filtra = ttk.Combobox(ramka_gorna, values=opcje_filtru, state="readonly", width=18)
wybor_filtra.set("Wszyscy")
wybor_filtra.pack(side=tk.LEFT, padx=5)

# Filtr wykresu (Wszystkie 4 wymagane typy z wytycznych uczelni!)
tk.Label(ramka_gorna, text="Typ wykresu:", font=("Arial", 9, "bold"), bg="#f0f0f0").pack(side=tk.LEFT, padx=10)
opcje_wykresow = [
    "Średni ból a praca siedząca (Słupkowy)",
    "Histogram wieku",
    "Wykres rozrzutu (Wiek vs Ból)",
    "Wykres pudełkowy (Skala bólu)"
]
wybor_wykresu = ttk.Combobox(ramka_gorna, values=opcje_wykresow, state="readonly", width=32)
wybor_wykresu.set("Średni ból a praca siedząca (Słupkowy)")
wybor_wykresu.pack(side=tk.LEFT, padx=5)

# 4. Obszar wykresu w środku okna
fig, ax = plt.subplots(figsize=(7, 3.2))
canvas = FigureCanvasTkAgg(fig, master=okno)
canvas.get_tk_widget().pack(pady=5, fill=tk.BOTH, expand=True)

# 5. Dolna ramka z tabelą danych
ramka_dolna = tk.Frame(okno)
ramka_dolna.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

tk.Label(ramka_dolna, text="Tabela danych (Filtrowanie i statystyka opisowa):", font=("Arial", 10, "bold")).pack(
    anchor="w", pady=2)

kolumny = list(df.columns)
tabela = ttk.Treeview(ramka_dolna, columns=kolumny, show="headings", height=5)

for kol in kolumny:
    tabela.heading(kol, text=kol)
    tabela.column(kol, width=100, anchor="center")

scrollbar = ttk.Scrollbar(ramka_dolna, orient="vertical", command=tabela.yview)
tabela.configure(yscrollcommand=scrollbar.set)

tabela.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)


# 6. Główna funkcja aktualizująca widok
def aktualizuj_widok(event=None):
    wybor_f = wybor_filtra.get()
    wybor_w = wybor_wykresu.get()

    # Filtrowanie danych
    if wybor_f == "Tylko ćwiczący (Tak)":
        dane = df[df['Regularne_Cwiczenia'] == 'Tak']
    elif wybor_f == "Tylko niećwiczący (Nie)":
        dane = df[df['Regularne_Cwiczenia'] == 'Nie']
    else:
        dane = df

    # --- RYSOWANIE WYKRESÓW ZGODNIE Z WYTYCZNYMI ---
    ax.clear()

    if wybor_w == "Histogram wieku":
        ax.hist(dane['Wiek'], color='lightgreen', edgecolor='black', bins=8)
        ax.set_title(f"Histogram wieku (Grupa: {wybor_f})", fontsize=11, fontweight='bold')
        ax.set_xlabel("Wiek")
        ax.set_ylabel("Liczba pacjentów")

    elif wybor_w == "Wykres rozrzutu (Wiek vs Ból)":
        ax.scatter(dane['Wiek'], dane['Skala_Bolu_1_10'], color='purple', alpha=0.7, edgecolors='black')
        ax.set_title(f"Wykres rozrzutu: Wiek vs Skala bólu ({wybor_f})", fontsize=11, fontweight='bold')
        ax.set_xlabel("Wiek")
        ax.set_ylabel("Skala bólu (1-10)")

    elif wybor_w == "Wykres pudełkowy (Skala bólu)":
        ax.boxplot(dane['Skala_Bolu_1_10'].dropna(), patch_artist=True, boxprops=dict(facecolor='lightblue'))
        ax.set_title(f"Wykres pudełkowy: Rozkład skali bólu ({wybor_f})", fontsize=11, fontweight='bold')
        ax.set_ylabel("Skala bólu (1-10)")

    else:  # Domyślny słupkowy
        srednie = dane.groupby('Praca_Siedzaca')['Skala_Bolu_1_10'].mean()
        etykiety = ['Brak pracy siedzącej', 'Praca siedząca']
        kolory = ['#4a90e2', '#e94e77']

        ax.bar(etykiety, srednie.values, color=kolory, width=0.4)
        ax.set_title(f"Średni ból pleców a praca siedząca ({wybor_f})", fontsize=11, fontweight='bold')
        ax.set_ylabel("Skala bólu (1-10)")
        ax.set_ylim(0, 10)

        for i, v in enumerate(srednie.values):
            ax.text(i, v + 0.3, f"{v:.1f}", ha='center', fontweight='bold')

    canvas.draw()

    # --- AKTUALIZACJA TABELI ---
    for row in tabela.get_children():
        tabela.delete(row)

    for _, row in dane.iterrows():
        tabela.insert("", "end", values=list(row))


# Powiązanie list z funkcją
wybor_filtra.bind("<<ComboboxSelected>>", aktualizuj_widok)
wybor_wykresu.bind("<<ComboboxSelected>>", aktualizuj_widok)

aktualizuj_widok()
okno.mainloop()