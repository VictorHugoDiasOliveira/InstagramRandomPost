import random
import instaloader
import webbrowser
import re
import os
from dotenv import load_dotenv

load_dotenv()

class InstagramUrlParser:
    def __init__(self):
        url_wordlist = self.read_wordlist("wordlist.txt")
        self.url = self.url_picker(url_wordlist)
    
    def get_username(self):
        # Expressão regular para extrair o nome de usuário
        regex = r"https://www\.instagram\.com/([A-Za-z0-9_.]+)\/?"

        # Procura por correspondências na URL
        match = re.search(regex, self.url)

        if match:
            return match.group(1)
        else:
            raise Exception(f"Desculpe, url {self.url} invalida")
        
    def url_picker(self, url_wordlist):
        return random.choice(list(url_wordlist))
    
    def read_wordlist(self, file_name):
        wordlist_array = []
        try:
            with open(file_name, 'r') as file:
                wordlist_array = file.readlines()
            # Remover quebras de linha do final de cada linha
            wordlist_array = [linha.strip() for linha in wordlist_array]
        except FileNotFoundError:
            print(f"Arquivo {file_name} não encontrado.")
        return wordlist_array


def fetch_random_post(L, username):
    profile = instaloader.Profile.from_username(L.context, username)
    posts = profile.get_posts()

    # Conta o número total de posts
    total_posts = profile.mediacount

    # Seleciona um índice aleatório
    random_index = random.randint(0, total_posts - 1)

    # Itera sobre os posts e pega o post no índice selecionado
    for idx, post in enumerate(posts):
        if idx == random_index:
            return post

    raise Exception("Nenhuma postagem encontrada")

# Cria uma instância do instaloader
L = instaloader.Instaloader()
L.login(os.getenv('LOGIN'), os.getenv('PASSWORD'))

parser = InstagramUrlParser()
username = parser.get_username()

try:
    random_post = fetch_random_post(L, username)
    random_post_url = f"https://www.instagram.com/p/{random_post.shortcode}/"
    
    webbrowser.open(random_post_url)
    print(f"Post aleatório: {random_post_url}")

except instaloader.ProfileNotExistsException:
    print("O perfil não existe.")
except Exception as e:
    print("Ocorreu um erro:", e)
