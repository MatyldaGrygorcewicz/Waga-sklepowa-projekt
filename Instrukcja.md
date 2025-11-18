# =€ Instrukcja Szybkiego Startu - Waga Sklepowa AI

## Witaj w systemie Waga Sklepowa AI!

To jest inteligentny system rozpoznawania owoców i warzyw, który wykorzystuje AI do automatycznego identyfikowania produktów, szacowania wagi i obliczania cen.

---

## ¡ Szybki start (3 kroki)

### 1. Zainstaluj zale|no[ci

Otwórz terminal w katalogu projektu i uruchom:

```bash
# Utwórz wirtualne [rodowisko (opcjonalne, ale zalecane)
python -m venv venv
venv\Scripts\activate

# Zainstaluj wymagane biblioteki
cd backend
pip install -r requirements.txt
```

### 2. Uruchom aplikacj

**Opcja A - Automatyczny start (Windows):**
```bash
# Kliknij dwukrotnie na plik start.bat lub uruchom:
start.bat
```

**Opcja B - Manualny start:**

Terminal 1 (Backend):
```bash
cd backend
python app.py
```

Terminal 2 (Frontend):
```bash
cd frontend
python -m http.server 8000
```

### 3. Otwórz przegldark

Przejdz do: **http://localhost:8000**

---

## =ñ Jak u|ywa aplikacji

1. **Kliknij "=÷ WBcz kamer"** - Zezwól przegldarce na dostp do kamery

2. **Umie[ owoc/warzywo przed kamer** - Upewnij si, |e jest dobrze o[wietlone i widoczne

3. **Kliknij " Skanuj produkt"** - System automatycznie:
   - Rozpozna produkt (97% dokBadno[ci)
   - Oszacuje wag
   - Obliczy cen

4. **Sprawdz wyniki** i kliknij:
   - **"=Ò Dodaj do koszyka"** - je[li wynik jest poprawny
   - **" Popraw rcznie"** - je[li chcesz zmieni produkt

5. **Kontynuuj skanowanie** kolejnych produktów

6. **Kliknij "=³ Przejdz do kasy"** gdy skoDczysz

---

## <¯ Co rozpoznaje system?

System rozpoznaje **131 ró|nych typów** owoców i warzyw, w tym:

- **Owoce:** jabBka (13 odmian), banany, truskawki, winogrona, cytrusy, brzoskwinie, [liwki, mango, i wiele innych
- **Warzywa:** pomidory, papryka, ogórki, cebula, ziemniaki, bakBa|an, i wicej
- **Orzechy:** wBoskie, laskowe, pekan, kasztany

PeBna lista jest w pliku `model_info.json`.

---

## ™ Wymagania techniczne

- **Python 3.8+**
- **Kamera** (wbudowana w laptop lub zewntrzna USB)
- **Przegldarka:** Chrome, Firefox, Edge lub Safari
- **RAM:** minimum 4 GB
- **Miejsce na dysku:** ~500 MB

---

## =' Rozwizywanie problemów

### Problem: Backend si nie uruchamia
**Rozwizanie:**
```bash
pip install --upgrade tensorflow flask flask-cors pillow numpy
```

### Problem: Kamera nie dziaBa
**Rozwizanie:**
- Sprawdz uprawnienia przegldarki (kliknij ikon kBódki w pasku adresu)
- U|yj `localhost` (nie u|ywaj adresu IP)
- Zamknij inne aplikacje u|ywajce kamery

### Problem: BBd "Module not found"
**Rozwizanie:**
```bash
# Upewnij si, |e jeste[ w [rodowisku wirtualnym
venv\Scripts\activate
# Zainstaluj ponownie wszystkie zale|no[ci
pip install -r backend/requirements.txt
```

### Problem: Model nie Baduje si
**Rozwizanie:**
- Sprawdz czy istniej pliki:
  - `fruit_classifier_model.h5` (31.9 MB)
  - `model_info.json` (2.6 KB)
- Upewnij si, |e s w gBównym katalogu projektu

---

## =Ö Wicej informacji

Dla peBnej dokumentacji zobacz plik **README.md**

---

## =¡ Wskazówki dla najlepszych wyników

1. ( **O[wietlenie** - U|ywaj dobrego, równomiernego [wiatBa
2. <¯ **Kadr** - Umie[ produkt centralnie, wypeBniajc wikszo[ kadru
3. =Ï **OdlegBo[** - Trzymaj kamer w odlegBo[ci 20-40 cm od produktu
4. = **Skupienie** - Poczekaj a| obraz jest ostry przed skanowaniem
5. = **Alternatywy** - Je[li rozpoznanie jest niepewne, obró produkt i spróbuj ponownie

---

## <“ Cel projektu

Ten projekt zostaB stworzony w celach **edukacyjnych** do demonstracji:
- Integracji modeli uczenia maszynowego z aplikacjami webowymi
- Przetwarzania obrazów w czasie rzeczywistym
- Tworzenia przyjaznych interfejsów u|ytkownika
- Praktycznego zastosowania Computer Vision w handlu

---

## =Ê Specyfikacja modelu

- **Typ:** Convolutional Neural Network (CNN)
- **Framework:** TensorFlow/Keras
- **DokBadno[:** 97.09%
- **Klasy:** 131 typów owoców i warzyw
- **Rozmiar wej[cia:** 32×32 pixels
- **Rozmiar modelu:** 31.9 MB
- **Data treningu:** 2025-11-18

---

## > Pomoc

Je[li potrzebujesz pomocy:
1. Przeczytaj sekcj "Rozwizywanie problemów" powy|ej
2. Sprawdz peBn dokumentacj w README.md
3. Sprawdz logi w terminalu (backend) i konsoli przegldarki (F12)

---

**MiBego u|ytkowania! <‰**

Stworzono z d do nauki i eksperymentowania z AI
