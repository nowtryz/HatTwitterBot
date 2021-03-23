import sys, os
import cv2
import numpy as np
from PIL import Image

def detecte_visages(image):
    # on charge l'image en mémoire
    img = cv2.imread(image)
    # on charge le modèle de détection des visages
    face_model = cv2.CascadeClassifier("haarcascade_frontalface_alt2.xml")
     
    # détection du ou des visages
    faces = face_model.detectMultiScale(img)
     
    # on place un cadre autour des visages 
    for face in faces:
        return (face[0], face[1]),(face[0]+face[2], face[1]), face[3]


def superpose(img, img_overlay, x, y, alpha_mask):
    """Overlay `img_overlay` onto `img` at (x, y) and blend using `alpha_mask`.

    `alpha_mask` must have same HxW as `img_overlay` and values in range [0, 1].
    """
    # Image ranges
    y1, y2 = max(0, y), min(img.shape[0], y + img_overlay.shape[0])
    x1, x2 = max(0, x), min(img.shape[1], x + img_overlay.shape[1])

    # Overlay ranges
    y1o, y2o = max(0, -y), min(img_overlay.shape[0], img.shape[0] - y)
    x1o, x2o = max(0, -x), min(img_overlay.shape[1], img.shape[1] - x)

    # Exit if nothing to do
    if y1 >= y2 or x1 >= x2 or y1o >= y2o or x1o >= x2o:
        return

    # Blend overlay within the determined ranges
    img_crop = img[y1:y2, x1:x2]
    img_overlay_crop = img_overlay[y1o:y2o, x1o:x2o]
    alpha = alpha_mask[y1o:y2o, x1o:x2o, np.newaxis]
    alpha_inv = 1.0 - alpha

    img_crop[:] = alpha * img_overlay_crop + alpha_inv * img_crop


def putTheHat(image):
    visage = detecte_visages(image)
    largeur = (visage[1][0]-visage[0][0])
    if largeur > 275:
        chapeau="chapeau/casquette_275.png"
    elif largeur > 225:
        chapeau="chapeau/casquette_225.png" 
    elif largeur > 175:
        chapeau="chapeau/casquette_175.png"       
    elif largeur > 125:
        chapeau="chapeau/casquette_125.png"   
    else :
        chapeau="chapeau/casquette_75.png"     
        
    hauteur = visage[2]
    img_overlay_rgba = np.array(Image.open(chapeau)) 
    x, y = visage[0][0]+(int)(largeur/2) - (int)(img_overlay_rgba.shape[1]/2), visage[0][1]- (int)(img_overlay_rgba.shape[0]) + int(hauteur/10)
    
    # Perform blending
    alpha_mask = img_overlay_rgba[:, :, 3] / 255.0
    img_result = img[:, :, :3].copy()
    img_overlay = img_overlay_rgba[:, :, :3]
    superpose(img_result, img_overlay, x, y, alpha_mask)
    
    # Save result
    Image.fromarray(img_result).save(image[:-4]+"WithHat.jpg") #image à tweeter
    print("The hat has been put :)")

putTheHat("oui.png")



 
