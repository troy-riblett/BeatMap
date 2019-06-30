import SongConvert
import os.path
import logging
import Spectrogram

if __name__ == "__main__":
    logging.basicConfig(level=logging.WARNING)
    if not os.path.exists("song.wav"):
        SongConvert.convert_song_egg_to_wav("song.egg")
        logging.debug("Converting song to wav")

    Spectrogram.plotstft("song.wav")

