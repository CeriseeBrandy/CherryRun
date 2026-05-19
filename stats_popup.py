from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QProgressBar, QFrame
from PyQt6.QtCore import QTimer, Qt
from system_stats import SystemStats


class StatsPopup(QWidget):
    def __init__(self):
        super().__init__()

        self.stats = SystemStats()
        self.cpu_value = 0
        self.ram_value = 0
        self.gpu_value = 0

        self.setWindowFlags(
            Qt.WindowType.Tool |
            Qt.WindowType.FramelessWindowHint |
            Qt.WindowType.WindowStaysOnTopHint
        )

        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.setFixedSize(240, 150)

        self.card = QFrame(self)
        self.card.setObjectName("card")
        self.card.setGeometry(0, 0, 240, 150)

        self.setStyleSheet("""
            #card {
                background-color: #111116;
                border: 1px solid #2b2b34;
                border-radius: 16px;
            }

            QLabel {
                color: #f5f5f7;
                background: transparent;
                border: none;
                font-family: Arial;
                font-size: 13px;
            }

            QProgressBar {
                height: 7px;
                border: none;
                border-radius: 4px;
                background-color: #2b2b34;
            }

            QProgressBar::chunk {
                border-radius: 4px;
                background-color: #ff2d55;
            }
        """)

        layout = QVBoxLayout(self.card)
        layout.setContentsMargins(16, 12, 16, 12)
        layout.setSpacing(6)

        self.title = QLabel("🍒 CherryRun")
        self.title.setStyleSheet("font-size: 17px; font-weight: bold;")

        self.cpu_label = QLabel("CPU  0%")
        self.cpu_bar = QProgressBar()

        self.ram_label = QLabel("RAM  0%")
        self.ram_bar = QProgressBar()

        self.gpu_label = QLabel("GPU  non détecté")
        self.gpu_bar = QProgressBar()

        for bar in [self.cpu_bar, self.ram_bar, self.gpu_bar]:
            bar.setRange(0, 100)
            bar.setTextVisible(False)

        layout.addWidget(self.title)
        layout.addWidget(self.cpu_label)
        layout.addWidget(self.cpu_bar)
        layout.addWidget(self.ram_label)
        layout.addWidget(self.ram_bar)
        layout.addWidget(self.gpu_label)
        layout.addWidget(self.gpu_bar)

        self.timer = QTimer()
        self.timer.timeout.connect(self.update_stats)
        self.timer.start(700)

        self.update_stats()

    def smooth(self, old, new, factor=0.25):
        return old + (new - old) * factor

    def update_stats(self):
        cpu = self.stats.cpu()
        ram = self.stats.ram()
        gpu = self.stats.gpu()

        self.cpu_value = self.smooth(self.cpu_value, cpu)
        self.ram_value = self.smooth(self.ram_value, ram)

        cpu_int = int(self.cpu_value)
        ram_int = int(self.ram_value)

        self.cpu_label.setText(f"CPU  {cpu_int}%")
        self.cpu_bar.setValue(cpu_int)

        self.ram_label.setText(f"RAM  {ram_int}%")
        self.ram_bar.setValue(ram_int)

        if gpu is None:
            self.gpu_label.setText("GPU  non détecté")
            self.gpu_bar.setValue(0)
        else:
            self.gpu_value = self.smooth(self.gpu_value, gpu)
            gpu_int = int(self.gpu_value)
            self.gpu_label.setText(f"GPU  {gpu_int}%")
            self.gpu_bar.setValue(gpu_int)