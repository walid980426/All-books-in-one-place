import json
from random import random
import mysql.connector
from time import sleep

server = 'dbstud.cunbm.utcluj.ro'
database = 'all-books-in-one-place'
username = 'all-books-in-one-place'
password = 'gRAyL3QShEFeruwv'
port = '23306'

mydb = mysql.connector.connect(host=server, user=username, password=password, port=port, database=database)

mycursor = mydb.cursor()



def databaseLibris():
    with open("./data/libris.json", 'r+', encoding="utf-8") as file:
        json_file = json.load(file)

    for key, value in json_file.items():
        mycursor.execute("""SELECT id FROM resource WHERE id_library=4 AND identifier = %s """, (key, ))
        exista = mycursor.fetchone()
        # varificam daca cartea exista in baza de date
        if exista is None:
            # adaugam titlul carii si biblioteca in tabelul carte
            mycursor.execute("""INSERT INTO resource(id_library, identifier) VALUES (4, %s)""", (key, ))
            mydb.commit()

            mycursor.execute("""SELECT id FROM resource WHERE id_library=4 AND identifier = %s """, (key, ))
            id = mycursor.fetchone()
            for i in value:
                # adaugam fiecare field in tabelul fields
                mycursor.execute("""INSERT INTO field (id_resource, value, field) VALUES (%s, %s, %s)""",
                                 (id[0], i['fld']['val'], i['fld']['fld_name']))
                mydb.commit()
        else:
            for i in value:
                # actualizam fiecare field in tabelul fields
                mycursor.execute("""UPDATE field SET value = %s WHERE id_resource = %s AND field = %s""",
                                 (i['fld']['val'], exista[0], i['fld']['fld_name']))
                mydb.commit()


def databasetinread(id:str):
    file = open("data/tinread.json", "r")
    jsonfile = json.load(file)
    for i in range(len(jsonfile)):
        identif = jsonfile[i]['1'][1]['fld']['val']

        mycursor.execute(f"INSERT INTO  resource (id_library,identifier) VALUES (1,{identif})")
        mydb.commit()
        mycursor.execute(f"SELECT id FROM resource WHERE id_library=1 AND identifier='{identif}'")
        id_resource = mycursor.fetchall()
        id_resource=id_resource[0][0]
        for j in range(len(jsonfile[i])):
            nume = jsonfile[i]['1'][j]['fld']['fld_name']
            index_1 = jsonfile[i]['1'][j]['fld']['ind_1']
            if (index_1 == ""):
                index_1 = -1

            index_2 = jsonfile[i]['1'][j]['fld']['ind_2']
            if (index_2 == ""):
                index_2 = -1
            valore = jsonfile[i]['1'][j]['fld']['val']
            if (valore == ""):
                valore = "#"
            mycursor.execute(
                f"INSERT INTO field (field.id_resource,field.value ,field.index_1,field.index_2,field.field) VALUES ({id_resource},'{valore}','{index_1}','{index_2}','{nume}')")
            mydb.commit()
            mycursor.execute(f"SELECT id FROM field WHERE field.id_resource= '{id_resource}' and field.value ='{valore}' and field.field='{nume}'and field.index_1 ='{index_1}'and field.index_2 ='{index_2}'")
            id_field = mycursor.fetchall()
            if(id_field):
                id_field=id_field[0][0]
                for k in range(len(jsonfile[i]['1'][j]['fld']['subflds'])):
                    nume = jsonfile[i]['1'][j]['fld']['subflds'][k]['subfld']['name']
                    val = jsonfile[i]['1'][j]['fld']['subflds'][k]['subfld']['val']
                    mycursor.execute(
                        f"INSERT INTO subfield (id_field,'name','value') VALUES ('{id_field}','{nume}','{val}'")
                    mydb.commit()



def databaseelefant(id: str, dict: dict):
    sleep(random() * 5)
    mycursor.execute(f"INSERT INTO  resource (id_library,identifier) VALUES (3,{id})")
    mydb.commit()
    mycursor.execute(f"SELECT id FROM resource WHERE id_library = 3 AND identifier='{id}'")
    id_resource = mycursor.fetchall()
    id_resource = id_resource[0][0]
    for j in range(len(dict['1'])):
        nume = dict['1'][j]['fld']['fld_name']
        valore = dict['1'][j]['fld']['val']
        comment = f"INSERT INTO field (field.id_resource,field.value ,field.field) VALUES ({id_resource},'{valore}','{nume}')"
        mycursor.execute(comment)
        mydb.commit()

    # jsonfile[i][str(i+1)][index]['fld']['fld_name']

