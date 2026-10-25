# Specyfikacja Techniczna i Funkcjonalna Aplikacji: Analiza Bólu Pleców

## 1. Cel i Przeznaczenie Aplikacji
Aplikacja jest systemem desktopowym stworzonym w języku Python, służącym do gromadzenia, zarządzania oraz analitycznego przeglądu danych medycznych pacjentów skarżących się na bóle pleców. Narzędzie ma na celu ułatwienie pracy specjalistom (np. fizjoterapeutom) poprzez automatyzację obliczeń statystycznych oraz wizualizację kluczowych parametrów zdrowotnych.

---

## 2. Opis Interfejsu Użytkownika (GUI)
Interfejs graficzny został zaprojektowany z wykorzystaniem biblioteki **Tkinter** warchitekturze okienkowej:
* **Główne okno aplikacji:** Zawiera menu nawigacyjne, tabelę podglądu danych pacjentów (wykorzystującą komponent `Treeview`) oraz panel przycisków funkcyjnych.
* **Formularze modalne (`tk.Toplevel`):** Wykorzystywane do wprowadzania nowych rekordów pacjentów oraz edycji istniejących danych, co zapewnia walidację wprowadzanych wartości przed ich zapisem.
* **Moduł wykresów:** Oddzielne okna i panele generujące wykresy analityczne oparte o bibliotekę **Matplotlib**.

---

## 3. Logika Działania i Architektura
* **Hybrydowe źródło danych:** Aplikacja operuje na plikach **CSV** oraz relacyjnej bazie danych **SQLite3**, co zapewnia elastyczność w odczycie i zapisie informacji.
* **Filtrowanie i wyszukiwanie:** Użytkownik ma możliwość filtrowania danych według parametrów bólowych, wieku oraz wskaźników klinicznych w czasie rzeczywistym.
* **Automatyczne raportowanie:** Moduł analityczny na bieżąco oblicza podstawowe statystyki opisowe (średnie, mediana, odchylenia) oraz generuje automatyczne wnioski tekstowe opisujące badaną grupę.

---
* `tkinter` (wbudowane w standardową bibliotekę Pythona) – do obsługi interfejsu graficznego,
* `sqlite3` – do obsługi bazy danych.
