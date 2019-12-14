import requests
import logging
import pandas as pd
import os
from io import BytesIO
import zipfile
import shutil
import glob


def get_all_songs_metadata():
    """Retrieves metadata for everysong on the beatsaver site. Does not have any checks for whether the song
    data has already been downloaded"""
    song_dict = {}
    song_columns = ["key", "level_author_name", "song_name", "song_sub_name", "bpm", "upvotes", "downvotes", "plays", "upload_date",
                    "downloads", "download_url", "overall_rating", "fun_factor", "rhythm", "flow",
                    "pattern_quality", "readability", "level_quality"]

    for col in song_columns:
        song_dict[col] = []

    last_page_num = int(requests.get("https://beatsaver.com/api/maps/latest/0").json()["lastPage"])
    logging.debug("Last page is " + str(last_page_num))

    for page in range(0, last_page_num + 1):
        logging.info("Starting page " + str(page))
        try:
            get_song_metadata_for_page(song_dict, page)
        except:
            logging.error("Failed to download page " + str(page))

    logging.debug(song_dict)

    song_df = pd.DataFrame.from_dict(song_dict)
    return song_df


def get_song_metadata_for_page(song_dict, page_num):
    """Gets the information for all of the songs on a passed in page and returns them to song_dict"""
    data = requests.get("https://beatsaver.com/api/maps/latest/{}".format(page_num)).json()

    logging.debug(data["docs"])
    for val in data["docs"]:
        # Basic counts for upvotes, downvotes, and downloads and the download URL
        _add_beat_saver_data_to_dict(song_dict, val)

        # Data from BSaber
        _get_bsaber_data(song_dict)

    logging.debug(song_dict)


def get_single_song_metadata(data_key):
    """Retrieves the metadata info for a single song"""
    ratings_data = {}
    # Basic counts for upvotes, downvotes, and downloads and the download URL
    data = requests.get("https://beatsaver.com/api/maps/detail/{}".format(data_key)).json()
    _add_beat_saver_data_to_dict(ratings_data, data)

    # Data from BSaber
    _get_bsaber_data(ratings_data, data_key)

    return ratings_data


def _add_beat_saver_data_to_dict(song_dict, resp_json):
    song_dict["key"].append(resp_json["key"])
    song_dict["level_author_name"].append(resp_json["metadata"]["levelAuthorName"])
    song_dict["song_name"].append(resp_json["metadata"]["songName"])
    song_dict["song_sub_name"].append(resp_json["metadata"]["songSubName"])
    song_dict["upvotes"].append(resp_json["stats"]["upVotes"])
    song_dict["downvotes"].append(resp_json["stats"]["downVotes"])
    song_dict["plays"].append(resp_json["stats"]["plays"])
    song_dict["upload_date"].append(resp_json["uploaded"])
    song_dict["downloads"].append(resp_json["stats"]["downloads"])
    song_dict["download_url"].append(resp_json["downloadURL"])
    song_dict["bpm"].append(resp_json["metadata"]["bpm"])


def _get_bsaber_data(song_dict):
    """Adds the relevant info for a single song to the passed in pandas row"""
    ratings_url = "https://bsaber.com/wp-json/bsaber-api/songs/{}/ratings".format(song_dict["key"][-1])
    ratings_request = requests.get(ratings_url)
    ratings_json = ratings_request.json()
    _add_bsaber_data_to_dict(song_dict, ratings_json)


def _add_bsaber_data_to_dict(song_dict, resp_json):
    """Adds the relevant info for a single song to the passed in pandas row"""
    logging.debug("Response json " + str(resp_json))
    song_dict["overall_rating"].append(resp_json["overall_rating"])
    song_dict["fun_factor"].append(resp_json["average_ratings"]["fun_factor"])
    song_dict["rhythm"].append(resp_json["average_ratings"]["rhythm"])
    song_dict["flow"].append(resp_json["average_ratings"]["flow"])
    song_dict["pattern_quality"].append(resp_json["average_ratings"]["pattern_quality"])
    song_dict["readability"].append(resp_json["average_ratings"]["readability"])
    song_dict["level_quality"].append(resp_json["average_ratings"]["level_quality"])


def create_dir(key):
    """Creates a folder for the passed in key if one does not already exist. Returns the directory name"""
    directory = "./Data/{}".format(key)
    if not os.path.exists(directory):
        logging.debug("Path for " + key + " didn't already exist. Creating")
        os.makedirs(directory)
    return directory


def download_song(key):
    """Perform the actual song download"""
    directory = create_dir(key)

    if already_downloaded(key):
        logging.warning("Songs already downloaded for key " + key)
    else:
        # Get the metadata and the song download link from the metadata
        song_zip = requests.get("https://beatsaver.com/api/download/key/{}".format(key), stream=True)
        os.chdir(directory)

        if song_zip.ok:
            # Extract to a zip file
            z = zipfile.ZipFile(BytesIO(song_zip.content))
            z.extractall()

            file_list = os.listdir(".")
            for file in file_list:
                # Clean up non-data files like cover, and random lightmap.exe
                if not file.endswith(".dat") and not file.endswith(".egg") and not file.endswith(".ogg"):
                    # There are also occasionally folders that are created. We don't need those either
                    if os.path.isfile(file):
                        os.remove(file)
                    else:
                        shutil.rmtree(file)
        else:
            logging.warning("Could not get files for key {}. Response code {}".format(key, song_zip.status_code))
            # Create a file in the folder showing that this key is invalid
            open("invalid.txt", "a").close()

        os.chdir("../..")


def already_downloaded(key):
    """Check if the song file has already been downloaded. Return true if it has"""
    lookup1 = "./Data/{}/*.egg".format(key)
    lookup2 = "./Data/{}/*.ogg".format(key)
    lookup3 = "./Data/{}/invalid.txt".format(key)
    return len(glob.glob(lookup1)) > 0 or len(glob.glob(lookup2)) > 0 or len(glob.glob(lookup3)) > 0
