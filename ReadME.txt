# BootForge

**BootForge** is a powerful USB and ISO creation toolkit for Windows and macOS. Built with love and forged for hackers, techs, legacy installers, and modern deployment heroes.

---

## 🚀 Features

- **macOS USB Creator**  
  Create bootable USB drives from `.dmg`, `.pkg`, or `.app` files

- **Windows ISO Modifier**  
  Inject drivers, apply TPM/RAM/Secure Boot bypass, and simulate modification

- **Smart OS Advisor**  
  Detects CPU, RAM, Disk, and system info — recommends OS versions

- **Plugin System**  
  Drop `.py` files into `/plugins` or load `.bfp` profile from URL

- **Dark Mode & Themes**  
  Toggle dark mode, import/export `.bftheme` files

- **Auto-Updater & Feedback**  
  Checks GitHub for updates, saves logs and user feedback

- **Experimental Tools**  
  - Virtual USB Simulator (dry run without writing)
  - Hackintosh Compatibility Check
  - Offline AI Helper Panel (stub)

---

## 📦 Installation

### Requirements
- Python 3.10+
- Pip packages:
```bash
pip install PyQt5 psutil
```

### Run the App
```bash
python usb_master_gui.py
```

---

## 🛠 Packaging (Optional)

### Windows
```bash
pyinstaller --noconfirm --windowed --onefile --icon=icon.ico usb_master_gui.py
```

### macOS
```bash
python setup.py py2app
```

### Linux (Optional)
Use AppImage or fpm to build `.deb`

---

## 🌈 Theming

- Export `.bftheme` files from Settings tab
- Share and load themes for your custom UI

---

## 🌐 Plugin Profiles

- `.bfp` files are lists of `.py` plugin URLs (raw)
- Load them in the Plugins tab to auto-import tools

---

## 🧩 Example Plugin Profile (.bfp)
```
https://pastebin.com/raw/yourtool1.py
https://gist.githubusercontent.com/user/plugin.py
```

---

## 🤖 AI + Experimental

- Virtual USB Tool (creates dummy .img in temp)
- Hackintosh Check (flags unsupported CPUs)
- AI Helper Panel (loads stub or local help file)

---

## 💬 Feedback & Logs

- Submit logs from Settings
- Save feedback files

---

## 🏁 You're Ready to Forge.
BootForge is modular, powerful, and just getting started. Use it, extend it, and make it yours.

---

Created by dreamers. Run by rebels. Built for tech legends.

> “In the forge, every spark is a story.”

---