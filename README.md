# 📊 YTGraphX - YouTube Statistics Tracker

Ein leistungsstarker Python-basierter YouTube-Statistik-Tracker, der Kanal-Daten mit interaktiven Diagrammen analysiert.

## ✨ Features

- 📊 **Interaktive Diagramme**: Abonnenten-, Aufruf- und Video-Entwicklung mit Plotly
- 🔍 **Kanal-Suche**: Suche nach Kanal-ID oder Benutzername
- 📈 **Trend-Analyse**: Historische Daten mit Wachstumstrends
- 🎨 **Modernes UI**: Streamlit-basierte Web-Oberfläche
- 💻 **CLI-Interface**: Kommandozeilen-Tool für Power-User
- 📱 **Responsive Design**: Funktioniert auf Desktop und Mobile
- ⚡ **Echtzeit-Daten**: Direkte YouTube Data API v3 Integration
- 💾 **Daten-Export**: CSV-Export für weitere Analysen

## 🛠️ Technologie-Stack

- **Backend**: Python 3.8+
- **Web Framework**: Streamlit
- **Visualisierung**: Plotly, Matplotlib
- **API**: Google YouTube Data API v3
- **Datenverarbeitung**: Pandas, NumPy
- **CLI**: argparse

## 📦 Installation

### 1. Repository klonen
```bash
git clone <repository-url>
cd YTGraphX
```

### 2. Python-Umgebung erstellen (empfohlen)
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# oder
venv\Scripts\activate     # Windows
```

### 3. Dependencies installieren
```bash
pip install -r requirements.txt
```

### 4. YouTube API Key konfigurieren
- Gehen Sie zu [Google Cloud Console](https://console.developers.google.com/)
- Erstellen Sie ein neues Projekt oder wählen Sie ein bestehendes
- Aktivieren Sie die YouTube Data API v3
- Erstellen Sie einen API Key
- Der API Key ist bereits in `config.py` konfiguriert

## 🚀 Verwendung

### Web-Interface (Streamlit)

Starten Sie die Streamlit-Anwendung:

```bash
streamlit run streamlit_app.py
```

Die Anwendung ist dann unter `http://localhost:8501` verfügbar.

**Features:**
- Interaktive Web-Oberfläche
- Echtzeit-Diagramme mit Plotly
- Daten-Export als CSV
- Responsive Design

### Kommandozeilen-Interface

Verwenden Sie das CLI-Tool für schnelle Analysen:

```bash
# Grundlegende Kanal-Analyse
python main.py @google

# Mit Diagramm-Speicherung
python main.py @pewdiepie --save-charts

# Mehr Videos anzeigen
python main.py @MrBeast --videos 10

# Ausgabe-Verzeichnis angeben
python main.py @TED --save-charts --output-dir my_analysis
```

**CLI-Optionen:**
- `--videos, -v`: Anzahl der neuesten Videos anzeigen
- `--save-charts, -s`: Diagramme als PNG-Dateien speichern
- `--output-dir, -o`: Ausgabe-Verzeichnis für Diagramme
- `--no-videos`: Keine Video-Informationen anzeigen

## 📊 Beispiel-Kanäle

Testen Sie die Anwendung mit diesen beliebten Kanälen:

- **Google**: `@google`
- **PewDiePie**: `@pewdiepie`
- **MrBeast**: `@MrBeast`
- **TED**: `@TED`
- **Kurzgesagt**: `@kurzgesagt`

## 📁 Projekt-Struktur

```
YTGraphX/
├── main.py                 # CLI-Interface
├── streamlit_app.py        # Streamlit Web-App
├── youtube_api.py          # YouTube API Integration
├── charts.py              # Diagramm-Erstellung
├── config.py              # Konfiguration
├── requirements.txt       # Python Dependencies
└── README.md             # Dokumentation
```

## 🔧 Konfiguration

### API-Limits
Die YouTube Data API v3 hat folgende Limits:
- 10.000 Quota-Einheiten pro Tag (kostenlos)
- 1 Einheit pro Kanal-Abfrage
- 1 Einheit pro Video-Abfrage

### Anpassungen
Bearbeiten Sie `config.py` für:
- API-Schlüssel
- Diagramm-Farben
- Historische Daten-Monat

## 📈 Diagramm-Typen

### 1. Abonnenten-Entwicklung
- Zeigt das Wachstum der Abonnentenzahl über Zeit
- Interaktive Hover-Informationen
- Trend-Analyse

### 2. Aufruf-Entwicklung
- Verfolgt die Gesamtaufrufe des Kanals
- Monatliche Entwicklung
- Durchschnittliche Aufrufe pro Video

### 3. Video-Entwicklung
- Anzahl der hochgeladenen Videos
- Upload-Häufigkeit
- Content-Produktivität

### 4. Kombinierte Ansicht
- Alle Metriken in einem Dashboard
- Vergleich verschiedener Zeiträume
- Gesamtübersicht

## 💾 Daten-Export

### CSV-Export
- **Statistiken**: Aktuelle Kanal-Metriken
- **Historische Daten**: Zeitreihen-Daten für alle Metriken
- **Video-Daten**: Informationen zu neuesten Videos

### Diagramm-Export
- **PNG-Format**: Hochauflösende Diagramme
- **Anpassbare Größe**: Verschiedene Auflösungen
- **Batch-Export**: Alle Diagramme auf einmal

## 🎨 Anpassung

### Diagramm-Farben
Bearbeiten Sie `config.py`:

```python
CHART_COLORS = {
    'subscribers': '#FF0000',  # YouTube Red
    'views': '#00D4AA',        # Teal
    'videos': '#FF6B35',       # Orange
    'background': '#0F0F0F',   # Dark background
    'grid': '#272727'          # Grid color
}
```

### Historische Daten
```python
HISTORICAL_MONTHS = 12  # Anzahl der Monate
```

## 🐛 Fehlerbehebung

### Häufige Probleme

1. **API-Quota überschritten**
   - Warten Sie bis zum nächsten Tag
   - Überprüfen Sie Ihren API-Key

2. **Kanal nicht gefunden**
   - Überprüfen Sie die Kanal-ID oder den Benutzernamen
   - Stellen Sie sicher, dass der Kanal öffentlich ist

3. **Import-Fehler**
   - Installieren Sie alle Dependencies: `pip install -r requirements.txt`
   - Überprüfen Sie Ihre Python-Version (3.8+)

## 🤝 Beitragen

Beiträge sind willkommen! Bitte:

1. Forken Sie das Repository
2. Erstellen Sie einen Feature-Branch
3. Committen Sie Ihre Änderungen
4. Erstellen Sie einen Pull Request

## 📄 Lizenz

MIT License - siehe LICENSE Datei für Details.

## 🆘 Support

Bei Fragen oder Problemen:

1. Überprüfen Sie die [Fehlerbehebung](#-fehlerbehebung)
2. Erstellen Sie ein Issue im Repository
3. Kontaktieren Sie den Entwickler

## 🔮 Roadmap

- [ ] Datenbank-Integration für historische Daten
- [ ] Mehrere Kanäle gleichzeitig vergleichen
- [ ] Erweiterte Statistiken (Engagement-Rate, etc.)
- [ ] Automatische Berichte per E-Mail
- [ ] Mobile App (React Native)

---

**Erstellt mit ❤️ für die YouTube-Community**