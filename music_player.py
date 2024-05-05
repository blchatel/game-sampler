import argparse
import configparser
import os
import random
import tkinter as tk
from collections import namedtuple

import pygame

class Song(namedtuple('Song', ['filepath', 'title', 'artist', 'timecode', 'key', 'category'])):

    def __repr__(self) -> str:
        """Return a string representation of the song for debugging"""
        return f'<Song {self.title} - {self.artist}>'

    @property
    def text(self) -> str:
        """Return a string representation of the song for button"""
        text = f'{self.title}\n{self.artist}'
        if self.key:
            text += f'\n({self.key})'
        return text


B_WIDTH = 130
B_HEIGHT = 90


class MusicPlayer:
    """A simple music player program for easy trigger of preconfigured and preloaded song samples"""

    def __init__(self, config_file: str, music_dir: str):
        """Construct and run the MusicPlayer"""

        songs = self._load_song_configs(config_file, music_dir)
        ui = self._setup_ui(songs)
        ui.mainloop()

    @staticmethod
    def _load_song_configs(config_file: str, music_dir: str) -> list[Song]:
        """Load the INI config file and return a list of songs"""

        if not os.path.isfile(config_file):
            raise FileNotFoundError(f'Given file at {config_file} does not exist')
        if not config_file.lower().endswith('.ini'):
            raise ValueError('Given config file must be an INI file')
        if not os.path.isdir(music_dir):
            raise NotADirectoryError(f'{music_dir} is not an existing directory')

        config = configparser.ConfigParser()
        config.read(config_file)
        songs = []
        for section in config.sections():
            filename = config.get(section, 'filename')
            filepath = os.path.join(music_dir, filename)
            if not os.path.isfile(filepath):
                raise FileNotFoundError(f'Given file at {filepath} does not exist')
            song = Song(
                filepath=filepath,
                title=config.get(section, 'title').strip('"'),
                artist=config.get(section, 'artist', fallback='Unknown Artist').strip('"'),
                timecode=config.getint(section, 'timecode', fallback=0),
                key=config.get(section, 'key', fallback='').strip('"')
            )
            if song.key in ['<Return>', '<space>']:
                raise ValueError(f'Key {song.key} is reserved')
            songs.append(song)
        return songs

    @staticmethod
    def _play(song: Song) -> None:
        """Play the music at given timecode"""
        try:
            pygame.mixer.music.load(song.filepath)
            pygame.mixer.music.play(start=song.timecode)
        except pygame.error:
            pygame.init()
            MusicPlayer._play(song)

    @staticmethod
    def _play_random(songs: list[Song]) -> None:
        i = random.randint(0, len(songs) - 1)
        MusicPlayer._play(songs[i])

    @staticmethod
    def _stop() -> None:
        """Stop the music"""
        pygame.mixer.music.stop()
        pygame.mixer.music.unload()

    @staticmethod
    def _setup_ui(songs: list[Song], n_rows: int = 5, n_cols: int = 9) -> tk.Tk:
        """Set up a minimalist UI with one button and one binding key per song"""
        root = tk.Tk()
        root.resizable(False, False)
        root.title('Game Music Player')

        for i, song in enumerate(songs):
            row = i // n_cols
            col = i % n_cols
            if row > n_rows:
                continue

            text = f'{song.title}\n{song.artist}'
            if song.key:
                text += f'\n({song.key})'
                root.bind(song.key, lambda event, s=song: MusicPlayer._play(s))
            button = tk.Button(root, text=text, command=lambda s=song: MusicPlayer._play(s))
            button.place(x=col*B_WIDTH, y=row*B_HEIGHT, width=B_WIDTH, height=B_HEIGHT)

        for i in range(len(songs), n_rows*n_cols):
            row = i // n_cols
            col = i % n_rows
            button = tk.Button(root)
            button.place(x=col*B_WIDTH, y=row*B_HEIGHT, width=B_WIDTH, height=B_HEIGHT)

        wide_width = n_cols / 2 * B_WIDTH

        root.bind("<Return>", lambda event: MusicPlayer._play_random(songs))
        random_button = tk.Button(root, text='Random Music\n<enter>', command=lambda: MusicPlayer._play_random(songs))
        random_button.place(x=0, y=n_rows * B_HEIGHT, width=wide_width, height=B_HEIGHT)

        root.bind("<space>", lambda event: MusicPlayer._stop())
        stop_button = tk.Button(root, text='Stop Music\n<space>', command=MusicPlayer._stop)
        stop_button.place(x=wide_width, y=n_rows * B_HEIGHT, width=wide_width, height=B_HEIGHT)

        total_width = n_cols * B_WIDTH
        total_height = (n_rows + 1) * B_HEIGHT
        root.geometry(f'{total_width}x{total_height}')

        root.protocol("WM_DELETE_WINDOW", lambda: root.destroy())

        return root


if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='Music Player - Play preconfigured songs with ease.')
    parser.add_argument('--config', help='Path to the configuration file (INI format)')
    parser.add_argument('--music_dir',  default='music', help='Path to the directory containing music files')
    args = parser.parse_args()

    MusicPlayer(args.config, args.music_dir)
