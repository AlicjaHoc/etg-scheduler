# ETG Scheduler - opis projektu dla studenta

Ten projekt jest aplikacja konsolowa w Pythonie do harmonogramowania rozszerzonego grafu zadan, czyli Extended Task Graph. Program wczytuje scenariusz z pliku JSON, sprawdza poprawność danych, dobiera zasoby do zadan, wyznacza harmonogram wykonania i zapisuje wyniki do plikow.

Projekt jest przygotowany jako praktyczna praca akademicka. Kod jest prosty, czytelny i skupiony na algorytmie, a nie na dodatkowej infrastrukturze.

Glowny scenariusz projektu dotyczy procesu budowy elektrowni wodnej. Program nadal potrafi wczytac dowolny scenariusz ETG zapisany w tym samym formacie JSON.

## Co robi aplikacja

Aplikacja:

- pokazuje menu wyboru scenariusza,
- pozwala wybrac tryb optymalizacji,
- wczytuje zadania i zasoby z JSON,
- waliduje zaleznosci w grafie,
- wykrywa cykle,
- sprawdza, czy kazde zadanie moze dostac zgodny zestaw zasobow,
- buduje harmonogram metoda zachlanna,
- moze uzyc algorytmu genetycznego do minimalizacji kosztu przy ograniczeniu czasu,
- oblicza czas startu i zakonczenia kazdego zadania,
- oblicza koszt kazdego zadania,
- oblicza laczny czas wykonania i laczny koszt,
- pokazuje wykorzystanie zasobow,
- pokazuje prosta tekstowa os czasu dla zasobow,
- eksportuje wynik do JSON, CSV i raportu Markdown.

## Czym jest Extended Task Graph

Klasyczny graf zadan to graf skierowany, w ktorym:

- wierzcholki oznaczaja zadania,
- krawedzie oznaczaja zaleznosci,
- zadanie moze wystartowac dopiero wtedy, gdy jego poprzednicy zostali zaplanowani.

Extended Task Graph rozszerza ten model o typy zadan i typy zasobow. Nie kazde zadanie moze byc wykonane przez kazdy zasob. Niektore zadania wymagaja zasobu wyspecjalizowanego, inne dowolnego, a jeszcze inne kilku zasobow jednoczesnie.

## Typy zadan w projekcie

### DT - Dedicated Task

Zadanie dedykowane wymaga jednego zasobu specjalistycznego. Przyklad: badanie przez lekarza albo ciecie elementow przez konkretna maszyne.

W JSON takie zadanie ma `task_type` ustawione na `DT` i musi miec wpisane `required_specializations`.

### GT - General Task

Zadanie ogolne wymaga jednego zasobu. Moze to byc zasob uniwersalny albo specjalistyczny.

Przyklad: rejestracja pacjenta, kontrola materialu, przygotowanie dokumentow.

### UT - Universal Task

Zadanie uniwersalne moze byc wykonane tylko przez zasob typu `Universal`.

Przyklad: prosta praca pomocnicza, monitoring, aktualizacja danych, czynnosci niewymagajace specjalizacji.

### CDT - Common Dedicated Task

Zadanie wspolne dedykowane wymaga kilku zasobow specjalistycznych jednoczesnie.

Przyklad: operacja w szpitalu wymaga chirurga, pielegniarki i sali operacyjnej. Zadanie nie moze wystartowac, dopoki wszystkie te zasoby nie sa wolne.

### CGT - Common General Task

Zadanie wspolne ogolne wymaga kilku zasobow dowolnego typu jednoczesnie.

Przyklad: pakowanie, rozladunek ciezarowki albo sortowanie paczek.

## Typy zasobow

### Universal

Zasob uniwersalny jest elastyczny. Moze wykonywac zadania ogolne i uniwersalne. Zwykle jest tanszy, ale moze byc wolniejszy.

### Specialized

Zasob specjalistyczny ma konkretna specjalizacje, na przyklad:

