
!pip install easyocr
import os
import re
import io
import torch
import logging
import pandas as pd
import easyocr
import tweepy
import matplotlib.pyplot as plt
from PIL import Image
from transformers import pipeline
from IPython.display import display
from google.colab import files

logging.basicConfig(level=logging.INFO)

def limpar_numeros(texto: str) -> str:
    """Remove todos os caracteres não numéricos de uma string."""
    return re.sub(r'[^0-9]', '', texto)

def coletar_dados_do_usuario() -> tuple:
    nome = input("Digite seu nome completo: ")
    cpf = input("Digite seu CPF: ")
    endereco = input("Digite seu endereço: ")
    idade = input("Digite sua idade: ")
    interesses = input("Liste seus interesses em e-sports (separados por vírgula): ")
    eventos = input("Quais eventos de e-sports você participou no último ano? ")
    return nome, cpf, endereco, idade, interesses, eventos

def extrair_dados_do_documento(reader: easyocr.Reader) -> list:
    uploaded = files.upload()
    file_name = next(iter(uploaded))
    img = Image.open(io.BytesIO(uploaded[file_name]))
    plt.imshow(img)
    plt.axis('off')
    plt.show()
    results = reader.readtext(uploaded[file_name], detail=0)
    return results

def validar_cpf(cpf_usuario: str, results: list) -> None:
    cpf_usuario = limpar_numeros(cpf_usuario)
    for linha in results:
        linha_numeros = limpar_numeros(linha)
        if cpf_usuario in linha_numeros:
            print(f"✅ CPF encontrado na linha: {linha}")
            return
    print("❌ CPF NÃO encontrado no documento.")

def buscar_usuario_por_username(client, username: str):
    try:
        user = client.get_user(username=username, user_fields=["description", "location", "public_metrics"])
        return user.data
    except Exception as e:
        logging.error(f"Erro ao buscar usuário: {e}")
        return None

def buscar_tweets_do_usuario(client, user_id: str, max_resultados: int = 10) -> dict:
    tweets = client.get_users_tweets(id=user_id, max_results=max_resultados)
    temas = [tweet.text for tweet in tweets.data] if tweets.data else ["Nenhum tweet encontrado."]
    return {"temas_tweets": temas}

def buscar_informacoes_twitter(client, username: str) -> dict:
    try:
        user = client.get_user(username=username, user_fields=["description", "location", "public_metrics"])
        user_id = user.data.id
        tweets_info = buscar_tweets_do_usuario(client, user_id)
        return {
            "interacoes": "informações não disponíveis",
            "paginas_seguidas": "não especificado",
            "temas_tweets": tweets_info["temas_tweets"]
        }
    except Exception as e:
        logging.error(f"Erro ao buscar informações do Twitter: {e}")
        return None

def gerar_resumo_perfil(nome: str, idade: str, interesses: str, eventos: str, twitter_info: dict) -> str:
    texto = f"""
    Perfil do fã de eSports:

    Nome: {nome}
    Idade: {idade}

    Interesses declarados em eSports: {interesses}.

    Participou dos seguintes eventos de eSports no último ano: {eventos}.
    """
    if twitter_info:
        texto += f"\nBaseado nas redes sociais, interage frequentemente com: {twitter_info.get('interacoes')}."
        texto += f"\nSegue as páginas: {twitter_info.get('paginas_seguidas')}."
        texto += f"\nSeus últimos tweets mostram interesse em: {', '.join(twitter_info.get('temas_tweets', []))}."
    return texto.strip()

def avaliar_links_por_relevancia(perfil: str, links: list, classificador) -> list:
    links_relevantes = []
    for link in links:
        resultado = classificador(link["descricao"], candidate_labels=[perfil], hypothesis_template="Esse conteúdo é relevante para o seguinte perfil: {}.")
        score = resultado['scores'][0]
        if score > 0.2:
            links_relevantes.append((link["url"], score))
    return links_relevantes

def main():
    logging.info("🧡 Bem-vindo ao Know Your Fan 🧡")
    nome, cpf, endereco, idade, interesses, eventos = coletar_dados_do_usuario()
    dados_fan = pd.DataFrame({'Nome': [nome], 'CPF': [cpf], 'Endereço': [endereco], 'Idade': [idade], 'Interesses': [interesses], 'Eventos Participados': [eventos]})
    print("\n✅ Dados coletados com sucesso!\n")
    display(dados_fan)

    print("\nAgora vamos fazer o upload do seu documento de identificação (imagem).")
    reader = easyocr.Reader(['pt'])
    resultados_ocr = extrair_dados_do_documento(reader)
    print("\n📝 Texto detectado no documento:")
    for linha in resultados_ocr:
        print(linha)

    validar_cpf(cpf, resultados_ocr)

    BEARER_TOKEN = "AAAAAAAAAAAAAAAAAAAAALK50wEAAAAAKiuYzgn4W60u3J4DATN0zjGFhXE%3D2CMS9IEozs14zkomdK94p2F6YARZJcWcUZPG1lmUmEx0i9Qjua"
    client = tweepy.Client(bearer_token=BEARER_TOKEN)
    username = "TapitaTapitao"
    usuario = buscar_usuario_por_username(client, username)

    if usuario:
        print("Nome:", usuario.name)
        print("Username:", usuario.username)
        print("Bio:", usuario.description)
        print("Localização:", usuario.location)
        print("Seguidores:", usuario.public_metrics['followers_count'])
        print("Seguindo:", usuario.public_metrics['following_count'])

    twitter_info = buscar_informacoes_twitter(client, username)
    resumo_perfil = gerar_resumo_perfil(nome, idade, interesses, eventos, twitter_info)
    print("\n🧾 Resumo do perfil do fã:\n")
    print(resumo_perfil)

    links_disponiveis = [
        {"url": "https://www.hltv.org/team/8297/furia", "descricao": "Perfil da FURIA no HLTV"},
        {"url": "https://www.esports.net/news/valorant/", "descricao": "Times do VCT 2024"},
        {"url": "https://www.lolesports.com/teams/loud", "descricao": "Equipe LOUD no LoL"},
        {"url": "https://ge.globo.com/e-sports/noticia/gaules-bate-recorde-de-viewers.ghtml", "descricao": "Notícia sobre Gaules"},
        {"url": "https://www.fifa.com/fifaesports", "descricao": "Portal FIFAe"}
    ]

    device = 0 if torch.cuda.is_available() else -1
    classificador = pipeline("zero-shot-classification", model="facebook/bart-large-mnli", device=device)
    print("\n🔍 Analisando links com IA...")
    recomendados = avaliar_links_por_relevancia(resumo_perfil, links_disponiveis, classificador)

    print("\n🔗 Links recomendados para você:\n")
    for link, score in recomendados:
        print(f"{link} (relevância: {score:.2f})")

if __name__ == "__main__":
    main()
