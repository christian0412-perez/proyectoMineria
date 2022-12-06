import random
import requests
from bs4 import BeautifulSoup
from lxml import etree
from flask import Flask, jsonify, request
import json
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

app = Flask(__name__)

@app.route('/mercadolibre', methods=['GET'])
def mercadolibre():
    
    data = json.loads(request.data)
    limitebool = False
    
    if 'limite' in data:
        limitebool = True
        print(data['limite'])
        
    siguiente = 'https://listado.mercadolibre.com.mx/'+data['producto'] 
    lista_titulos = list()
    lista_urls = list()
    lista_precios = list()

    while True:
        
        r = requests.get(siguiente)    
        
        if r.status_code == 200:
            soup = BeautifulSoup(r.content, 'html.parser')
            
            # //h2[@class="ui-row-item__title ui-row-item__group__element"]
            titulos = soup.find_all('h2', attrs={"class":"ui-search-item__title shops__item-title"})
            titulos = [i.text for i in titulos]
            lista_titulos.extend(titulos)

            urls = soup.find_all('a', attrs={"class":"ui-search-item__group__element shops__items-group-details ui-search-link"})
            urls = [i.get('href') for i in urls]
            lista_urls.extend(urls)
            
            # //li[@class="ui-search-layout__item shops__layout-item"]//div[@class="ui-search-result__content-columns shops__content-columns"]//div[@class="ui-search-result__content-column ui-search-result__content-column--left shops__content-columns-left"]/div[1]/div[1]//div[@class="ui-search-price__second-line shops__price-second-line"]//span[@class="price-tag-amount"]/span[2]
            dom = etree.HTML(str(soup))
            precios = dom.xpath('//li[@class="ui-search-layout__item shops__layout-item"]//div[@class="ui-search-result__content-columns shops__content-columns"]//div[@class="ui-search-result__content-column ui-search-result__content-column--left shops__content-columns-left"]/div[1]/div[1]//div[@class="ui-search-price__second-line shops__price-second-line"]//span[@class="price-tag-amount"]/span[2]')
            precios = [i.text for i in precios]
            lista_precios.extend(precios)
            
            
            # //span[@class="andes-pagination__link"]
            ini = soup.find('span', attrs={"class":"andes-pagination__link"}).text
            ini = int(ini)

            # //li[@class="andes-pagination__page-count"]
            cantidad = soup.find('li', attrs={"class":"andes-pagination__page-count"})
            cantidad = int(cantidad.text.split(" ")[1])
            
            print(f'{ini} de {cantidad}')
            
        else:
            break
        
        if (limitebool and len(lista_titulos) >= data['limite']):
            predict(lista_precios,lista_titulos,lista_urls)
            return jsonify({"datos":{
                "titulos": lista_titulos[:data['limite']],
                "urls" : lista_urls[:data['limite']],
                "precios" : lista_precios[:data['limite']]
            }})
            
        if ini == cantidad: break
        # //div[@class="ui-search-pagination shops__pagination-content"]/ul/li[contains(@class,"--next")]/a
        siguiente = dom.xpath('//div[@class="ui-search-pagination shops__pagination-content"]/ul/li[contains(@class,"--next")]/a')[0].get('href')
    predict(lista_precios,lista_titulos,lista_urls)
    return jsonify({"datos":{
        "titulos": lista_titulos,
        "urls" : lista_urls,
        "precios" : lista_precios
    }})

def predict(lista_precios,titulos,lista_urls):
    lista_descuento = list()
    lista_x = list()

    cont = 0
    lista_precios= [int(i.replace(',',''))for i in lista_precios]
    for i in lista_precios:
    
        dias = list()
        lista_pre = list()
        
        for x in range(28):
            lista_pre.append(random.randint(i-(round(i*0.3)), i))
            dias.append(x+1)
        
        lista_pre.append(i)
        dias.append(29)

        x = np.array(dias)
        y = np.array(lista_pre)

        dia = 30
        coef = np.polyfit(x, y, 4)
        p = np.polyval(coef, dia)
        print(f"\nPara el dia {dia} la prediccion de {titulos[cont]}es de {p} | Precio actual: {i} | {lista_urls[cont]}")
        cont += 1
        
        lista_x.append(cont)
        lista_descuento.append(p)
    dict = {'dias': lista_x, 'descuento': lista_descuento} 
    df = pd.DataFrame(dict) 
    df.to_csv('test.csv')
        

    
if __name__ == '__main__':
    app.run(host="0.0.0.0")
