# 📤 Jak wypushować zmiany na GitHub

## Metoda 1: GitHub Desktop (najłatwiejsza)

1. Otwórz **GitHub Desktop**
2. Wybierz repo `Waga-sklepowa-projekt`
3. Zobaczysz commit "Przygotowanie do deployment..."
4. Kliknij **Push origin** (przycisk z strzałką w górę)
5. Gotowe!

---

## Metoda 2: Przez przeglądarkę (bez CLI)

1. Wejdź na https://github.com/MatyldaGrygorcewicz/Waga-sklepowa-projekt
2. Kliknij "Add file" → "Upload files"
3. Przeciągnij te pliki:
   - `build.sh`
   - `render.yaml`
   - `DEPLOYMENT.md`
   - `backend/app.py`
   - `backend/requirements.txt`
   - `frontend/app.js`
4. W opisie commit napisz: "Deployment configuration"
5. Kliknij "Commit changes"

---

## Metoda 3: Terminal z tokenem

```bash
cd "/mnt/c/projektyProgramistyczne/Waga sklepowa projekt"

# Użyj tego jeśli masz Personal Access Token
git push https://YOUR_TOKEN@github.com/MatyldaGrygorcewicz/Waga-sklepowa-projekt.git main
```

Zamień `YOUR_TOKEN` na swój GitHub Personal Access Token

---

## Stworzenie Personal Access Token (jeśli nie masz)

1. GitHub → Settings (prawy górny róg, Twój avatar)
2. Scroll w dół → **Developer settings**
3. **Personal access tokens** → **Tokens (classic)**
4. **Generate new token (classic)**
5. Nazwa: `Render Deployment`
6. Zaznacz: `repo` (pełny dostęp do repozytoriów)
7. **Generate token**
8. **SKOPIUJ TOKEN TERAZ** (nie zobaczysz go więcej!)

---

## Po pushu:

Wróć do Render Dashboard i:
1. Kliknij **Manual Deploy** → **Deploy latest commit**
2. Lub poczekaj - Render automatycznie wykryje nowy commit

---

## ⚠️ Jeśli nie chcesz pushować teraz

Możesz użyć **Szybkiego rozwiązania** z poprzedniej wiadomości:
- Zmień Build Command w Render na bezpośrednie polecenia
- Aplikacja będzie działać, ale bez nowych funkcji (upload + top 5)
