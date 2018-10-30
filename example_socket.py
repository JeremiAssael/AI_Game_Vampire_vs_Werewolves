# -*- coding: UTF-8 -*-

import argparse
import socket
import struct
import time
import random

HOST = "localhost"
PORT = "5555" 

parser = argparse.ArgumentParser()
parser.add_argument("host")
parser.add_argument("port")

#args = parser.parse_args()


def receive_data(sock, size, fmt):
    data = bytes()
    while len(data) < size:
        data += sock.recv(size - len(data))
    return struct.unpack(fmt, data)



#fonction qui recupere une tuple constitué de n*5 coordonnées et revoies n listes de 5 elements dans une liste
def split_in_chunks(liste, size_chunk):
    new_liste = []
    for i in range(0, len(liste), size_chunk):
        new_liste.append(list(liste[i:i+size_chunk]))
    return new_liste


#fonction qui recupere les updates et les applique sur l'ancien etat du tableau, renvoyant le nouvel etat du tableau
def new_state(old_state, changes):
    new = old_state.copy()
    for i in range(len(changes)):
        for j in range(len(old_state)):
            if changes[i][0] == old_state[j][0] and changes[i][1] == old_state[j][1]:
                new[j] = changes[i]
    return new

#def deplacement_aleatoire(liste_loups):
#    liste_deplacements = []
#    #new_list = []
#    for j in range(liste_loups[2]):
#        for i in range(2):
#            aleax = random.randint(-1,1)
#            aleay = random.randint(-1,1)
#            new_x = liste_loups[0] + aleax
#            new_y = liste_loups[0] + aleay
#        liste_deplacements.append([new_x, new_y, 1])
##    for i in range(len(liste_deplacements)):
##        for j in range(i+1, len(liste_deplacements)):
##            if liste_deplacements[i][0] == liste_deplacements[j][0] and liste_deplacements[i][1] == liste_deplacements[j][1]:
##                liste_deplacements[i][2] += 1
##                new_list = new_list.append(liste_deplacements[i])
#    return liste_deplacements
        
        
          
            
    
        
        

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect((HOST, int(PORT)))

# NME
sock.send("NME".encode("ascii"))
sock.send(struct.pack("1B",  7))
sock.send('MAJELOR'.encode("ascii"))

# SET
header = sock.recv(3).decode("ascii")
if header != "SET":
    print("Protocol Error at SET")
else:
    (height, width )= receive_data(sock, 2, "2B")

# HUM
header = sock.recv(3).decode("ascii")
if header != "HUM":
    print("Protocol Error at HUM")
else:
    number_of_homes = receive_data(sock, 1, "1B")[0]
    homes_raw = receive_data(sock, number_of_homes * 2, "{}B".format(number_of_homes * 2))
    
# HME
header = sock.recv(3).decode("ascii")
if header != "HME":
    print("Protocol Error at HME")
else:
    start_position = tuple(receive_data(sock, 2, "2B"))

# MAP
header = sock.recv(3).decode("ascii")
if header != "MAP":
    print("Protocol Error at MAP")
else:
    number_map_commands = receive_data(sock,1, "1B")[0]
    map_commands_raw = receive_data(sock, number_map_commands * 5, "{}B".format(number_map_commands * 5))
    
    
etat_intermediaire = split_in_chunks(map_commands_raw , 5)


entree = True

while entree:
    reply = sock.recv(3)
    if not reply:   
        time.sleep(0.02)
        
    elif reply.decode("ascii") == "END" or reply.decode("ascii") == "BYE":
        entree = False
    
    else:
        # UPD
        header = reply.decode("ascii")
        if header != "UPD":
            print("Protocol Error at UPD")
        else:
            number_upd_commands = receive_data(sock,1, "1B")[0]
            upd_commands_raw = receive_data(sock, number_upd_commands * 5, "{}B".format(number_upd_commands * 5))
        
        
        #obtention de l'etat intermediaire de la carte
        modifications = split_in_chunks(upd_commands_raw, 5)
        etat_intermediaire = new_state(etat_intermediaire, modifications)
        
        
        #liste des loups
        liste_wolfs = []
        for i in range(len(etat_intermediaire)):
            if etat_intermediaire[i][3] != 0:
                liste_wolfs.append([etat_intermediaire[i][0], etat_intermediaire[i][1], etat_intermediaire[i][3]])
                
#        #preparation de mouvements aleatoires
#        for i in range(len(liste_wolfs)):
#            dep = deplacement_aleatoire(liste_wolfs[i])
        
        
        # MOV
        list_movements=[]
        NUMBEROFMOVESTOPERFORM = len(list_movements)
        
        sock.send("MOV".encode("ascii"))
        sock.send(struct.pack("1B",  NUMBEROFMOVESTOPERFORM))
        for i in range(NUMBEROFMOVESTOPERFORM):
            for j in range(5):
                sock.send(struct.pack("1B",  list_movements[i][j])) 