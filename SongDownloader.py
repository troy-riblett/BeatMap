import requests
import logging
# Create a directory for the new data and change to it
'''directory = create_dir(data_key)
os.chdir(directory)

# Get the metadata and the song download link from the metadata

song_zip = requests.get("https://beatsaver.com{}".format(data["downloadURL"]), stream=True)

# Extract to a zip file
z = zipfile.ZipFile(BytesIO(song_zip.content))
z.extractall()
'''


def get_all_songs_metadata():
    song_dict = {}
    last_page_num = int(requests.get("https://beatsaver.com/api/maps/latest/0").json()["lastPage"])
    logging.info("Last page is " + str(last_page_num))

    for page in range(0, 3):
        get_song_metadata_for_page(song_dict, page)

    return song_dict


def get_song_metadata_for_page(song_dict, page_num):
    data = requests.get("https://beatsaver.com/api/maps/latest/{}".format(page_num)).json()

    logging.info(data["docs"])
    for val in data["docs"]:
        song_metadata = {}
        # Basic counts for upvotes, downvotes, and downloads and the download URL
        _add_beat_saver_data_to_dict(song_metadata, val)

        # Data from BSaber
        _get_bsaber_data(song_metadata, song_metadata["key"])
        song_dict[song_metadata["key"]] = song_metadata


def get_single_song_metadata(data_key):
    ratings_data = {}
    # Basic counts for upvotes, downvotes, and downloads and the download URL
    data = requests.get("https://beatsaver.com/api/maps/detail/{}".format(data_key)).json()
    _add_beat_saver_data_to_dict(ratings_data, data)

    # Data from BSaber
    _get_bsaber_data(ratings_data, data_key)

    return ratings_data


def _add_beat_saver_data_to_dict(song_metadata, resp_json):
    song_metadata["key"] = resp_json["key"]
    song_metadata["song_name"] = resp_json["metadata"]["songName"]
    song_metadata["song_sub_name"] = resp_json["metadata"]["songSubName"]
    song_metadata["upvotes"] = resp_json["stats"]["upVotes"]
    song_metadata["downvotes"] = resp_json["stats"]["downVotes"]
    song_metadata["plays"] = resp_json["stats"]["plays"]
    song_metadata["upload_date"] = resp_json["uploaded"]
    song_metadata["downloads"] = resp_json["stats"]["downloads"]
    song_metadata["download_url"] = resp_json["downloadURL"]
    song_metadata["bpm"] = resp_json["metadata"]["bpm"]


def _get_bsaber_data(song_metadata, data_key):
    # Other rating information
    ratings_url = "https://bsaber.com/wp-json/bsaber-api/songs/{}/ratings".format(data_key)
    ratings_request = requests.get(ratings_url)
    ratings_json = ratings_request.json()
    _add_bsaber_data_to_dict(song_metadata, ratings_json)


def _add_bsaber_data_to_dict(song_metadata, resp_json):
    logging.info("Response json " + str(resp_json))
    """Adds the relevant for a single song to the passed in dictionary"""
    song_metadata["overall_rating"] = resp_json["overall_rating"]
    song_metadata["fun_factor"] = resp_json["average_ratings"]["fun_factor"]
    song_metadata["rhythm"] = resp_json["average_ratings"]["rhythm"]
    song_metadata["flow"] = resp_json["average_ratings"]["flow"]
    song_metadata["pattern_quality"] = resp_json["average_ratings"]["pattern_quality"]
    song_metadata["readability"] = resp_json["average_ratings"]["readability"]
    song_metadata["level_quality"] = resp_json["average_ratings"]["level_quality"]