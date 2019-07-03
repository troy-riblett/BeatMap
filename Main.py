import SongConvert
import os.path
import logging
import Spectrogram
import SongDownloader

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    song_dict = SongDownloader.get_all_songs_metadata()
    print(song_dict)

