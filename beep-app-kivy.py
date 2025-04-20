import kivy
from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
import threading
import time
import platform

kivy.require('2.0.0')  # versão do kivy necessária

def beep():
    """Função que toca o beep no Windows ou imprime no terminal em outros sistemas"""
    if platform.system() == "Windows":
        import winsound
        winsound.Beep(1000, 500)  # Frequência, Duração
    else:
        print('\a')

def beep_loop(interval, stop_event):
    """Faz o beep acontecer a cada 'interval' segundos até o stop_event ser ativado"""
    while not stop_event.is_set():
        beep()
        time.sleep(interval)

class BeepApp(App):
    def build(self):
        self.stop_event = threading.Event()

        # Layout principal
        self.layout = BoxLayout(orientation='vertical', padding=10, spacing=10)

        # Campo de texto para o tempo entre os beeps
        self.label_seconds = Label(text="Segundos entre beeps:")
        self.layout.add_widget(self.label_seconds)

        self.entry_seconds = TextInput(hint_text="Digite os segundos", multiline=False, input_filter='int')
        self.layout.add_widget(self.entry_seconds)

        # Botões
        self.start_button = Button(text="Iniciar Beep", on_press=self.start_beeping)
        self.layout.add_widget(self.start_button)

        self.stop_button = Button(text="Parar Beep", on_press=self.stop_beeping, disabled=True)
        self.layout.add_widget(self.stop_button)

        # Status
        self.label_status = Label(text="Insira o tempo e inicie o beep.")
        self.layout.add_widget(self.label_status)

        return self.layout

    def start_beeping(self, instance):
        """Inicia o loop de beeps com o intervalo escolhido"""
        try:
            interval = int(self.entry_seconds.text)  # Pega o valor do campo de entrada
            if interval <= 0:
                self.label_status.text = "Por favor, insira um número válido de segundos."
                return

            self.label_status.text = f"Beep a cada {interval} segundos."
            self.stop_event.clear()
            threading.Thread(target=beep_loop, args=(interval, self.stop_event), daemon=True).start()
            self.start_button.disabled = True
            self.stop_button.disabled = False
        except ValueError:
            self.label_status.text = "Por favor, insira um número válido de segundos."

    def stop_beeping(self, instance):
        """Interrompe o loop de beeps"""
        self.stop_event.set()
        self.label_status.text = "Beeping parado."
        self.start_button.disabled = False
        self.stop_button.disabled = True

if __name__ == '__main__':
    BeepApp().run()
