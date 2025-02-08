import json
import os
import shutil
from tkinter import *
from tkinter import filedialog, colorchooser, messagebox

class ConfigManager:
    def __init__(self):
        self.config_file = 'config.json'
        self.default_config = {
            "nome_empresa": "Nome da Empresa",
            "descricao": "Assistência Técnica Especializada",
            "contato": "(00) 0000-0000",
            "accent_color": "#007bff",
            "imagem": ""
        }

        self.root = Tk()
        self.root.title("Configurações do Sistema")
        self.root.geometry("600x550")
        self.create_widgets()
        self.load_config()

    def create_widgets(self):
        main_frame = Frame(self.root, padx=20, pady=20)
        main_frame.pack(fill=BOTH, expand=True)

        Label(main_frame, text="Nome da Empresa:").pack(pady=5)
        self.nome_entry = Entry(main_frame, width=50)
        self.nome_entry.pack(pady=5)

        Label(main_frame, text="Descrição:").pack(pady=5)
        self.desc_entry = Entry(main_frame, width=50)
        self.desc_entry.pack(pady=5)

        Label(main_frame, text="Contato:").pack(pady=5)
        self.contato_entry = Entry(main_frame, width=50)
        self.contato_entry.pack(pady=5)

        Button(main_frame, text="Selecionar Cor de Destaque", command=self.select_color).pack(pady=5)
        self.color_preview = Label(main_frame, width=20, height=2)
        self.color_preview.pack(pady=5)

        Button(main_frame, text="Selecionar Imagem PNG", command=self.select_image).pack(pady=5)
        
        button_frame = Frame(main_frame)
        button_frame.pack(pady=10)

        Button(button_frame, 
               text="Salvar Alterações", 
               command=self.save_and_apply,
               bg="#28a745", fg="white",
               width=20, height=2).pack(side=LEFT, padx=5)

        Button(button_frame, 
               text="Voltar", 
               command=self.root.destroy,
               bg="#dc3545", fg="white",
               width=20, height=2).pack(side=LEFT, padx=5)

    def select_color(self):
        color = colorchooser.askcolor(title="Escolha a cor de destaque")[1]
        if color:
            self.color_preview.config(bg=color)
            self.accent_color = color

    def select_image(self):
        file_path = filedialog.askopenfilename(filetypes=[("PNG files", "*.png")])
        if file_path:
            try:
                shutil.copy(file_path, "frontend/logo.png")
                shutil.copy(file_path, "frontend/views/logo.png")
                self.image_path = "logo.png"
            except Exception as e:
                messagebox.showerror("Erro", f"Erro ao salvar a imagem: {str(e)}")

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
                "imagem": self.image_path if hasattr(self, 'image_path') else ""
            }
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(config, f, ensure_ascii=False, indent=2)
            messagebox.showinfo("Sucesso", "Configurações salvas com sucesso!")
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao salvar configurações: {str(e)}")

    def save_and_apply(self):
        try:
            self.save_config()
            messagebox.showinfo("Sucesso", "Alterações salvas com sucesso!")
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao salvar alterações: {str(e)}")

    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    app = ConfigManager()
    app.run()
