import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import argparse
import os
from dotenv import load_dotenv
import re
import yt_dlp

# from pathvalidate import sanitize_filename
from tqdm import tqdm


def clean_song_name(name):
    """Removes what is in (feat ... )"""

    name = re.sub(r"\s*\(feat.*$", "", name, flags=re.IGNORECASE)
    return " ".join(name.split())


def get_youtube_link(song_name, artist, verbose=False):
    search_query = f"{song_name} {artist} audio"
    ydl_opts = {
        "quiet": not verbose,
        "no_warnings": not verbose,
        "noprogress": not verbose,
        "extract_flat": True,
        "default_search": "ytsearch",
        "format": "bestaudio/best",
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        try:
            result = ydl.extract_info(f"ytsearch1:{search_query}", download=False)
            if result and "entries" in result and result["entries"]:
                return result["entries"][0]["url"]
        except Exception as e:
            print(f"Error searching YouTube: {str(e)}")
    return None


def download_audio(url, output_filename, format="mp3", verbose=False):
    ydl_opts = {
        "format": "bestaudio/best",
        "postprocessors": [
            {
                "key": "FFmpegExtractAudio",
                "preferredcodec": format,
                "preferredquality": "192",
            }
        ],
        "outtmpl": output_filename,
        "quiet": not verbose,
        "no_warnings": not verbose,
        "noprogress": not verbose,
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        try:
            ydl.download([url])
            return True
        except Exception as e:
            print(f"Error downloading: {str(e)}")
            return False


def parse_arguments():
    parser = argparse.ArgumentParser(
        description="Fetch songs from a Spotify playlist and download from YouTube"
    )
    parser.add_argument(
        "playlist_id",
        help="Spotify playlist ID or URI (e.g., '37i9dQZF1DXcBWIGoYBM5M' or 'spotify:playlist:37i9dQZF1DXcBWIGoYBM5M')",
    )
    parser.add_argument(
        "--list",
        action="store_true",
        help="Only list songs in the playlist without downloading",
    )
    parser.add_argument(
        "--download",
        action="store_true",
        help="Download all songs from the playlist",
    )
    parser.add_argument(
        "--output",
        default=".",
        help="Specify custom download directory (default: current directory)",
    )
    parser.add_argument(
        "--format",
        default="mp3",
        choices=["mp3", "m4a", "wav", "aac", "ogg"],
        help="Audio format to download (default: mp3)",
    )
    parser.add_argument(
        "--verbose",
        action="store_true",
        help="Enable verbose output",
    )
    return parser.parse_args()


def get_spotify_client():
    load_dotenv(override=True)
    client_id = os.getenv("SPOTIFY_CLIENT_ID")
    client_secret = os.getenv("SPOTIFY_CLIENT_SECRET")

    if not client_id or not client_secret:
        raise ValueError(
            "Missing Spotify credentials! Please create a .env file with your Spotify credentials:\n"
            "SPOTIFY_CLIENT_ID=your_client_id_here\n"
            "SPOTIFY_CLIENT_SECRET=your_client_secret_here\n\n"
        )

    client_credentials_manager = SpotifyClientCredentials(
        client_id=client_id, client_secret=client_secret
    )
    return spotipy.Spotify(client_credentials_manager=client_credentials_manager)


def get_playlist_tracks(sp, playlist_id):
    if "spotify:playlist:" in playlist_id:
        playlist_id = playlist_id.split("spotify:playlist:")[1]

    results = sp.playlist_tracks(playlist_id)
    if not results or "items" not in results:
        raise ValueError(
            f"Could not find playlist with ID: {playlist_id}. "
            "Please check if the playlist ID is correct and the playlist is public"
        )

    tracks = results["items"]

    # Implement pagination to get all tracks
    while results["next"]:
        results = sp.next(results)
        tracks.extend(results["items"])

    if not tracks:
        print("This playlist appears to be empty")
        return []

    return tracks


def get_track_info(track):
    """Extract and clean track information from Spotify track data."""
    if track["track"] is None:
        return None, None

    song_name = clean_song_name(track["track"]["name"])
    artists = ", ".join(artist["name"] for artist in track["track"]["artists"])
    return song_name, artists


def sanitize_filename(filename: str) -> str:
    sanitized = re.sub(r'[\\/*?:"<>|]', "", filename)
    return sanitized.strip()


def process_track(song_name, artists, args):
    """Process a single track: display info, find YouTube link, and download if requested."""
    if not song_name:
        return

    if args.verbose or args.list:
        print(f"{song_name} by {artists}")

    if args.list:
        return

    youtube_link = get_youtube_link(song_name, artists, args.verbose)
    if not youtube_link:
        if args.verbose:
            print("\tYouTube: No link found")
        return

    if args.verbose:
        print(f"\tYouTube: {youtube_link}")

    if args.download:
        if args.verbose:
            print(f"\nDownloading {song_name}...")
        output_filename = os.path.join(
            args.output, sanitize_filename(f"{song_name} - {artists}")
        )
        if download_audio(youtube_link, output_filename, args.format, args.verbose):
            if args.verbose:
                print(f"Successfully downloaded {output_filename}.{args.format}")
        else:
            if args.verbose:
                print("Download failed")


def main():
    args = parse_arguments()

    try:
        sp = get_spotify_client()
        tracks = get_playlist_tracks(sp, args.playlist_id)

        if args.verbose:
            print("\nProcessing songs from playlist:")
            for i, track in enumerate(tracks):
                song_name, artists = get_track_info(track)
                process_track(song_name, artists, args)
        else:
            tq = tqdm(tracks, desc="Downloading songs", unit="song")
            for track in tq:
                song_name, artists = get_track_info(track)
                tq.set_description(f"{song_name} by {artists}")
                process_track(song_name, artists, args)

    except spotipy.exceptions.SpotifyOauthError as e:
        raise ValueError(
            f"Invalid Spotify credentials! Full error: {str(e)}\n"
            "Please check your Client ID and Client Secret in the .env file"
        )
    except Exception as e:
        raise RuntimeError(f"Unexpected error: {str(e)}")


if __name__ == "__main__":
    main()
