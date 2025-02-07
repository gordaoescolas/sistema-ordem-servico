import json
import os
import base64
from tkinter import *
from tkinter import filedialog, colorchooser, messagebox
import sys
import win32gui
import win32con

class ConfigManager:
    def __init__(self):
        self.config_file = 'config.json'
        self.default_config = {
            "nome_empresa": "Nome da Empresa",
            "descricao": "Assistência Técnica Especializada",
            "contato": "(00) 0000-0000",
            "accent_color": "#007bff",
            "logo": None
        }
        
        # Esconde a janela do console
        if os.path.splitext(sys.executable)[1].lower() == '.exe':
            hwnd = win32gui.GetForegroundWindow()
            win32gui.ShowWindow(hwnd, win32con.SW_HIDE)
        
        self.root = Tk()
        self.root.title("Configurações do Sistema")
        self.root.geometry("600x600")
        self.create_widgets()
        self.load_config()

    def create_widgets(self):
        # Frame principal
        main_frame = Frame(self.root, padx=20, pady=20)
        main_frame.pack(fill=BOTH, expand=True)

        # Logo
        Button(main_frame, text="Selecionar Logo", command=self.select_logo).pack(pady=5)
        self.logo_preview = Label(main_frame)
        self.logo_preview.pack(pady=5)

        # Nome da Empresa
        Label(main_frame, text="Nome da Empresa:").pack(pady=5)
        self.nome_entry = Entry(main_frame, width=50)
        self.nome_entry.pack(pady=5)

        # Descrição
        Label(main_frame, text="Descrição:").pack(pady=5)
        self.desc_entry = Entry(main_frame, width=50)
        self.desc_entry.pack(pady=5)

        # Contato
        Label(main_frame, text="Contato:").pack(pady=5)
        self.contato_entry = Entry(main_frame, width=50)
        self.contato_entry.pack(pady=5)

        # Cor de Destaque
        Button(main_frame, text="Selecionar Cor de Destaque", command=self.select_color).pack(pady=5)
        self.color_preview = Label(main_frame, width=20, height=2)
        self.color_preview.pack(pady=5)

        # Frame para os botões
        button_frame = Frame(main_frame)
        button_frame.pack(pady=10)

        # Botões
        Button(button_frame, 
               text="Salvar Alterações", 
               command=self.save_and_apply,
               bg="#28a745",  # Verde
               fg="white",
               width=20,
               height=2).pack(side=LEFT, padx=5)

        Button(button_frame, 
               text="Voltar", 
               command=self.root.destroy,
               bg="#dc3545",  # Vermelho
               fg="white",
               width=20,
               height=2).pack(side=LEFT, padx=5)

    def select_logo(self):
        file_path = filedialog.askopenfilename(
            filetypes=[("Imagens", "*.png *.jpg *.jpeg")]
        )
        if file_path:
            with open(file_path, "rb") as image_file:
                encoded_string = base64.b64encode(image_file.read()).decode()
                self.logo_data = f"data:image/png;base64,{encoded_string}"
                # Mostrar preview
                from PIL import Image, ImageTk
                image = Image.open(file_path)
                image = image.resize((150, 150), Image.Resampling.LANCZOS)
                photo = ImageTk.PhotoImage(image)
                self.logo_preview.config(image=photo)
                self.logo_preview.image = photo

    def select_color(self):
        color = colorchooser.askcolor(title="Escolha a cor de destaque")[1]
        if color:
            self.color_preview.config(bg=color)
            self.accent_color = color

    def load_config(self):
        try:
            if os.path.exists(self.config_file):
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    config = json.load(f)
                    self.nome_entry.insert(0, config.get('nome_empresa', ''))
                    self.desc_entry.insert(0, config.get('descricao', ''))
                    self.contato_entry.insert(0, config.get('contato', ''))
                    self.accent_color = config.get('accent_color', '#007bff')
                    self.color_preview.config(bg=self.accent_color)
                    self.logo_data = config.get('logo', None)
                    if self.logo_data:
                        # TODO: Mostrar preview da logo salva
                        pass
            else:
                self.nome_entry.insert(0, self.default_config['nome_empresa'])
                self.desc_entry.insert(0, self.default_config['descricao'])
                self.contato_entry.insert(0, self.default_config['contato'])
                self.accent_color = self.default_config['accent_color']
                self.color_preview.config(bg=self.accent_color)
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao carregar configurações: {str(e)}")

    def save_config(self):
        try:
            config = {
                "nome_empresa": self.nome_entry.get(),
                "descricao": self.desc_entry.get(),
                "contato": self.contato_entry.get(),
                "accent_color": self.accent_color,
                "logo": getattr(self, 'logo_data', None)
            }
            
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(config, f, ensure_ascii=False, indent=2)
            
            self.apply_config()
            messagebox.showinfo("Sucesso", "Configurações salvas com sucesso!")
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao salvar configurações: {str(e)}")

    def apply_config(self):
        """Aplica as configurações a todos os arquivos HTML"""
        try:
            # Lista de arquivos HTML
            html_files = [
                'frontend/index.html',
                'frontend/views/cadastro.html',
                'frontend/views/consulta.html',
                'frontend/views/visualizar.html'
            ]
            
            # Atualiza o CSS
            self.update_css()
            
            # Atualiza os HTMLs
            for html_file in html_files:
                self.update_html(html_file)
                
            messagebox.showinfo("Sucesso", "Configurações aplicadas com sucesso!")
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao aplicar configurações: {str(e)}")

    def update_css(self):
        """Atualiza o arquivo CSS com a nova cor de destaque"""
        css_file = 'frontend/css/style.css'
        try:
            with open(css_file, 'r', encoding='utf-8') as f:
                css = f.read()
            
            # Atualiza a cor de destaque
            import re
            css = re.sub(
                r'--accent-color:\s*#[0-9a-fA-F]{6};',
                f'--accent-color: {self.accent_color};',
                css
            )
            
            with open(css_file, 'w', encoding='utf-8') as f:
                f.write(css)
        except Exception as e:
            raise Exception(f"Erro ao atualizar CSS: {str(e)}")

    def update_html(self, html_file):
        """Atualiza um arquivo HTML com as novas configurações"""
        try:
            with open(html_file, 'r', encoding='utf-8') as f:
                html = f.read()
            
            # Atualiza os campos
            import re
            html = re.sub(
                r'<h2>.*?</h2>',
                f'<h2>{self.nome_entry.get()}</h2>',
                html
            )
            html = re.sub(
                r'<p>Assistência.*?</p>',
                f'<p>{self.desc_entry.get()}</p>',
                html
            )
            html = re.sub(
                r'<p>Contato:.*?</p>',
                f'<p>Contato: {self.contato_entry.get()}</p>',
                html
            )
            
            # Atualiza a logo
            if hasattr(self, 'logo_data'):
                html = re.sub(
                    r'src="/images/logo.png"',
                    f'src="{self.logo_data}"',
                    html
                )
            
            with open(html_file, 'w', encoding='utf-8') as f:
                f.write(html)
        except Exception as e:
            raise Exception(f"Erro ao atualizar {html_file}: {str(e)}")

    def save_and_apply(self):
        """Salva e aplica as configurações"""
        try:
            self.save_config()
            self.apply_config()
            messagebox.showinfo("Sucesso", "Alterações salvas e aplicadas com sucesso!")
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao salvar alterações: {str(e)}")

    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    app = ConfigManager()
    app.run()