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

list_vizinhos = [0,32,15,19,4,21,2,25,17,34,6,27,22,9,31,14,20,1,33,16,24,5,10,23]

telegram_bot_sendtext('Iniciando')

contador_vitoria = 0
contador_derrota = 1

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
                                    # Verificar se há resultados anteriores para comparar
                                    if resultados_anteriores is not None:
                                        # Comparar resultados
                                        
                                        if json_['results'] == resultados_anteriores:
                                            pass
                                        else:
                                            
                                            if entrou_vizinhos:
                                                if int(json_['results'][0]) in list_vizinhos: # Verifica se bateu
                                                    telegram_bot_sendtext(('Vitória: {}'.format(json_['results'][0]))) # Bateu
                                                    gale2 = None
                                                    gale1 = None
                                                    entrou_vizinhos = None

                                                else: # Se não bater
                                                    if gale1: # verifica se ja está no gale 1
                                                        telegram_bot_sendtext('Derrota gale 1'.format(json_['results'][0]))
                                                        telegram_bot_sendtext('Entrar gale 2')
                                                        gale2 = True
                                                        gale1 = None

                                                    elif gale2: # verifica se ja está no gale 2
                                                        telegram_bot_sendtext('Derrota gale 2'.format(json_['results'][0]))
                                                        gale2 = None
                                                        gale1 = None
                                                        entrou_vizinhos = None
                                                    else: # Primeira derrota
                                                        gale1 = True
                                                        telegram_bot_sendtext('Derrota: {}'.format(json_['results'][0]))
                                                        telegram_bot_sendtext("Entrar no gale 1")
                                                        
                                            else:
                                                #telegram_bot_sendtext('Verificando se pode entrar em vizinhos...')
                                                #telegram_bot_sendtext('resultado atual: {}'.format(int(json_['results'][0])))
                                                #telegram_bot_sendtext('resultado anterior: {}'.format(int(resultados_anteriores[0])))
                                                
                                                if int(resultados_anteriores[0]) not in list_vizinhos and int(json_['results'][0]) not in list_vizinhos:
                                                    telegram_bot_sendtext('Entrar em vizinhos')
                                                    telegram_bot_sendtext("Resultado atual: {}\nResultado anterior: {}".format(json_['results'][0],resultados_anteriores[0]))
                                                    
                                                    entrou_vizinhos = True
                                                    
                                        resultados_anteriores = json_['results']    

                                    # Atualizar os resultados anteriores com os resultados do item atual
                                    else:
                                        resultados_anteriores = json_['results']
                            else:
                                pass

                        except:
                            pass
        else:
            print("Erro ao acessar a API:", response.status_code)
    except ChunkedEncodingError as e:
        print(f"Erro de codificação chunked: {e}")