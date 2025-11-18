# 🚀 Deployment Guide - Waga Sklepowa AI

## Darmowy deployment na Render.com

Aplikacja jest gotowa do deployment na **Render.com** - darmowej platformie hostingowej.

---

## 📋 Przygotowania (już zrobione!)

✅ Pliki konfiguracyjne deployment:
- `render.yaml` - konfiguracja serwisu
- `build.sh` - skrypt budowania
- `backend/requirements.txt` - zależności Python
- `.gitignore` - ignorowane pliki

✅ Kod zaktualizowany:
- Backend serwuje również frontend
- API używa relatywnych URL
- CORS skonfigurowany

✅ Repository GitHub:
- https://github.com/MatyldaGrygorcewicz/Waga-sklepowa-projekt.git

---

## 🎯 Kroki deployment na Render.com

### Krok 1: Utwórz konto na Render

1. Przejdź na https://render.com
2. Kliknij **"Get Started for Free"**
3. Zaloguj się przez GitHub
4. Autoryzuj dostęp Render do swojego konta GitHub

### Krok 2: Utwórz nowy Web Service

1. W dashboard Render kliknij **"New +"** → **"Web Service"**

2. Połącz repository:
   - Kliknij **"Connect a repository"**
   - Znajdź `Waga-sklepowa-projekt` na liście
   - Kliknij **"Connect"**

3. Konfiguracja serwisu:

   **Name:** `waga-sklepowa-ai` (lub dowolna nazwa)

   **Region:** `Frankfurt` (najbliżej Polski)

   **Branch:** `main`

   **Root Directory:** zostaw puste

   **Runtime:** `Python 3`

   **Build Command:**
   ```
   ./build.sh
   ```

   **Start Command:**
   ```
   cd backend && gunicorn --bind 0.0.0.0:$PORT app:app
   ```

   **Instance Type:** `Free`

4. Zaawansowane ustawienia (kliknij "Advanced"):

   **Environment Variables:** Dodaj jeśli potrzebne
   - `PYTHON_VERSION`: `3.11.0`

   **Auto-Deploy:** `Yes` (włącz automatyczny deployment przy push do GitHub)

5. Kliknij **"Create Web Service"**

### Krok 3: Poczekaj na build

⏳ Render będzie:
1. Klonować repository z GitHub (1-2 min)
2. Instalować zależności Python (5-10 min - TensorFlow jest duży!)
3. Uruchamiać aplikację (1-2 min)

**Cały proces: około 10-15 minut**

### Krok 4: Sprawdź deployment

Po zakończeniu buildu zobaczysz:
- ✅ **"Live"** - status serwisu
- 🌐 **URL:** `https://waga-sklepowa-ai.onrender.com` (lub podobny)

Kliknij na URL żeby otworzyć aplikację!

---

## 🎉 Gotowe!

Twoja aplikacja jest teraz dostępna publicznie pod adresem Render!

### URL będzie wyglądał tak:
```
https://waga-sklepowa-ai-XXXX.onrender.com
```

### Możesz teraz:
- ✅ Udostępnić link znajomym
- ✅ Pokazać projekt na prezentacji
- ✅ Dodać do portfolio
- ✅ Testować z telefonu/tabletu

---

## 📱 Testowanie

1. Otwórz URL w przeglądarce
2. Kliknij "📁 Prześlij zdjęcie"
3. Wybierz zdjęcie owocu/warzywa
4. Zobacz top 5 wyników!

**Uwaga:** Kamera może nie działać na wszystkich urządzeniach ze względu na wymagania HTTPS i uprawnienia. Upload zdjęć zawsze działa!

---

## 🔄 Automatyczne aktualizacje

Po skonfigurowaniu, każdy push do GitHub automatycznie uruchamia nowy deployment!

```bash
git add .
git commit -m "Aktualizacja aplikacji"
git push
```

Render automatycznie zbuduje i wdroży nową wersję w ciągu 10-15 minut.

---

## ⚙️ Zarządzanie

### Dashboard Render:
- **Logs:** Zobacz logi aplikacji w czasie rzeczywistym
- **Metrics:** Monitoruj użycie CPU, pamięci
- **Settings:** Zmień konfigurację
- **Environment:** Zarządzaj zmiennymi środowiskowymi

### Zatrzymanie aplikacji:
- Jeśli chcesz oszczędzać zasoby, możesz zatrzymać serwis
- Free tier: serwis usypia się po 15 min bezczynności
- Pierwsze żądanie po uśpieniu trwa ~30 sekund (cold start)

---

## 💰 Koszty

**Free Tier obejmuje:**
- ✅ 750 godzin/miesiąc (wystarczy na 24/7 przez cały miesiąc!)
- ✅ Automatyczny SSL (HTTPS)
- ✅ Automatyczne deploymenty z GitHub
- ✅ Podstawowe metryki
- ⚠️ Serwis usypia się po 15 min bezczynności
- ⚠️ Pierwsze żądanie po uśpieniu: ~30 sekund

**Paid tier ($7/miesiąc):**
- Brak uśpiania
- Więcej zasobów CPU/RAM
- Priorytetowe wsparcie

---

## 🐛 Rozwiązywanie problemów

### Build failuje:
- Sprawdź logi w Render Dashboard
- Upewnij się że `build.sh` ma uprawnienia wykonywania
- Sprawdź czy wszystkie pliki są w repo GitHub

### Aplikacja nie startuje:
- Sprawdź logi w sekcji "Logs"
- Zweryfikuj czy ścieżki w `render.yaml` są poprawne
- Upewnij się że model `.h5` jest w repo (31.9 MB)

### Błąd 404:
- Sprawdź czy pliki frontend są w folderze `frontend/`
- Zweryfikuj routing w `app.py`

### TensorFlow errors:
- Render używa CPU (brak GPU na free tier)
- To normalne - model działa na CPU
- Predykcja zajmuje 2-5 sekund

---

## 📞 Wsparcie

- **Render Docs:** https://render.com/docs
- **Community:** https://community.render.com
- **Status:** https://status.render.com

---

## 🎓 Alternatywne platformy

Jeśli Render nie działa, inne opcje:

1. **Railway.app**
   - Podobny do Render
   - 500h darmowo/miesiąc
   - https://railway.app

2. **Fly.io**
   - Darmowy tier
   - Bardziej skomplikowany setup
   - https://fly.io

3. **PythonAnywhere**
   - Specjalizuje się w Pythonie
   - Ograniczenia na free tier
   - https://www.pythonanywhere.com

---

**Powodzenia z deploymentem! 🚀**

Jeśli masz pytania, sprawdź logi w Render Dashboard lub dokumentację.
