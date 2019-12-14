import SongDownloader
import logging
import soundfile as sf


if __name__ == "__main__":
    f = sf.SoundFile("./Data/52cc/song.egg")
    print(len(f) / f.samplerate)
