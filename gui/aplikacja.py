import tkinter as tk
import pandas as pd
import matplotlib.pyplot as plt
from tkinter import messagebox, filedialog
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
okno.geometry("1280x800")

# Konfiguracja nowoczesnego stylu interfejsu
styl = ttk.Style()
styl.theme_use('clam')

# --- 1. DOLNY PANEL STATYSTYCZNY (NA SAMYM DOLE) ---
ramka_dolna = ttk.LabelFrame(okno, text="Podsumowanie statystyczne i jakość danych", padding="10")
ramka_dolna.pack(side="bottom", fill="x", padx=10, pady=10)

# Górny rząd statystyk (Wiek)
gorna_stat_ramka = ttk.Frame(ramka_dolna)
gorna_stat_ramka.pack(fill="x", pady=2)

etykieta_liczba_pacjentow = ttk.Label(gorna_stat_ramka, text="Liczba pacjentów: -", font=("Arial", 10, "bold"))
etykieta_liczba_pacjentow.pack(side="left", padx=10)

etykieta_sredni_wiek = ttk.Label(gorna_stat_ramka, text="Średni wiek: -", font=("Arial", 10))
etykieta_sredni_wiek.pack(side="left", padx=10)

etykieta_mediana_wieku = ttk.Label(gorna_stat_ramka, text="Mediana wieku: -", font=("Arial", 10))
etykieta_mediana_wieku.pack(side="left", padx=10)

# Dolny rząd statystyk (Ból) + Przyciski akcji po prawej stronie
dolna_stat_ramka = ttk.Frame(ramka_dolna)
dolna_stat_ramka.pack(fill="x", pady=(5, 2))

etykieta_sredni_bol = ttk.Label(dolna_stat_ramka, text="Średni ból: -", font=("Arial", 10))
etykieta_sredni_bol.pack(side="left", padx=10)

etykieta_mediana_bol = ttk.Label(dolna_stat_ramka, text="Mediana bólu: -", font=("Arial", 10))
etykieta_mediana_bol.pack(side="left", padx=10)

etykieta_std_bol = ttk.Label(dolna_stat_ramka, text="Odch. std. bólu: -", font=("Arial", 10))
etykieta_std_bol.pack(side="left", padx=10)

etykieta_min_max_bol = ttk.Label(dolna_stat_ramka, text="Min / Max ból: -", font=("Arial", 10))
etykieta_min_max_bol.pack(side="left", padx=10)

# Ramka na przyciski Jakość danych i Eksport CSV w dolnym panelu po prawej stronie
ramka_przyciski_dol = ttk.Frame(dolna_stat_ramka)
ramka_przyciski_dol.pack(side="right", padx=5)


def pokaz_jakosc_danych():
    braki = df.isnull().sum()

    wiek_kolumna = pd.to_numeric(df.get('Wiek'), errors='coerce')
    kolumna_bolu = 'Skala_Bolu_1_10' if 'Skala_Bolu_1_10' in df.columns else 'Skalo_Bolu_1_10'
    bol_kolumna = pd.to_numeric(df.get(kolumna_bolu), errors='coerce')

    niepoprawny_wiek = ((wiek_kolumna < 0) | (wiek_kolumna > 120)).sum()
    niepoprawny_bol = ((bol_kolumna < 1) | (bol_kolumna > 10)).sum()

    raport = "=== RAPORT JAKOŚCI DANYCH ===\n\n"
    raport += "Liczba braków danych (NaN) w kolumnach:\n"
    for kolumna, liczba_brakow in braki.items():
        raport += f"• {kolumna}: {liczba_brakow} braków\n"

    raport += f"\nKontrola zakresów logicznych:\n"
    raport += f"• Wiek poza zakresem (0-120 lat): {niepoprawny_wiek}\n"
    raport += f"• Skala bólu poza zakresem (1-10): {niepoprawny_bol}\n"

    messagebox.showinfo("Jakość danych (Data Quality)", raport)
    etykieta_status.config(text="Status: Sprawdzono jakość danych")