- `Doctor`,
- `Surgeon`,
- `Nurse`,
- `OperatingRoom`,
- `MachineA`,
- `RobotArm`,
- `ForkliftOperator`.

Specjalizacja jest uzywana przy dopasowaniu zasobow do zadan typu `DT` i `CDT`.

## Najwazniejsze pola zadania

Kazde zadanie ma:

- `id` - unikalny identyfikator,
- `name` - nazwe,
- `task_type` - typ zadania,
- `duration` - bazowy czas trwania,
- `dependencies` - liste identyfikatorow zadan, ktore musza byc wykonane wczesniej,
- `required_specializations` - wymagane specjalizacje,
- `required_resource_count` - liczbe potrzebnych zasobow,
- `base_cost` - dodatkowy koszt niezalezny od czasu pracy,
- `description` - krotki opis.

## Najwazniejsze pola zasobu

Kazdy zasob ma:

- `id` - unikalny identyfikator,
- `name` - nazwe,
- `resource_type` - `Universal` albo `Specialized`,
- `specialization` - specjalizacje dla zasobow specjalistycznych,
- `cost_per_time_unit` - koszt za jednostke czasu,
- `speed_multiplier` - mnoznik szybkosci.

Jesli `speed_multiplier` jest wiekszy niz 1, zasob wykonuje prace szybciej. Jesli jest mniejszy niz 1, wykonuje ja wolniej.

## Jak liczony jest czas trwania zadania

Dla jednego zasobu:

```text
rzeczywisty czas = bazowy czas / speed_multiplier
```

Dla kilku zasobow jednoczesnie program bierze sredni mnoznik szybkosci przypisanych zasobow:

```text
rzeczywisty czas = bazowy czas / sredni speed_multiplier
```

To jest uproszczony model, ale jest logiczny i latwy do wyjasnienia podczas prezentacji.

## Jak liczony jest koszt

Koszt zadania to:

```text
koszt = rzeczywisty czas * suma kosztow przypisanych zasobow za jednostke czasu + base_cost
```

Przy zadaniach wymagajacych kilku zasobow koszt obejmuje wszystkie zasoby pracujace jednoczesnie.

## Walidacja danych

Przed harmonogramowaniem program sprawdza:

- czy identyfikatory zadan sa unikalne,
- czy identyfikatory zasobow sa unikalne,
- czy wszystkie zaleznosci wskazuja na istniejace zadania,
- czy zadanie nie zalezy samo od siebie,
- czy graf zadan nie ma cyklu,
- czy typ zadania zgadza sie z liczba wymaganych zasobow,
- czy zadanie typu `DT` ma wymagana specjalizacje,
- czy zadanie typu `UT` nie wymaga specjalizacji,
- czy kazde zadanie ma przynajmniej jedno mozliwe dopasowanie zasobow.

Wykrywanie cyklu jest zrobione w prosty sposob w kodzie programu, bez dodatkowej biblioteki grafowej.

## Algorytm harmonogramowania

Program uzywa zachlannego algorytmu listowego. Algorytm nie gwarantuje najlepszego matematycznie wyniku, ale jest poprawny logicznie i prosty do omowienia.

Kroki algorytmu:

1. Wczytaj scenariusz.
2. Utworz liste zadan jeszcze niezaplanowanych.
3. Ustaw dostepnosc wszystkich zasobow na czas 0.
4. Znajdz zadania gotowe, czyli takie, ktorych zaleznosci sa juz zaplanowane.
5. Dla kazdego gotowego zadania wygeneruj wszystkie zgodne przypisania zasobow.
6. Dla kazdego kandydata policz najwczesniejszy start.
7. Policz czas zakonczenia i koszt.
8. Wybierz najlepszego kandydata wedlug trybu optymalizacji.
9. Dodaj zadanie do harmonogramu.
10. Zaktualizuj czas dostepnosci zasobow.
11. Powtarzaj, az wszystkie zadania beda zaplanowane.

## Tryby optymalizacji

### MinimizeTime

