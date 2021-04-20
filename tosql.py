import json
import mysql.connector

server = 'dbstud.cunbm.utcluj.ro'
database = 'all-books-in-one-place'
username = 'all-books-in-one-place'
password = 'gRAyL3QShEFeruwv'
port = '23306'


mydb = mysql.connector.connect(host=server, user=username, password=password, port=port, database=database)

mycursor = mydb.cursor()


def databasealeph():
    file = open("data/Aleph.json","r")
    jsonfile=json.load(file)
    nume = jsonfile[1][str(2)][0]['fld']['fld_name']
    index_1=jsonfile[1][str(2)][0]['fld']['ind_1']
    index_2=jsonfile[1][str(2)][0]['fld']['ind_2']
    valore=jsonfile[1][str(2)][0]['fld']['val']
    # for i in jsonfile[1][str(2)][0]['fld']['subflds']:
    #   print(i)
    sql = "INSERT INTO carte (bibloteca_id) VALUES (1)"
    mycursor.execute(sql)
    mydb.commit()
    sql = f"INSERT INTO fields (carte_id,valore,nume) VALUES (1,'{valore}','{nume}')"
    mycursor.execute(sql)

    mydb.commit()
    print(mycursor.rowcount, "record inserted.")


    pass


def databaseLibris():
    with open("./data/libris.json", 'r+', encoding="utf-8") as file:
        json_file = json.load(file)

    for key, value in json_file.items():
        mycursor.execute(f"SELECT id FROM resource WHERE bibloteca_id=4 AND identifier='{key}'")
        exista = mycursor.fetchone()
        # varificam daca cartea exista in baza de date
        if exista is None:
            # adaugam titlul carii si biblioteca in tabelul carte
            mycursor.execute(f"INSERT INTO resource(bibloteca_id, identifier) VALUES (4, '{key}')")
            mydb.commit()

            id = mycursor.lastrowid
            for i in value:
                # adaugam fiecare field in tabelul fields
                mycursor.execute(f"""INSERT INTO field (carte_id, value, field) VALUES ({id} ,
                 "{i['fld']['val']}", "{i['fld']['fld_name']}")""")
                mydb.commit()
        else:
            for i in value:
                # actualizam fiecare field in tabelul fields
                mycursor.execute(f"""UPDATE field SET value="{i['fld']['val']}" WHERE carte_id={exista[0]} AND field="{i['fld']['fld_name']}" """)
                mydb.commit()


file = open("data/tinread.json","r")
jsonfile=json.load(file)
nume = jsonfile[1][str(2)][0]['fld']['fld_name']
index_1=jsonfile[1][str(2)][0]['fld']['ind_1']
index_2=jsonfile[1][str(2)][0]['fld']['ind_2']
valore=jsonfile[1][str(2)][0]['fld']['val']
# for i in jsonfile[1][str(2)][0]['fld']['subflds']:
#   print(i)
sql = "INSERT INTO carte (bibloteca_id) VALUES (1)"
mycursor.execute(sql)
mydb.commit()
sql = f"INSERT INTO fields (carte_id,valore,nume) VALUES (1,'{valore}','{nume}')"
mycursor.execute(sql)

mydb.commit()
print(mycursor.rowcount, "record inserted.")

jsonfile[i][str(i+1)][index]['fld']['fld_name']
