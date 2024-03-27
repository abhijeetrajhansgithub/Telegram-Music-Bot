import re
import urllib.request as url

from moviepy.editor import *
from tqdm import tqdm

import string


def remove_punctuation(input_string):
    # Create a translation table to remove punctuation
    translator = str.maketrans('', '', string.punctuation)

    # Use the translate method to remove punctuation
    cleaned_string = input_string.translate(translator)

    return cleaned_string.lower()


def get_video_links(song, singer):
    url_link = f"https://www.youtube.com/results?search_query={song} by {singer}"
    url_link = url_link.replace(" ", "%20")

    html = url.urlopen(url_link)

    video_id = re.findall(r"watch\?v=(\S{11})", html.read().decode())
    print(video_id)

    final_link = f"https://www.youtube.com/watch?v={video_id[0]}"
    print(final_link)

    # webbrowser.open(final_link)
    #
    # video = pytube.YouTube(final_link)
    # video_length = video.length
    # print(type(video_length))
    # print(video_length)

    return final_link

# ---------------------------------------------------------------------------------------------------------------------

import os
from pytube import YouTube


def download_(link, song_name, output_path="downloads"):
    # Create the output directory if it doesn't exist
    os.makedirs(output_path, exist_ok=True)

    yt_obj = YouTube(link)

    filters = yt_obj.streams.filter(progressive=True, file_extension='mp4')

    # Download the highest quality video
    video_stream = filters.get_highest_resolution()
    video_stream.download(output_path)

    # Move the downloaded video to the downloads folder
    original_file_path = os.path.join(output_path, video_stream.default_filename)
    new_file_path = os.path.join(output_path, f"{song_name}.mp4")

    print(f"Video downloaded and moved to: {new_file_path}")
    if os.path.isfile(new_file_path):
        print("File exists")

    return new_file_path, song_name


def convert_to_audio(path, song):
    # Load the video
    video = VideoFileClip(path)

    # Convert the video to audio
    audio = video.audio

    # Specify the output audio file path (in MP3 format)
    audio_path = f"{song}.mp3"

    # Save the audio as an MP3 file
    audio.write_audiofile(audio_path)

    # Return the path to the audio file
    return audio_path


def move():
    import os
    import shutil

    # Create the 'music' folder if it doesn't exist
    music_folder = os.path.join(os.getcwd(), 'music')
    os.makedirs(music_folder, exist_ok=True)

    # Get a list of all files in the current directory
    current_directory = os.getcwd()
    all_files = os.listdir(current_directory)

    # Filter mp3 files
    mp3_files = [file for file in all_files if file.lower().endswith('.mp3')]

    # Move each mp3 file to the 'music' folder
    for mp3_file in mp3_files:
        source_path = os.path.join(current_directory, mp3_file)
        destination_path = os.path.join(music_folder, mp3_file)
        shutil.move(source_path, destination_path)

    print("MP3 files moved to the 'music' folder.")


def run_downloader(song, singer):
    search = get_video_links(song, singer)

    def check_if_file_exists_in_downloads():
        import os
        file_path = os.path.join(os.getcwd(), 'downloads', f"{remove_punctuation(song)}.mp4")
        return os.path.exists(file_path)

    if check_if_file_exists_in_downloads():
        print("File exists in downloads folder")
        video_file_path = f"downloads/{remove_punctuation(song)}.mp4"
        audio_file_path = convert_to_audio(video_file_path, remove_punctuation(song))
        print(f"Audio file saved to: {audio_file_path}")
        move()
        return

    else:
        print("File does not exist in downloads folder")

        print("Downloading...")

        # Replace 'your_youtube_link' with the actual YouTube video URL

        # Call the function with the search link
        print("Downloading video...")
        result_search = download_(search, remove_punctuation(song))

        file_path = result_search[0]
        song = result_search[1]
        song = remove_punctuation(song)

        # Check if the video file exists before proceeding
        import time

        print("Main Process: ")

        for remaining in tqdm(range(10, 0, -1)):
            time.sleep(1)

        if os.path.isfile(file_path):
            print("File exists")
            video_file_path = file_path
            audio_file_path = convert_to_audio(video_file_path, remove_punctuation(song))

            print(f"Audio file saved to: {audio_file_path}")

            move()
        else:
            print("File does not exist")
            return


def run_again(song, singer):

    def check_if_file_exists_in_downloads():
        import os
        file_path = os.path.join(os.getcwd(), 'downloads', f"{remove_punctuation(song)}.mp4")
        return os.path.exists(file_path)

    if check_if_file_exists_in_downloads():
        print("File exists in downloads folder")
        video_file_path = f"downloads/{remove_punctuation(song)}.mp4"
        audio_file_path = convert_to_audio(video_file_path, remove_punctuation(song))
        print(f"Audio file saved to: {audio_file_path}")
        move()
        return

    else:
        print("File does not exist in downloads folder")
        search = get_video_links(song, singer)

        print("Downloading...")

        # Replace 'your_youtube_link' with the actual YouTube video URL

        # Call the function with the search link
        print("Downloading video...")
        result_search = download_(search, remove_punctuation(song))

        file_path = result_search[0]
        song = result_search[1]
        song = remove_punctuation(song)

        # Check if the video file exists before proceeding
        import time

        print("Main Process: ")

        for remaining in tqdm(range(10, 0, -1)):
            time.sleep(1)

        if os.path.isfile(file_path):
            print("File exists")
            video_file_path = file_path
            audio_file_path = convert_to_audio(video_file_path, remove_punctuation(song))

            print(f"Audio file saved to: {audio_file_path}")

            move()
        else:
            print("File does not exist")
            return