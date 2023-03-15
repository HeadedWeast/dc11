## dc11
This is a discord bot I built to interface with elevenlabs.io.

## Setup
I personally run this on a docker container. I included a Dockerfile you can update with the necessary API keys to access your Discord Bot and Elevenlabs.io.

When running your docker container, you will need to set your enviroment variables like this:
```
docker run -e apikey=INSERT-ELEVENLABS-API-KEY -e DISCORDBOTKEY=INSERT-DISCORD-BOT-KEY NAME-OF-INSTANCE
```

If you are running outside of a docker container, you will need to install the following dependencies:
```
pip install discord requests PyNaCl json os asyncio
```
You will also need to set your environment variables with your API keys. Doing so is dependent upon your system environment, but these are what you will need to set:
```
apikey = "INSERT API KEY FOR ELEVENLABS.IO"
DISCORDBOTKEY = "INSERT DISCORD BOT KEY"
```
## Usage
- `~speak [NAME OF VOICE] [TEXT TO PLAY]`: This will play back audio from a specified voice.
- `~voices`: This will display the voices you have available.
