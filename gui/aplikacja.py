import tkinter as tk
import pandas as pd
import matplotlib.pyplot as plt

# 1. WCZYTANIE DANYCH
try:
    df = pd.read_csv('data/dane_pacjenci_bol_plecow.csv')
except FileNotFoundError:
    df = pd.read_csv('../data/dane_pacjenci_bol_plecow.csv')

# 2. FUNKCJE
def pokaz_wiek():
    plt.hist(df['Wiek'], color='lightgreen', edgecolor='black')
    plt.title('Rozkład wieku pacjentów')
    plt.show()

def pokaz_bol():
    # Poprawiona nazwa kolumny skali bólu
    srednia = df.groupby('Praca_Siedzaca')['Skala_Bolu_1_10'].mean()
    plt.bar(['Brak pracy siedzącej', 'Praca siedząca'], srednia, color=['skyblue', 'salmon'])
    plt.title('Ból a praca siedząca')
    plt.show()

# 3. BUDOWA OKIENKA
okno = tk.Tk()
okno.title("Projekt - Analiza")
okno.geometry("300x200")

# 4. DODANIE PRZYCISKÓW DO OKIENKA
przycisk1 = tk.Button(okno, text="1. Pokaż wykres wieku", command=pokaz_wiek)
przycisk1.pack(pady=20)

przycisk2 = tk.Button(okno, text="2. Pokaż wykres bólu", command=pokaz_bol)
przycisk2.pack()

# Odpalenie aplikacji
okno.mainloop()