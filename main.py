import sys
from playsound import playsound
from PyQt5.QtCore import QTimer, Qt
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QPushButton, QMenuBar, QMenu
from PyQt5.QtGui import QIcon, QFont

class FlowStateTimer(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("FlowState Timer")
        self.setWindowIcon(QIcon('assets/timer_icon.ico'))
        self.setStyleSheet("background-color: #214E34; color: white;")

        self.work_duration = 25 * 60
        self.break_duration = 5 * 60
        self.long_break_duration = 30 * 60
        self.time_left = self.work_duration
        self.running = False
        self.mode = "Work"
        self.cycle_index = 0

        layout = QVBoxLayout()

        # Menu Bar
        menu_bar = QMenuBar(self)
        themes_menu = menu_bar.addMenu("Themes")
        themedictionary = {
            "Forest": ["#214E34", "#30734C", "white"],
            "Dark": ["#202020", "#383D3B", "grey"],
            "Light": ["#CCCCCC", "#E0E0E0", "black"]
        }

        for theme_entry, colors in themedictionary.items():
            action = themes_menu.addAction(theme_entry)
            action.triggered.connect(lambda _, c=colors: self.change_theme(c))

        layout.setMenuBar(menu_bar)

        # Mode display (Work/Break)
        self.mode_label = QLabel(self.mode, self)
        self.mode_label.setFont(QFont('Arial', 24))
        self.mode_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.mode_label)

        # Timer display
        self.timer_label = QLabel(self.format_time(self.time_left), self)
        self.timer_label.setFont(QFont('Arial', 48))
        self.timer_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.timer_label)

        # Start and Stop buttons
        self.start_button = QPushButton("Start", self)
        self.start_button.setStyleSheet("background-color: #30734C; color: white; font-size: 18px; padding: 10px;")
        self.start_button.clicked.connect(self.toggle_timer)
        layout.addWidget(self.start_button)

        self.stop_button = QPushButton("Stop", self)
        self.stop_button.setStyleSheet("background-color: #30734C; color: white; font-size: 18px; padding: 10px;")
        self.stop_button.clicked.connect(self.stop_timer)
        layout.addWidget(self.stop_button)

        self.setLayout(layout)

        # Timer
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.run_timer)

    def format_time(self, seconds):
        mins, secs = divmod(seconds, 60)
        return f"{mins:02d}:{secs:02d}"

    def toggle_timer(self):
        if not self.running:
            self.running = True
            self.start_button.setText("Pause")
            self.timer.start(1000)
        else:
            self.running = False
            self.start_button.setText("Resume")
            self.timer.stop()

    def stop_timer(self):
        self.running = False
        self.time_left = self.work_duration
        self.timer_label.setText(self.format_time(self.time_left))
        self.mode_label.setText(self.mode)
        self.start_button.setText("Start")
        self.timer.stop()

    def run_timer(self):
        if self.time_left > 0:
            self.time_left -= 1
            self.timer_label.setText(self.format_time(self.time_left))
        else:
            self.play_alarm()
            self.switch_mode()

    def switch_mode(self):
        if self.time_left == 0:
            if self.mode == "Work":
                if self.cycle_index > 2:
                    self.cycle_index = 0
                    self.mode = "Long Break"
                    self.time_left = self.long_break_duration
                else:
                    self.cycle_index += 1
                    self.mode = "Break"
                    self.time_left = self.break_duration
            else:
                self.mode = "Work"
                self.time_left = self.work_duration

            self.mode_label.setText(self.mode)
            self.timer.start(1000)

    def play_alarm(self):
        playsound("assets/alert1.mp3")

    def change_theme(self, color_list):
        primary_color, secondary_color, text_color = color_list
        self.setStyleSheet(f"background-color: {primary_color}; color: {text_color};")
        self.start_button.setStyleSheet(f"background-color: {secondary_color}; color: {text_color}; font-size: 18px; padding: 10px;")
        self.stop_button.setStyleSheet(f"background-color: {secondary_color}; color: {text_color}; font-size: 18px; padding: 10px;")
        self.mode_label.setStyleSheet(f"color: {text_color};")
        self.timer_label.setStyleSheet(f"color: {text_color};")

def main():
    app = QApplication(sys.argv)
    timer = FlowStateTimer()
    timer.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()