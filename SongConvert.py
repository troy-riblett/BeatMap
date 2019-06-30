import soundfile as sf


def convert_song_egg_to_wav(filename):
    # Converts the song.egg file to a song.wav file, returns the new file name
    data, sample_rate = sf.read(filename)
    new_file_name = filename.replace(".egg", ".wav")
    sf.write(new_file_name, data, sample_rate)
    return new_file_name
