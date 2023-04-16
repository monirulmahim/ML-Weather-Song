import APIs
import subprocess
import datetime
import requests
from googleapiclient.discovery import build
import random
import csv
from importlib import import_module
from time import sleep


# Auto Install modules
def install(package):
    subprocess.check_call(["pip", "install", package], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

modules = ['requests', 'googleapiclient', 'csv']

for module in modules:
    try:
        import_module(module)
    except ImportError:
        install(module)

        
# Weather API(Weatherstack.com)
def weather():

    # APIs(Add API Keys in [APIs.py] file)
    api_key = APIs.api_key

    # Add City in [APIs.py] file
    city = APIs.city

    url = f'http://api.weatherstack.com/current?access_key={api_key}&query={city}'

    response = requests.get(url)

    data = response.json()

    weather_stats = (data['current']['weather_descriptions'][0])
    tempreture = (data['current']['temperature'])
    day_night = (data['current']['is_day'])
    return weather_stats, tempreture, day_night


# Quotes 
def qoutes():
    with open('./csv/quotes.csv', 'r') as file:
        csv_reader = csv.reader(file)
        rows = list(csv_reader)
        random_choice = random.choice(rows)
        decor = f'🌱 {random_choice[1]} - {random_choice[0]}'
        return decor

# Time ; to determine the day-night//noon-afternoon
def times():
    with open('./csv/talks.csv', 'r', encoding='utf-8') as csv_file:
        csv_read = csv.reader(csv_file)

        morningPhrase = []
        afterPhrase = []
        nightPhrase = []

        for line in csv_read:
            morningPhrase.append(line[0])
            afterPhrase.append(line[1])
            nightPhrase.append(line[2])

    current_time = int(datetime.datetime.now().strftime('%H'))

    if (current_time) >= 6 and (current_time) < 12:
        return random.choice(morningPhrase)
    
    elif (current_time) >= 12 and (current_time) <= 15:
        return "Good noon!"
    
    elif (current_time) >= 15 and (current_time) <= 19:
        return random.choice(afterPhrase)
    
    elif (current_time) >= 19 and (current_time) <= 23:
        return random.choice(nightPhrase)
    
    else:
        return random.choice(nightPhrase)
    

# ____main____ function
def main():
    

    apiYT = APIs.apiYT
    bot_token = APIs.token # bot token
    chat_id = APIs.chat_id

    wd = weather()
    time = times()
    quote = qoutes()

    if wd[1] >= 38:
        phrase = f"{quote}\n\n{time}\n\n{wd[1]}°C ☀️🔥 The sun is scorching today!\n\n"
        playlist_id = 'PLzzpWpGIiFdpov9y3D8ygkCbEejExWels' # Playlists_id

    if wd[0] == 'Sunny' and wd[1] >= 31:
        phrase = f"{quote}\n\n{time}\n\n{wd[1]}°C Weather Looks a little warm today?\n\n"
        playlist_id = 'PLMC9KNkIncKtsacKpgMb0CVq43W80FKvo' # Playlists_id

    elif wd[0] != 'sunny' and wd[1] < 28 :
        phrase = f'{quote}\n\n{time}\n\n{wd[1]}°C Average Weather Today!\n\n'
        playlist_id = 'PLgzTt0k8mXzEP-Oc7lnk5T3f4XFSqQPNr'

    elif wd[0] != 'Clear' and wd[0] != 'sunny' and wd[1] < 25 and wd[2] == 'yes':
        phrase = f"{quote}\n\n{time}\n\n{wd[1]}°C Looks like the weather can't make up its mind whether to chill or be chill.\n\n"
        playlist_id = 'PLCnyicEIGcsdzjc41-cOkHSsFUzxCZmrg'

    elif wd[1] < 28 and wd[2] =='no':
        phrase = f"{quote}\n\n{time}\n\n{wd[1]}°C It's a great night sky!\n\n"
        playlist_id = 'PLCnyicEIGcsdzjc41-cOkHSsFUzxCZmrg'

    else:
        phrase = f'{quote}\n\n{time}\n\n{wd[1]}°C Fully Avarage Weather!\n\n'
        playlist_id = 'PLBO3y7nHyBTdntbqKGSrj4MHVY6kBgErl'


    youtube = build('youtube', 'v3', developerKey=apiYT)

    playlist_items = []
    next_page_token = None
    while True:
        request = youtube.playlistItems().list(
            part='snippet',
            playlistId=playlist_id,
            maxResults=100,
            pageToken=next_page_token
        )
        response = request.execute()
        playlist_items += response['items']
        next_page_token = response.get('nextPageToken')
        if not next_page_token:
            break
    
    song_titles = [item['snippet']['title'] for item in playlist_items]
    video_ids = [item['snippet']['resourceId']['videoId'] for item in playlist_items]
    video_urls = ['https://www.youtube.com/watch?v=' + video_id for video_id in video_ids]

    while True:
        lenth_playlist = len(song_titles)
        choice = random.choice(range(1, lenth_playlist))

        # song with the NAME and LINK
        song = (f"{song_titles[choice]}:{video_urls[choice]}")

        # Random Time for check the weather on random time 
        random_time = random.choice(range(5000, 7000))

        # Main Messege whihch send to Telegram
        messege = f"{phrase} 🎵 Here's a song, which might match the weather\n{song}"
                    
        #telegram bot
        url = f'https://api.telegram.org/bot{bot_token}/sendMessage'
        
        payload = {
            'chat_id': chat_id,
            'text': messege
                }
        
        
        response = requests.post(url, json=payload)
        print("[ Program Running ]")
        sleep(random_time)


if __name__ == '__main__':
    main()
