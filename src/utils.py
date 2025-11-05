import cv2
import os
import numpy as np

#====================================================================================================
# méthode getTemplates
# input :
#   - path : STRING = chemin vers les images
#   - extensions : STRING = extension des images
# output :
#    - templates : DICT = dictionnaire des images avec leur noms
#====================================================================================================
def getTemplates(path) :
    templates = {}
    for file in os.listdir(path):
        filename = file.split(".")[0]
        template = cv2.imread(os.path.join(path, file), cv2.IMREAD_GRAYSCALE) #image grise
        templates[filename] = template
    return templates

#====================================================================================================
# méthode getFaceCard
# input :
#   - pts : ARRAY_LIKE = image de face
#   - pts : ??? = ???
# output :
#   - warp : ARRAY_LIKE = image vu de face
#====================================================================================================
def getFaceCard(image, approx):
    pts = np.array([p[0] for p in approx], dtype=np.float32)
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
    warp = cv2.warpPerspective(image, H, (width, height))
    return warp



# rank_name, rank_score = compare(rank, template_ranks, roi_size_x, roi_size_y)
def compare(image, templates, size_x, size_y) :
    best_name = "?"
    best_score = size_x*size_y
    scanned_image = cv2.resize(image, (size_x, size_y))
    for template_name, template in templates.items() :
        template = cv2.resize(template, (size_x, size_y))
        _, template = cv2.threshold(template, 175, 255, cv2.THRESH_BINARY_INV)
        comparaison = cv2.bitwise_xor(scanned_image, template)
        # cv2.imshow("scanned_image", scanned_image)
        # cv2.imshow("template", template)
        # cv2.imshow("comparaison", comparaison)
        # cv2.waitKey(0)
        score = cv2.countNonZero(comparaison)
        if score < best_score :
            best_score = score
            best_name = template_name
    return best_name, best_score
