import time
import requests

def telegram_bot(bot_message, chat_id):
    
    bot_token = '7083063469:AAEiIc4wvs8yAfVbECFz9LJwiW1owbcD06M'

    send_text = 'https://api.telegram.org/bot' + bot_token + '/sendMessage?chat_id=' + chat_id + '&parse_mode=Markdown&text=' + bot_message

    response = requests.get(send_text)

    return response.json()