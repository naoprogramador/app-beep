import tkinter as tk
import threading
import time
import platform

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

def start_beeping():
    """Inicia o loop de beeps com o intervalo escolhido"""
    try:
        interval = int(entry_seconds.get())  # Pega o valor do campo de entrada
        if interval <= 0:
            label_status.config(text="Por favor, insira um número válido de segundos.")
            return
        
        label_status.config(text=f"Beep a cada {interval} segundos.")
        stop_event.clear()
        threading.Thread(target=beep_loop, args=(interval, stop_event), daemon=True).start()
        start_button.config(state=tk.DISABLED)
        stop_button.config(state=tk.NORMAL)
    except ValueError:
        label_status.config(text="Por favor, insira um número válido de segundos.")

def stop_beeping():
    """Interrompe o loop de beeps"""
    stop_event.set()
    label_status.config(text="Beeping parado.")
    start_button.config(state=tk.NORMAL)
    stop_button.config(state=tk.DISABLED)

# Criar a interface gráfica
root = tk.Tk()
root.title("App de Beep")

stop_event = threading.Event()

# Campo para definir os segundos
label_seconds = tk.Label(root, text="Segundos entre beeps:")
label_seconds.pack()

entry_seconds = tk.Entry(root)
entry_seconds.pack()

# Botões de iniciar e parar
start_button = tk.Button(root, text="Iniciar Beep", command=start_beeping)
start_button.pack()

stop_button = tk.Button(root, text="Parar Beep", command=stop_beeping, state=tk.DISABLED)
stop_button.pack()

# Status do app
label_status = tk.Label(root, text="Insira o tempo e inicie o beep.")
label_status.pack()

# Rodar a interface gráfica
root.mainloop()
