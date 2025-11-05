#========== Import ==========
import matplotlib.pyplot as plt
import cv2
import numpy as np

from utils import getTemplates
from utils import getFaceCard
from utils import compare

from board import Card, Board

roi_size_y = 80
roi_size_x = 50

#====================================================================================================
# Méthode Main           comparaisoon rank et suit idependant
#====================================================================================================
if __name__ == '__main__' :

    #========== Manipulation image ==========
    image = cv2.imread("./datas/tables/quinte_flush_royal.jpg")
    # pair                  V
    # double pair           V
    # brelan                V
    # quinte                V
    # couleur               V
    # full                  V
    # carre                 V
    # quinte flush          V
    # quinte flush royal    V
    image_original = image.copy()
    image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)                     # Image en niveau de gris
    image = cv2.blur(image, (5, 5))                                     # Image en niveau de gris flouté
    _, image_thresh = cv2.threshold(image, 127, 255, cv2.THRESH_BINARY) # seuillage sur l'image pour détecter les cartes

    #========== Manipulation contours ==========
    contours, _ = cv2.findContours(image_thresh, 1, 2)  # Récupération de tout les contours
    img = image_original.copy()
    for contour in contours :
        x, y, w, h = cv2.boundingRect(contour)
        img = cv2.rectangle(img, (x,y), (x+w,y+h), (0, 255, 0), 2)

    card_contours = []
    for contour in contours:
        area = cv2.contourArea(contour)                         
        img_area = image.shape[0] * image.shape[1]
        if area / img_area > 0.02 :                     # On garde pas les petits objets
            card_contours.append(contour)
    print("nombre de carte:", len(card_contours))
    img = image_original.copy()
    for contour in card_contours :
        x, y, w, h = cv2.boundingRect(contour)
        img = cv2.rectangle(img, (x,y), (x+w,y+h), (0, 255, 0), 2)

    #========== Manipulation des CARTES SCANNEES ==========
    template_ranks = getTemplates("./datas/ranks") # carte grise
    template_suits = getTemplates("./datas/suits") # carte grise
    board = Board()
    for contour in card_contours :
        perimeter = cv2.arcLength(contour, True)
        approx = cv2.approxPolyDP(contour, 0.02 * perimeter, True)
        faced_card = getFaceCard(image_original, approx)

        faced_card = cv2.cvtColor(faced_card, cv2.COLOR_BGR2GRAY)
        roi_card = faced_card[10:90, 0:30]
        _, card_thresh = cv2.threshold(roi_card, 175, 255, cv2.THRESH_BINARY_INV)       # Seuillage inverse du haut gauche de la carte scannée

        roi_contours, _ = cv2.findContours(card_thresh, 1, 2)
        roi_contours = sorted(roi_contours, key=cv2.contourArea, reverse=True)
        roi_contours = roi_contours[:2]

        def contour_top_y(contour):
            _, y, _, _ = cv2.boundingRect(contour)
            return y

        rank_suit_contour = sorted(roi_contours, key=contour_top_y)
        rank_contour, suit_contour = rank_suit_contour

        # Gestion du rank
        x, y, w, h = cv2.boundingRect(rank_contour)
        rank = card_thresh[y:y+h, x:x+w]
        rank = cv2.resize(rank, (roi_size_x, roi_size_y))
        rank_name, rank_score = compare(rank, template_ranks, roi_size_x, roi_size_y)

        # Gestion du suit
        x, y, w, h = cv2.boundingRect(suit_contour)
        suit = card_thresh[y:y+h, x:x+w]
        suit = cv2.resize(suit, (roi_size_x, roi_size_y))
        suit_name, suit_score = compare(suit, template_suits, roi_size_x, roi_size_y)

        # Ajout au plateau
        center = np.mean(approx[:, 0, 1])
        if center < image_original.shape[1]/2 :
            board.add_table_card(Card(rank_name, suit_name, contour))
        else :
            board.add_player_card(Card(rank_name, suit_name, contour))

    # Affichage
    print(board)
    main, cards = board.best_hand()
    image_original = cv2.putText(image_original, main, (0, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (211, 255, 66), 2, cv2.LINE_AA)
    for card in cards :
        x, y, w, h = cv2.boundingRect(card.contour)
        image_original = cv2.rectangle(image_original, (x,y), (x+w,y+h), (211, 255, 66), 3)
        image_original = cv2.rectangle(image_original, (x,y-30), (x+w,y), (211, 255, 66), -1)
        image_original = cv2.putText(image_original, str(card), (x+5, y-10), cv2.FONT_HERSHEY_COMPLEX, 0.5, (0, 0, 0), 1, cv2.LINE_AA)
    cv2.imshow("image_original", image_original)
    cv2.waitKey(0)
    cv2.destroyAllWindows()