"""
spotify_lyrics.py
Script para buscar a letra da música tocando no momento no Spotify e exibir na tela.

Dependências:
- spotipy
- lyricsgenius
"""
import os
from dotenv import load_dotenv
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from lyricsgenius import Genius

load_dotenv()

# Configurações do Spotify
SPOTIFY_CLIENT_ID = os.getenv('SPOTIFY_CLIENT_ID') #'seu_spotify_client_id'
SPOTIFY_CLIENT_SECRET = os.getenv('SPOTIFY_CLIENT_SECRET') #'seu_spotify_client_secret'
SPOTIFY_REDIRECT_URI = 'http://localhost:8888/callback'  # Pode ser alterado

# Configurações do Genius
GENIUS_ACCESS_TOKEN = os.getenv('GENIUS_ACCESS_TOKEN') #'seu_genius_access_token'

# Inicializar Spotify e Genius
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
    client_id=SPOTIFY_CLIENT_ID,
    client_secret=SPOTIFY_CLIENT_SECRET,
    redirect_uri=SPOTIFY_REDIRECT_URI,
    scope="user-read-playback-state"
))

genius = Genius(GENIUS_ACCESS_TOKEN)

def get_current_track():
    """
    Obtém a música que está sendo ouvida no Spotify.
    Nota: O spotify precisa estar tocando no browser
    """
    current_track = sp.current_playback()
    if current_track and current_track['is_playing']:
        track_name = current_track['item']['name']
        artist_name = current_track['item']['artists'][0]['name']
        return track_name, artist_name
    else:
        return None, None

def get_lyrics(track_name, artist_name):
    """Busca a letra da música no Genius."""
    song = genius.search_song(track_name, artist_name)
    if song:
        lyrics = song.lyrics
        # Remove a primeira linha que contém informações extras
        if '\n' in lyrics:
            lyrics = lyrics.split('\n', 1)[1]
        # Remove o número e "Embed" do final da letra
        lyrics = lyrics.strip()
        import re
        lyrics = re.sub(r'\d+Embed$', '', lyrics)
        return lyrics
    return "Letra não encontrada."

if __name__ == "__main__":
    track, artist = get_current_track()
    if track and artist:
        print(f"Tocando agora: {track} - {artist}")
        lyrics = get_lyrics(track, artist)
        print("\nLetra da música:\n")
        print(lyrics)
    else:
        print("Nenhuma música tocando no momento.")
