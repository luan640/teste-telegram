import time
import requests

def telegram_bot_sendtext(bot_message):
    
    bot_token = '7083063469:AAEiIc4wvs8yAfVbECFz9LJwiW1owbcD06M'
    bot_chatID = '-1001861393714'

    send_text = 'https://api.telegram.org/bot' + bot_token + '/sendMessage?chat_id=' + bot_chatID + '&parse_mode=Markdown&text=' + bot_message

    response = requests.get(send_text)

    return response.json()