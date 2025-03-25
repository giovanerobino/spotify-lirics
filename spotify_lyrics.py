"""
spotify_lyrics.py
Script para buscar a letra da música tocando no momento no Spotify e exibir na tela.

Dependências:
- spotipy
- BeautifulSoup
"""
import os
import requests
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from bs4 import BeautifulSoup

# Configurações das credenciais
SPOTIFY_CLIENT_ID = os.getenv("SPOTIFY_CLIENT_ID")
SPOTIFY_CLIENT_SECRET = os.getenv("SPOTIFY_CLIENT_SECRET")
GENIUS_ACCESS_TOKEN = os.getenv("GENIUS_ACCESS_TOKEN")

# Autenticação no Spotify
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
    client_id=SPOTIFY_CLIENT_ID,
    client_secret=SPOTIFY_CLIENT_SECRET,
    redirect_uri="http://localhost:8888/callback",
    scope="user-read-currently-playing"
))

def get_current_track():
    """Obtém a faixa que está tocando no momento no Spotify."""
    current_track = sp.currently_playing()
    if current_track and current_track['is_playing']:
        artist = current_track['item']['artists'][0]['name']
        track = current_track['item']['name']
        return artist, track
    return None, None

def get_lyrics(artist, track):
    """Obtém a letra da música através do Genius."""
    search_url = "https://api.genius.com/search"
    headers = {"Authorization": f"Bearer {GENIUS_ACCESS_TOKEN}"}
    params = {"q": f"{artist} {track}"}
    response = requests.get(search_url, headers=headers, params=params, timeout=10)

    if response.status_code != 200:
        return "Erro ao buscar música no Genius."

    json_data = response.json()
    hits = json_data['response']['hits']
    if not hits:
        return "Letra não encontrada."

    # Melhorando a precisão na escolha da música correta
    for hit in hits:
        if artist.lower() in hit['result']['primary_artist']['name'].lower():
            song_url = hit['result']['url']
            return scrape_lyrics(song_url)

    return "Letra não encontrada."

def scrape_lyrics(url):
    """Faz o scraping da letra da música a partir do Genius."""
    response = requests.get(url, timeout=10)
    if response.status_code != 200:
        return "Erro ao acessar a página da música."

    soup = BeautifulSoup(response.text, "html.parser")

    # Primeira tentativa: usando data-lyrics-container
    lyrics_divs = soup.find_all("div", attrs={"data-lyrics-container": "true"})
    if lyrics_divs:
        lyrics = '\n'.join([div.get_text(separator="\n") for div in lyrics_divs])
        return lyrics.strip()

    # Segunda tentativa: Estrutura alternativa
    lyrics_divs = soup.find_all("div", class_=lambda x: x and "Lyrics__Container" in x)
    if lyrics_divs:
        lyrics = '\n'.join([line.get_text(separator="\n") for div in lyrics_divs for line in div.find_all("p")])
        return lyrics.strip()

    return "Letra não encontrada."

def main():
    """Função principal do script."""
    artist, track = get_current_track()
    if artist and track:
        print(f"Tocando agora: {artist} - {track}\n")
        lyrics = get_lyrics(artist, track)
        print(lyrics)
    else:
        print("Nenhuma música tocando no momento.")

if __name__ == "__main__":
    main()
