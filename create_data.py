import os
import spotipy
import pandas as pd
from dotenv import load_dotenv
from spotipy.oauth2 import SpotifyOAuth

def get_audio_features_in_batches(sp_client, track_ids):
    """Fetches audio features for a list of track IDs in batches of 100."""
    features = []
    for i in range(0, len(track_ids), 100):
        batch = track_ids[i:i+100]
        features_batch = sp_client.audio_features(batch)
        # Filter out any None results if a track is unavailable
        features.extend([f for f in features_batch if f])
    return features

def main():
    # --- Step 1: Authentication ---
    print("Attempting to authenticate...")
    load_dotenv()
    
    client_id = os.getenv("SPOTIPY_CLIENT_ID")
    client_secret = os.getenv("SPOTIPY_CLIENT_SECRET")
    redirect_uri = os.getenv("SPOTIPY_REDIRECT_URI")
    
    if not all([client_id, client_secret, redirect_uri]):
        print("❌ Error: Missing Spotify credentials in .env file.")
        return

    # Fill in your Spotify username
    YOUR_USERNAME = "lm8ckfx0ywuhkcv9zpcipzon9"
    
    # Scope for reading user's library and playlists
    scope = "user-library-read playlist-read-private"
    
    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope, username=YOUR_USERNAME))
    print("✅ Authentication successful!")

    # --- Step 2: Fetch Liked Songs (Bangers) ---
    print("\nFetching your liked songs (bangers)... This might take a moment.")
    banger_track_ids = []
    offset = 0
    limit = 50

    while True:
        results = sp.current_user_saved_tracks(limit=limit, offset=offset)
        if not results['items']:
            break
        for item in results['items']:
            track = item['track']
            if track and track['id']:
                banger_track_ids.append(track['id'])
        offset += limit
        print(f"Fetched {len(banger_track_ids)} bangers so far...")
    print(f"✅ Found a total of {len(banger_track_ids)} bangers.")

    # --- Step 3: Fetch Songs from a "Skip" Playlist ---
    # Find a playlist you dislike, right-click > Share > Copy Spotify URI
    SKIP_PLAYLIST_URI = "37i9dQZF1DWWQRwui0ExPn" # Example: Classical Essentials
    
    print(f"\nFetching songs from the 'skip' playlist: {SKIP_PLAYLIST_URI}")
    skip_track_ids = []
    offset = 0
    limit = 100

    while True:
        results = sp.playlist_items(SKIP_PLAYLIST_URI, limit=limit, offset=offset)
        if not results['items']:
            break
        for item in results['items']:
            track = item['track']
            if track and track['id'] and track['id'] not in banger_track_ids:
                skip_track_ids.append(track['id'])
        offset += limit
        print(f"Fetched {len(skip_track_ids)} skips so far...")
    print(f"✅ Found a total of {len(skip_track_ids)} unique skips.")

    # --- Step 4: Get Audio Features & Create DataFrame ---
    print("\nFetching audio features for all tracks...")
    
    # Process bangers
    bangers_features = get_audio_features_in_batches(sp, banger_track_ids)
    bangers_df = pd.DataFrame(bangers_features)
    bangers_df['banger'] = 1
    
    # Process skips
    skips_features = get_audio_features_in_batches(sp, skip_track_ids)
    skips_df = pd.DataFrame(skips_features)
    skips_df['banger'] = 0
    
    print("Combining and cleaning the dataset...")
    final_df = pd.concat([bangers_df, skips_df], ignore_index=True)
    final_df = final_df.dropna(subset=['id'])
    final_df = final_df.drop_duplicates(subset=['id'])

    # --- Step 5: Save the Dataset ---
    output_file = 'spotify_data.csv'
    final_df.to_csv(output_file, index=False)
    
    print(f"\nSuccess! Your dataset is saved as '{output_file}'.")
    print(f"It contains {len(final_df)} total songs.")
    print("\nDataset preview:")
    print(final_df.head())

if __name__ == '__main__':
    main()