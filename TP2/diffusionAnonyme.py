import datetime
import sqlite3
import datetime
import time
import random

from ValueThread import ValueThread

db = 'message.db'


def posterMessageAnonyme(msg, timestamp=datetime.datetime.now().timestamp()):
    # nombre de secondes depuis l'heure Unix
    try:
        conn = sqlite3.connect(db)
        cursor = conn.cursor()
        sql_query = "INSERT INTO MESSAGE (message, timestamp) VALUES (?, ?)"
        data = [msg, timestamp]
        cursor.execute(sql_query, data)
        conn.commit()
        cursor.close()
    except sqlite3.Error as error:
        print("Failed to a new message into the sqlite table MESSAGE", error)
    finally:
        if conn:
            conn.close()


def recupererMessagesAnonymes(debut, fin):
    messages = []
    try:
        conn = sqlite3.connect(db)
        cursor = conn.cursor()
        sql_query = "SELECT message, timestamp from MESSAGE WHERE timestamp >= ? and timestamp <= ? ORDER BY timestamp ASC"
        data = [debut, fin]
        cursor.execute(sql_query, data)
        conn.commit()
        rows = cursor.fetchall()
        messages = rows
        cursor.close()
    except sqlite3.Error as error:
        print("Failed to select message between two timestamp of sqlite table MESSAGE", error)
    finally:
        if conn:
            conn.close()
            # print("The sqlite connection is closed")
    return messages


def genererMessageSecret(interlocuteur1, interlocuteur2, delta):
    vue_partielle = []
    end_time = datetime.datetime.now() + delta
    while datetime.datetime.now() < end_time:
        now_timestamp = datetime.datetime.now().timestamp()
        msg = random.choice([interlocuteur1, interlocuteur2])
        vue_partielle.append((msg == interlocuteur1, now_timestamp))
        posterMessageAnonyme(msg, now_timestamp)
        time.sleep(random.uniform(0.001, 0.01))
    return vue_partielle


def genererSecret(interlocuteur1, interlocuteur2, delta):
    thread_interlocuteur_1 = ValueThread(target=genererMessageSecret, args=(interlocuteur1, interlocuteur2, delta))
    thread_interlocuteur_2 = ValueThread(target=genererMessageSecret, args=(interlocuteur2, interlocuteur1, delta))
    thread_interlocuteur_1.start()
    thread_interlocuteur_2.start()
    vue_1 = thread_interlocuteur_1.join()
    vue_2 = thread_interlocuteur_2.join()
    return vue_1, vue_2


def extraireSecret(interlocuteur1, interlocuteur2, vue, messages_anonymes):
    index = 0
    len_vue = len(vue)
    res = 0b0
    for msg, time_msg in messages_anonymes:
        if msg == interlocuteur1:
            if index < len_vue and vue[index][0] and time_msg == vue[index][1]:
                # Real
                res = (res << 1) + 0b0
                index = index + 1
            else:
                # Fake
                res = (res << 1) + 0b1
        elif msg == interlocuteur2:
            if index < len_vue and not(vue[index][0]) and time_msg == vue[index][1]:
                # Fake
                res = (res << 1) + 0b1
                index = index + 1
            else:
                # Real
                res = (res << 1) + 0b0
    return res


def test_canal():
    interlocuteur1 = "Alice"
    interlocuteur2 = "Bob"

    debut_stamp = datetime.datetime.now().timestamp()
    delta = datetime.timedelta(days=0, seconds=2, microseconds=0)
    vue_1, vue_2 = genererSecret(interlocuteur1, interlocuteur2, delta)
    fin_stamp = datetime.datetime.now().timestamp()
    messages_anonymes = recupererMessagesAnonymes(debut_stamp, fin_stamp)
    secret1 = extraireSecret(interlocuteur1, interlocuteur2, vue_1, messages_anonymes)
    secret2 = extraireSecret(interlocuteur2, interlocuteur1, vue_2, messages_anonymes)

    print("Secret1 == Secret2 : " + str(secret1 == secret2))


if __name__ == '__main__':
    test_canal()
