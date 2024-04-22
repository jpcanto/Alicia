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

        self.create_environment()
        self.loop()

    def create_environment():
        audio_folder = "audios"

        if not os.path.exists(audio_folder):
            os.makedirs(audio_folder)

    def microphone_listen(self):
        microphone = sr.Recognizer()
        with sr.Microphone() as source:
            microphone.adjust_for_ambient_noise(source)

            self.play_audio("Pode falar", "default.mp3")

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
        self.play_audio("Não entendi", "error.mp3")

        time.sleep(3)
        return self.microphone_listen()

    def play_audio(self, txt, file="last_command.mp3"):
        audios_path = "audios"
        file_path = os.path.join(audios_path, file)

        if not os.path.exists(file_path):
            tts = gTTS(txt, lang="pt-BR")
            time.sleep(0.5)

            try:
                tts.save(file_path)
            except:
                print("last_command file save error")

        playsound(file_path)

    def loop(self, txt=""):
        txt = txt + "" + self.microphone_listen()
        if any(word in txt for word in self.quit_keywords):
            self.quit = True

        elif any(word in txt for word in self.order_keywords):
            if not "path_configured" in txt:
                self.play_audio("Qual pedido de sempre?", "alternative_command.mp3")
                return self.loop(f"path_configured {txt}")

            if any(word in txt for word in ["um", "1"]):
                self.callback = ["default", 1]
                print("order 1")

            if any(word in txt for word in ["dois", "2"]):
                self.callback = ["default", 2]
                print("order 2")

            if any(word in txt for word in ["três", "3"]):
                self.callback = ["default", 3]
                print("order 3")

        else:
            return self.microphone_listen()

        print(txt)


ali = Alicia()
