import os
import re
import string
import threading
import time

from dotenv import load_dotenv
import telebot
from telebot import types
import subprocess

from tqdm import tqdm

# Load environment variables from the .env file
load_dotenv()

# Access the key
api_key = os.getenv("API_KEY")

# Initialize the bot
bot = telebot.TeleBot(api_key)


def remove_punctuation(input_string):
    # Create a translation table to remove punctuation
    translator = str.maketrans('', '', string.punctuation)

    # Use the translate method to remove punctuation
    cleaned_string = input_string.translate(translator)

    return cleaned_string.lower()


# Define the command handler
@bot.message_handler(func=lambda message: message.text.lower().startswith('play'))
def song_and_artist(message):
    # Extract song and artist from the message
    command_parts = message.text.lower().split(' ')
    if len(command_parts) < 4:
        bot.reply_to(message, "Invalid command. Please use the format: play {song} by {artist}")
        return

    # Extract song and artist from the command
    song = ' '.join(command_parts[1:command_parts.index('by')])
    artist = ' '.join(command_parts[command_parts.index('by') + 1:])

    # Create a custom keyboard with clickable buttons
    keyboard = types.InlineKeyboardMarkup(row_width=1)
    music_button = types.InlineKeyboardButton("Only Music", callback_data='only_music')
    video_button = types.InlineKeyboardButton("Music Video", callback_data='music_video')
    cancel_button = types.InlineKeyboardButton("Cancel", callback_data='cancel')

    keyboard.add(music_button, video_button, cancel_button)

    # Ask the user to choose an option
    sent_message = bot.reply_to(message, f"Choose an option for '{song}' by '{artist}':", reply_markup=keyboard)

    # Store the message ID for later deletion
    bot.register_next_step_handler(sent_message, handle_next_step)


def extract_song_and_artist(prompt):
    # Define the pattern to match "choose an option for '{song_name}' by '{artist_name}'"
    pattern = re.compile(r"choose an option for '(.*?)' by '(.*?)'")

    # Search for the pattern in the prompt
    match = pattern.search(prompt)

    if match:
        # Extract the song and artist names
        song_name = match.group(1)
        artist_name = match.group(2)

        return song_name, artist_name
    else:
        # Return None if no match is found
        return None


# Handle button clicks
@bot.callback_query_handler(func=lambda call: True)
def handle_callback(call):
    # play song by artist
    # song name could be more than one word

    prompt = call.message.text
    prompt = prompt.lower()
    print("prompt: ", prompt)

    song_name, artist_name = "", ""
    result = extract_song_and_artist(prompt)
    print(result)

    song_name = result[0]
    artist_name = result[1]

    if call.data == 'only_music':
        # Call the run() function from run.py

        # check if song_name exists in the ../music folder or not
        import os
        if os.path.exists(f"music/{remove_punctuation(song_name)}.mp3"):
            # Get the audio file path from the "music" folder
            audio_file_name = f"{remove_punctuation(song_name)}.mp3"  # Replace with the actual file name
            audio_file_path = os.path.join("music", audio_file_name)

            # Check if the file exists before sending
            if os.path.exists(audio_file_path):
                # Send the audio file
                bot.send_audio(call.message.chat.id, open(audio_file_path, 'rb'), title=f"Your Audio Track: {remove_punctuation(song_name)} by {artist_name}")
            else:
                bot.send_message(call.message.chat.id, f"Error: Audio file '{audio_file_name}' not found.")

            return

        from run import run_downloader, run_again
        run_downloader(remove_punctuation(song_name), artist_name)

        import time
        for remaining in tqdm(range(10, 0, -1)):
            time.sleep(1)

        # Call the run_again() function from run.py
        # check if file exists in music folder
        import os

        for i in range(3):
            if os.path.exists(f"music/{remove_punctuation(song_name)}.mp3"):
                # Get the audio file path from the "music" folder
                audio_file_name = f"{remove_punctuation(song_name)}.mp3"  # Replace with the actual file name
                audio_file_path = os.path.join("music", audio_file_name)

                # Check if the file exists before sending
                if os.path.exists(audio_file_path):
                    # Send the audio file
                    bot.send_audio(call.message.chat.id, open(audio_file_path, 'rb'), title=f"Your Audio Track: {remove_punctuation(song_name)} by {artist_name}")
                else:
                    bot.send_message(call.message.chat.id, f"Error: Audio file '{audio_file_name}' not found.")

                return

            else:
                run_again(remove_punctuation(song_name), artist_name)

        # Get the audio file path from the "music" folder
        audio_file_name = f"{remove_punctuation(song_name)}.mp3"  # Replace with the actual file name
        audio_file_path = os.path.join("music", audio_file_name)

        # Check if the file exists before sending
        if os.path.exists(audio_file_path):
            # Send the audio file
            bot.send_audio(call.message.chat.id, open(audio_file_path, 'rb'), title=f"Your Audio Track: {song_name} by {artist_name}")
        else:
            bot.send_message(call.message.chat.id, f"Error: Audio file '{audio_file_name}' not found.")
    elif call.data == 'music_video':
        # Handle the "Music Video" option
        bot.answer_callback_query(call.id, text="Playing music video...")
    elif call.data == 'cancel':
        # Handle the "Cancel" option
        bot.answer_callback_query(call.id, text="Command canceled.")
        bot.delete_message(call.message.chat.id, call.message.message_id)


# Function to handle the next step after the command is canceled
def handle_next_step(message):
    bot.delete_message(message.chat.id, message.message_id)


# Start the bot
bot.polling()
