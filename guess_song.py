import os
os.environ['SPOTIPY_CLIENT_ID'] = 'SPOTIPY_CLIENT_ID'
os.environ['SPOTIPY_CLIENT_SECRET'] = 'SPOTIPY_CLIENT_SECRET'
os.environ['SPOTIPY_REDIRECT_URI'] = 'SPOTIPY_REDIRECT_URI'

import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

from random import seed
from random import shuffle
import webbrowser

auth_manager = SpotifyClientCredentials()
sp = spotipy.Spotify(auth_manager=auth_manager)
#print(json.dumps(category, sort_keys=True, indent=4))
print('Welcome to the "Guess Song" game! In this game you need to listen to a 30-second song preview and guess the name of the song and/or artist/band.')
print('If you guess both right - artist and title you get 2 points. If you guess only one of them you get 1 point and 0 if you guess none.')
print('The winner is the person who gets the highest score.')
players_num = int(input('How many players will be playing? '))
players_names = []
for i in range(players_num):
    name = input('Enter the name of the player #' + str(i + 1) + ': ')
    players_names.append(name)


print("Enter the country's code: 'US' - USA, 'RU' - Russia, 'UK' - England. Or any other country:'AD', 'AR', 'AU', 'AT', 'BE', 'BO', 'BR', 'BG', 'CA', 'CL', 'CO', 'CR'")
print("'CY', 'CZ', 'DK', 'DO', 'EC', 'SV', 'EE', 'FI', 'FR', 'DE', 'GR', 'GT', 'HN', 'HK', 'HU', 'IS', 'ID', 'IE', 'IT', 'JP', 'LV', 'LI', 'LT', 'LU', 'MY', 'MT', 'MX'")
country = input("'MC', 'NL', 'NZ', 'NI', 'NO', 'PA', 'PY', 'PE', 'PH', 'PL', 'PT', 'SG', 'ES', 'SK', 'SE', 'CH', 'TW', 'TR', 'GB', 'US', 'UY' ")
category = sp.categories(country=country, limit=50)
print('Here are categories:')

n = 0
s_p = []
for i in category['categories']['items']:
    spotify_playlists = []
    n += 1
    print(n, i['name'])
    spotify_playlists.append(i['name'])
    spotify_playlists.append(i['id'])
    s_p += [spotify_playlists]

n = int(input('Enter the number of the chosen category: '))
category_playlists = sp.category_playlists(s_p[n - 1][-1], country=country, limit=50)

n = 0
c_p = []
for i in category_playlists['playlists']['items']:
    categories_playlists = []
    n += 1
    print(n, i['name'])
    categories_playlists.append(i['name'])
    categories_playlists.append(i['id'])
    c_p += [categories_playlists]

playlist_num = int(input('Enter the number of the chosen playlist: '))

results = sp.playlist_items(c_p[playlist_num - 1][-1], market=country)
tr = []
full_tracks = []
i = 0
for item in results['items']:
    if item['track']['preview_url'] != None:
        i += 1
        tr = [i, item['track']['artists'][0]['name']]
        if len(item['track']['artists']) > 1:
            for j in item['track']['artists'][1:]:
                tr.append(j['name'])
        tr.append(item['track']['name'])
        tr.append(item['track']['preview_url'])
        full_tracks += [tr]



seed(1)
shuffle(full_tracks)
scores = [0] * len(players_names)
count = 0
how_many_tracks = (len(full_tracks) // len(players_names)) - 1

for i in full_tracks[:how_many_tracks]:
    if count == len(players_names):
        count = 0
    for _ in players_names:
        input(players_names[count] + ", press any key when you're ready ")
        song_name = ', '.join(i[1:-2])
        song_title = i[-2]
        webbrowser.open(i[-1])
        n = int(input('Do you know this song? (1 - Yes, 2 - No): '))
        if n == 1:
            answer = int(input('Did you say ' + song_name + ' - ' + song_title + "? (1 - Only song's artist, 2 - Only song's title, 3 - Both): "))
            if answer == 1 or answer == 2:
                scores[count] += 1
            elif answer == 3:
                scores[count] += 2
        elif n == 2:
            print('It was ' + song_name + ' - ' + song_title)

        count += 1
        break

print(scores)