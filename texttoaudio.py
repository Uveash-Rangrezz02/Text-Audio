import sys
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QLabel, QPushButton, QTextEdit,
    QComboBox, QSlider, QMessageBox, QHBoxLayout
)
from PyQt5.QtCore import Qt
import pyttsx3
import speech_recognition as sr

# Initialize Text to Speech engine
tts_engine = pyttsx3.init()
voices = tts_engine.getProperty('voices')

class SpeechApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Speech ↔ Text Converter")
        self.setGeometry(100, 100, 500, 400)
        self.setStyleSheet("background-color: #2b2b2b; color: white; font-size: 14px;")

        layout = QVBoxLayout()

        # Textbox for input
        layout.addWidget(QLabel("Type your text:", styleSheet="color:white;"))
        self.textbox = QTextEdit()
        layout.addWidget(self.textbox)

        # Buttons
        button_layout = QHBoxLayout()
        self.speak_btn = QPushButton("Text to Speech")
        self.speak_btn.clicked.connect(self.text_to_speech)
        button_layout.addWidget(self.speak_btn)

        self.listen_btn = QPushButton("Speech to Text")
        self.listen_btn.clicked.connect(self.speech_to_text)
        button_layout.addWidget(self.listen_btn)

        layout.addLayout(button_layout)

        # Output label
        self.result_label = QLabel("")
        layout.addWidget(self.result_label)

        # Voice dropdown
        layout.addWidget(QLabel("Select Voice:", styleSheet="color:white;"))
        self.voice_dropdown = QComboBox()
        self.voice_dropdown.addItems([v.name for v in voices])
        self.voice_dropdown.currentIndexChanged.connect(self.change_voice)
        layout.addWidget(self.voice_dropdown)

        # Speed slider
        layout.addWidget(QLabel("Speaking Speed:", styleSheet="color:white;"))
        self.slider = QSlider(Qt.Horizontal)
        self.slider.setMinimum(50)
        self.slider.setMaximum(300)
        self.slider.setValue(150)
        self.slider.valueChanged.connect(self.change_speed)
        layout.addWidget(self.slider)

        self.setLayout(layout)

    # Text to Speech function
    def text_to_speech(self):
        text = self.textbox.toPlainText()
        if not text:
            QMessageBox.warning(self, "Warning", "Please enter some text to speak.")
            return
        tts_engine.say(text)
        tts_engine.runAndWait()

    # Speech to Text function (English)
    def speech_to_text(self):
        recognizer = sr.Recognizer()
        with sr.Microphone() as source:
            self.result_label.setText("Listening...")
            try:
                audio = recognizer.listen(source, timeout=5)
                result = recognizer.recognize_google(audio, language='en-IN')  # Set to English India
                self.result_label.setText("You said: " + result)
                self.textbox.setText(result)
            except sr.UnknownValueError:
                self.result_label.setText("Could not understand audio.")
            except sr.RequestError:
                self.result_label.setText("Check your internet connection.")
            except sr.WaitTimeoutError:
                self.result_label.setText("Listening timed out.")

    # Change Voice
    def change_voice(self):
        selected_voice = self.voice_dropdown.currentText()
        for voice in voices:
            if selected_voice in voice.name:
                tts_engine.setProperty('voice', voice.id)
                break

    # Change Speaking Speed
    def change_speed(self):
        tts_engine.setProperty('rate', self.slider.value())

# Run the application
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = SpeechApp()
    window.show()
    sys.exit(app.exec_())         