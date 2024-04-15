import requests
import time
import json
from requests.exceptions import ChunkedEncodingError
import logging
from app_telegram import *

url = "https://evolution-gaming-proxy-prod.global.ssl.fastly.net/api/com/v2/diff"

resultados_anteriores = None
entrou = None
gale1 = None
gale2 = None

valor1 = None
valor2 = None
valor3 = None

duzia1 = range(1, 13)  # Primeira dúzia: 1 a 12
duzia2 = range(13, 25) # Segunda dúzia: 13 a 24
duzia3 = range(25, 37) # Terceira dúzia: 25 a 36

contador_vitoria = 0
contador_derrota = 0

chat_id = '-4119617591'

telegram_bot("Iniciou dúzia única",chat_id)
telegram_bot("Dúzia única\nGreen: {}\nRed: {}".format(contador_vitoria,contador_derrota),chat_id)

while True:
    try:
        response = requests.get(url, stream=True)

        if response.status_code == 200:
            # Iterar sobre os chunks de dados conforme eles são recebidos
            for chunk in response.iter_content(chunk_size=4000):  # Defina o tamanho do chunk conforme necessário
                
                if chunk:
                    # Converter o chunk para uma string
                    chunk_str = chunk.decode('utf-8')
                    # Dividir os dados em linhas
                    lines = chunk_str.split('\n')
                    
                    if lines[0] != ":" and lines[0] != '':

                        lines = lines[0].replace("true",'1').replace("false",'0').replace('data:','')
                        
                        try:
                            
                            json_transformed = json.loads(lines)

                            for i, json_ in enumerate(json_transformed):
                                if json_['id'] == '237':

                                    if int(json_['results'][0]) == valor1 and int(json_['results'][1]) == valor2: #verifica se ainda está na mesma rodada
                                        pass                                    
                                    else: #se nao tiver na mesma rodada
                                        valor1 = int(json_['results'][0])
                                        valor2 = int(json_['results'][1])
                                        ultimo_valor = int(json_['results'][2])

                                        if entrou:

                                            if not gale1 or not gale2:

                                                if duzia12:
                                                    if valor1 in duzia1 or valor1 in duzia2 or valor1 == 0:
                                                        telegram_bot("Green!",chat_id)
                                                        entrou=None
                                                        contador_vitoria+=1

                                                        telegram_bot("\nGreen: {}\nRed: {}".format(contador_vitoria,contador_derrota),chat_id)
                                                        duzia12=None                                                   
                                                    else:
                                                        telegram_bot("Gale 1",chat_id)
                                                        gale1=True

                                                elif duzia13:
                                                    if valor1 in duzia1 or valor1 in duzia3 or valor1 == 0:
                                                        telegram_bot("Green!",chat_id)
                                                        entrou=None
                                                        contador_vitoria+=1

                                                        telegram_bot("\nGreen: {}\nRed: {}".format(contador_vitoria,contador_derrota),chat_id)
                                                        duzia13=None
                                                    else:
                                                        telegram_bot("Gale 1",chat_id)
                                                        gale1=True

                                                elif duzia23:
                                                    if valor1 in duzia2 or valor1 in duzia3 or valor1 == 0:
                                                        telegram_bot("Green!",chat_id)
                                                        entrou=None
                                                        contador_vitoria+=1

                                                        telegram_bot("\nGreen: {}\nRed: {}".format(contador_vitoria,contador_derrota),chat_id)
                                                        duzia23=None
                                                    else:
                                                        telegram_bot("Gale 1",chat_id)
                                                        gale1=True

                                            else:
                                                
                                                if gale1:

                                                    if gale1 and duzia12:
                                                    
                                                        if valor1 in duzia1 or valor1 in duzia2 or valor1 == 0:
                                                            telegram_bot("Green!",chat_id)
                                                            entrou=None
                                                            contador_vitoria+=1

                                                            telegram_bot("\nGreen: {}\nRed: {}".format(contador_vitoria,contador_derrota),chat_id)
                                                            duzia12=None                                                   
                                                        else:
                                                            telegram_bot("Gale 2",chat_id)
                                                            gale1=None
                                                            gale2=True

                                                    elif gale1 and duzia13:

                                                        if valor1 in duzia1 or valor1 in duzia3 or valor1 == 0:
                                                            telegram_bot("Green!",chat_id)
                                                            entrou=None
                                                            contador_vitoria+=1

                                                            telegram_bot("\nGreen: {}\nRed: {}".format(contador_vitoria,contador_derrota),chat_id)
                                                            duzia13=None
                                                        else:
                                                            telegram_bot("Gale 2",chat_id)
                                                            gale1=None
                                                            gale2=True

                                                    elif gale1 and duzia23:

                                                        if valor1 in duzia2 or valor1 in duzia3 or valor1 == 0:
                                                            telegram_bot("Green!",chat_id)
                                                            entrou=None
                                                            contador_vitoria+=1

                                                            telegram_bot("\nGreen: {}\nRed: {}".format(contador_vitoria,contador_derrota),chat_id)
                                                            duzia23=None
                                                        else:
                                                            telegram_bot("Gale 2",chat_id)
                                                            gale1=None
                                                            gale2=True

                                                elif gale2:

                                                    if gale2 and duzia12:
                                                    
                                                        if valor1 in duzia1 or valor1 in duzia2 or valor1 == 0:
                                                            telegram_bot("Green!",chat_id)
                                                            entrou=None
                                                            contador_vitoria+=1

                                                            telegram_bot("\nGreen: {}\nRed: {}".format(contador_vitoria,contador_derrota),chat_id)
                                                            duzia12=None   
                                                            entrou=None                                                
                                                        else:
                                                            telegram_bot("Red",chat_id)
                                                            contador_derrota+=1
                                                            telegram_bot("\nGreen: {}\nRed: {}".format(contador_vitoria,contador_derrota),chat_id)

                                                            gale1=None
                                                            gale2=None
                                                            entrou=None

                                                    elif gale2 and duzia13:

                                                        if valor1 in duzia1 or valor1 in duzia3 or valor1 == 0:
                                                            telegram_bot("Green!",chat_id)
                                                            entrou=None
                                                            contador_vitoria+=1

                                                            telegram_bot("\nGreen: {}\nRed: {}".format(contador_vitoria,contador_derrota),chat_id)
                                                            duzia13=None
                                                            gale2=None
                                                            gale1=None
                                                            entrou=None
                                                        else:
                                                            telegram_bot("Red",chat_id)
                                                            contador_derrota+=1
                                                            telegram_bot("\nGreen: {}\nRed: {}".format(contador_vitoria,contador_derrota),chat_id)

                                                            gale1=None
                                                            gale2=None
                                                            entrou=None

                                                    elif gale2 and duzia23:

                                                        if valor1 in duzia2 or valor1 in duzia3 or valor1 == 0:
                                                            telegram_bot("Green!",chat_id)
                                                            entrou=None
                                                            contador_vitoria+=1

                                                            telegram_bot("\nGreen: {}\nRed: {}".format(contador_vitoria,contador_derrota),chat_id)
                                                            duzia23=None

                                                            gale2=None
                                                            gale1=None
                                                            entrou=None
                                                        else:
                                                            telegram_bot("Red",chat_id)
                                                            contador_derrota+=1
                                                            telegram_bot("\nGreen: {}\nRed: {}".format(contador_vitoria,contador_derrota),chat_id)

                                                            gale1=None
                                                            gale2=None
                                                            entrou=None
                                                            
                                        
                                        elif (valor1 in duzia1 and valor2 in duzia1) or \
                                            (valor1 in duzia2 and valor2 in duzia2) or \
                                            (valor1 in duzia3 and valor2 in duzia3):

                                            if valor1 in duzia1 and valor2 in duzia1:
                                                duzia_entrada = 'duzia 2 e 3'
                                                duzia23 = True
                                            elif valor1 in duzia2 and valor2 in duzia2:
                                                duzia_entrada = 'duzia 1 e 3'
                                                duzia13 = True
                                            elif valor1 in duzia3 and valor2 in duzia3:
                                                duzia_entrada = 'duzia 1 e 2'
                                                duzia12 = True
                                                
                                            telegram_bot('Entrar na {}'.format(duzia_entrada),chat_id)                                             
                                            entrou=True
                                                
                            else:
                                pass

                        except:
                            pass
        else:
            print("Erro ao acessar a API:", response.status_code)
    except ChunkedEncodingError as e:
        print(f"Erro de codificação chunked: {e}")