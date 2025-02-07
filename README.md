# 📌 Sistema de Ordens de Serviço

Um sistema de gerenciamento de ordens de serviço (OS) desenvolvido em Python e tecnologias web.

## 📋 Requisitos

- Python 3.x
- pywin32 (para Windows)
- Flask
- tkinter

## 📂 Estrutura do Projeto

```
📁 backend/
  ├── app.py          # Servidor Flask
  ├── data/           # Armazena as OS em JSON
📁 frontend/
  ├── index.html      # Página inicial
  📁 css/
    ├── style.css     # Estilos do sistema
  📁 js/
    ├── script.js     # Lógica do frontend
  📁 views/
    ├── cadastro.html # Formulário de nova OS
    ├── consulta.html # Lista de OS
    ├── visualizar.html # Ver/editar OS
📄 config.json        # Configurações do sistema
```

## 🚀 Como Executar

1. Execute `Iniciar Servidor.py` para iniciar o servidor web.
2. Acesse [http://localhost](http://localhost) o o IP do host no navegador.
3. Use `Personalizar o Cabeçalho.py` para customizar o cabeçalho.

## ✨ Funcionalidades

✅ Cadastro de ordens de serviço  
✅ Consulta e pesquisa de OS  
✅ Edição e exclusão de OS  
✅ Impressão de OS  
✅ Personalização do cabeçalho e identidade visual  

## 📑 Campos da OS

- **📌 Dados do cliente**
- **🖥️ Equipamento**
- **🔧 Defeito relatado**
- **🛠️ Serviço executado**
- **📊 Status**
- **💰 Valores**
- **💳 Forma de pagamento**
- **👨‍🔧 Técnico responsável**
- **📝 Observações**

## Licença

Distribuído sob Licença de Uso Livre Não Comercial. Veja `LICENSE` para mais informações.

Desenvolvido por Gordão Escolas - 🔗 [GitHub](https://github.com/gordaoescolas)
