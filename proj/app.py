from dotenv import load_dotenv
import base64
import os
import base64
import requests
import re
import json
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from flask import Flask, url_for, session, request, redirect, render_template
import time
from bs4 import BeautifulSoup

load_dotenv()

client_id = os.getenv("CLIENT_ID")
client_secret = os.getenv("CLIENT_SECRET")

print(client_id, client_secret)

app = Flask(__name__)

app.secret_key = 'SOMETHING-RANDOM'
app.config['SESSION_COOKIE_NAME'] = 'spotify-login-session'

redirect_uri = "http://127.0.0.1:5000"

def getHTMLdocument(url): 
    response = requests.get(url) 
    print(response)
    return response.text 

with open("lolla2025.htm", "r") as file:
    html_content = file.read()
soup = BeautifulSoup(html_content, 'html.parser') 
artistHTML = soup.select_one("div.hublineup").find_all('li')
lineup = [artist.get_text() for artist in artistHTML]

@app.route('/')
def login():
    sp_oauth = create_spotify_oauth()
    auth_url = sp_oauth.get_authorize_url()
    print(auth_url)
    return redirect(auth_url)

@app.route('/authorize')
def authorize():
    sp_oauth = create_spotify_oauth()
    session.clear()
    code = request.args.get('code')
    token_info = sp_oauth.get_access_token(code)
    session["token_info"] = token_info
    return redirect("/getArtists")

@app.route('/logout')
def logout():
    for key in list(session.keys()):
        session.pop(key)
    return redirect('/')

