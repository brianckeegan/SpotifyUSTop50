import os, json, datetime
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

current_timestamp = datetime.datetime.now().strftime('%Y-%m-%dT%H:%M:%S')

def update_data(filename,data,timestamp):
    """
    A function for appending a dictionary to a list of dictionaries in a JSON file.

      filename - The name of the file to create/update
      data - The dictionary to be appended to the file
    """
    if filename in os.listdir():

        with open(filename,'r',encoding='utf-8') as f:
            data_dict = json.load(f)

        data_dict.update(payload)

        with open(filename,'w',encoding='utf-8') as f:
            json.dump(data_dict,f)

    else:
        with open(filename,'w',encoding='utf-8') as f:
            json.dump(payload,f)

def main():
    manager = SpotifyClientCredentials(
        client_id = os.environ.get("SPOTIFY_CLIENT_ID","Missing"),
        client_secret = os.environ.get("SPOTIFY_CLIENT_SECRET","Missing")
    )

    sp = spotipy.Spotify(client_credentials_manager = manager)

    top50_playlist = sp.playlist_tracks('37i9dQZEVXbLRQDuF5jeBp',market='US')

    tracks = []

    for i,item in enumerate(top50_playlist['items'],start=1):
        _d = {'pos':i}
        _d['id'] = item['track']['id']
        _d['artists'] = ','.join([a['name'] for a in item['track']['artists']])
        _d['name'] = item['track']['name']
        _d['popularity'] = item['track']['popularity']
        tracks.append(_d)

    payload = {current_timestamp:tracks}

    update_data('top50.json',payload,current_timestamp)
        

if __name__ == "__main__":
    main()