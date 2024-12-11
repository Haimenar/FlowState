import sys
from playsound import playsound
from PyQt5.QtCore import QTimer, Qt
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QPushButton
from PyQt5.QtGui import QIcon, QFont
from PyQt5.QtWidgets import QSystemTrayIcon, QMenu

class FlowStateTimer(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("FlowState Timer")
        self.setWindowIcon(QIcon('assets/timer_icon.png'))
        self.setStyleSheet("background-color: #214E34; color: white;")

        self.work_duration = 25 * 60
        self.break_duration = 5 * 60
        self.long_break_duration = 30 * 60
        self.time_left = self.work_duration
        self.running = False
        self.mode = "Work"
        self.cycle_index = 0

        layout = QVBoxLayout()

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

        self.create_tray_icon()

        # This timer updates the countdown every second
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.run_timer)

    def format_time(self, seconds):
        """Convert seconds into minutes:seconds format."""
        mins, secs = divmod(seconds, 60)
        return f"{mins:02d}:{secs:02d}"

    def toggle_timer(self):
        """Start or pause the timer."""
        if not self.running:
            self.running = True
            self.start_button.setText("Pause")
            self.timer.start(1000)
        else:
            self.running = False
            self.start_button.setText("Resume")
            self.timer.stop()

    def stop_timer(self):
        """Stop the timer and reset."""
        self.running = False
        self.time_left = self.work_duration
        self.timer_label.setText(self.format_time(self.time_left))
        self.mode_label.setText(self.mode)
        self.start_button.setText("Start")
        self.timer.stop()

    def run_timer(self):
        """Run the countdown timer."""
        if self.time_left > 0:
            self.time_left -= 1
            self.timer_label.setText(self.format_time(self.time_left))
        else:
            self.play_alarm()
            self.switch_mode()

    def switch_mode(self):
        """Switch between work and break modes."""
        if self.time_left == 0:
            if self.mode == "Work":
                if self.cycle_index > 2:
                    self.cycle_index = 0
                    self.mode = "Long Break"
                    self.time_left = self.long_break_duration
                    self.mode_label.setText(self.mode)

                      # Switch to break time
                else:
                    self.cycle_index += 1
                    self.mode = "Break"  # Switch to break time
                    self.time_left = self.break_duration
                    self.mode_label.setText(self.mode)

            else:
                self.mode = "Work"  # Switch back to work time
                self.time_left = self.work_duration
                self.mode_label.setText(self.mode)
            self.timer.start(1000)  # Start the new mode timer

    def play_alarm(self):
        """Play an alarm sound when the timer finishes."""
        playsound("assets/alert1.mp3")

    def create_tray_icon(self):
        """Create the system tray icon."""
        tray_icon = QSystemTrayIcon(QIcon('assets/timer_icon.png'), self)
        tray_icon.setToolTip("FlowState Timer")

        quit_action = lambda: sys.exit()
        pause_action = lambda: self.toggle_timer()  # Pause/Resume action
        menu = QMenu()

        pause_action_item = menu.addAction("Pause/Resume")
        pause_action_item.triggered.connect(pause_action)

        quit_action_item = menu.addAction("Quit")
        quit_action_item.triggered.connect(quit_action)

        tray_icon.setContextMenu(menu)
        tray_icon.show()

def main():
    app = QApplication(sys.argv)
    timer = FlowStateTimer()
    timer.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
