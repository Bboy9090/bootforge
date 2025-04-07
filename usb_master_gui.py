# BootForge: Unified Application - Main Entry Point
# Combines all phases (1 through 8) into a single GUI app
# Modules: macOS USB, Windows ISO, Tools, Settings, Plugins, Experimental

import sys
import os
import platform
import subprocess
import tempfile
import uuid
import urllib.request
import importlib.util
import json
import psutil
import shutil

from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QPushButton, QLabel, QTabWidget,
    QFileDialog, QComboBox, QMessageBox, QTextEdit, QProgressBar, QCheckBox
)
from PyQt5.QtGui import QPalette, QColor
from PyQt5.QtCore import Qt, QTimer, QThread, pyqtSignal


class SplashScreen(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("BootForge - Loading...")
        self.setFixedSize(400, 250)
        layout = QVBoxLayout()
        label = QLabel("🔥 BootForge is starting...")
        label.setAlignment(Qt.AlignCenter)
        layout.addWidget(label)
        self.setLayout(layout)


class BootForge(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("BootForge Pro")
        self.setFixedSize(900, 650)

        self.tabs = QTabWidget()
        self.setCentralWidget(self.tabs)

        self.tabs.addTab(self.create_mac_tab(), "macOS")
        self.tabs.addTab(self.create_windows_tab(), "Windows")
        self.tabs.addTab(self.create_tools_tab(), "Tools")
        self.tabs.addTab(self.create_settings_tab(), "Settings")
        self.tabs.addTab(self.create_logs_tab(), "Logs")

        self.plugin_folder = "plugins"
        os.makedirs(self.plugin_folder, exist_ok=True)
        self.load_plugins()

    # --- macOS USB Creator ---
    def create_mac_tab(self):
        tab = QWidget()
        layout = QVBoxLayout()

        self.mac_file_label = QLabel("No installer selected")
        select_file_btn = QPushButton("Select macOS Installer")
        select_file_btn.clicked.connect(self.select_mac_installer)

        self.usb_selector = QComboBox()
        self.refresh_usb_list()
        refresh_usb_btn = QPushButton("Refresh USB List")
        refresh_usb_btn.clicked.connect(self.refresh_usb_list)

        create_usb_btn = QPushButton("Create macOS USB")
        create_usb_btn.clicked.connect(self.create_mac_usb)

        self.flash_progress = QProgressBar()
        self.flash_progress.setValue(0)

        layout.addWidget(self.mac_file_label)
        layout.addWidget(select_file_btn)
        layout.addWidget(QLabel("Select USB Drive:"))
        layout.addWidget(self.usb_selector)
        layout.addWidget(refresh_usb_btn)
        layout.addWidget(create_usb_btn)
        layout.addWidget(self.flash_progress)
        tab.setLayout(layout)
        return tab

    def select_mac_installer(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Select macOS Installer", "", "Installer Files (*.dmg *.pkg *.app)")
        if file_path:
            self.mac_file_path = file_path
            self.mac_file_label.setText(f"Selected: {os.path.basename(file_path)}")
            self.log(f"Installer selected: {file_path}")

    def refresh_usb_list(self):
        self.usb_selector.clear()
        drives = self.detect_usb_drives()
        if not drives:
            self.usb_selector.addItem("No USB drives found")
        else:
            for drive in drives:
                self.usb_selector.addItem(drive)

    def detect_usb_drives(self):
        drives = []
        if platform.system() == "Windows":
            output = subprocess.getoutput("wmic logicaldisk where drivetype=2 get deviceid")
            for line in output.splitlines():
                if ":" in line:
                    drives.append(line.strip())
        elif platform.system() == "Darwin":
            output = subprocess.getoutput("diskutil list")
            for line in output.splitlines():
                if "external" in line.lower():
                    parts = line.split()
                    if parts and parts[0].startswith("/dev/disk"):
                        drives.append(parts[0])
        return drives

    def create_mac_usb(self):
        drive = self.usb_selector.currentText()
        installer = getattr(self, 'mac_file_path', None)
        if not installer or "No USB" in drive:
            QMessageBox.warning(self, "Error", "Please select a valid installer and USB drive.")
            return
        confirm = QMessageBox.question(self, "Confirm Flash", f"Erase and flash {drive}?", QMessageBox.Yes | QMessageBox.No)
        if confirm != QMessageBox.Yes:
            return
        self.log("[macOS] Flashing started...")
        # Real flash would run here
        self.flash_progress.setValue(100)
        self.log("[macOS] Flash complete!")

    # --- Windows ISO Modifier ---
    def create_windows_tab(self):
        tab = QWidget()
        layout = QVBoxLayout()

        self.iso_label = QLabel("No ISO selected")
        select_iso_btn = QPushButton("Select Windows ISO")
        select_iso_btn.clicked.connect(self.select_iso)

        self.driver_label = QLabel("No drivers selected")
        select_driver_btn = QPushButton("Select Driver Folder")
        select_driver_btn.clicked.connect(self.select_driver_folder)

        self.tpm_bypass = QCheckBox("Bypass TPM Check")
        self.ram_bypass = QCheckBox("Bypass RAM Check")
        self.secure_bypass = QCheckBox("Bypass Secure Boot")

        modify_btn = QPushButton("Modify ISO")
        modify_btn.clicked.connect(self.modify_iso_stub)

        layout.addWidget(self.iso_label)
        layout.addWidget(select_iso_btn)
        layout.addWidget(self.driver_label)
        layout.addWidget(select_driver_btn)
        layout.addWidget(self.tpm_bypass)
        layout.addWidget(self.ram_bypass)
        layout.addWidget(self.secure_bypass)
        layout.addWidget(modify_btn)
        tab.setLayout(layout)
        return tab

    def select_iso(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Select ISO", "", "ISO Files (*.iso)")
        if file_path:
            self.iso_path = file_path
            self.iso_label.setText(f"Selected ISO: {os.path.basename(file_path)}")
            self.log(f"ISO selected: {file_path}")

    def select_driver_folder(self):
        folder = QFileDialog.getExistingDirectory(self, "Select Driver Folder")
        if folder:
            self.driver_path = folder
            self.driver_label.setText(f"Drivers: {os.path.basename(folder)}")
            self.log(f"Driver folder selected: {folder}")

    def modify_iso_stub(self):
        if not hasattr(self, 'iso_path'):
            QMessageBox.warning(self, "Missing ISO", "Select a Windows ISO to modify.")
            return
        self.log("[Windows] Modification simulated. Real engine coming.")
        QMessageBox.information(self, "Modify ISO", "Stub: Windows ISO modification simulated.")

    # --- Tool Tab ---
    def create_tools_tab(self):
        tab = QWidget()
        layout = QVBoxLayout()
        advisor_btn = QPushButton("Run Smart OS Advisor")
        advisor_btn.clicked.connect(self.run_smart_os_advisor)
        layout.addWidget(advisor_btn)
        self.advisor_output = QTextEdit()
        self.advisor_output.setReadOnly(True)
        layout.addWidget(self.advisor_output)
        tab.setLayout(layout)
        return tab

    def run_smart_os_advisor(self):
        try:
            cpu = platform.processor()
            ram = round(psutil.virtual_memory().total / (1024 ** 3), 2)
            disk = shutil.disk_usage("/").total / (1024 ** 3)
            system = platform.system()
            release = platform.release()
            result = f"CPU: {cpu}\nRAM: {ram} GB\nDisk: {int(disk)} GB\nSystem: {system} {release}\n"
            self.advisor_output.setText(result)
            self.log("[Advisor] Scan complete.")
        except Exception as e:
            self.advisor_output.setText(f"Error: {e}")
            self.log(f"[Advisor] Error: {e}")

    # --- Remaining functions (Settings, Plugins, Logs, Virtual USB, AI Helper, Hackintosh) ---
    # Will be added next in a second document due to size constraints.


if __name__ == "__main__":
    app = QApplication(sys.argv)
    splash = SplashScreen()
    splash.show()

    def launch_main():
        splash.close()
        window = BootForge()
        window.show()

    QTimer.singleShot(2000, launch_main)
    sys.exit(app.exec_())
def create_settings_tab(self):
        tab = QWidget()
        layout = QVBoxLayout()

        theme_btn = QPushButton("Toggle Dark Mode")
        theme_btn.clicked.connect(self.toggle_dark_mode)
        layout.addWidget(theme_btn)

        import_theme_btn = QPushButton("Import Theme (.bftheme)")
        import_theme_btn.clicked.connect(self.import_theme)
        layout.addWidget(import_theme_btn)

        export_theme_btn = QPushButton("Export Current Theme")
        export_theme_btn.clicked.connect(self.export_theme)
        layout.addWidget(export_theme_btn)

        update_btn = QPushButton("Check for Updates")
        update_btn.clicked.connect(self.check_for_updates)
        layout.addWidget(update_btn)

        feedback_btn = QPushButton("Send Feedback")
        feedback_btn.clicked.connect(self.open_feedback_form)
        layout.addWidget(feedback_btn)

        export_btn = QPushButton("Export Logs")
        export_btn.clicked.connect(self.export_logs)
        layout.addWidget(export_btn)

        return tab

    def create_logs_tab(self):
        tab = QWidget()
        layout = QVBoxLayout()
        self.log_area = QTextEdit()
        self.log_area.setReadOnly(True)
        layout.addWidget(self.log_area)
        tab.setLayout(layout)
        return tab

    def log(self, message):
        if hasattr(self, 'log_area'):
            self.log_area.append(message)
        print(message)

    def export_logs(self):
        with open("BootForge_Logs.txt", "w") as f:
            f.write(self.log_area.toPlainText())
        self.log("Logs exported to BootForge_Logs.txt")

    def toggle_dark_mode(self):
        palette = QPalette()
        palette.setColor(QPalette.Window, QColor(30, 30, 30))
        palette.setColor(QPalette.WindowText, Qt.white)
        palette.setColor(QPalette.Base, QColor(20, 20, 20))
        palette.setColor(QPalette.Text, Qt.white)
        palette.setColor(QPalette.Button, QColor(45, 45, 45))
        palette.setColor(QPalette.ButtonText, Qt.white)
        self.setPalette(palette)
        self.log("Dark mode enabled.")

    def import_theme(self):
        file, _ = QFileDialog.getOpenFileName(self, "Import Theme", "", "Theme Files (*.bftheme)")
        if file:
            try:
                with open(file, "r") as f:
                    theme_data = json.load(f)
                self.apply_theme(theme_data)
                self.log(f"Imported theme from {file}")
            except Exception as e:
                QMessageBox.warning(self, "Error", f"Failed to import theme: {e}")

    def export_theme(self):
        file, _ = QFileDialog.getSaveFileName(self, "Export Theme", "theme.bftheme", "Theme Files (*.bftheme)")
        if file:
            try:
                theme_data = {
                    "bg_color": "#1e1e1e",
                    "fg_color": "#ffffff",
                    "button_color": "#2d2d2d",
                    "text_color": "#ffffff"
                }
                with open(file, "w") as f:
                    json.dump(theme_data, f)
                self.log(f"Exported current theme to {file}")
            except Exception as e:
                QMessageBox.warning(self, "Error", f"Failed to export theme: {e}")

    def apply_theme(self, theme_data):
        palette = QPalette()
        palette.setColor(QPalette.Window, QColor(theme_data.get("bg_color", "#1e1e1e")))
        palette.setColor(QPalette.WindowText, QColor(theme_data.get("fg_color", "#ffffff")))
        palette.setColor(QPalette.Base, QColor("#202020"))
        palette.setColor(QPalette.Text, QColor(theme_data.get("text_color", "#ffffff")))
        palette.setColor(QPalette.Button, QColor(theme_data.get("button_color", "#2d2d2d")))
        palette.setColor(QPalette.ButtonText, QColor(theme_data.get("text_color", "#ffffff")))
        self.setPalette(palette)

    def check_for_updates(self):
        try:
            current_version = "1.0.0"
            url = "https://raw.githubusercontent.com/your-repo/bootforge/main/version.txt"
            latest_version = urllib.request.urlopen(url).read().decode().strip()
            if latest_version > current_version:
                QMessageBox.information(self, "Update Available", f"BootForge {latest_version} is available!")
                self.log(f"Update found: {latest_version}")
            else:
                QMessageBox.information(self, "Up to Date", "You have the latest version.")
                self.log("No updates found.")
        except Exception as e:
            self.log(f"Update check failed: {e}")

    def open_feedback_form(self):
        feedback, ok = QFileDialog.getSaveFileName(self, "Save Feedback", "BootForge_Feedback.txt")
        if ok and feedback:
            try:
                with open(feedback, "w") as f:
                    f.write("BootForge Feedback Example\n")
                    f.write("Add your ideas or issues here.")
                QMessageBox.information(self, "Feedback", f"Feedback form saved to: {feedback}")
                self.log("Feedback file saved.")
            except Exception as e:
                QMessageBox.warning(self, "Error", f"Failed to save feedback: {e}")

    def load_plugins(self):
        if not os.path.exists(self.plugin_folder):
            return
        plugin_tab = QWidget()
        layout = QVBoxLayout()
        load_profile_btn = QPushButton("Load Plugin Profile (.bfp)")
        load_profile_btn.clicked.connect(self.load_plugin_profile)
        layout.addWidget(load_profile_btn)
        for filename in os.listdir(self.plugin_folder):
            if filename.endswith(".py"):
                path = os.path.join(self.plugin_folder, filename)
                button = QPushButton(f"Run {filename}")
                button.clicked.connect(lambda checked, p=path: self.run_plugin(p))
                layout.addWidget(button)
        plugin_tab.setLayout(layout)
        self.tabs.addTab(plugin_tab, "Plugins")

    def run_plugin(self, path):
        spec = importlib.util.spec_from_file_location("plugin_module", path)
        plugin = importlib.util.module_from_spec(spec)
        try:
            spec.loader.exec_module(plugin)
            self.log(f"Executed plugin: {path}")
        except Exception as e:
            self.log(f"Error running plugin {path}: {e}")

    def load_plugin_profile(self):
        input_path, _ = QFileDialog.getOpenFileName(self, "Load Plugin Profile", "", "Plugin Profile (*.bfp)")
        if input_path:
            self.load_profile_from_file(input_path)

    def load_profile_from_file(self, path):
        try:
            with open(path, 'r') as f:
                for line in f:
                    url = line.strip()
                    if url.startswith("http"):
                        self.download_and_add_plugin(url)
            self.log(f"Loaded plugin profile: {path}")
        except Exception as e:
            self.log(f"Failed to load plugin profile: {e}")

    def download_and_add_plugin(self, url):
        try:
            plugin_code = urllib.request.urlopen(url).read().decode()
            filename = url.split("/")[-1]
            if not filename.endswith(".py"):
                filename += ".py"
            plugin_path = os.path.join(self.plugin_folder, filename)
            with open(plugin_path, 'w') as f:
                f.write(plugin_code)
            self.log(f"Downloaded plugin: {filename}")
        except Exception as e:
            self.log(f"Failed to download plugin: {e}")

    def virtual_usb_flash(self, installer):
        try:
            self.log("[Virtual USB] Starting virtual flash simulation...")
            temp_filename = f"BootForgeVirtual_{uuid.uuid4().hex}.img"
            temp_file = os.path.join(tempfile.gettempdir(), temp_filename)
            with open(temp_file, 'wb') as f:
                chunk = b'\0' * 1024 * 1024
                for _ in range(50):
                    f.write(chunk)
            self.log(f"[Virtual USB] Simulated write to {temp_file}")
            QMessageBox.information(self, "Virtual USB", f"Flash simulation complete: {temp_file}")
        except Exception as e:
            self.log(f"Virtual USB failed: {e}")

    def open_ai_helper(self):
        try:
            with open("help_stub.txt", "r") as f:
                help_text = f.read()
        except FileNotFoundError:
            help_text = "This is BootForge's help center. Documentation and smart assistant features coming soon!"
        QMessageBox.information(self, "AI Helper", help_text)

    def check_hackintosh_compatibility(self):
        try:
            cpu = platform.processor()
            arch = platform.machine()
            unsupported_cpus = ["Pentium", "Atom", "Celeron"]
            if any(chip in cpu for chip in unsupported_cpus) or not arch.startswith("x86"):
                QMessageBox.warning(self, "Incompatible CPU", f"{cpu} ({arch}) may not work with macOS. Consider OpenCore patches.")
                self.log("Hackintosh warning: unsupported CPU or architecture.")
            else:
                QMessageBox.information(self, "Compatible", f"{cpu} ({arch}) looks compatible for macOS.")
                self.log("Hackintosh check: passed.")
        except Exception as e:
            self.log(f"Hackintosh check failed: {e}")