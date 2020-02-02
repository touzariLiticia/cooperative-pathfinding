#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Mar 14 12:24:54 2019

@author: 3803192
"""
import Aetoile 
import pygame
import random 

#------------------------
#Stratégie une 
#------------------------
def recalculChemin1(suivant,precedent,pos,chemin,wallStates,nbreCol,nbreLig) :
    restart=True
    wall=wallStates
    while(restart):
        c = Aetoile.Astar(chemin[pos-1],chemin[pos+1],wall,nbreCol,nbreLig)
        if(c[1] in suivant or c[1] in precedent):
            wall.append(c[1])
        else :
            restart = False
    res=[]
    for i in range(len(chemin)):
        if(i != pos):
            if (i == pos-1) :
                for j in range(len(c)-1):
                    res.append(c[j])
            else :
                res.append(chemin[i])
    return res

def strategie1(game,players,initStates,goalStates,wallStates,nbreCol,nbreLig):
    nbPlayers = len(players)
    score = [0]*nbPlayers
    chemins=[] #liste des chemins des joueurs
    suivant=[] #liste contenant les positions suivantes
    for i in range(nbPlayers):# ici on récupére tous les chemins des joueurs 
        chemins.append(Aetoile.Astar(initStates[i],goalStates[i],wallStates,nbreCol,nbreLig))
        
    joueursRestants =nbPlayers #Nous permet de quitter la boucle principale
    pos=0 # indice pour parcourir les chemins simultanément 
    while(joueursRestants>0): # tant qu'il existe un joueur qui n'a pas encore trouvé son objet
        j=0 # l'indice du joueur courant
        precedent=suivant 
        suivant=[]
        for chemin in chemins: #on recupere la position suivante pour chaque joueur  
            if(len(chemin)>pos): 
                if((chemin[pos] in suivant) or (chemin[pos] in precedent)): #tester s'il y a une collision
                    #ajouter la position comme un obstacle et recalculer le chemin
                    wall=wallStates 
                    wall.append(chemin[pos])
                    chemin=recalculChemin1(suivant,precedent,pos,chemin,wall,nbreCol,nbreLig)
                    chemins[j]=chemin
                suivant.append(chemin[pos])
                row,col=chemin[pos][0],chemin[pos][1]
                players[j].set_rowcol(row,col)
                game.mainiteration()
                
                if (row,col)==goalStates[j]:
                    o = players[j].ramasse(game.layers)
                    game.mainiteration()
                    joueursRestants-=1 
                    score[j]+=1
                    
                    # et on remet un même objet à un autre endroit
                    """
                    x = random.randint(1,19)
                    y = random.randint(1,19)
                    while (x,y) in wallStates:
                        x = random.randint(1,19)
                        y = random.randint(1,19)
                    o.set_rowcol(x,y)
                    goalStates[j]=(x,y) # on ajoute ce nouveau goalState
                    game.layers['ramassable'].add(o)
                    game.mainiteration()   
                    extension=Aetoile.Astar((row,col),(x,y),wallStates,nbreCol,nbreLig)
                    chemins[j]=chemins[j]+extension
                    """ 
            j+=1
        pos+=1
    print ("scores:", score)
    pygame.quit()
    