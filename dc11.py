import discord
import requests
import tempfile
import json
import os
import asyncio

apikey = str(os.getenv('apikey'))
DISCORDBOTKEY = str(os.getenv('DISCORDBOTKEY'))
intents = discord.Intents.all()
client = discord.Client(intents=intents)

def get_voices():
    url = "https://api.elevenlabs.io/v1/voices"
    payload={}
    headers = {
        'xi-api-key': apikey
        }
    response = requests.request("GET", url, headers=headers, data=payload)
    voicedict = {}
    json_data = json.loads(response.text)
    for s in json_data['voices']:
        name = s['name']
        vid = s['voice_id']
        cat = s['category']
        voicedict[name] = vid,cat
    return voicedict
def get_voice_settings(voiceid):
    settings = []
    url = "https://api.elevenlabs.io/v1/voices/"+voiceid+"/settings"
    payload={}
    headers = {
        'xi-api-key': apikey
        }
    response = requests.request("GET", url, headers=headers, data=payload)
    json_data = json.loads(response.text)
    return json_data
def get_audio(voiceid,texttoplay):
    settings = get_voice_settings(voiceid)
    url = "https://api.elevenlabs.io/v1/text-to-speech/"+voiceid+"/stream"
    payload = json.dumps({
    "text": texttoplay,
    "voice_settings": {
        "stability": settings['stability'],
        "similarity_boost": settings['similarity_boost']
    }
    })
    headers = {
    'xi-api-key': apikey,
    'Accept': 'audio/mpeg'
    }
    response = requests.request("POST", url, headers=headers, data=payload)
    return response

@client.event
async def on_ready():
    print('Bot is ready.')

@client.event
async def on_message(message):

    if message.author.bot:
        return
    if message.content.startswith('~help'):
        await message.channel.send('\n when in voice chat, type ~speak [VOICETOBEUSED] [MESSAGETOBEPLAYED] to have me respond in voice chat. For a list of available voices, type ~voices')
    if message.content.startswith('~voices'):
        voicedict = get_voices()
        obmes = '\n'
        for ob in voicedict:
            obmes = obmes + ob + ' \n'
        await message.channel.send(obmes)
    if message.content.startswith('~speak'):
        voice_channel = message.author.voice.channel
        if voice_channel is not None:
            removeplay = message.content.replace('~speak ','')
            if client.voice_clients:
                await client.voice_clients[0].disconnect()
            voice_client = await voice_channel.connect()
            txtarr = removeplay.split()
            texttoplay = txtarr[1:]
            texttoplay = str(" ".join(texttoplay))
            user = txtarr[0].lower()
            voicedict = get_voices()
            try:
                voiceid = voicedict[user][0]
            except:
                await message.channel.send('No voice matching that name.')
            response = get_audio(voiceid,texttoplay)
            if response.status_code == 200:
                audio_data = response.content
                with tempfile.NamedTemporaryFile(delete=False) as tmp_file:
                    tmp_file.write(audio_data)
                    audio_file_path = tmp_file.name
                audio_source = discord.FFmpegPCMAudio(audio_file_path, options="-vn -ar 48000 -ac 2 -f s16le", executable="ffmpeg")
                voice_client.play(audio_source)
                while voice_client.is_playing():
                    await asyncio.sleep(1)
                await voice_client.disconnect()
                os.unlink(audio_file_path)
            else:
                await message.channel.send('Failed to get audio stream from API.')
        else:
            await message.channel.send('You need to be in a voice channel to use this command.')

client.run(DISCORDBOTKEY)

