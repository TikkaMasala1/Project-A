import psycopg2

con = psycopg2.connect(
    host="localhost",
    database="postgres",
    user="postgres",
    password="root"
)

cur = con.cursor()

name = input('Naam: ')
if name == '':
    name = 'Anoniem'

message = input('Bericht: ')
if message == '':
    retry = True
    while retry:
        message = input('Ongeldige bericht: ')
        if not message == '':
            retry = False

cur.execute("insert into berichten (naam, bericht) values ( %s, %s)", (name, message))
cur.execute("select berichten_id, naam, bericht from berichten")

rows = cur.fetchall()

for x in rows:
    print(f"id: {x[0]} name: {x[1]} message: {x[2]}")

con.commit()
cur.close()
con.close()
