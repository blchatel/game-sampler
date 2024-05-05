# Music Player

A simple music player program for easy triggering of preconfigured and preloaded song samples.

## Features

- Loads songs from a configuration file.
- Plays songs at specified timecodes.
- Provides keyboard shortcuts for playing, stopping, and playing random songs.
- Minimalist user interface with buttons for each song.
- One tab per category of song with a dedicated "play random" button

## Requirements

- Python 3.10+
- [Pygame](https://pypi.org/project/pygame/)
- [ConfigParser](https://pypi.org/project/configparser/)
- [Tkinter](https://docs.python.org/3/library/tkinter.html)

Note the tkinter package is the standard Python interface and is usually available on most Unix platforms, 
including macOS, as well as on Windows systems. To test you may run `python -m tkinter`

## Project Structure

Once cloned the project should have the following structure:
```
game-sampler/
├── config/
│   └── config.ini
├── music/
│   ├── song1.mp3
│   ├── song2.mp3
│   └── ...
├── music_player.py
├── requirements.py
└── README.md
```

## Installation

1. Install Python 3.x if you haven't already.
2. (Optional) Create a dedicated environment for this project
3. Install Pygame and ConfigParser if you haven't already (`pip install pygame configparser`).
4. Place your music files in the music directory.
5. Create a configuration file (INI format) specifying the details of each song, including file paths, titles, artists, timecodes, and keyboard shortcuts.
6. Run the `music_player.py` script with the path to the configuration file and the directory containing your music files as arguments.

```
python music_player.py --config config/config.ini --music_dir music
```

## Configuration File Format

The configuration file should be in INI format with the following structure:

```
[song1]
filename = song1.mp3
title = Song Title
artist = "Artist Name"
timecode = 10
key = s
category = category_name

[song2]
filename = song2.mp3
title = "Another Song"
artist = "Another Artist"
timecode = 20
key = a
category = category_name
```

Each song is defined under a section (e.g., [song1]).

- `filename` (mandatory) specifies the name of the MP3 file inside the music directory .
- `title` (mandatory) specifies the title of the song.
- `artist` (optional) specifies the artist of the song.
- `timecode` (optional) specifies the time in seconds where the song should start playing. Default 0.
- `key` (optional) specifies the keyboard shortcut for the song.
- `category` (optional) specifies the category for the song. Each song belongs to specified category + "all"

Note: Quotes (") are optional but can help in case of title and artist with space or special char

Note: the key are case-sensitive and `<space>` + all numeric key are reserved key
