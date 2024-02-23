# Anilist Discord Bot

Anilist Discord Bot is a Discord bot that provides information about anime and manga using the Anilist API. Users can use commands to search for anime or manga by their names and receive detailed information such as start date, end date, description, banner, cover images, and more. The bot also offers additional features such as message purging, system statistics display, and system log retrieval.

## Screenshot
<p float="left">
  <img src="https://raw.githubusercontent.com/dhruvin771/AnilistDiscordBot/main/screenshot/1.png" width="400" alt="Screenshot 1" />
  <img src="https://raw.githubusercontent.com/dhruvin771/AnilistDiscordBot/main/screenshot/2.png" width="400" alt="Screenshot 2" />
</p>

## Features
- **Anime Details**: Use the /anime command followed by the name of the anime to retrieve detailed information such as start date, end date, description, banner image, cover image, and more.
- **Manga Details**: Use the /manga command followed by the name of the manga to fetch detailed information including start date, end date, description, banner image, cover image, and more.
- **Message Purging**: Utilize the /purge command to remove messages from the server.
- **System Statistics**: Get insights into the system statistics by using the /stats command.
- **System Logs**: Access system logs by executing the /logs command and download the log file directly from Discord.

## Setup Instructions
1. Clone the repository: `git clone https://github.com/dhruvin771/AnilistDiscordBot.git`
2. Install dependencies: `pip install -r requirements.txt`
3. Create a `.env` file based on the provided `.env.example` and add your Telegram Bot token and chat ID.
4. Obtain a Discord bot token from the Discord Developer Portal.
5. Find the webhook URL in the channel settings on Discord. This will be used for sending system logs.
6. Customize the bot's commands and features based on your preferences.
7. Run the bot: `python main.py`

## Usage
- **/anime [anime_name]**: Fetch detailed information about an anime, including start date, end date, description, banner image, cover image, and more.
- **/manga [manga_name]**: Retrieve detailed information about a manga, including start date, end date, description, banner image, cover image, and more.
- **/purge [number_of_messages]**: Remove a specified number of messages from the server.   
- **/stats**: Display system statistics such as CPU usage, memory usage, and more.
- **/logs**: Show system log and download the log file directly from Discord.

## Technologies Used
- Python
- Discord.py (Discord API wrapper)
- Anilist API

## Contributing
Contributions are welcome! If you'd like to contribute to the Anilist Discord Bot, please fork the repository, make your changes, and submit a pull request.

## Credits
The Anilist Discord Bot utilizes the Anilist API for fetching anime and manga information.

## License
This project is licensed under the [MIT License](https://opensource.org/licenses/MIT). Feel free to modify and distribute it according to the terms of the license.
