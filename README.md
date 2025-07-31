# Spotify Playlist Downloader

A Python tool that fetches songs from Spotify playlists and downloads them as audio files from YouTube.

## Requirements

- Python 3.7 or higher
- FFmpeg (for audio conversion)
- Spotify Developer Account (for API credentials)

## Installation & Setup

### Windows

1. **Create and activate virtual environment:**
```cmd
python -m venv venv
venv\Scripts\activate
```

2. **Install dependencies:**
```cmd
pip install -r requirements.txt
```

3. **Install FFmpeg:**
   - Download from [https://ffmpeg.org/download.html](https://ffmpeg.org/download.html)
   - Add to your PATH environment variable

### Linux

1. **Create and activate virtual environment:**
```bash
python3 -m venv venv
source venv/bin/activate
```

2. **Install dependencies:**
```bash
pip install -r requirements.txt
```

3. **Install FFmpeg:**
```bash
# Ubuntu/Debian
sudo apt update && sudo apt install ffmpeg

# CentOS/RHEL
sudo yum install ffmpeg

# Arch Linux
sudo pacman -S ffmpeg
```

## Spotify API Setup

1. Go to [Spotify Developer Dashboard](https://developer.spotify.com/dashboard)
2. Create a new app
3. Copy your Client ID and Client Secret
4. Create a `.env` file in the project directory:

```env
SPOTIFY_CLIENT_ID=your_client_id_here
SPOTIFY_CLIENT_SECRET=your_client_secret_here
```

## Features

- **List Playlist Songs**: View all songs in a Spotify playlist without downloading
- **Download Audio**: Download songs as high-quality audio files from YouTube
- **Multiple Formats**: Support for MP3, M4A, WAV, AAC, and OGG formats
- **Custom Output Directory**: Specify where to save downloaded files
- **Progress Tracking**: Visual progress bar during downloads
- **Verbose Mode**: Detailed output for debugging
- **Smart Search**: Automatically searches YouTube for the best audio match
- **Clean Filenames**: Removes problematic characters and cleans song names

## Usage

### Basic Commands

**List songs in a playlist:**
```bash
python main.py PLAYLIST_ID --list
```

**Download all songs from a playlist:**
```bash
python main.py PLAYLIST_ID --download
```

**Download with custom format and output directory:**
```bash
python main.py PLAYLIST_ID --download --format m4a --output ./music
```

**Enable verbose output:**
```bash
python main.py PLAYLIST_ID --download --verbose
```

### Example Commands

```bash
# List songs from a popular playlist
python main.py 37i9dQZF1DXcBWIGoYBM5M --list

# Download playlist as MP3 files
python main.py 37i9dQZF1DXcBWIGoYBM5M --download

# Download as high-quality M4A files to a specific folder
python main.py 37i9dQZF1DXcBWIGoYBM5M --download --format m4a --output ./downloads

# Download with full URI format and verbose output
python main.py spotify:playlist:37i9dQZF1DXcBWIGoYBM5M --download --verbose

# Download as WAV files (highest quality)
python main.py 37i9dQZF1DXcBWIGoYBM5M --download --format wav --output ./music/wav
```

## Command Line Arguments

| Argument | Description | Example |
|----------|-------------|---------|
| `playlist_id` | Spotify playlist ID or URI (required) | `37i9dQZF1DXcBWIGoYBM5M` |
| `--list` | Only list songs without downloading | `--list` |
| `--download` | Download all songs from playlist | `--download` |
| `--output` | Custom download directory (default: current) | `--output ./music` |
| `--format` | Audio format (mp3, m4a, wav, aac, ogg) | `--format m4a` |
| `--verbose` | Enable detailed output | `--verbose` |

## Finding Playlist IDs

**From Spotify Web/Desktop:**
1. Right-click on any playlist
2. Select "Share" → "Copy link to playlist"
3. Extract the ID from the URL: `https://open.spotify.com/playlist/PLAYLIST_ID`

**From Spotify Mobile:**
1. Tap the three dots on a playlist
2. Tap "Share" → "Copy link"
3. Extract the ID from the copied URL

## Troubleshooting

**"Missing Spotify credentials" error:**
- Ensure your `.env` file exists and contains valid credentials
- Check that there are no extra spaces in your `.env` file

**"Could not find playlist" error:**
- Verify the playlist ID is correct
- Ensure the playlist is public (private playlists require additional permissions)

**FFmpeg errors:**
- Make sure FFmpeg is properly installed and in your system PATH
- Try reinstalling FFmpeg

**Download failures:**
- Some songs may not be available on YouTube
- Try running with `--verbose` to see detailed error messages

## Notes

- The tool searches YouTube for audio matches automatically
- Downloaded files are named as "Song Name - Artist.format"
- Only public Spotify playlists are supported by default
- Audio quality is set to 192 kbps for MP3 files
