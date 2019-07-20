import SongDownloader
import logging

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    SongDownloader.download_song("569")
    SongDownloader.download_song("570")
