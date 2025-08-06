import tkinter as tk
from tkinter import ttk, simpledialog
import requests
import keyboard

class CronometroFutsal:
    def __init__(self, master):
        self.master = master
        self.master.title("Cronômetro de Futsal")
        self.running = False
        self.total_time = 20 * 60
        self.remaining = self.total_time
        self.tempo_atual = "1º Tempo"

        # Rótulo do cronômetro
        self.label = ttk.Label(master, text=self.format_time(), font=("Roboto", 20))
        self.label.pack(pady=20)

        # Rótulo do período (1º/2º tempo)
        self.label_tempo = ttk.Label(master, text=self.tempo_atual, font=("Arial", 20))
        self.label_tempo.pack(pady=5)

        # Botões
        self.btn_toggle = ttk.Button(master, text="Iniciar / Pausar (Espaço)", command=self.toggle)
        self.btn_toggle.pack(pady=5)

        self.btn_reset = ttk.Button(master, text="Resetar Tempo", command=self.resetar_tempo)
        self.btn_reset.pack(pady=5)

        self.btn_inserir = ttk.Button(master, text="Inserir Tempo Manualmente", command=self.inserir_tempo_manual)
        self.btn_inserir.pack(pady=5)

        # Atalho de espaço para iniciar/pausar
        keyboard.add_hotkey('-', self.toggle)

        self.atualizar_tela()
        self.enviar_para_vmix()

    def toggle(self):
        self.running = not self.running

    def resetar_tempo(self):
        self.running = False
        self.remaining = self.total_time
        self.enviar_para_vmix()

    def inserir_tempo_manual(self):
        entrada = simpledialog.askstring("Tempo manual", "Insira o tempo (MM:SS):", parent=self.master)
        if entrada:
            try:
                minutos, segundos = map(int, entrada.strip().split(":"))
                self.remaining = minutos * 60 + segundos
                self.enviar_para_vmix()
            except:
                print("Formato inválido. Use MM:SS.")

    def format_time(self):
        minutos = self.remaining // 60
        segundos = self.remaining % 60
        return f"{minutos:02}:{segundos:02}"

    def enviar_para_vmix(self):
        tempo = self.format_time()
        try:
            titulo = "TimerTitle" #INSERIR O NOME EXATO DO CAMPO NAME DO VMIX
            campo_tempo = "Heading"   # INSERIR O NOME EXATO DO CAMPO NO VMIX
            
            url1 = f"http://localhost:8088/API/?Function=SetText&Input={titulo}&SelectedName={campo_tempo}&Value={tempo}"
            requests.get(url1)

        except Exception as e:
            print("Erro ao enviar para vMix:", e)

    def atualizar_tela(self):
        if self.running and self.remaining > 0:
            self.remaining -= 1
            self.enviar_para_vmix()
        self.label.config(text=self.format_time())
        self.master.after(1000, self.atualizar_tela)

# Executar o app
root = tk.Tk()
app = CronometroFutsal(root)
root.mainloop()

