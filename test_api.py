import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import os

# It's best practice to set these as environment variables
# but for a quick test, you can paste them directly.
# os.environ["SPOTIPY_CLIENT_ID"] = "YOUR_CLIENT_ID_HERE"
# os.environ["SPOTIPY_CLIENT_SECRET"] = "YOUR_CLIENT_SECRET_HERE"

# Replace with your actual credentials
client_id = "4f80bcad745e4fc29f0c7f29418e899d"
client_secret = "79d74a6dbd7148b1a894676fdee21c98"

# Set up authentication
auth_manager = SpotifyClientCredentials(client_id=client_id, client_secret=client_secret)
sp = spotipy.Spotify(auth_manager=auth_manager)

# Let's test by searching for an artist
artist_name = "Tame Impala"
results = sp.search(q=f'artist:{artist_name}', type='artist')

# Print the results to see if it worked
if results['artists']['items']:
    artist = results['artists']['items'][0]
    print(f"Successfully found artist: {artist['name']}")
    print(f"Followers: {artist['followers']['total']:,}")
    print(f"Genres: {', '.join(artist['genres'])}")
else:
    print(f"Could not find artist: {artist_name}")