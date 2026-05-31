# 🏠 Alfred — Home Assistant

> Your personal bedroom assistant. Alfred starts with alarm management and grows into a full smart bedroom controller — weather, lights, and more.

---

## 🚧 Project Status

Alfred is in early development. Features are being rolled out in phases.

| Phase | Feature | Status |
|-------|---------|--------|
| 1 | Alarm management | 🔨 In progress |
| 2 | Smart lights control | 📅 Planned |
| 3 | Weather forecast | 📅 Planned |
| 4 | General bedroom automation | 📅 Planned |

---

## Features

### Phase 1 — Alarm Management
- Set, edit, and delete alarms
- Recurring alarms (daily, weekdays, weekends, custom)
- Alarm labels and snooze support

### Phase 2 — Weather Forecast *(coming soon)*
- Morning briefing with today's forecast
- Alerts for rain, extreme temperatures, or notable conditions
- Integration with a weather API

### Phase 3 — Smart Lights *(coming soon)*
- Turn bedroom lights on/off
- Adjust brightness and color temperature
- Automate lights based on alarms (e.g. gentle wake-up light)

### Phase 4 — Bedroom Automation *(coming soon)*
- Unified routines (e.g. "good morning" triggers alarm off + lights on + weather brief)
- Extensible plugin system for new devices and services

---

## 🛠️ Getting Started

### Prerequisites

```bash
# Example for Python
python --version  # 3.9+
pip install -r requirements.txt
```

### Installation

```bash
# Clone the repo
git clone https://github.com/Nat300/alfred-home-assistant.git
cd alfred-home-assistant

# Install dependencies
pip install -r requirements.txt  # or: npm install
```

### Running Alfred

```bash
# Start the assistant
python main.py  # or: node index.js
```

---

## 📁 Project Structure

```
alfred-home-assistant/
├── alarms/          # Alarm management module
├── weather/         # Weather forecast module (Phase 2)
├── lights/          # Smart lights module (Phase 3)
├── core/            # Shared utilities and config
├── main.py          # Entry point
└── README.md
```

---

## 🤝 Contributing

This is a personal project for now, but feel free to open issues or suggest ideas!

---

## 📄 License

MIT License — see [LICENSE](LICENSE) for details.

---

*Named after Alfred Pennyworth — the most reliable assistant there is.*