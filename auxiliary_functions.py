import datetime as dt
from bs4 import BeautifulSoup
import requests,re,time

def sistema_data_ora(caricato_il):
    if caricato_il == None:
        return None
    if "Oggi" in caricato_il.text:
        index = (caricato_il.text.find(":"))
        ora = int(caricato_il.text[index - 2:index])
        minuti = int(caricato_il.text[index + 1:index + 3])
        orario = dt.time(ora, minuti)
        today = dt.date.today()
        data_con_orario = dt.datetime.combine(today, orario)
    elif "Ieri" in caricato_il.text:
        index = (caricato_il.text.find(":"))
        yesterday = dt.date.today() - dt.timedelta(days=1)
        ora = int(caricato_il.text[index - 2:index])
        minuti = int(caricato_il.text[index + 1:index + 3])
        orario = dt.time(ora, minuti)
        data_con_orario = dt.datetime.combine(yesterday, orario)
    else:
        mesi = ["gen", "feb", "mar", "apr", "mag", "giu", "lug", "ago", "set", "ott", "nov", "dic"]
        split = caricato_il.text.split(" ")
        strorario = split[3]
        index = (strorario.find(":"))
        ora = int(strorario[index - 2:index])
        minuti = int(strorario[index + 1:index + 3])
        orario = dt.time(ora, minuti)
        giorno = int(split[0])
        mese = mesi.index(split[1]) + 1
        data = dt.date(2020, mese, giorno)
        data_con_orario = dt.datetime.combine(data, orario)
    return data_con_orario

def details_grid(link_page_inside:str):
    tmp_source = requests.get(link_page_inside).text
    tmp_soup = BeautifulSoup(tmp_source, "lxml")
    tmp_detail = tmp_soup.find("p",
                               "classes_sbt-text-atom__2GBat classes_token-body__1dLNW size-normal classes_weight-book__3zPi1 jsx-3711062521 description classes_preserve-new-lines__1X-M6").text
    grid_detail = tmp_soup.find_all("span",
                                    class_="classes_sbt-text-atom__2GBat classes_token-body__1dLNW size-normal classes_weight-book__3zPi1 value jsx-3561725324")
    tipo = ["benzina", "diesel", "gpl", "metano", "ibrida", "elettrica"]
    check_version = []
    version = tmp_soup.find_all("span",
                                class_="classes_sbt-text-atom__2GBat classes_token-body__1dLNW size-normal classes_weight-book__3zPi1 label jsx-3561725324")
    for iel in range(0, 3):
        check_version.append(version[iel].text)
    marca, modello, versione, km, immatricolazione, carburante, euro = None, None, None, None, None, None, None
    i = 0
    for raw in grid_detail:
        if i == 0:
            marca = raw.text.strip().upper()
            i += 1
        elif i == 1:
            modello = raw.text.strip().lower()
            i += 1
        elif i == 2 and "Versione" in check_version:
            versione = raw.text.strip().lower()
            i += 1
        else:
            raw_text = raw.text
            if "Km" in raw_text and raw_text != "Km0":
                if raw_text.split(" ")[0] == "Km":
                    pass
                else:
                    km = int(raw_text.split(" ")[0])
            if "/" in raw_text and raw_text.split("/")[0].isdigit():
                mese = int(raw_text.split("/")[0])
                anno = int(raw_text.split("/")[1])
                if anno > 1900:
                    immatricolazione = dt.date(anno, mese, 1)
            if raw_text.strip().lower() in tipo:
                carburante = raw_text.strip().lower()
            if "Euro" in raw_text or "euro" in raw_text:
                if len(raw_text.split(" ")) != 1:
                    euro = int(raw_text.split(" ")[1])
            for word in tmp_detail.split():
                word = word.lower()
                if "incidente" == word or "incidentata" == word or "incidentato" == word:
                    return (None, None, None, None, None, None, None)
            if euro == None:
                try:
                    second_tmp = tmp_soup.find_all("p", class_= "classes_sbt-text-atom__2GBat classes_token-body__1dLNW size-normal classes_weight-book__3zPi1")
                    for row in second_tmp:
                        txt = row.text.replace(" ", "")
                        check = re.search("Euro*", txt)
                        if check != None:
                            if txt[check.span()[0]+4].isdigit():
                                euro = int(txt[check.span()[0]+4])
                except:
                    euro = None
    return (marca, modello, versione, km, immatricolazione, carburante, euro)

def excel_date(df):
    new_date_up = []
    new_imm = []
    for iel in range(len(df)):
        if df.loc[iel]["Immatricolazione"] != None:
            new_imm.append(df.loc[iel]["Immatricolazione"].strftime("%x %X"))
        else:
            new_imm.append(None)
        new_date_up.append(df.loc[iel]["Data_upload"].strftime("%x %X"))
    df["Data_upload"] = new_date_up
    df["Immatricolazione"] = new_imm
    return df


def starting_time(hour, minute):
    if dt.datetime.now().hour != hour or dt.datetime.now().minute != minute:
        today = dt.datetime.today()
        domani = today + dt.timedelta(days=1)
        ora = dt.time(hour, minute)
        until = domani.combine(domani, ora)
        diff = until - dt.datetime.today()
        secnd = diff.total_seconds()
        print("i will start at:", dt.datetime.today() + dt.timedelta(seconds=secnd))
        time.sleep(secnd)