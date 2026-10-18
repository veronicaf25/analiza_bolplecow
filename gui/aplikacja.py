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
okno.geometry("1220x750")

# Konfiguracja nowoczesnego stylu interfejsu
styl = ttk.Style()
styl.theme_use('clam')

# Stworzenie głównej ramki na górne elementy sterujące (filtry)
ramka_gorna = ttk.Frame(okno, padding="10")
ramka_gorna.pack(fill="x", padx=10, pady=10)

# 1. Wybór typu wykresu (z dodaną opcją aktywności fizycznej)
etykieta_wykres = ttk.Label(ramka_gorna, text="Wykres:")
etykieta_wykres.pack(side="left", padx=2)
wybor_wykresu = ttk.Combobox(
    ramka_gorna,
    values=[
        "Wiek a ból",
        "Płeć a ból",
        "Histogram poziomu bólu",
        "Wykres rozrzutu (Wiek vs Ból)",
        "Aktywność fizyczna a ból"
    ],
    state="readonly",
    width=28
)
wybor_wykresu.set("Wiek a ból")
wybor_wykresu.pack(side="left", padx=5)

# 2. Odcinek kręgosłupa
etykieta_grupa = ttk.Label(ramka_gorna, text="Odcinek:")
etykieta_grupa.pack(side="left", padx=(10, 2))
wybor_grupy = ttk.Combobox(
    ramka_gorna,
    values=["Wszyscy", "szyjny", "piersiowy", "lędźwiowy"],
    state="readonly",
    width=10
)
wybor_grupy.set("Wszyscy")
wybor_grupy.pack(side="left", padx=5)

# 3. Wybór widoku (Wykres / Tabela)
etykieta_widok = ttk.Label(ramka_gorna, text="Widok:")
etykieta_widok.pack(side="left", padx=(10, 2))
wybor_widoku = ttk.Combobox(
    ramka_gorna,
    values=["Wykres", "Tabela"],
    state="readonly",
    width=9
)
wybor_widoku.set("Wykres")
wybor_widoku.pack(side="left", padx=5)

# 4. Aktywność fizyczna
etykieta_cwiczenia = ttk.Label(ramka_gorna, text="Aktywność:")
etykieta_cwiczenia.pack(side="left", padx=(10, 2))
wybor_cwiczen = ttk.Combobox(ramka_gorna, values=["Wszyscy", "Tak", "Nie"], state="readonly", width=8)
wybor_cwiczen.set("Wszyscy")
wybor_cwiczen.pack(side="left", padx=5)

# 5. Praca siedząca
etykieta_styl = ttk.Label(ramka_gorna, text="Praca siedząca:")
etykieta_styl.pack(side="left", padx=(10, 2))
wybor_stylu = ttk.Combobox(ramka_gorna, values=["Wszyscy", "Tak", "Nie"], state="readonly", width=8)
wybor_stylu.set("Wszyscy")
wybor_stylu.pack(side="left", padx=5)


def resetuj_filtry():
    wybor_grupy.set("Wszyscy")
    wybor_cwiczen.set("Wszyscy")
    wybor_stylu.set("Wszyscy")
    wybor_wykresu.set("Wiek a ból")
    wybor_widoku.set("Wykres")
    zmien_widok()
    rysuj_wykres()
    etykieta_status.config(text="Status: Zresetowano filtry")


# Przycisk resetowania filtrów po prawej stronie
przycisk_reset = ttk.Button(ramka_gorna, text="🔄 Resetuj filtry", command=resetuj_filtry, width=15)
przycisk_reset.pack(side="right", padx=5)


# --- RAMKA NA WYKRES (Środek - domyślnie widoczna) ---
ramka_srodek = ttk.Frame(okno, padding="10")
ramka_srodek.pack(fill="both", expand=True, padx=10, pady=5)

fig, ax = plt.subplots(figsize=(6, 4), dpi=100)
canvas = FigureCanvasTkAgg(fig, master=ramka_srodek)
canvas.get_tk_widget().pack(fill="both", expand=True)


# --- RAMKA NA TABELĘ (Środek - domyślnie ukryta) ---
ramka_tabela = ttk.LabelFrame(okno, text="Tabela filtrowanych pacjentów", padding="5")

kolumny = ('Wiek', 'Plec', 'Odcinek', 'Skala_Bolu', 'Cwiczenia', 'Praca_siedzaca')
tabela = ttk.Treeview(ramka_tabela, columns=kolumny, show='headings', height=12)

