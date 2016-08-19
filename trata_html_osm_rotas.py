import json
import bs4
import ast
import pandas as pd
from os import listdir
from os.path import isfile, join


# http://www.openstreetmap.org/relation/
address = './rotas_output'
onlyfiles = [f for f in listdir(address) if isfile(join(address, f))]

data_arq = []
count = 0
for file in onlyfiles:
    with open(address+"/"+file) as json_data:
        d = json.load(json_data)
        json_data.close()
        html = d

    soup = bs4.BeautifulSoup(html, 'lxml')
    try:
        info_r = ast.literal_eval(soup.body.text.replace('false', 'False'))
        # Informacoes da busca-rota
        alter_rota = info_r['found_alternative']
        distancia_total = info_r['route_summary']['total_distance']
        tempo_total = info_r['route_summary']['total_time']
        nome_rota = info_r['route_name']
        start_point = info_r['route_summary']['start_point']
        end_point = info_r['route_summary']['end_point']

        header = ['origem', 'destino', 'start_point', 'end_point','rota_alternativa', 'nome_rota','distancia', 'tempo']
        data = [file.split("_")[2], file.split("_")[3], start_point, end_point, alter_rota, nome_rota, distancia_total, tempo_total]
        data_pd = pd.DataFrame([data], columns=header)
        data_arq.append(data_pd)
        #print(file)
    except:
        print("deu ruim: ",count, file)

    count += 1

frame = pd.DataFrame()
frame = pd.concat(data_arq)
frame.to_csv("rotas_de_para.csv", sep=";", decimal=".")