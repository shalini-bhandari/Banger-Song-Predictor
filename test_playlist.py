import os
import spotipy
from dotenv import load_dotenv
from spotipy.oauth2 import SpotifyClientCredentials
from spotipy.exceptions import SpotifyException

def run_test():
    """
    This script uses the simplest authentication method (Client Credentials)
    to check if the Spotify API can find the public playlist.
    """
    print("--- Running Diagnostic Test ---")
    load_dotenv()
    
    client_id = os.getenv("SPOTIPY_CLIENT_ID")
    client_secret = os.getenv("SPOTIPY_CLIENT_SECRET")
    
    if not client_id or not client_secret:
        print("❌ Error: Could not find credentials in .env file.")
        return

    # Use the simple, public-data-only authentication
    auth_manager = SpotifyClientCredentials(client_id=client_id, client_secret=client_secret)
    sp_public = spotipy.Spotify(auth_manager=auth_manager)
    
    # The ID for the public "lofi beats" playlist
    playlist_id = "37i9dQZF1DWWQRwui0ExPn"
    print(f"Attempting to fetch playlist with ID: {playlist_id}")

    try:
        # Fetch the first item from the playlist
        results = sp_public.playlist_items(playlist_id, limit=1)
        
        if results['items']:
            track_name = results['items'][0]['track']['name']
            print(f"\n✅ SUCCESS! Successfully fetched the playlist.")
            print(f"The first track is: '{track_name}'")
            print("\nThis means your credentials are correct and the playlist is accessible.")
            print("The issue is likely with the user authentication (OAuth) in your main script.")
        else:
            print("❓ The request succeeded but the playlist appears to be empty.")

    except SpotifyException as e:
        print(f"\n❌ FAILED. The test script also encountered an error.")
        print(f"Status Code: {e.http_status}")
        print(f"Reason: {e.msg}")
        print("\nThis could mean a network issue or a problem with your Spotify App configuration.")

if __name__ == '__main__':
    run_test()