@app.route('/getArtists')
def get_artists():
    # session['token_info'], authorized = get_token()
    # session.modified = True
    # if not authorized:
    #     return redirect('/')
    # sp = spotipy.Spotify(auth=session.get('token_info').get('access_token'))
    # top_artist_ranked = []
    # top_artists = {}
    # recommended_artists = {}
    # favorite_genres = {}
    # iter = 0

    # lowercase_lineup = [lineup_artist.lower() for lineup_artist in lineup]

    # while True:
    #     offset = iter * 50
    #     iter += 1
    #     curGroup = sp.current_user_top_artists(limit=50, time_range='long_term', offset=offset)['items']
    #     for artist in curGroup:
    #         if artist['name'].lower() in lowercase_lineup:
    #             top_artist_ranked += [artist['name']]
    #             top_artists[artist['name']] = {'id': artist['id'], 'images': artist['images'], 'external_urls': artist['external_urls']}
    #             for genre in artist['genres']:
    #                 favorite_genres[genre] = favorite_genres.get(genre, 0) + 1
    #     if (len(curGroup) < 50):
    #         break
    
    # overlap = [artist for artist in top_artists.keys() if artist.lower() in lowercase_lineup]
    
    # for artist in lineup:
    #     artistResult = sp.search(q=artist,limit=10,type="artist")['artists']['items'][0]
    #     if artistResult['genres'] != [] and artistResult['name'] not in overlap:
    #         for genre in artistResult['genres']:
    #             if genre in favorite_genres:
    #                 recommended_artists[artistResult['name']] = {'genres': artistResult['genres'], 'id':artistResult['id'], 'images':artistResult['images'], 'external_urls': artistResult['external_urls']}
    #                 break
    #             break
    
    # result = {'top_artists_ranked': top_artist_ranked, 'favorite_artists_attending': top_artists, 'recommended_artists': recommended_artists}
    # print(result)

    result = {'top_artists_ranked': ['Xdinary Heroes', 'wave to earth', 'TWICE', 'Sabrina Carpenter', 'Fujii Kaze', 'Clairo', 'Tyler, The Creator', 'Olivia Rodrigo', 'BOYNEXTDOOR', 'hey, nothing', 'Wasia Project', 'The Marías', 'Wallows'], 'favorite_artists_attending': {'Xdinary Heroes': {'id': '1khChLj7REGqjM043PlYyn', 'images': [{'height': 640, 'url': 'https://i.scdn.co/image/ab6761610000e5eb30d64c6cd2d9e685d5580296', 'width': 640}, {'height': 320, 'url': 'https://i.scdn.co/image/ab6761610000517430d64c6cd2d9e685d5580296', 'width': 320}, {'height': 160, 'url': 'https://i.scdn.co/image/ab6761610000f17830d64c6cd2d9e685d5580296', 'width': 160}], 'external_urls': {'spotify': 'https://open.spotify.com/artist/1khChLj7REGqjM043PlYyn'}}, 'wave to earth': {'id': '5069JTmv5ZDyPeZaCCXiCg', 'images': [{'height': 640, 'url': 'https://i.scdn.co/image/ab6761610000e5eb49799010fa77f1f862ab207e', 'width': 640}, {'height': 320, 'url': 'https://i.scdn.co/image/ab6761610000517449799010fa77f1f862ab207e', 'width': 320}, {'height': 160, 'url': 'https://i.scdn.co/image/ab6761610000f17849799010fa77f1f862ab207e', 'width': 160}], 'external_urls': {'spotify': 'https://open.spotify.com/artist/5069JTmv5ZDyPeZaCCXiCg'}}, 'TWICE': {'id': '7n2Ycct7Beij7Dj7meI4X0', 'images': [{'height': 640, 'url': 'https://i.scdn.co/image/ab6761610000e5ebca6c145421fa9ceb58d6f9d4', 'width': 640}, {'height': 320, 'url': 'https://i.scdn.co/image/ab67616100005174ca6c145421fa9ceb58d6f9d4', 'width': 320}, {'height': 160, 'url': 'https://i.scdn.co/image/ab6761610000f178ca6c145421fa9ceb58d6f9d4', 'width': 160}], 'external_urls': {'spotify': 'https://open.spotify.com/artist/7n2Ycct7Beij7Dj7meI4X0'}}, 'Sabrina Carpenter': {'id': '74KM79TiuVKeVCqs8QtB0B', 'images': [{'height': 640, 'url': 'https://i.scdn.co/image/ab6761610000e5ebe053b8338322b9c8609ee7ae', 'width': 640}, {'height': 320, 'url': 'https://i.scdn.co/image/ab67616100005174e053b8338322b9c8609ee7ae', 'width': 320}, {'height': 160, 'url': 'https://i.scdn.co/image/ab6761610000f178e053b8338322b9c8609ee7ae', 'width': 160}], 'external_urls': {'spotify': 'https://open.spotify.com/artist/74KM79TiuVKeVCqs8QtB0B'}}, 'Fujii Kaze': {'id': '6bDWAcdtVR3WHz2xtiIPUi', 'images': [{'height': 640, 'url': 'https://i.scdn.co/image/ab6761610000e5ebd3828da41bb2b2a02886b16f', 'width': 640}, {'height': 320, 'url': 'https://i.scdn.co/image/ab67616100005174d3828da41bb2b2a02886b16f', 'width': 320}, {'height': 160, 'url': 'https://i.scdn.co/image/ab6761610000f178d3828da41bb2b2a02886b16f', 'width': 160}], 'external_urls': {'spotify': 'https://open.spotify.com/artist/6bDWAcdtVR3WHz2xtiIPUi'}}, 'Clairo': {'id': '3l0CmX0FuQjFxr8SK7Vqag', 'images': [{'height': 640, 'url': 'https://i.scdn.co/image/ab6761610000e5eb4804c4a44c85afea1a72d1bd', 'width': 640}, {'height': 320, 'url': 'https://i.scdn.co/image/ab676161000051744804c4a44c85afea1a72d1bd', 'width': 320}, {'height': 160, 'url': 'https://i.scdn.co/image/ab6761610000f1784804c4a44c85afea1a72d1bd', 'width': 160}], 'external_urls': {'spotify': 'https://open.spotify.com/artist/3l0CmX0FuQjFxr8SK7Vqag'}}, 'Tyler, The Creator': {'id': '4V8LLVI7PbaPR0K2TGSxFF', 'images': [{'height': 640, 'url': 'https://i.scdn.co/image/ab6761610000e5ebdfa2b0c7544a772042a12e52', 'width': 640}, {'height': 320, 'url': 'https://i.scdn.co/image/ab67616100005174dfa2b0c7544a772042a12e52', 'width': 320}, {'height': 160, 'url': 'https://i.scdn.co/image/ab6761610000f178dfa2b0c7544a772042a12e52', 'width': 160}], 'external_urls': {'spotify': 'https://open.spotify.com/artist/4V8LLVI7PbaPR0K2TGSxFF'}}, 'Olivia Rodrigo': {'id': '1McMsnEElThX1knmY4oliG', 'images': [{'height': 640, 'url': 'https://i.scdn.co/image/ab6761610000e5ebe03a98785f3658f0b6461ec4', 'width': 640}, {'height': 320, 'url': 'https://i.scdn.co/image/ab67616100005174e03a98785f3658f0b6461ec4', 'width': 320}, {'height': 160, 'url': 'https://i.scdn.co/image/ab6761610000f178e03a98785f3658f0b6461ec4', 'width': 160}], 'external_urls': {'spotify': 'https://open.spotify.com/artist/1McMsnEElThX1knmY4oliG'}}, 'BOYNEXTDOOR': {'id': '4hnHLgMSOiqERWBL4jINP1', 'images': [{'height': 640, 'url': 'https://i.scdn.co/image/ab6761610000e5ebcfdb5b7a40a359345dc49270', 'width': 640}, {'height': 320, 'url': 'https://i.scdn.co/image/ab67616100005174cfdb5b7a40a359345dc49270', 'width': 320}, {'height': 160, 'url': 'https://i.scdn.co/image/ab6761610000f178cfdb5b7a40a359345dc49270', 'width': 160}], 'external_urls': {'spotify': 'https://open.spotify.com/artist/4hnHLgMSOiqERWBL4jINP1'}}, 'hey, nothing': {'id': '6YWqJQS9TETSb8LgZONUzI', 'images': [{'height': 640, 'url': 'https://i.scdn.co/image/ab6761610000e5eb874b9ff5ed8fa4c146054f50', 'width': 640}, {'height': 320, 'url': 'https://i.scdn.co/image/ab67616100005174874b9ff5ed8fa4c146054f50', 'width': 320}, {'height': 160, 'url': 'https://i.scdn.co/image/ab6761610000f178874b9ff5ed8fa4c146054f50', 'width': 160}], 'external_urls': {'spotify': 'https://open.spotify.com/artist/6YWqJQS9TETSb8LgZONUzI'}}, 'Wasia Project': {'id': '7poQNrOwZoUcoqihg4Xex0', 'images': [{'height': 640, 'url': 'https://i.scdn.co/image/ab6761610000e5eb02f6c87ef3a12120c10fa7c8', 'width': 640}, {'height': 320, 'url': 'https://i.scdn.co/image/ab6761610000517402f6c87ef3a12120c10fa7c8', 'width': 320}, {'height': 160, 'url': 'https://i.scdn.co/image/ab6761610000f17802f6c87ef3a12120c10fa7c8', 'width': 160}], 'external_urls': {'spotify': 'https://open.spotify.com/artist/7poQNrOwZoUcoqihg4Xex0'}}, 'The Marías': {'id': '2sSGPbdZJkaSE2AbcGOACx', 'images': [{'height': 640, 'url': 'https://i.scdn.co/image/ab6761610000e5ebaf586afa2b397f1288683a76', 'width': 640}, {'height': 320, 'url': 'https://i.scdn.co/image/ab67616100005174af586afa2b397f1288683a76', 'width': 320}, {'height': 160, 'url': 'https://i.scdn.co/image/ab6761610000f178af586afa2b397f1288683a76', 'width': 160}], 'external_urls': {'spotify': 'https://open.spotify.com/artist/2sSGPbdZJkaSE2AbcGOACx'}}, 'Wallows': {'id': '0NIPkIjTV8mB795yEIiPYL', 'images': [{'height': 640, 'url': 'https://i.scdn.co/image/ab6761610000e5eb408976d7037d509610b9b4cf', 'width': 640}, {'height': 320, 'url': 'https://i.scdn.co/image/ab67616100005174408976d7037d509610b9b4cf', 'width': 320}, {'height': 160, 'url': 'https://i.scdn.co/image/ab6761610000f178408976d7037d509610b9b4cf', 'width': 160}], 'external_urls': {'spotify': 'https://open.spotify.com/artist/0NIPkIjTV8mB795yEIiPYL'}}}, 'recommended_artists': {'KATSEYE': {'genres': ['k-pop'], 'id': '3c0gDdb9lhnHGFtP4prQpn', 'images': [{'url': 'https://i.scdn.co/image/ab6761610000e5eb031e8e2a9c4893810a02f863', 'height': 640, 'width': 640}, {'url': 'https://i.scdn.co/image/ab67616100005174031e8e2a9c4893810a02f863', 'height': 320, 'width': 320}, {'url': 'https://i.scdn.co/image/ab6761610000f178031e8e2a9c4893810a02f863', 'height': 160, 'width': 160}], 'external_urls': {'spotify': 'https://open.spotify.com/artist/3c0gDdb9lhnHGFtP4prQpn'}}, 'KickFlip': {'genres': ['k-pop'], 'id': '6F4yXjmhQBqo6HVr6K234k', 'images': [{'url': 'https://i.scdn.co/image/ab6761610000e5eb657d42d52f15961a1dbf4a8f', 'height': 640, 'width': 640}, {'url': 'https://i.scdn.co/image/ab67616100005174657d42d52f15961a1dbf4a8f', 'height': 320, 'width': 320}, {'url': 'https://i.scdn.co/image/ab6761610000f178657d42d52f15961a1dbf4a8f', 'height': 160, 'width': 160}], 'external_urls': {'spotify': 'https://open.spotify.com/artist/6F4yXjmhQBqo6HVr6K234k'}}, 'Matt Champion': {'genres': ['bedroom pop', 'rock'], 'id': '29Oq9Nv8zLgu3IvX1tIpbm', 'images': [{'url': 'https://i.scdn.co/image/ab6761610000e5eb689767f4c7e64dc01a4cb83d', 'height': 640, 'width': 640}, {'url': 'https://i.scdn.co/image/ab67616100005174689767f4c7e64dc01a4cb83d', 'height': 320, 'width': 320}, {'url': 'https://i.scdn.co/image/ab6761610000f178689767f4c7e64dc01a4cb83d', 'height': 160, 'width': 160}], 'external_urls': {'spotify': 'https://open.spotify.com/artist/29Oq9Nv8zLgu3IvX1tIpbm'}}, 'ROLE MODEL': {'genres': ['bedroom pop'], 'id': '1dy5WNgIKQU6ezkpZs4y8z', 'images': [{'url': 'https://i.scdn.co/image/ab6761610000e5ebffd538785c8288abd8235b41', 'height': 640, 'width': 640}, {'url': 'https://i.scdn.co/image/ab67616100005174ffd538785c8288abd8235b41', 'height': 320, 'width': 320}, {'url': 'https://i.scdn.co/image/ab6761610000f178ffd538785c8288abd8235b41', 'height': 160, 'width': 160}], 'external_urls': {'spotify': 'https://open.spotify.com/artist/1dy5WNgIKQU6ezkpZs4y8z'}}, 'Royel Otis': {'genres': ['indie'], 'id': '5b5bt4mZQpJMoCRbiQ7diH', 'images': [{'url': 'https://i.scdn.co/image/ab6761610000e5eb080de26afb71545d9666e2a4', 'height': 640, 'width': 640}, {'url': 'https://i.scdn.co/image/ab67616100005174080de26afb71545d9666e2a4', 'height': 320, 'width': 320}, {'url': 'https://i.scdn.co/image/ab6761610000f178080de26afb71545d9666e2a4', 'height': 160, 'width': 160}], 'external_urls': {'spotify': 'https://open.spotify.com/artist/5b5bt4mZQpJMoCRbiQ7diH'}}, 'Still Woozy': {'genres': ['bedroom pop'], 'id': '4iMO20EPodreIaEl8qW66y', 'images': [{'url': 'https://i.scdn.co/image/ab6761610000e5eb213487aac43637b03baf9db8', 'height': 640, 'width': 640}, {'url': 'https://i.scdn.co/image/ab67616100005174213487aac43637b03baf9db8', 'height': 320, 'width': 320}, {'url': 'https://i.scdn.co/image/ab6761610000f178213487aac43637b03baf9db8', 'height': 160, 'width': 160}], 'external_urls': {'spotify': 'https://open.spotify.com/artist/4iMO20EPodreIaEl8qW66y'}}}}

    # to do:
    # - make a playlist
    # - export image
    # - manually input the day breakdown
    # - use recent playlists to grab genres
    # - transitions
    # - add by day (strip the artist name of everything and store lineup as also stripped to compare)
    return render_template('getArtists.html', value = result)

