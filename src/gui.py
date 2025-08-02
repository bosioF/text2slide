from PyQt5.QtWidgets import (
    QApplication, QWidget, QLabel, QPushButton,
    QLineEdit, QFileDialog, QComboBox, QVBoxLayout, QMessageBox
)

from backend import *

class Text2SlideGUI(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Text2Slide GUI")
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        self.input_path = QLineEdit(self)
        self.input_path.setPlaceholderText("Input .txt file")
        browse_input = QPushButton("Browse Input File", self)
        browse_input.clicked.connect(self.browse_input_file)
        layout.addWidget(QLabel("Input File:"))
        layout.addWidget(self.input_path)
        layout.addWidget(browse_input)

        self.output_name = QLineEdit(self)
        self.output_name.setPlaceholderText("Output file name (no .mp4)")
        layout.addWidget(QLabel("Output File Name:"))
        layout.addWidget(self.output_name)

        self.audio_path = QLineEdit(self)
        self.audio_path.setPlaceholderText("Optional MP3 path")
        browse_audio = QPushButton("Browse MP3", self)
        browse_audio.clicked.connect(self.browse_audio_file)
        layout.addWidget(QLabel("Optional Audio:"))
        layout.addWidget(self.audio_path)
        layout.addWidget(browse_audio)

        self.quality = QComboBox(self)
        self.quality.addItems(["-ql", "-qm", "-qh", "-qp", "-qk"])
        layout.addWidget(QLabel("Quality:"))
        layout.addWidget(self.quality)

        self.color = QComboBox(self)
        from backend import COLOR_NAMES
        self.color.addItems(COLOR_NAMES)
        layout.addWidget(QLabel("Text Color:"))
        layout.addWidget(self.color)

        render_button = QPushButton("Generate Video", self)
        render_button.clicked.connect(self.render_video)
        layout.addWidget(render_button)

        self.setLayout(layout)

    def browse_input_file(self):
        file, _ = QFileDialog.getOpenFileName(self, "Open Input File", "", "Text Files (*.txt)")
        if file:
            self.input_path.setText(file)

    def browse_audio_file(self):
        file, _ = QFileDialog.getOpenFileName(self, "Open MP3 File", "", "Audio Files (*.mp3)")
        if file:
            self.audio_path.setText(file)

    def render_video(self):
        input_file = self.input_path.text()
        output_file = self.output_name.text()
        audio_file = self.audio_path.text() or None
        quality = self.quality.currentText()
        color = self.color.currentText().upper()

        try:
            check_args(input_file, quality, output_file)
            dir_name = get_dir_name(quality)
            process_video(input_file, color, output_file, quality, dir_name, audio_file)
            QMessageBox.information(self, "Success", "Video generated successfully!")
        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Text2SlideGUI()
    window.show()
    sys.exit(app.exec_())
