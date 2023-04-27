import spotipy
from spotipy.oauth2 import SpotifyOAuth
import datetime
import logging

# 4. Configurar o log
logging.basicConfig(filename=__file__.replace('.py', '.log'), level=logging.INFO, format='%(asctime)s - %(message)s')

# Insira suas credenciais do Spotify
SPOTIFY_CLIENT_ID = ''
SPOTIFY_CLIENT_SECRET = ''
SPOTIFY_REDIRECT_URI = 'http://localhost:8000/callback'
USERNAME = ''

import env 

# Define o escopo para criar playlists e adicionar músicas
scope = "playlist-modify-public"

# Obtém a autorização do usuário
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=SPOTIFY_CLIENT_ID,
                                               client_secret=SPOTIFY_CLIENT_SECRET,
                                               redirect_uri=SPOTIFY_REDIRECT_URI,
                                               scope=scope,
                                               username=USERNAME))

# 1. Cria a playlist com o nome "Xadrak Rock da Eternidade"
playlist_name = 'Xadrak Rock da Eternidade'
new_playlist = sp.user_playlist_create(USERNAME, playlist_name, public=True)
logging.info(f"New playlist {playlist_name} created")

# 2. Procurar todos os álbuns da lista fornecida
album_list = [
    ('Linkin Park', 'Hybrid Theory'),
    ('Nirvana', 'Nevermind'),
    ('Guns N’ Roses', 'Appetite for Destruction'),
    ('Red Hot Chili Peppers', 'Californication'),
    ('Queen', 'A Night at the Opera'),
    ('Linkin Park', 'Meteora'),
    ('Metallica', 'Metallica'),
    ('Panic! At The Disco', 'Pray for the Wicked'),
    ('AC/DC', 'Back in Black'),
    ('Panic! At The Disco', 'Death of a Bachelor'),
    ('System Of A Down', 'Toxicity'),
    ('My Chemical Romance', 'The Black Parade'),
    ('Fall Out Boy', 'American Beauty/American Psycho'),
    ('Red Hot Chili Peppers', 'Stadium Arcadium'),
    ('Pink Floyd', 'The Wall'),
    ('Bon Jovi', 'Slippery When Wet'),
    ('Queen', 'The Game'),
    ('Green Day', 'American Idiot'),
    ('Queen', 'Jazz'),
    ('Red Hot Chili Peppers', 'By the Way'),
    ('Blink-182', 'Enema of the State'),
    ('Journey', 'Escape'),
    ('Red Hot Chili Peppers', 'Blood Sugar Sex Magik'),
    ('Linkin Park', 'Minutes to Midnight'),
    ('Queen', 'News of the World'),
    ('Fall Out Boy', 'Save Rock and Roll'),
    ('Green Day', 'Dookie'),
    ('Pink Floyd', 'The Dark Side of the Moon'),
    ('Led Zeppelin', 'Led Zeppelin IV'),
    ('Pearl Jam', 'Ten'),
]

all_track_ids = []

for artist, album in album_list:
    results = sp.search(q=f'artist:{artist} album:{album}', type='album')
    if results['albums']['items']:
        album_data = results['albums']['items'][0]
        album_id = album_data['id']
        logging.info(f"Found album {album} by {artist}")
        
        # 3. Adicionar todas as músicas de todos os álbuns nesta playlist
        tracks = sp.album_tracks(album_id)
        track_ids = [track['id'] for track in tracks['items']]
        all_track_ids.extend(track_ids)
        logging.info(f"Added tracks from album {album} by {artist} to the playlist")
    else:
        logging.info(f"Album {album} by {artist} not found")

# Divide os IDs de faixas em grupos de 100, pois essa é a quantidade máxima que a função suporta
for i in range(0, len(all_track_ids), 100):
    sp.playlist_add_items(new_playlist['id'], all_track_ids[i:i+100])

logging.info("All tracks added to the playlist")

# 6. Gerar uma lista de todas as músicas inseridas na playlist
with open(__file__.replace('.py', '.playlist'), 'w') as f:
    for track_id in all_track_ids:
        f.write(f"https://open.spotify.com/track/{track_id}\n")

logging.info("Playlist tracks saved to file")

