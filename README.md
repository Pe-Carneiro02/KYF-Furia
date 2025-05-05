
# 🎮 Know Your Fan

## 📖 Descrição

Este projeto tem como objetivo criar um sistema de análise de fãs de eSports, coletando dados do usuário, extraindo informações de documentos com OCR e buscando dados adicionais na internet (Twitter) para gerar um perfil detalhado e recomendar conteúdo relevante.

---

## ✨ Funcionalidades

### 🔹 Coleta de Dados do Usuário
- Solicita nome, idade, interesses em eSports e eventos que participou.
- Armazena os dados em um `DataFrame` do `Pandas`.

### 🔹 Extração de Dados de Documentos
- Permite o upload de um documento de identificação (imagem).
- Utiliza `EasyOCR` para extrair texto.
- Valida o CPF informado com o extraído do documento.

### 🔹 Busca de Informações no Twitter
- Utiliza `Tweepy` para buscar dados de um perfil no Twitter.
- Extrai nome, localização, número de seguidores e tweets recentes.
- Analisa os tweets para identificar temas de interesse.

### 🔹 Geração de Resumo e Recomendações
- Cria um resumo do perfil do fã.
- Usa `Transformers` da Hugging Face para avaliar a relevância de links.
- Recomenda links personalizados com base na análise.

---

## 🛠️ Instalação

Requisitos:
- Python 3

### 📦 Instale as bibliotecas:

```bash
pip install easyocr
pip install tweepy
pip install transformers
pip install torch
apt-get update
apt-get install -y ca-certificates
update-ca-certificates
```

---

## 🔐 Credenciais do Twitter

- Crie uma conta de desenvolvedor no Twitter.
- Obtenha o Bearer Token da API.
- Substitua `YOUR_BEARER_TOKEN` no código pelo seu token.

---

## ▶️ Uso

- Execute o código no **Google Colab** ou em um ambiente **Jupyter Notebook**.
- Siga as instruções para:
  - Inserir seus dados
  - Fazer upload do documento
- O sistema irá gerar um resumo do perfil e recomendar links relevantes.

---

## 🧩 Estrutura do Código

As principais funções do sistema são:

- `coletar_dados_do_usuario()`
- `extrair_dados_do_documento()`
- `validar_cpf()`
- `buscar_informacoes_twitter()`
- `gerar_resumo_e_recomendacoes()`

---

## 💡 Melhorias Futuras

- Extrair interações e páginas seguidas do Twitter.
- Adicionar mais fontes de dados externas.
- Refinar o modelo de recomendação.

---

