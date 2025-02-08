import tkinter as tk
from tkinter import filedialog, messagebox
import os
import shutil
import re

def selecionar_logo():
    """
    Abre uma caixa de diálogo para o usuário selecionar o arquivo PNG que será utilizado como logo.
    Caso o arquivo selecionado não seja PNG, é exibida uma mensagem de erro.
    """
    file_path = filedialog.askopenfilename(
        title="Selecione o arquivo PNG para o logo",
        filetypes=[("Arquivos PNG", "*.png"), ("Todos os arquivos", "*.*")]
    )
    if file_path:
        if not file_path.lower().endswith(".png"):
            messagebox.showerror("Erro", "O arquivo selecionado não é um PNG.")
            return
        # Atualiza o campo de entrada com o caminho do arquivo selecionado
        entry_logo.delete(0, tk.END)
        entry_logo.insert(0, file_path)

def aplicar_modificacoes():
    """
    Esta função é responsável por:
    1. Ler os dados inseridos nos campos de 'Nome da Empresa', 'Descrição' e 'Contato';
    2. Atualizar o conteúdo da div <div class="company-info"> nos arquivos HTML;
    3. Copiar o arquivo de logo (PNG) para a pasta 'frontend', renomeando-o para 'logo.png'.
    """
    # Obtém os valores dos campos de entrada
    nome_empresa = entry_nome.get().strip()
    descricao = entry_descricao.get().strip()
    contato = entry_contato.get().strip()
    logo_path = entry_logo.get().strip()

    # Validação dos campos obrigatórios
    if not nome_empresa or not descricao or not contato:
        messagebox.showerror("Erro", "Preencha todos os campos de informações da empresa.")
        return

    # Monta o novo conteúdo HTML para a div 'company-info'
    nova_div = f'''<div class="company-info">
    <h2>{nome_empresa}</h2>
    <p>{descricao}</p>
    <p>{contato}</p>
</div>'''

    # Lista dos arquivos HTML que serão modificados
    arquivos = [
        os.path.join("frontend", "index.html"),
        os.path.join("frontend", "views", "consulta.html"),
        os.path.join("frontend", "views", "visualizar.html"),
        os.path.join("frontend", "views", "cadastro.html")
    ]

    # Expressão regular para identificar a div com class="company-info" (considera que pode haver quebras de linha)
    padrao_div = re.compile(r'(<div\s+class=["\']company-info["\'][^>]*>).*?(</div>)', re.DOTALL | re.IGNORECASE)

    # Processa cada arquivo da lista
    for arquivo in arquivos:
        if os.path.exists(arquivo):
            try:
                with open(arquivo, "r", encoding="utf-8") as f:
                    conteudo = f.read()
                # Se a div for encontrada, realiza a substituição
                if padrao_div.search(conteudo):
                    novo_conteudo = padrao_div.sub(nova_div, conteudo)
                else:
                    # Se não for encontrada, insere a div logo após a tag <body>
                    novo_conteudo = re.sub(r'(<body[^>]*>)', r'\1\n' + nova_div, conteudo, count=1, flags=re.IGNORECASE)
                with open(arquivo, "w", encoding="utf-8") as f:
                    f.write(novo_conteudo)
            except Exception as e:
                messagebox.showerror("Erro", f"Erro ao processar o arquivo {arquivo}.\nDetalhes: {e}")
                return
        else:
            messagebox.showwarning("Aviso", f"O arquivo {arquivo} não foi encontrado e será ignorado.")

    # Se um arquivo de logo foi selecionado, realiza a cópia para a pasta 'frontend' com o nome 'logo.png'
    if logo_path:
        if not logo_path.lower().endswith(".png"):
            messagebox.showerror("Erro", "O arquivo de logo deve estar no formato PNG.")
            return
        destino_logo = os.path.join("frontend", "logo.png")
        try:
            shutil.copy(logo_path, destino_logo)
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao copiar o arquivo de logo.\nDetalhes: {e}")
            return

    messagebox.showinfo("Sucesso", "As modificações foram aplicadas com sucesso.")

# Configuração da interface gráfica com tkinter
janela = tk.Tk()
janela.title("Personalizador de Arquivos HTML")
janela.geometry("600x300")

# Criação dos rótulos e campos de entrada para os dados da empresa
label_nome = tk.Label(janela, text="Nome da Empresa:")
label_nome.pack(anchor="w", padx=10, pady=(10, 0))
entry_nome = tk.Entry(janela, width=70)
entry_nome.pack(anchor="w", padx=10)

label_descricao = tk.Label(janela, text="Descrição:")
label_descricao.pack(anchor="w", padx=10, pady=(10, 0))
entry_descricao = tk.Entry(janela, width=70)
entry_descricao.pack(anchor="w", padx=10)

label_contato = tk.Label(janela, text="Contato:")
label_contato.pack(anchor="w", padx=10, pady=(10, 0))
entry_contato = tk.Entry(janela, width=70)
entry_contato.pack(anchor="w", padx=10)

# Campo e botão para a seleção do arquivo de logo
label_logo = tk.Label(janela, text="Selecione o arquivo de logo (PNG):")
label_logo.pack(anchor="w", padx=10, pady=(10, 0))
frame_logo = tk.Frame(janela)
frame_logo.pack(anchor="w", padx=10)
entry_logo = tk.Entry(frame_logo, width=50)
entry_logo.pack(side="left", fill="x", expand=True)
btn_selecionar_logo = tk.Button(frame_logo, text="Selecionar", command=selecionar_logo)
btn_selecionar_logo.pack(side="left", padx=5)

# Botão para aplicar as modificações
btn_aplicar = tk.Button(janela, text="Aplicar Modificações", command=aplicar_modificacoes, width=30)
btn_aplicar.pack(pady=20)

# Inicia o loop principal da interface
janela.mainloop()
