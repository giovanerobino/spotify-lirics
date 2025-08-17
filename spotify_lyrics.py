"""spotify_lyrics.py

Script CLI para exibir a faixa atual do Spotify e buscar a letra no Genius.

Features:
 - Spotify currently playing via Spotipy
 - Letra via API + scraping de fallback
 - Tipagem estática (Pyright strict)
 - Tratamento simples de erros de rede
"""
import os
from typing import Optional, Tuple, Any, Dict, cast

import requests
import spotipy  # type: ignore  # Biblioteca sem stubs oficiais
from spotipy.oauth2 import SpotifyOAuth  # type: ignore
from bs4 import BeautifulSoup

from dotenv import load_dotenv
load_dotenv()

SPOTIFY_CLIENT_ID: Optional[str] = os.getenv("SPOTIFY_CLIENT_ID")
SPOTIFY_CLIENT_SECRET: Optional[str] = os.getenv("SPOTIFY_CLIENT_SECRET")
GENIUS_ACCESS_TOKEN: Optional[str] = os.getenv("GENIUS_ACCESS_TOKEN")

if not (SPOTIFY_CLIENT_ID and SPOTIFY_CLIENT_SECRET):
    raise RuntimeError("Credenciais Spotify ausentes. Defina SPOTIFY_CLIENT_ID e SPOTIFY_CLIENT_SECRET no .env")

if not GENIUS_ACCESS_TOKEN:
    raise RuntimeError("Token do Genius ausente. Defina GENIUS_ACCESS_TOKEN no .env")

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
    client_id=SPOTIFY_CLIENT_ID,
    client_secret=SPOTIFY_CLIENT_SECRET,
    redirect_uri="http://localhost:8888/callback",
    scope="user-read-currently-playing"
))

def get_current_track() -> Tuple[Optional[str], Optional[str]]:
    """Obtém (artista, faixa) que está tocando agora, ou (None, None)."""
    current_track: Any = sp.currently_playing()  # type: ignore  # API sem tipagem
    if isinstance(current_track, dict):
        track_dict = cast(Dict[str, Any], current_track)
        if not (track_dict.get('is_playing') and track_dict.get('item')):
            return None, None
        item = cast(Dict[str, Any], track_dict['item'])
        artists_raw = item.get('artists')
        artist_name: Optional[str] = None
        if isinstance(artists_raw, list) and artists_raw:  # type: ignore[arg-type]
            first_artist: Any = cast(Any, artists_raw[0])  # type: ignore[index]
            if isinstance(first_artist, dict):
                name_val: Any = first_artist.get('name')  # type: ignore[call-arg]
                if isinstance(name_val, str):
                    artist_name = name_val
        track_val = item.get('name')
        if isinstance(artist_name, str) and isinstance(track_val, str):
            return artist_name, track_val
    return None, None

def get_lyrics(artist: str, track: str) -> str:
    """Obtém a letra da música através da API do Genius e scraping.

    Retorna mensagem de erro ou a letra completa.
    """
    search_url = "https://api.genius.com/search"
    headers = {"Authorization": f"Bearer {GENIUS_ACCESS_TOKEN}"}
    params = {"q": f"{artist} {track}"}
    try:
        response = requests.get(search_url, headers=headers, params=params, timeout=10)
    except requests.RequestException as exc:
        return f"Erro de rede ao buscar música: {exc}"

    if response.status_code != 200:
        return "Erro ao buscar música no Genius."

    json_data = response.json()
    hits = json_data['response']['hits']
    if not hits:
        return "Letra não encontrada."

    for hit in hits:
        result = hit.get('result', {})
        primary_artist = result.get('primary_artist', {})
        artist_name = primary_artist.get('name', '')
        if isinstance(artist_name, str) and artist.lower() in artist_name.lower():
            song_url = result.get('url')
            if isinstance(song_url, str):
                return scrape_lyrics(song_url)

    return "Letra não encontrada."

def scrape_lyrics(url: str) -> str:
    """Faz o scraping da letra da música a partir da página do Genius."""
    try:
        response = requests.get(url, timeout=10)
    except requests.RequestException as exc:
        return f"Erro de rede ao acessar a página: {exc}"

    if response.status_code != 200:
        return "Erro ao acessar a página da música."

    soup = BeautifulSoup(response.text, "html.parser")

    container_divs = soup.select('div[data-lyrics-container="true"]')
    if container_divs:
        joined = '\n'.join(div.get_text(separator='\n') for div in container_divs)
        return joined.strip()

    alt_divs = soup.select('div[class*="Lyrics__Container"]')
    if alt_divs:
        joined = '\n'.join(div.get_text(separator='\n') for div in alt_divs)
        return joined.strip()

    return "Letra não encontrada."

def main() -> None:
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