for col in kolumny:
    tabela.heading(col, text=col)
    tabela.column(col, width=120, anchor='center')

tabela.pack(side="left", fill="both", expand=True)

scrollbar = ttk.Scrollbar(ramka_tabela, orient="vertical", command=tabela.yview)
scrollbar.pack(side="right", fill="y")
tabela.configure(yscrollcommand=scrollbar.set)


def zmien_widok(event=None):
    wybrany = wybor_widoku.get()
    if wybrany == "Wykres":
        ramka_tabela.pack_forget()  # Schowaj tabelę
        ramka_srodek.pack(fill="both", expand=True, padx=10, pady=5)  # Pokaż wykres
    else:
        ramka_srodek.pack_forget()  # Schowaj wykres
        ramka_tabela.pack(fill="both", expand=True, padx=10, pady=5)  # Pokaż tabelę


def rysuj_wykres(event=None):
    typ = wybor_wykresu.get()
    grupa = wybor_grupy.get()
    aktywnosc = wybor_cwiczen.get()
    styl_pracy = wybor_stylu.get()

    # Klonowanie i filtrowanie wielokryteriowe
    dane_f = df.copy()

    if grupa != "Wszyscy":
        dane_f = dane_f[dane_f['Odcinek'] == grupa]
    if aktywnosc != "Wszyscy":
        dane_f = dane_f[dane_f['Regularne_cwiczenia'] == aktywnosc]
    if styl_pracy != "Wszyscy":
        dane_f = dane_f[dane_f['Praca_siedzaca'] == styl_pracy]

    # Statystyki na dole (Średnia i Mediana)
    liczba_pacjentow = len(dane_f)
    sredni_wiek = dane_f['Wiek'].mean() if liczba_pacjentow > 0 else 0
    mediana_wieku = dane_f['Wiek'].median() if liczba_pacjentow > 0 else 0

    etykieta_liczba_pacjentow.config(text=f"Liczba pacjentów: {liczba_pacjentow}")
    etykieta_sredni_wiek.config(text=f"Średni wiek: {sredni_wiek:.1f}")
    etykieta_mediana_wieku.config(text=f"Mediana wieku: {mediana_wieku:.1f}")

    # Rysowanie wykresu
    ax.clear()

    if typ == "Wiek a ból":
        dane_f_kopia = dane_f.copy()
        dane_f_kopia['Przedzial_Wiekowy'] = pd.cut(
            dane_f_kopia['Wiek'],
            bins=[0, 30, 40, 50, 60, 100],
            labels=['<30', '30-40', '41-50', '51-60', '60+']
        )

        if not dane_f_kopia.empty:
            grupy_danych = [g_df['Skala_Bolu_1_10'].dropna().values for _, g_df in
                            dane_f_kopia.groupby('Przedzial_Wiekowy', observed=True)]
            etykiety = [str(nazwa) for nazwa, _ in dane_f_kopia.groupby('Przedzial_Wiekowy', observed=True)]

            ax.boxplot(grupy_danych, tick_labels=etykiety)
            ax.set_title("Rozkład poziomu bólu w grupach wiekowych")
            ax.set_xlabel("Grupa wiekowa")
            ax.set_ylabel("Skala bólu (1-10)")
            ax.grid(True, linestyle='--', alpha=0.6)
        else:
            ax.text(0.5, 0.5, "Brak danych dla wybranego filtra", horizontalalignment='center',
                    verticalalignment='center', transform=ax.transAxes)

    elif typ == "Histogram poziomu bólu":
        if not dane_f.empty:
            ax.hist(dane_f['Skalo_Bolu_1_10'] if 'Skalo_Bolu_1_10' in dane_f.columns else dane_f['Skala_Bolu_1_10'], bins=8, color='#e74c3c', edgecolor='black', alpha=0.85)
            ax.set_title("Histogram poziomu bólu pacjentów")
            ax.set_xlabel("Skala bólu (1-10)")
            ax.set_ylabel("Liczba pacjentów")
            ax.grid(axis='y', linestyle='--', alpha=0.6)
        else:
            ax.text(0.5, 0.5, "Brak danych dla wybranego filtra", horizontalalignment='center',
                    verticalalignment='center', transform=ax.transAxes)

    elif typ == "Wykres rozrzutu (Wiek vs Ból)":
        if not dane_f.empty and len(dane_f) > 1:
            x = dane_f['Wiek']
            y = dane_f['Skala_Bolu_1_10']

            # Obliczenie współczynnika korelacji Pearsona
            korelacja = x.corr(y)

            ax.scatter(x, y, color='#2980b9', alpha=0.7, edgecolors='black', s=60)
            ax.set_title(f"Zależność wieku od bólu (Korelacja r = {korelacja:.2f})")
            ax.set_xlabel("Wiek (lata)")
            ax.set_ylabel("Skala bólu (1-10)")
            ax.grid(True, linestyle='--', alpha=0.6)
        else:
            ax.text(0.5, 0.5, "Za mało danych do analizy korelacji", horizontalalignment='center',
                    verticalalignment='center', transform=ax.transAxes)

    elif typ == "Płeć a ból":
        srednie_bolu = dane_f.groupby('Plec')['Skala_Bolu_1_10'].mean()

        if not srednie_bolu.empty:
            ax.bar(srednie_bolu.index, srednie_bolu.values, color=['#e74c3c', '#3498db'], edgecolor='black', alpha=0.85)
            ax.set_title("Średni poziom bólu w zależności od płci")
            ax.set_xlabel("Płeć")
            ax.set_ylabel("Średnia skala bólu (1-10)")
            ax.grid(axis='y', linestyle='--', alpha=0.6)
        else:
             ax.text(0.5, 0.5, "Brak danych dla wybranego filtra", horizontalalignment='center',
                    verticalalignment='center', transform=ax.transAxes)

    elif typ == "Aktywność fizyczna a ból":
        srednie_bolu = dane_f.groupby('Regularne_cwiczenia')['Skala_Bolu_1_10'].mean()

        if not srednie_bolu.empty:
            ax.bar(srednie_bolu.index, srednie_bolu.values, color=['#27ae60', '#e74c3c'], edgecolor='black', alpha=0.85)
            ax.set_title("Średni poziom bólu u osób ćwiczących i niećwiczących")
            ax.set_xlabel("Regularne ćwiczenia fizyczne")
            ax.set_ylabel("Średnia skala bólu (1-10)")
            ax.grid(axis='y', linestyle='--', alpha=0.6)
        else:
             ax.text(0.5, 0.5, "Brak danych dla wybranego filtra", horizontalalignment='center',
                    verticalalignment='center', transform=ax.transAxes)

    canvas.draw()

    # Aktualizacja tabeli danych
    for row in tabela.get_children():
        tabela.delete(row)

    for _, row_data in dane_f.iterrows():
        tabela.insert("", "end", values=(
            row_data.get('Wiek', '-'),
            row_data.get('Plec', '-'),
            row_data.get('Odcinek', '-'),
            row_data.get('Skala_Bolu_1_10', '-'),
            row_data.get('Regularne_cwiczenia', '-'),
            row_data.get('Praca_siedzaca', '-')
        ))


