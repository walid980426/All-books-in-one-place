import json
import mysql.connector

server = 'dbstud.cunbm.utcluj.ro'
database = 'all-books-in-one-place'
username = 'all-books-in-one-place'
password = 'gRAyL3QShEFeruwv'
port='23306'


mydb = mysql.connector.connect(host=server, user=username, password=password, port=port,database=database)

mycursor = mydb.cursor()






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

#jsonfile[i][str(i+1)][index]['fld']['fld_name']
