from bs4 import BeautifulSoup
import requests, time
import datetime as dt
from datetime import datetime
import pandas as pd
from auxiliary_functions import *

def scraping_web_prices_day_by_day():
    print("here")
    now = datetime.now()
    df = pd.DataFrame()
    t = []
    for iel in range(1, 25):
        link1 = "https://www.subito.it/annunci-lombardia/vendita/auto/?o="
        link2 = "&ys=2013&ps=1000&pe=11000&me=20"
        link_page = link1 + str(iel) + link2
        source = requests.get(link_page).text
        soup = BeautifulSoup(source, "lxml")
        list_of_car = soup.find_all("div", class_ ="SmallCard-module_container__Qd2gC container small")
        for visible_description in list_of_car:
            title = visible_description.find("h2", class_="classes_sbt-text-atom__2GBat classes_token-h6__1ZJNe size-normal classes_weight-semibold__1RkLc ItemTitle_item-title__3xYm- AdItemBigCard_card-title__399Ml")
            for word in title.text.split(" "):
                word = word.lower()
                if word == "van":
                    title = None
            if title == None:
                continue
            data = sistema_data_ora(visible_description.find("span",
                                                             "classes_sbt-text-atom__2GBat classes_token-caption__1Ofu6 classes_size-small__3diir classes_weight-semibold__1RkLc classes_date__2lOoE classes_with-spacer__3WQbi"))
            if data != None:
                diff = pd.Timestamp.now() - data
                if diff > dt.timedelta(days=1):
                    df = pd.DataFrame(t)
                    df = df[
                        ["Data_upload", "Marca", "Modello", "Versione", "Luogo", "Provincia", "Immatricolazione", "Km",
                         "Carburante", "Classe_emissioni", "Prezzo", "Link"]]
                    df = df.sort_values("Prezzo", ascending=True)
                    print(df)
                    return df
                else:
                    link = visible_description.a["href"]
                    luogo = visible_description.find("span",
                                                     "classes_sbt-text-atom__2GBat classes_token-caption__1Ofu6 classes_size-small__3diir classes_weight-semibold__1RkLc classes_town__W-0Iq").text.strip()
                    provincia = visible_description.find("span",
                                                         "classes_sbt-text-atom__2GBat classes_token-caption__1Ofu6 classes_size-small__3diir classes_weight-semibold__1RkLc city").text.replace(
                        "(", "").replace(")", "")
                    prize = (
                    visible_description.find("p", class_="classes_price__HmHqw classes_small__38Lur").text.split(" ")[
                        0])
                    if u'\xa0' in prize:
                        prize = prize.split((u'\xa0'))[0]
                    int_prize = int(prize.split(".")[0] + prize.split(".")[1])
                    marca, modello, versione, km, immatricolazione, carburante, euro = details_grid(link)
                    check = [x == None for x in (marca, modello, versione, km, immatricolazione, carburante, euro)]
                    if False not in check:
                        continue
                    tmp = dict(Data_upload=data, Marca=marca, Modello=modello, Versione=versione, Luogo=luogo,
                               Provincia=provincia, Immatricolazione=immatricolazione, Km=km, Carburante=carburante,
                               Classe_emissioni=euro, Prezzo=int_prize, Link=link)
                    t.append(tmp)