# --- DOLNA RAMKA NA STATYSTYKI ---
ramka_dolna = ttk.LabelFrame(okno, text="Podsumowanie statystyczne", padding="10")
ramka_dolna.pack(fill="x", padx=10, pady=10)

etykieta_status = ttk.Label(ramka_dolna, text="Status: Gotowy do pracy", font=("Arial", 9, "italic"))
etykieta_status.pack(side="right", padx=15)

etykieta_liczba_pacjentow = ttk.Label(ramka_dolna, text="Liczba pacjentów: -", font=("Arial", 10, "bold"))
etykieta_liczba_pacjentow.pack(side="left", padx=10)

etykieta_sredni_wiek = ttk.Label(ramka_dolna, text="Średni wiek: -", font=("Arial", 10))
etykieta_sredni_wiek.pack(side="left", padx=10)

etykieta_mediana_wieku = ttk.Label(ramka_dolna, text="Mediana wieku: -", font=("Arial", 10))
etykieta_mediana_wieku.pack(side="left", padx=10)


# --- POWIĄZANIA ZDARZEŃ (BINDY) ---
wybor_wykresu.bind("<<ComboboxSelected>>", rysuj_wykres)
wybor_grupy.bind("<<ComboboxSelected>>", rysuj_wykres)
wybor_widoku.bind("<<ComboboxSelected>>", zmien_widok)
wybor_cwiczen.bind("<<ComboboxSelected>>", rysuj_wykres)
wybor_stylu.bind("<<ComboboxSelected>>", rysuj_wykres)


def zamknij_aplikacje():
    okno.destroy()


okno.protocol("WM_DELETE_WINDOW", zamknij_aplikacje)

# Wstępne wygenerowanie wykresu przy starcie i uruchomienie okna
rysuj_wykres()
okno.mainloop()