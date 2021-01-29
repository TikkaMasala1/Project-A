import psycopg2
import tkinter
from datetime import datetime

con = psycopg2.connect(
    host="localhost",
    database="postgres",
    user="postgres",
    password="root"
)

cur = con.cursor()


def convert(set):
    return list(set)


def tweetName():
    name = input('Naam: ')
    if name == '':
        name = 'Anoniem'
    return name


def tweetMessage():
    message = input('Bericht: ')
    if not message == '':
        return message
    elif message == '':
        while True:
            message = input('Ongeldige bericht, Probeer opnieuw: ')
            if not message == '':
                return message


# cur.execute("insert into berichten (naam, bericht, datum) values (%s, %s, %s)",
#             (tweetName(), tweetMessage(), datetime.now()))

def showModeratedMessages():
    cur.execute("select berichten.berichten_id, naam, bericht, datum from berichten "
                "LEFT JOIN moderaties ON moderaties.berichten_id = berichten.berichten_id "
                "WHERE moderaties.moderatie = 'accept'")
    rows = cur.fetchall()
    for x in rows:
        print(f"id: {x[0]} name: {x[1]} message: {x[2]} datum: {x[3]}")


def showNonModeratedMessages():
    cur.execute("select berichten.berichten_id, naam, bericht, datum from berichten "
                "WHERE NOT EXISTS (select 1 from moderaties where berichten.berichten_id = moderaties.berichten_id)"
                "ORDER BY datum ASC ")
    rows = cur.fetchall()
    for x in rows:
        print(f"id: {x[0]} name: {x[1]} message: {x[2]} datum: {x[3]}")


def showOldestNonModeratedMessage():
    cur.execute("select berichten.berichten_id, naam, bericht, datum from berichten "
                "WHERE NOT EXISTS (select 1 from moderaties where berichten.berichten_id = moderaties.berichten_id)"
                "ORDER BY datum ASC LIMIT 1 ")
    rows = cur.fetchall()
    for x in rows:
        print(f"id: {x[0]} name: {x[1]} message: {x[2]} datum: {x[3]}")


def moderateOldestMessage():
    cur.execute("select berichten.berichten_id, naam, bericht, datum from berichten "
                "WHERE NOT EXISTS (select 1 from moderaties where berichten.berichten_id = moderaties.berichten_id)"
                "ORDER BY datum ASC LIMIT 1 ")

    rows = cur.fetchall()

    for x in rows:
        print(f"id: {x[0]} name: {x[1]} message: {x[2]} datum: {x[3]}")
        messageId = {x[0]}

    convertedId = convert(messageId)[0]

    moderation = input('Accept or Reject? : ').lower()
    modName = input('Moderator:  ').capitalize()
    while True:
        if moderation == 'accept' or moderation == 'reject':
            cur.execute("insert into moderaties (moderatie, naam, datum, berichten_id) values(%s, %s, %s, %s)",
                        (moderation, modName, datetime.now(), convertedId))
            return
        else:
            moderation = input('invalid input please try again, Accept or Reject? :').lower()


moderateOldestMessage()

con.commit()
cur.close()
con.close()