def eksportuj_csv():
    dane_f = pobierz_filtrowane_dane()
    if dane_f.empty:
        messagebox.showinfo("Brak danych", "Nie ma danych do eksportowania.")
        return

    sciezka = filedialog.asksaveasfilename(
        title="Zapisz filtrowane dane",
        defaultextension=".csv",
        filetypes=[("Pliki CSV", "*.csv")]
    )
    if sciezka:
        try:
            dane_f.to_csv(sciezka, index=False, encoding="utf-8-sig")
            etykieta_status.config(text="Status: Wyeksportowano dane")
            messagebox.showinfo("Eksport zakończony", "Dane zostały zapisane do pliku CSV.")
        except OSError as blad:
            messagebox.showerror("Błąd zapisu", f"Nie udało się zapisać pliku:\n{blad}")


przycisk_eksport = ttk.Button(ramka_przyciski_dol, text="💾 Eksport CSV", command=eksportuj_csv, width=14)
przycisk_eksport.pack(side="right", padx=5)

przycisk_jakosc = ttk.Button(ramka_przyciski_dol, text="🔍 Jakość danych", command=pokaz_jakosc_danych, width=15)
przycisk_jakosc.pack(side="right", padx=5)

etykieta_status = ttk.Label(ramka_dolna, text="Status: Gotowy do pracy", font=("Arial", 9, "italic"))
etykieta_status.pack(anchor="w", padx=10, pady=(5, 0))

# --- 2. GÓRNA RAMKA (FILTRY) ---
ramka_gorna = ttk.Frame(okno, padding="10")
ramka_gorna.pack(side="top", fill="x", padx=10, pady=10)


def resetuj_filtry():
    wybor_grupy.set("Wszyscy")
    wybor_cwiczen.set("Wszyscy")
    wybor_stylu.set("Wszyscy")
    wybor_wykresu.set("Wiek a ból")
    wybor_widoku.set("Wykres")
    zmien_widok()
    rysuj_wykres()
    etykieta_status.config(text="Status: Zresetowano filtry")


