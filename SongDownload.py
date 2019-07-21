import pandas as pd
import SongDownloader
import logging

if __name__ == "__main__":
    df = pd.read_csv("./Data/Metadata.csv")

    logging.basicConfig(level=logging.INFO)

    count = 0
    for key in df["key"]:
        SongDownloader.download_song(key)
        count = count + 1
        if count % 10 == 0:
            logging.info("Completed {} downloads".format(count))
