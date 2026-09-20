import tkinter as tk
import pandas as pd
import matplotlib.pyplot as plt

from tkinter import ttk

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

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