import datetime
import sqlite3
import datetime
import time
import random

from ValueThread import ValueThread

db = 'message.db'


def posterMessageAnonyme(msg, timestamp=datetime.datetime.now().timestamp()):
    """
    Poster un message anonyme

    Keyword arguments:
    msg -- chaine de caractères correspondant au message
    timestamp -- nombre de secondes depuis l'heure Unix (default timestamp de l'heure actuelle)
    """
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
    """
    Lire une série de messages postés de manière anonyme

    Keyword arguments:
    debut -- timestamp début de période des messages
    fin -- timestamp fin de période des messages
    """

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
    """
    Génération des messages (aléatoire entre interlocteur1 et interlocteur2) pendant un temps delta
    et renvoie la vue partielle correspondante.

    Keyword arguments:
    interlocuteur1 -- Message qui va identifier l'interlocteur1
    interlocuteur2 -- Message qui va identifier l'interlocteur2
    delta -- timedelta utilisé pour pour générer des messages pendant tout ce temps
    """
    vue_partielle = []
    end_time = datetime.datetime.now() + delta
    while datetime.datetime.now() < end_time:
        now_timestamp = datetime.datetime.now().timestamp()
        msg = random.choice([interlocuteur1, interlocuteur2])
        vue_partielle.append((msg == interlocuteur1, now_timestamp))
        posterMessageAnonyme(msg, now_timestamp)
        time.sleep(random.uniform(0.001, 0.01))  # le thread dédié dort pendant un temps aléatoire entre 1ms et 10ms
    return vue_partielle


def genererSecret(interlocuteur1, interlocuteur2, delta):
    """
    Simuler protocole de génération de secret entre deux interlocuteurs.
        Pour cela, deux threads sont créés, il s'agit de threads customs (voir classe ValueThread) 
        qui retournent des valeurs lorsqu'ils sont terminés.
        Chaque Thread va générer des messages pendant un temps delta comme étant respectivement
        interlocuteur1 puis interlocuteur2 et renvoyer la vue de l'interlocuteur.

    Keyword arguments:
    interlocuteur1 -- Message qui va identifier l'interlocteur1
    interlocuteur2 -- Message qui va identifier l'interlocteur2
    delta -- timedelta utilisé pour pour générer des messages pendant tout ce temps
    """

    thread_interlocuteur_1 = ValueThread(target=genererMessageSecret, args=(interlocuteur1, interlocuteur2, delta))
    thread_interlocuteur_2 = ValueThread(target=genererMessageSecret, args=(interlocuteur2, interlocuteur1, delta))
    thread_interlocuteur_1.start()
    thread_interlocuteur_2.start()
    vue_1 = thread_interlocuteur_1.join()
    vue_2 = thread_interlocuteur_2.join()
    return vue_1, vue_2


def extraireSecret(interlocuteur1, interlocuteur2, vue, messages_anonymes):
    """
    Extraction d'un secret à partir d'un ensemble de messages_anonymes, du nom des deux interlocuteurs et d'une des deux vues.

    Keyword arguments:
    interlocuteur1 -- Message qui va identifier l'interlocteur1
    interlocuteur2 -- Message qui va identifier l'interlocteur2
    vue -- vue partielle qui est utilisée pour savoir si les messages anonymes sont ceux postés par interlocteur1 ou non
    messages_anonymes -- liste des messages postés avec leur timestamp associé
    """
    index = 0
    len_vue = len(vue)
    res = 0b0
    for msg, time_msg in messages_anonymes:
        if msg == interlocuteur1:
            # Si le contenu du message est interlocuteur1, on regarde dans la vue s'il s'agit bien d'un message 
            #   posté par interlocteur1 on ajoute un bit = 0 à notre résultat
            # Sinon, il s'agit d'un faux message posté par interlocteur2, on ajoute un bit = 1 à notre résultat
            if index < len_vue and vue[index][0] and time_msg == vue[index][1]:
                # Real --> Confirmation de la vue qu'il s'agit d'un VRAI message ET les timestamps correspondent
                res = (res << 1) + 0b0
                index = index + 1
            else:
                # Fake
                res = (res << 1) + 0b1
        elif msg == interlocuteur2:
            # Inversement à la condition précédente, s'il s'agit de l'interlocuteur2, on regarde dans la vue si c'est un faux,
            # sinon, il s'agit d'un vrai car pour ce TP, on suppose que l'adversaire est passif et ne triche pas dans les messages
            if index < len_vue and not(vue[index][0]) and time_msg == vue[index][1]:
                # Fake --> Confirmation de la vue qu'il s'agit d'un FAUX message ET les timestamps correspondent
                res = (res << 1) + 0b1
                index = index + 1
            else:
                # Real
                res = (res << 1) + 0b0
    return res


def test_canal():
    """
    Test du canal de diffusion anonyme et de la génération d'un secret
    """
    # Nom des interlocuteurs
    interlocuteur1 = "Alice"
    interlocuteur2 = "Bob"

    # debut_stamp et fin_stamp utilisés pour récupérer les messages anonymes à la fin de l'échange
    debut_stamp = datetime.datetime.now().timestamp()
    delta = datetime.timedelta(days=0, seconds=5, microseconds=0) # Durée de l'échange
    vue_1, vue_2 = genererSecret(interlocuteur1, interlocuteur2, delta)
    fin_stamp = datetime.datetime.now().timestamp()
    messages_anonymes = recupererMessagesAnonymes(debut_stamp, fin_stamp)

    # Extraction des secrets selon la vue de l'interlocteur1 et de l'interlocuteur2
    secret1 = extraireSecret(interlocuteur1, interlocuteur2, vue_1, messages_anonymes)
    secret2 = extraireSecret(interlocuteur2, interlocuteur1, vue_2, messages_anonymes)

    # Affichage pour voir si les secrets correspondent
    print("Secret1 == Secret2 : " + str(secret1 == secret2))


if __name__ == '__main__':
    test_canal()
