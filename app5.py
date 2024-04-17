import requests
import time
import json
from requests.exceptions import ChunkedEncodingError
import logging
from app_telegram import *
import csv
from datetime import datetime
import pandas as pd

def contagem_red_green():
    # Carregar o arquivo CSV para um DataFrame do pandas
    df = pd.read_csv("registros.csv")

    # Contar as entradas de cada tipo
    contagem_por_tipo = df['tipo'].value_counts()
    lucro = df['valor_liquido'].sum()
    inicio = 300
    lucro_liquido = inicio + lucro

    return "Green: {}\nRed: {}\nLucro líq.: R$ {}".format((contagem_por_tipo.get('Green', 0)+contagem_por_tipo.get('Green no 0', 0)),contagem_por_tipo.get('Red', 0),lucro_liquido)

url = "https://evolution-gaming-proxy-prod.global.ssl.fastly.net/api/com/v2/diff"

resultados_anteriores = None
entrou_vizinhos = None
gale1 = None
gale2 = None
gale3=None

redou=None

contar_rodadas=0

entrada='Sem gale'

list_vizinhos = [0,32,15,19,4,21,2,25,17,34,6,27,22,9,31,14,20,1,33,16,24,5,10,23]

contador_vitoria = 0
contador_derrota = 0

chat_id = '-1001861393714'

def salvar_registro_csv(arquivo, registro):
    with open(arquivo, 'a', newline='') as csvfile:
        csvfile.write(','.join(registro) + '\n')    

def tem_duplicatas(lista):
    return len(lista) != len(set(lista))

valor_liquido=None

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
                                        
                                        if json_['results'] == resultados_anteriores: # se estiver na mesma rodada
                                            pass
                                            
                                        else: # se tiver em outra rodada

                                            lista_resultados = json_['results']

                                            if '0' in lista_resultados:
                                                lista_resultados = json_['results'][:9]
                                            else:
                                                lista_resultados = json_['results'][:8]
                                            
                                            if entrou_vizinhos:

                                                if json_['results'][0] in lista_resultados_entrada or json_['results'][0] == '0':
                                                    
                                                    if json_['results'][0] == '0':
                                                        telegram_bot('Green no 0', chat_id)
                                                        resultado = 'Green no 0'

                                                        registro = [datetime.now().strftime("%Y-%m-%d %H:%M:%S"),resultado,entrada,str(valor_liquido)]  # Data e hora atual e uma contagem de exemplo
                                                        arquivo_csv = "registros.csv"
                                                        salvar_registro_csv(arquivo_csv, registro)

                                                        gale3=None
                                                        gale2=None
                                                        gale1=None
                                                        entrou_vizinhos=None
                                                        
                                                        telegram_bot(contagem_red_green(),chat_id)
                                                    
                                                    else:
                                                    
                                                        telegram_bot('Green',chat_id)

                                                        resultado = 'Green'

                                                        registro = [datetime.now().strftime("%Y-%m-%d %H:%M:%S"),resultado,entrada,str(valor_liquido)]  # Data e hora atual e uma contagem de exemplo
                                                        arquivo_csv = "registros.csv"
                                                        salvar_registro_csv(arquivo_csv, registro)

                                                        gale3=None
                                                        gale2=None
                                                        gale1=None
                                                        entrou_vizinhos=None

                                                        telegram_bot(contagem_red_green(),chat_id)
                                                
                                                elif gale1:
                                                    telegram_bot('Gale 2 nos numeros {}'.format(lista_resultados_entrada),chat_id)
                                                    gale2=True
                                                    gale1=None

                                                    entrada = 'Gale 2'
                                                    valor_liquido=54

                                                elif gale2:
                                                    telegram_bot('Gale 3 nos numeros {}'.format(lista_resultados_entrada),chat_id)
                                                    gale3=True
                                                    gale2=None
                                                    gale1=None

                                                    entrada = 'Gale 3'
                                                    valor_liquido=54
                                                
                                                elif gale3:
                                                    redou=True
                                                    telegram_bot('Red',chat_id)
                                                    gale3=None
                                                    gale2=None
                                                    gale1=None
                                                    entrou_vizinhos=None

                                                    resultado = 'Red'
                                                    valor_liquido = -90

                                                    registro = [datetime.now().strftime("%Y-%m-%d %H:%M:%S"),resultado,entrada,str(valor_liquido)]  # Data e hora atual e uma contagem de exemplo
                                                    arquivo_csv = "registros.csv"
                                                    salvar_registro_csv(arquivo_csv, registro)

                                                    entrada='Sem gale'

                                                    telegram_bot(contagem_red_green(),chat_id)
                                                
                                                else:
                                                    gale1=True
                                                    telegram_bot('Gale 1 nos numeros {}'.format(lista_resultados_entrada),chat_id)
                                                    entrada = 'Gale 1'
                                                    valor_liquido=45

                                            elif redou:
                                                contar_rodadas+=1 
                                                print(contar_rodadas)
                                                if contar_rodadas == 9:
                                                    contar_rodadas = 0
                                                    redou=None

                                            elif tem_duplicatas(lista_resultados) == False:
                                                lista_resultados_entrada = lista_resultados
                                                telegram_bot('Entrar nos números {}'.format(lista_resultados),chat_id)
                                                entrou_vizinhos=True
                                                valor_liquido=27

                                            else:
                                                redou=True
                                                
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
    