# Checks to see if token is valid and gets a new token if not
def get_token():
    token_valid = False
    token_info = session.get("token_info", {})

    # Checking if the session already has a token stored
    if not (session.get('token_info', False)):
        token_valid = False
        return token_info, token_valid

    # Checking if token has expired
    now = int(time.time())
    is_token_expired = session.get('token_info').get('expires_at') - now < 60

    # Refreshing token if it has expired
    if (is_token_expired):
        sp_oauth = create_spotify_oauth()
        token_info = sp_oauth.refresh_access_token(session.get('token_info').get('refresh_token'))

    token_valid = True
    return token_info, token_valid


def create_spotify_oauth():
    return SpotifyOAuth(
            client_id=client_id,
            client_secret=client_secret,
            redirect_uri=url_for('authorize', _external=True),
            scope="user-library-read user-top-read")

# def get_token():
#     auth_string = client_id + ":" + client_secret
#     auth_bytes = auth_string.encode("utf-8")
#     auth_base64 = str(base64.b64encode(auth_bytes), "utf-8")

#     url = "https://accounts.spotify.com/api/token"
#     headers = {
#         "Authorization": "Basic " + auth_base64,
#         "Content-Type": "application/x-www-form-urlencoded"
#     }
#     data = {"grant_type": "client_credentials"}
#     result = post(url, headers=headers, data=data)
#     json_result = json.loads(result.content)
#     token = json_result["access_token"]
#     return token

# def get_auth_header(token):
#     return {"Authorization": "Bearer " + token}

# def search_for_artist(token, artist_name):
#     url = "https://api.spotify.com/v1/search"
#     headers = get_auth_header(token)
#     query = f"?q={artist_name}&type=artist"

#     query_url = url + query
#     result = get(query_url, headers=headers)
#     json_result = json.loads(result.content)["artists"]["items"]

#     if len(json_result) == 0:
#         print("No artist")

#     return json_result[0]

# def get_songs_by_artist(token, artist_id):
#     url = f"https://api.spotify.com/v1/artists/{artist_id}/top-tracks?country=US"
#     headers = get_auth_header(token)
#     result = get(url, headers=headers)
#     json_result = json.loads(result.content)["tracks"]
#     return json_result

# def get_top_artists(token):
#     url = f"https://api.spotify.com/v1/me/top/artists?time_range=long_term&limit=50"
#     headers = get_auth_header(token)
#     result = get(url, headers=headers)
#     json_result = json.loads(result.content)
#     print(json_result)
#     return json_result
    

# token = get_token()
# artists = get_top_artists(token)

# # for idx, artist in enumerate(artists):
# #     print(f"{idx + 1}. {artist['name']}")
