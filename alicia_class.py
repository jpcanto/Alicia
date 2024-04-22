import speech_recognition as sr
from gtts import gTTS
from playsound import playsound
import os
import time


class Alicia:
    def __init__(self):
        self.order_keywords = [
            "pedido",
            "rápido",
            "rapido",
            "instantâneo",
            "padrão",
            "sempre",
        ]
        self.quit_keywords = ["sai", "cancela", "fecha", "encerra"]
        self.quit = False
        self.callback = []

        self.loop()

    def microphone_listen(self):
        microphone = sr.Recognizer()
        with sr.Microphone() as source:
            microphone.adjust_for_ambient_noise(source)

            path = os.path.abspath(os.path.join("default_audios", "talk.mp3"))
            formatted_path = path.replace(" ", "%20")
            playsound(formatted_path)

            try:
                audio = microphone.listen(source, timeout=5)
            except sr.WaitTimeoutError:
                self.microphone_error_handler()

        try:
            phrase = microphone.recognize_google(audio, language="pt-BR")

            return phrase

        except sr.UnknownValueError:
            self.microphone_error_handler()

    def microphone_error_handler(self):
        path = os.path.abspath(os.path.join("default_audios", "error.mp3"))
        formatted_path = path.replace(" ", "%20")
        playsound(formatted_path)

        time.sleep(3)
        return self.microphone_listen()

    def play_audio(self, txt, file="last_command.mp3"):
        tts = gTTS(txt, lang="pt-BR")
        time.sleep(0.5)

        try:
            tts.save(file)
        except:
            print("last_command file save error")

        path = os.path.abspath(file)
        formatted_path = path.replace(" ", "%20")
        playsound(formatted_path)

    def loop(self, txt=""):
        txt = txt + "" + self.microphone_listen()
        if any(word in txt for word in self.quit_keywords):
            self.quit = True

        # TODO add orders
        elif any(word in txt for word in self.order_keywords):
            pass

        print(txt)


ali = Alicia()
