import cv2
import os
import numpy as np

#===============================================================
# méthode getTemplates
# input :
#   - path : STRING = chemin vers les images
#   - extensions : STRING = extension des images
# output :
#    - templates : DICT = dictionnaire des images avec leur noms
#===============================================================
def getTemplates(path) :
    templates = {}
    for file in os.listdir(path):
        filename = file.split(".")[0]
        template = cv2.imread(os.path.join(path, file), cv2.IMREAD_GRAYSCALE) #image grise
        templates[filename] = template
    return templates

#=======================================================================
# méthode getFaceCard
# input :
#   - image_ : ARRAY_LIKE = image entière composé de la zone à redresser
#   - approx_ : ??? = ???
# output :
#   - warp : ARRAY_LIKE = image vu de face
#=======================================================================
def getFaceCard(image_, approx_):
    pts = np.array([p[0] for p in approx_], dtype=np.float32)
    src = np.zeros((4, 2), dtype="float32")
    s = pts.sum(axis=1)
    src[0] = pts[np.argmin(s)]
    src[2] = pts[np.argmax(s)]
    diff = np.diff(pts, axis=1)
    src[1] = pts[np.argmin(diff)]
    src[3] = pts[np.argmax(diff)]

    width, height = 200, 300
    dst = np.array([
        [0, 0],
        [width - 1, 0],
        [width - 1, height - 1],
        [0, height - 1]
    ], dtype="float32")
    H, _ = cv2.findHomography(src, dst)
    warp = cv2.warpPerspective(image_, H, (width, height))
    return warp

#==============================================================================================
# méthode compare
# input :
#   - image_ : ARRAY_LIKE = image à comparer
#   - templates_ : LIST_LIKE[ ARRAY_LIKE ] = liste des images de références
#   - size_x_ : INT = taille pour le redimensionnement sur x
#   - size_y_ : INT = taille pour le redimensionnement sur y
# output :
#   - best_name : STRING = nom de l'image de référence la plus ressemblante
#   - best_score : INT = nombre de pixel différent entre image_ et l'image la plus ressemblante
#==============================================================================================
def compare(image_, templates_, size_x_, size_y_) :
    best_name = "?"
    best_score = size_x_*size_y_
    scanned_image = cv2.resize(image_, (size_x_, size_y_))
    for template_name, template in templates_.items() :
        template = cv2.resize(template, (size_x_, size_y_))
        _, template = cv2.threshold(template, 175, 255, cv2.THRESH_BINARY_INV)
        comparaison = cv2.bitwise_xor(scanned_image, template)
        score = cv2.countNonZero(comparaison)
        if score < best_score :
            best_score = score
            best_name = template_name
    return best_name, best_score
