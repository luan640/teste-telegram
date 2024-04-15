import requests
import time
import json
from requests.exceptions import ChunkedEncodingError
import logging
from app_telegram import *

url = "https://evolution-gaming-proxy-prod.global.ssl.fastly.net/api/com/v2/diff"

resultados_anteriores = None
entrou_vizinhos = None
gale1 = None
gale2 = None

valor1 = None
valor2 = None
valor3 = None

list_vizinhos = [0,32,15,19,4,21,2,25,17,34,6,27,22,9,31,14,20,1,33,16,24,5,10,23]

contador_vitoria = 0
contador_derrota = 0

chat_id = '-1001957169294'

telegram_bot("Iniciou vizinhos conservador",chat_id)
telegram_bot("Vizinhos Conservador\nGreen: {}\nRed: {}".format(contador_vitoria,contador_derrota),chat_id)

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

                                    if int(json_['results'][0]) == valor1 and int(json_['results'][1]) == valor2 and int(json_['results'][2]) == valor3:
                                        pass                                    
                                    else:
                                        valor1 = int(json_['results'][0])
                                        valor2 = int(json_['results'][1])
                                        valor3 = int(json_['results'][2])

                                        ultimo_valor = int(json_['results'][0])

                                        if entrou_vizinhos:
                                            if ultimo_valor in list_vizinhos:
                                                telegram_bot("Ganhou vizinhos conservador",chat_id)
                                                entrou_vizinhos=None
                                                contador_vitoria+=1

                                                telegram_bot("Vizinhos Conservador\nGreen: {}\nRed: {}".format(contador_vitoria,contador_derrota),chat_id)
                                            else:

                                                if gale1:
                                                    if ultimo_valor in list_vizinhos:
                                                        telegram_bot('Ganhou vizinhos conservador')
                                                        gale1=None
                                                        entrou_vizinhos=None
                                                        contador_vitoria+=1

                                                        telegram_bot("Vizinhos Conservador\nGreen: {}\nRed: {}".format(contador_vitoria,contador_derrota),chat_id)
                                                    else:
                                                        telegram_bot('entrar gale 2 vizinhos conservador',chat_id)
                                                        gale2=True    
                                                        gale1=None
                                                
                                                elif gale2:
                                                    if ultimo_valor in list_vizinhos:
                                                        telegram_bot('Ganhou vizinhos conservador',chat_id)
                                                        gale2=None
                                                        gale1=None
                                                        entrou_vizinhos=None
                                                        contador_vitoria+=1
                                                        
                                                        telegram_bot("Vizinhos Conservador\nGreen: {}\nRed: {}".format(contador_vitoria,contador_derrota),chat_id)

                                                    else:
                                                        telegram_bot('Red vizinhos conservador',chat_id)
                                                        gale2=None
                                                        gale1=None
                                                        entrou_vizinhos=None    
                                                        contador_derrota+=1

                                                        telegram_bot("Vizinhos Conservador\nGreen: {}\nRed: {}".format(contador_vitoria,contador_derrota),chat_id)

                                                else:
                                                    telegram_bot('entrar gale 1 vizinhos conservador',chat_id)
                                                    gale1=True


                                        elif valor1 not in list_vizinhos and valor2 not in list_vizinhos and valor3 not in list_vizinhos:
                                            
                                            telegram_bot('entrar vizinhos conservador',chat_id)                                             
                                            entrou_vizinhos=True
                                                
                            else:
                                pass

                        except:
                            pass
        else:
            print("Erro ao acessar a API:", response.status_code)
    except ChunkedEncodingError as e:
        print(f"Erro de codificação chunked: {e}")