# 1. Wybór typu wykresu
etykieta_wykres = ttk.Label(ramka_gorna, text="Wykres:")
etykieta_wykres.pack(side="left", padx=2)
wybor_wykresu = ttk.Combobox(
    ramka_gorna,
    values=[
        "Wiek a ból",
        "Płeć a ból",
        "Histogram poziomu bólu",
        "Wykres rozrzutu (Wiek vs Ból)",
        "Aktywność fizyczna a ból",
        "Porównanie grup pacjentów"
    ],
    state="readonly",
    width=26
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

# Przycisk resetowania filtrów po prawej stronie w górnej ramce
przycisk_reset = ttk.Button(ramka_gorna, text="🔄 Resetuj filtry", command=resetuj_filtry, width=15)
przycisk_reset.pack(side="right", padx=5)

# --- 3. ŚRODKOWA CZĘŚĆ (WYKRES / TABELA) ---
ramka_srodek = ttk.Frame(okno, padding="10")
ramka_srodek.pack(side="top", fill="both", expand=True, padx=10, pady=5)

fig, ax = plt.subplots(figsize=(6, 4), dpi=100)
canvas = FigureCanvasTkAgg(fig, master=ramka_srodek)
canvas.get_tk_widget().pack(fill="both", expand=True)

# Ramka na tabelę (domyślnie ukryta)
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
        ramka_tabela.pack_forget()
        ramka_srodek.pack(side="top", fill="both", expand=True, padx=10, pady=5)
    else:
        ramka_srodek.pack_forget()
        ramka_tabela.pack(side="top", fill="both", expand=True, padx=10, pady=5)


def pobierz_filtrowane_dane():
    dane_f = df.copy()

    grupa = wybor_grupy.get()
    aktywnosc = wybor_cwiczen.get()
    styl_pracy = wybor_stylu.get()

    if grupa != "Wszyscy":
        dane_f = dane_f[dane_f['Odcinek'].astype(str).str.strip().str.lower() == grupa.lower()]

    if aktywnosc != "Wszyscy":
        dane_f = dane_f[dane_f['Regularne_cwiczenia'].astype(str).str.strip().str.lower() == aktywnosc.lower()]

    if styl_pracy != "Wszyscy":
        dane_f = dane_f[dane_f['Praca_siedzaca'].astype(str).str.strip().str.lower() == styl_pracy.lower()]

    return dane_f


def rysuj_wykres(event=None):
    typ = wybor_wykresu.get()
    dane_f = pobierz_filtrowane_dane()

    # --- OBLICZENIA STATYSTYCZNE ---
    liczba_pacjentow = len(dane_f)
    sredni_wiek = dane_f['Wiek'].mean() if liczba_pacjentow > 0 else 0
    mediana_wieku = dane_f['Wiek'].median() if liczba_pacjentow > 0 else 0

    kolumna_bolu = 'Skala_Bolu_1_10' if 'Skala_Bolu_1_10' in dane_f.columns else 'Skalo_Bolu_1_10'
    bol_seria = pd.to_numeric(dane_f.get(kolumna_bolu, pd.Series(dtype=float)), errors='coerce').dropna()

    sredni_bol = bol_seria.mean() if not bol_seria.empty else 0
    mediana_bol = bol_seria.median() if not bol_seria.empty else 0
    std_bol = bol_seria.std() if len(bol_seria) > 1 else 0
    min_bol = bol_seria.min() if not bol_seria.empty else 0
    max_bol = bol_seria.max() if not bol_seria.empty else 0

    # Aktualizacja etykiet statystyk
    etykieta_liczba_pacjentow.config(text=f"Liczba pacjentów: {liczba_pacjentow}")
    etykieta_sredni_wiek.config(text=f"Średni wiek: {sredni_wiek:.1f}" if pd.notna(sredni_wiek) else "Średni wiek: -")
    etykieta_mediana_wieku.config(
        text=f"Mediana wieku: {mediana_wieku:.1f}" if pd.notna(mediana_wieku) else "Mediana wieku: -")

    etykieta_sredni_bol.config(text=f"Średni ból: {sredni_bol:.2f}" if pd.notna(sredni_bol) else "Średni ból: -")
    etykieta_mediana_bol.config(text=f"Mediana bólu: {mediana_bol:.1f}" if pd.notna(mediana_bol) else "Mediana bólu: -")
    etykieta_std_bol.config(text=f"Odch. std. bólu: {std_bol:.2f}" if pd.notna(std_bol) else "Odch. std. bólu: -")
    etykieta_min_max_bol.config(
        text=f"Min / Max ból: {int(min_bol)} / {int(max_bol)}" if not bol_seria.empty else "Min / Max ból: - / -")

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
            ax.text(0.5, 0.5, "Brak danych dla wybranego filtra", ha='center', va='center', transform=ax.transAxes)

    elif typ == "Histogram poziomu bólu":
        if not bol_seria.empty:
            ax.hist(bol_seria, bins=8, color='#e74c3c', edgecolor='black', alpha=0.85)
            ax.set_title("Histogram poziomu bólu pacjentów")
            ax.set_xlabel("Skala bólu (1-10)")
            ax.set_ylabel("Liczba pacjentów")
            ax.grid(axis='y', linestyle='--', alpha=0.6)
        else:
            ax.text(0.5, 0.5, "Brak danych dla wybranego filtra", ha='center', va='center', transform=ax.transAxes)

    elif typ == "Wykres rozrzutu (Wiek vs Ból)":
        if not dane_f.empty and len(dane_f) > 1:
            x = dane_f['Wiek']
            y = dane_f['Skala_Bolu_1_10']
            korelacja = x.corr(y)

            ax.scatter(x, y, color='#2980b9', alpha=0.7, edgecolors='black', s=60)
            ax.set_title(f"Zależność wieku od bólu (Korelacja r = {korelacja:.2f})")
            ax.set_xlabel("Wiek (lata)")
            ax.set_ylabel("Skala bólu (1-10)")
            ax.grid(True, linestyle='--', alpha=0.6)
        else:
            ax.text(0.5, 0.5, "Za mało danych do analizy korelacji", ha='center', va='center', transform=ax.transAxes)

    elif typ == "Płeć a ból":
        srednie_bolu = dane_f.groupby('Plec')['Skala_Bolu_1_10'].mean()

        if not srednie_bolu.empty:
            ax.bar(srednie_bolu.index, srednie_bolu.values, color=['#e74c3c', '#3498db'], edgecolor='black', alpha=0.85)
            ax.set_title("Średni poziom bólu w zależności od płci")
            ax.set_xlabel("Płeć")
            ax.set_ylabel("Średnia skala bólu (1-10)")
            ax.grid(axis='y', linestyle='--', alpha=0.6)
        else:
            ax.text(0.5, 0.5, "Brak danych dla wybranego filtra", ha='center', va='center', transform=ax.transAxes)

    elif typ == "Aktywność fizyczna a ból":
        srednie_bolu = dane_f.groupby('Regularne_cwiczenia')['Skala_Bolu_1_10'].mean()

        if not srednie_bolu.empty:
            ax.bar(srednie_bolu.index, srednie_bolu.values, color=['#27ae60', '#e74c3c'], edgecolor='black', alpha=0.85)
            ax.set_title("Średni poziom bólu u osób ćwiczących i niećwiczących")
            ax.set_xlabel("Regularne ćwiczenia fizyczne")
            ax.set_ylabel("Średnia skala bólu (1-10)")
            ax.grid(axis='y', linestyle='--', alpha=0.6)
        else:
            ax.text(0.5, 0.5, "Brak danych dla wybranego filtra", ha='center', va='center', transform=ax.transAxes)

    elif typ == "Porównanie grup pacjentów":
        srednie_cw = dane_f.groupby('Regularne_cwiczenia')['Skala_Bolu_1_10'].mean()
        srednie_pr = dane_f.groupby('Praca_siedzaca')['Skala_Bolu_1_10'].mean()

        kategorie = []
        wartosci = []
        kolory = []

        if 'Tak' in srednie_cw.index:
            kategorie.append('Ćwiczenia: Tak')
            wartosci.append(srednie_cw['Tak'])
            kolory.append('#27ae60')
        if 'Nie' in srednie_cw.index:
            kategorie.append('Ćwiczenia: Nie')
            wartosci.append(srednie_cw['Nie'])
            kolory.append('#e74c3c')
        if 'Tak' in srednie_pr.index:
            kategorie.append('Praca siedząca: Tak')
            wartosci.append(srednie_pr['Tak'])
            kolory.append('#e67e22')
        if 'Nie' in srednie_pr.index:
            kategorie.append('Praca siedząca: Nie')
            wartosci.append(srednie_pr['Nie'])
            kolory.append('#3498db')

        if kategorie:
            slupki = ax.bar(kategorie, wartosci, color=kolory, edgecolor='black', alpha=0.85)
            ax.bar_label(slupki, fmt='%.2f', padding=3)
            ax.set_title("Porównanie poziomu bólu w zależności od stylu życia")
            ax.set_xlabel("Czynnik stylu życia")
            ax.set_ylabel("Średnia skala bólu (1-10)")
            ax.set_ylim(0, 10)
            ax.grid(axis='y', linestyle='--', alpha=0.6)
            plt.setp(ax.get_xticklabels(), rotation=15, ha='right')
        else:
            ax.text(0.5, 0.5, "Brak danych dla wybranego filtra", ha='center', va='center', transform=ax.transAxes)

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