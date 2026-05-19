import sys
import os
import math
import psutil

from PyQt6.QtWidgets import QApplication, QSystemTrayIcon, QMenu
from PyQt6.QtGui import QIcon, QPixmap, QAction, QPainter
from PyQt6.QtCore import QTimer, Qt, QSize


class CherryRun:
    def __init__(self):
        self.app = QApplication(sys.argv)
        self.app.setQuitOnLastWindowClosed(False)

        self.app_dir = os.path.dirname(os.path.abspath(__file__))
        self.assets_dir = os.path.join(self.app_dir, "assets")
        self.cherry_path = os.path.join(self.assets_dir, "cherry.png")

        self.autostart_dir = os.path.expanduser("~/.config/autostart")
        self.autostart_file = os.path.join(self.autostart_dir, "cherryrun.desktop")

        self.base_pixmap = QPixmap(self.cherry_path)

        if self.base_pixmap.isNull():
            print(f"Erreur: impossible de charger {self.cherry_path}")
            sys.exit(1)

        self.base_pixmap = self.base_pixmap.scaled(
            QSize(48, 48),
            Qt.AspectRatioMode.KeepAspectRatio,
            Qt.TransformationMode.SmoothTransformation
        )

        self.frame = 0
        self.cpu = 0
        self.ram = 0
        self.gpu = None

        self.tray = QSystemTrayIcon()
        self.menu = QMenu()

        self.startup_action = QAction("Lancer au démarrage")
        self.startup_action.setCheckable(True)
        self.startup_action.setChecked(self.is_autostart_enabled())
        self.startup_action.triggered.connect(self.toggle_autostart)
        self.menu.addAction(self.startup_action)

        self.menu.addSeparator()

        quit_action = QAction("Quitter CherryRun")
        quit_action.triggered.connect(self.app.quit)
        self.menu.addAction(quit_action)

        self.tray.setContextMenu(self.menu)
        self.tray.setIcon(QIcon(self.render_icon(0)))
        self.tray.show()

        psutil.cpu_percent(interval=None)

        self.animation_timer = QTimer()
        self.animation_timer.timeout.connect(self.animate)
        self.animation_timer.start(80)

        self.stats_timer = QTimer()
        self.stats_timer.timeout.connect(self.update_stats)
        self.stats_timer.start(2500)

        self.update_stats()

    def is_autostart_enabled(self):
        return os.path.exists(self.autostart_file)

    def toggle_autostart(self):
        if self.startup_action.isChecked():
            self.enable_autostart()
        else:
            self.disable_autostart()

    def enable_autostart(self):
        os.makedirs(self.autostart_dir, exist_ok=True)

        python_path = sys.executable
        script_path = os.path.abspath(__file__)

        desktop_content = f"""[Desktop Entry]
Type=Application
Name=CherryRun
Comment=Animated cherry system tray monitor
Exec={python_path} "{script_path}"
Icon={self.cherry_path}
Terminal=false
X-GNOME-Autostart-enabled=true
"""

        with open(self.autostart_file, "w", encoding="utf-8") as file:
            file.write(desktop_content)

    def disable_autostart(self):
        if os.path.exists(self.autostart_file):
            os.remove(self.autostart_file)

    def get_gpu_usage(self):
        try:
            with open("/sys/class/drm/card1/device/gpu_busy_percent", "r") as file:
                return int(file.read().strip())
        except Exception:
            return None

    def render_icon(self, y_offset):
        pixmap = QPixmap(64, 64)
        pixmap.fill(Qt.GlobalColor.transparent)

        painter = QPainter(pixmap)
        painter.setRenderHint(QPainter.RenderHint.SmoothPixmapTransform)

        x = int((64 - self.base_pixmap.width()) / 2)
        y = int((64 - self.base_pixmap.height()) / 2 + y_offset)

        painter.drawPixmap(x, y, self.base_pixmap)
        painter.end()

        return pixmap

    def update_stats(self):
        real_cpu = psutil.cpu_percent(interval=None)
        real_ram = psutil.virtual_memory().percent
        self.gpu = self.get_gpu_usage()

        self.cpu = self.cpu + (real_cpu - self.cpu) * 0.20
        self.ram = self.ram + (real_ram - self.ram) * 0.20

        display_cpu = round(self.cpu / 5) * 5
        display_ram = round(self.ram / 5) * 5

        gpu_text = "non détecté" if self.gpu is None else f"{self.gpu:.0f}%"

        self.tray.setToolTip(
            f"CherryRun 🍒\n"
            f"CPU: {display_cpu:.0f}%\n"
            f"RAM: {display_ram:.0f}%\n"
            f"GPU: {gpu_text}"
        )

    def animate(self):
        speed = 0.18 + (self.cpu / 100) * 1.0
        self.frame += speed

        bounce = math.sin(self.frame) * (4.0 + self.cpu / 20)
        y_offset = int(bounce)

        self.tray.setIcon(QIcon(self.render_icon(y_offset)))

    def run(self):
        sys.exit(self.app.exec())


if __name__ == "__main__":
    CherryRun().run()