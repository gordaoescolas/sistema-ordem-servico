import tkinter as tk
from tkinter import messagebox, scrolledtext
import subprocess
import sys
import os
from threading import Thread
import webbrowser
import win32gui
import win32con

class ServerGUI:
    def __init__(self):
        # Esconde a janela do console
        hwnd = win32gui.GetForegroundWindow()
        win32gui.ShowWindow(hwnd, win32con.SW_HIDE)
        
        self.root = tk.Tk()
        self.root.title("Gerenciador do Servidor")
        self.root.geometry("600x400")
        
        # Configurar estilo
        self.root.configure(bg='#f0f0f0')
        
        self.server_process = None
        self.create_widgets()
        
    def create_widgets(self):
        # Frame principal
        main_frame = tk.Frame(self.root, bg='#f0f0f0')
        main_frame.pack(padx=20, pady=20, fill=tk.BOTH, expand=True)
        
        # Título
        title = tk.Label(
            main_frame,
            text="Gerenciador do Servidor",
            font=("Arial", 16, "bold"),
            bg='#f0f0f0'
        )
        title.pack(pady=10)
        
        # Log de saída
        self.log_area = scrolledtext.ScrolledText(
            main_frame,
            height=15,
            width=60,
            font=("Consolas", 10)
        )
        self.log_area.pack(pady=10)
        
        # Frame para botões
        button_frame = tk.Frame(main_frame, bg='#f0f0f0')
        button_frame.pack(pady=10)
        
        # Botão Iniciar
        self.start_btn = tk.Button(
            button_frame,
            text="Iniciar Servidor",
            command=self.start_server,
            bg='#28a745',
            fg='white',
            width=15,
            height=2
        )
        self.start_btn.pack(side=tk.LEFT, padx=5)
        
        # Botão Parar
        self.stop_btn = tk.Button(
            button_frame,
            text="Parar Servidor",
            command=self.stop_server,
            bg='#dc3545',
            fg='white',
            width=15,
            height=2,
            state=tk.DISABLED
        )
        self.stop_btn.pack(side=tk.LEFT, padx=5)
        
        # Botão Abrir Navegador
        self.browser_btn = tk.Button(
            button_frame,
            text="Abrir no Navegador",
            command=lambda: webbrowser.open('http://localhost'),
            bg='#007bff',
            fg='white',
            width=15,
            height=2,
            state=tk.DISABLED
        )
        self.browser_btn.pack(side=tk.LEFT, padx=5)
        
    def start_server(self):
        if self.server_process is None:
            try:
                # Caminho para o app.py
                app_path = os.path.join(os.path.dirname(__file__), 'backend', 'app.py')
                
                # Usa pythonw.exe para executar sem console
                python_exe = os.path.join(os.path.dirname(sys.executable), 'pythonw.exe')
                
                # Inicia o servidor Flask
                self.server_process = subprocess.Popen(
                    [python_exe, app_path],
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    universal_newlines=True,
                    creationflags=subprocess.CREATE_NO_WINDOW  # Esconde a janela do console
                )
                
                # Atualiza botões
                self.start_btn.config(state=tk.DISABLED)
                self.stop_btn.config(state=tk.NORMAL)
                self.browser_btn.config(state=tk.NORMAL)
                
                # Inicia thread para monitorar a saída
                Thread(target=self.monitor_output, daemon=True).start()
                
                self.log_area.insert(tk.END, "Servidor iniciado!\n")
                self.log_area.insert(tk.END, "Para acessar por outros computadores, use o IP deste computador.\n")
                
            except Exception as e:
                messagebox.showerror("Erro", f"Erro ao iniciar servidor: {str(e)}")
    
    def stop_server(self):
        if self.server_process:
            try:
                self.server_process.kill()
                self.server_process = None
                
                # Atualiza botões
                self.start_btn.config(state=tk.NORMAL)
                self.stop_btn.config(state=tk.DISABLED)
                self.browser_btn.config(state=tk.DISABLED)
                
                self.log_area.insert(tk.END, "Servidor parado.\n")
                messagebox.showinfo("Sucesso", "Servidor parado com sucesso!")
                
            except Exception as e:
                messagebox.showerror("Erro", f"Erro ao parar servidor: {str(e)}")
    
    def monitor_output(self):
        """Monitora a saída do servidor"""
        while self.server_process:
            output = self.server_process.stdout.readline()
            if output:
                self.log_area.insert(tk.END, output)
                self.log_area.see(tk.END)
    
    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    app = ServerGUI()
    app.run()