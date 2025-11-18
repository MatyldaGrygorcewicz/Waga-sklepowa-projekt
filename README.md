# 🍎 Waga Sklepowa AI - AI-Powered Shop Scale System

Inteligentny system rozpoznawania owoców i warzyw z wykorzystaniem sztucznej inteligencji, który automatycznie identyfikuje produkty, szacuje wagę i oblicza ceny.

## 📋 Spis treści

- [O projekcie](#o-projekcie)
- [Funkcje](#funkcje)
- [Technologie](#technologie)
- [Wymagania](#wymagania)
- [Instalacja](#instalacja)
- [Uruchomienie](#uruchomienie)
- [Struktura projektu](#struktura-projektu)
- [API Documentation](#api-documentation)
- [Jak używać](#jak-używać)
- [Możliwości rozwoju](#możliwości-rozwoju)

## 🎯 O projekcie

Waga Sklepowa AI to aplikacja webowa stworzona w celach edukacyjnych, która demonstruje praktyczne zastosowanie uczenia maszynowego w handlu detalicznym. System wykorzystuje kamerę do rozpoznawania 131 różnych typów owoców i warzyw z dokładnością 97.09%, a następnie szacuje ich wagę i automatycznie oblicza cenę.

### Kluczowe możliwości:
- ✅ Rozpoznawanie 131 typów owoców i warzyw
- ✅ Szacowanie wagi bez fizycznej wagi
- ✅ Automatyczne obliczanie cen
- ✅ Koszyk zakupowy z obsługą wielu produktów
- ✅ Interfejs w języku polskim
- ✅ Możliwość ręcznej korekty rozpoznania

## ✨ Funkcje

### 1. Rozpoznawanie AI
- Wykorzystanie wytrenowanego modelu TensorFlow/Keras
- Dokładność: 97.09%
- 131 kategorii produktów (owoce, warzywa, orzechy)
- Rozpoznawanie w czasie rzeczywistym

### 2. Szacowanie wagi
- Inteligentne szacowanie wagi na podstawie typu produktu
- Baza danych typowych wag dla każdego produktu
- Przedziały wagowe (min, typowa, max)

### 3. System cenowy
- Baza danych cen za kilogram (w PLN)
- Automatyczne obliczanie ceny końcowej
- Realistyczne ceny polskiego rynku

### 4. Koszyk zakupowy
- Dodawanie wielu produktów
- Podgląd sumy zakupów
- Usuwanie pojedynczych produktów
- Funkcja kasowania całego koszyka

### 5. Interfejs użytkownika
- Nowoczesny, responsywny design
- Polski interfejs
- Łatwa obsługa kamery
- Podgląd na żywo
- Wizualizacja pewności rozpoznania

## 🛠 Technologie

### Backend:
- **Python 3.x**
- **Flask** - framework webowy
- **TensorFlow/Keras** - uczenie maszynowe
- **SQLite** - baza danych
- **Pillow** - przetwarzanie obrazów
- **NumPy** - operacje numeryczne

### Frontend:
- **HTML5**
- **CSS3** (z gradientami i animacjami)
- **Vanilla JavaScript** (ES6+)
- **WebRTC** - dostęp do kamery

### Model ML:
- **Architektura:** CNN (Convolutional Neural Network)
- **Framework:** TensorFlow/Keras
- **Rozmiar wejścia:** 32x32 pixels
- **Liczba klas:** 131
- **Dokładność:** 97.09%

## 📦 Wymagania

### Systemowe:
- Python 3.8 lub nowszy
- Kamera (wbudowana lub USB)
- Przeglądarka wspierająca WebRTC (Chrome, Firefox, Edge, Safari)
- 4 GB RAM minimum
- 500 MB wolnego miejsca na dysku

### Python packages:
```
flask==3.0.0
flask-cors==4.0.0
tensorflow==2.15.0
numpy==1.24.3
pillow==10.1.0
gunicorn==21.2.0
```

## 🚀 Instalacja

### Krok 1: Sklonuj repozytorium lub przejdź do katalogu projektu

```bash
cd "Waga sklepowa projekt"
```

### Krok 2: Utwórz wirtualne środowisko Python (zalecane)

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/Mac
python3 -m venv venv
source venv/bin/activate
```

### Krok 3: Zainstaluj zależności

```bash
cd backend
pip install -r requirements.txt
```

### Krok 4: Sprawdź, czy model jest na miejscu

Upewnij się, że w głównym katalogu projektu znajdują się:
- `fruit_classifier_model.h5` (31.9 MB)
- `model_info.json` (2.6 KB)

## ▶️ Uruchomienie

### Metoda 1: Uruchomienie manualne

#### Uruchom backend (Terminal 1):
```bash
cd backend
python app.py
```

Backend będzie dostępny pod adresem: `http://localhost:5000`

#### Uruchom frontend (Terminal 2):
```bash
cd frontend
python -m http.server 8000
```

Frontend będzie dostępny pod adresem: `http://localhost:8000`

### Metoda 2: Użyj skryptu startowego (jeśli dostępny)

```bash
# Windows
start.bat

# Linux/Mac
./start.sh
```

## 📁 Struktura projektu

```
Waga sklepowa projekt/
│
├── backend/                          # Backend aplikacji
│   ├── app.py                       # Główna aplikacja Flask
│   ├── model_loader.py              # Ładowanie i obsługa modelu ML
│   ├── weight_estimator.py          # Szacowanie wagi produktów
│   ├── database.py                  # Obsługa bazy danych SQLite
│   └── requirements.txt             # Zależności Python
│
├── frontend/                         # Frontend aplikacji
│   ├── index.html                   # Struktura HTML
│   ├── styles.css                   # Style CSS
│   └── app.js                       # Logika JavaScript
│
├── data/                            # Dane aplikacji
│   └── products.db                  # Baza danych SQLite (tworzony automatycznie)
│
├── fruit_classifier_model.h5        # Wytrenowany model ML (31.9 MB)
├── model_info.json                  # Metadane modelu i etykiety
├── fruit_simple_just_data.ipynb     # Notatnik treningu modelu
└── README.md                        # Ten plik

```

## 🔌 API Documentation

### Endpoints:

#### `GET /`
Sprawdzenie statusu serwera
```json
{
  "status": "running",
  "app": "AI-Powered Shop Scale",
  "version": "1.0.0"
}
```

#### `POST /api/predict`
Rozpoznaj produkt i oblicz cenę
```json
// Request
{
  "image": "data:image/jpeg;base64,..."
}

// Response
{
  "success": true,
  "classification": {
    "product": "Apple Golden 1",
    "confidence": 98.5,
    "alternatives": [...]
  },
  "weight": {
    "weight_grams": 175.2,
    "weight_kg": 0.175,
    "confidence": "medium"
  },
  "price": {
    "product_name_polish": "Jabłko Golden",
    "price_per_kg": 5.50,
    "total_price": 0.96,
    "currency": "PLN"
  }
}
```

#### `GET /api/products`
Pobierz listę wszystkich produktów

#### `GET /api/product/<name>`
Pobierz informacje o konkretnym produkcie

#### `POST /api/calculate_price`
Oblicz cenę dla produktu i wagi

#### `POST /api/transaction`
Zapisz transakcję

#### `GET /api/transactions?limit=10`
Pobierz ostatnie transakcje

#### `GET /api/model_info`
Pobierz informacje o modelu ML

## 📱 Jak używać

### Podstawowy przepływ pracy:

1. **Uruchom aplikację**
   - Otwórz przeglądarkę i przejdź do `http://localhost:8000`

2. **Włącz kamerę**
   - Kliknij przycisk "📷 Włącz kamerę"
   - Zezwól na dostęp do kamery w przeglądarce

3. **Zeskanuj produkt**
   - Umieść owoc lub warzywo przed kamerą
   - Kliknij "✅ Skanuj produkt"
   - Poczekaj na wyniki rozpoznawania

4. **Sprawdź wyniki**
   - Zobacz rozpoznany produkt i pewność rozpoznania
   - Sprawdź szacowaną wagę
   - Zobacz obliczoną cenę

5. **Dodaj do koszyka**
   - Jeśli wynik jest prawidłowy, kliknij "🛒 Dodaj do koszyka"
   - Jeśli nieprawidłowy, kliknij "✏️ Popraw ręcznie" i wybierz właściwy produkt

6. **Kontynuuj zakupy**
   - Kliknij "🔄 Skanuj ponownie" dla kolejnych produktów
   - Obserwuj rosnącą sumę w koszyku

7. **Finalizuj zakupy**
   - Sprawdź zawartość koszyka
   - Kliknij "💳 Przejdź do kasy"

### Wskazówki:
- ✨ Zapewnij dobre oświetlenie
- 🎯 Umieść produkt centralnie w kadrze
- 📏 Utrzymuj odpowiednią odległość od kamery
- 🔄 Jeśli rozpoznanie jest niepewne, spróbuj ponownie lub użyj korekty ręcznej

## 🎓 Kontekst edukacyjny

Ten projekt został stworzony jako demonstracja praktycznego zastosowania uczenia maszynowego. Jest idealny do:

- Nauki integracji modeli ML z aplikacjami webowymi
- Zrozumienia pipeline'u przetwarzania obrazów
- Praktyki z REST API i asynchronicznym JavaScript
- Nauki tworzenia przyjaznych interfejsów użytkownika
- Eksperymentowania z Computer Vision

## 🔮 Możliwości rozwoju

### Krótkoterminowe:
- [ ] Dodanie autentykacji użytkowników
- [ ] Eksport rachunków do PDF
- [ ] Historia zakupów
- [ ] Statystyki sprzedaży
- [ ] Obsługa kodów kreskowych jako backup

### Długoterminowe:
- [ ] Integracja z fizyczną wagą (przez USB/Bluetooth)
- [ ] Trenowanie modelu do szacowania rozmiaru z obrazu
- [ ] Aplikacja mobilna (iOS/Android)
- [ ] Multi-kamerowe rozpoznawanie 3D
- [ ] Integracja z systemami kasowymi (POS)
- [ ] Rozpoznawanie wielu produktów jednocześnie
- [ ] Obsługa produktów pakowanych
- [ ] System promocji i rabatów

### Ulepszenia ML:
- [ ] Transfer learning na większym modelu
- [ ] Data augmentation dla lepszej generalizacji
- [ ] Obsługa różnych kątów i oświetleń
- [ ] Detekcja jakości/dojrzałości produktów
- [ ] Rozpoznawanie defektów

## 🐛 Rozwiązywanie problemów

### Backend nie startuje:
```bash
# Sprawdź czy TensorFlow jest zainstalowany
python -c "import tensorflow; print(tensorflow.__version__)"

# Przeinstaluj zależności
pip install --upgrade -r backend/requirements.txt
```

### Kamera nie działa:
- Sprawdź uprawnienia przeglądarki
- Użyj HTTPS (lub localhost)
- Sprawdź czy kamera nie jest używana przez inną aplikację

### Błędy CORS:
- Upewnij się, że backend działa na porcie 5000
- Sprawdź czy flask-cors jest zainstalowany
- Otwórz konsolę przeglądarki (F12) dla szczegółów

### Model nie ładuje się:
- Sprawdź czy `fruit_classifier_model.h5` istnieje
- Sprawdź czy `model_info.json` istnieje
- Upewnij się, że pliki nie są uszkodzone

## 👨‍💻 Autorzy

Projekt stworzony w celach edukacyjnych.

## 📄 Licencja

Projekt edukacyjny - użycie dozwolone w celach nauki i rozwoju.

## 🙏 Podziękowania

- Dataset: [Horea94/Fruit-Images-Dataset](https://github.com/Horea94/Fruit-Images-Dataset)
- TensorFlow/Keras team
- Flask framework
- Społeczność open source

---

**Made with ❤️ for learning and education**

## 📞 Pomoc

Jeśli napotkasz problemy:
1. Sprawdź sekcję "Rozwiązywanie problemów" powyżej
2. Przejrzyj logi w konsoli przeglądarki (F12)
3. Sprawdź logi backendu w terminalu
4. Upewnij się, że wszystkie wymagania są spełnione

---

Miłego kodowania! 🚀
