import logging
import SongDownloader


def download_all_metadata():
    logging.basicConfig(level=logging.INFO)
    song_df = SongDownloader.get_all_songs_metadata()
    song_df.to_csv("Metadata.csv")


if __name__ == "__main__":
    download_all_metadata()
