# 🍒 CherryRun

CherryRun is a lightweight Linux system tray application inspired by RunCat.

A small animated cherry lives in your taskbar and moves faster depending on your computer activity.
Hover the cherry to instantly see your system usage in real time.

## ✨ Features

* 🍒 Animated cherry in the system tray
* ⚡ Animation speed reacts to CPU usage
* 🖥️ Real-time CPU usage
* 🧠 Real-time RAM usage
* 🎮 AMD GPU usage support
* 🚀 Launch at startup option
* 🪶 Lightweight and minimal
* 🐧 Designed for Linux desktops

## 📸 Preview

CherryRun sits directly in your Linux tray area and animates continuously depending on system load.

## 🛠️ Built With

* Python 3
* PyQt6
* psutil

## 📦 Installation

Clone the repository:

```bash
git clone https://github.com/CeriseeBrandy/CherryRun.git
cd CherryRun
```

Install dependencies:

```bash
pip install PyQt6 psutil
```

Run CherryRun:

```bash
python3 cherryrun.py
```

## 🏗️ Build Executable

Install PyInstaller:

```bash
pip install pyinstaller
```

Build the app:

```bash
pyinstaller --onefile --windowed --name CherryRun --icon assets/cherryrun.png cherryrun.py
```

The executable will be available in:

```bash
dist/CherryRun
```

## 🚀 Autostart

CherryRun can automatically launch when your system starts.

Right click the cherry icon and enable:

```text
Lancer au démarrage
```

## 📁 Project Structure

```text
CherryRun/
├── assets/
│   ├── cherry.png
│   └── cherryrun.png
├── cherryrun.py
└── README.md
```

## ❤️ Inspiration

Inspired by the famous macOS application:

* RunCat

But redesigned for Linux with a cherry mascot 🍒

## 📜 License

MIT License