Program wybiera kandydata z najwczesniejszym czasem zakonczenia. Ten tryb preferuje szybkie wykonanie harmonogramu.

### MinimizeCost

Program wybiera kandydata o najnizszym koszcie. Ten tryb preferuje tansze zasoby, nawet jesli harmonogram trwa dluzej.

### Balanced

Program laczy czas i koszt. Dla aktualnych kandydatow normalizuje czas zakonczenia i koszt, a nastepnie liczy wynik:

```text
score = 0.6 * czas + 0.4 * koszt
```

Ten tryb lekko bardziej ceni czas, ale nadal uwzglednia koszt.

## Scenariusze przykladowe

Projekt zawiera cztery scenariusze:

- `scenarios/water_power_plant.json` - budowa elektrowni wodnej,
- `scenarios/hospital.json` - proces szpitalny,
- `scenarios/production_line.json` - linia produkcyjna,
- `scenarios/logistics_warehouse.json` - magazyn logistyczny.

Scenariusze pokazują wszystkie typy zadan i oba typy zasobow.

W scenariuszu elektrowni wodnej pole `time_constraint` oznacza maksymalny dopuszczalny czas harmonogramu dla algorytmu genetycznego.

## Jak uruchomic projekt

### Windows

```bat
setup_windows.bat
run_app.bat
```

### PowerShell

```powershell
.\setup_windows.ps1
.\.venv\Scripts\Activate.ps1
python -m etg_scheduler
```

### Terminal macOS/Linux

```bash
cd ~/etg-scheduler
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
pip install -r requirements.txt
python -m etg_scheduler
```

Na Pop!_OS i Ubuntu komenda `python` moze nie istniec globalnie. To normalne. Do utworzenia srodowiska uzyj `python3`, a po aktywacji `.venv` uzywaj `python`.

Kolejne uruchomienia:

```bash
cd ~/etg-scheduler
source .venv/bin/activate
python -m etg_scheduler
```

## Jak uruchomic konkretny scenariusz

Scenariusz wymagany w temacie projektu:

```bash
python -m etg_scheduler --scenario scenarios/water_power_plant.json --algorithm genetic
```

Z wlasnym ograniczeniem czasu:

```bash
python -m etg_scheduler --scenario scenarios/water_power_plant.json --algorithm genetic --time-constraint 48
```

```bash
python -m etg_scheduler --scenario scenarios/hospital.json --mode Balanced
```

```bash
python -m etg_scheduler --scenario scenarios/production_line.json --mode MinimizeTime
```

```bash
python -m etg_scheduler --scenario scenarios/logistics_warehouse.json --mode MinimizeCost
```

## Pliki wynikowe

Po udanym uruchomieniu program zapisuje wyniki w folderze `output/`:

- JSON z pelnym wynikiem,
- CSV z tabela harmonogramu,
- raport Markdown z podsumowaniem.

Nazwa pliku zawiera nazwe scenariusza i znacznik czasu.

## Jak testowac

Po instalacji zaleznosci:

```bash
pytest
```

Testy sprawdzaja walidator, harmonogramowanie i wszystkie przykladowe scenariusze.

## Jak wyjasnic projekt na prezentacji

Najprostsza struktura wypowiedzi:

1. Projekt dotyczy planowania zadan w rozszerzonym grafie zadan.
2. Kazde zadanie moze miec zaleznosci od innych zadan.
3. Zadania roznia sie wymaganiami dotyczacymi zasobow.
4. Zasoby moga byc uniwersalne albo specjalistyczne.
5. Program najpierw sprawdza poprawnosc danych.
6. Potem wykonuje zachlanne harmonogramowanie.
7. Dla kazdego kroku wybiera najlepsze aktualnie mozliwe zadanie i zasoby.
8. Na koncu pokazuje harmonogram, koszt, czas i wykorzystanie zasobow.

Najwazniejsza zaleta projektu: wynik jest latwy do przeanalizowania i uzasadnienia, bo kazdy wybor wynika z gotowych zadan, dostepnych zasobow, kosztu i czasu.
