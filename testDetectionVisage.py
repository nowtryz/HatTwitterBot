# -*- coding: utf-8 -*-
"""
Created on Tue Mar 23 21:54:36 2021

@author: masso
"""


import sys, os
import cv2
  
def detecte_visages(image, image_out, show = True):
    # on charge l'image en mémoire
    img = cv2.imread(image)
    # on charge le modèle de détection des visages
    face_model = cv2.CascadeClassifier("haarcascade_frontalface_alt2.xml")
     
     
    # détection du ou des visages
    faces = face_model.detectMultiScale(img)
     
    # on place un cadre autour des visages
    print ("nombre de visages", len(faces), "dimension de l'image", img.shape, "image", image)
    for face in faces:
        cv2.rectangle(img, (face[0], face[1]), (face[0] + face[2], face[0] + face[3]), (255, 0, 0), 3)
         
    # on sauvegarde le résultat final
    cv2.imwrite(image_out, img)
     
    # pour voir l'image, presser ESC pour sortir
    if show :
        cv2.imshow("visage",img)
        if cv2.waitKey(5000) == 27: cv2.destroyWindow("visage")
   
 
detecte_visages("humain1.jpg", "visage_trouve.jpg")