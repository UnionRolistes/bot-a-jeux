#UnitTest

import unittest
from puissance4 import *

class TestPuissance4(unittest.TestCase):
  def test_jouer_coup(self):
    # Initialiser la grille
    grille = [[' ' for j in range(7)] for i in range(6)]

    # Vérifier que le coup est joué correctement
    jouer_coup(grille, 1, 'X')
    self.assertEqual(grille[5][0], 'X')
    jouer_coup(grille, 3, 'O')
    self.assertEqual(grille[5][2], 'O')
    jouer_coup(grille, 3, 'X')
    self.assertEqual(grille[4][2], 'X')

    # Vérifier qu'une erreur est levée si la colonne est pleine
    with self.assertRaises(ValueError):
      jouer_coup(grille, 3, 'O')

  def test_gagnant(self):
    # Initialiser la grille
    grille = [[' ' for j in range(7)] for i in range(6)]

    # Vérifier que la fonction renvoie False si aucun joueur n'a gagné
    self.assertFalse(gagnant(grille, 'X'))
    self.assertFalse(gagnant(grille, 'O'))

    # Simuler une victoire en ligne
    grille[0] = ['X', 'X', 'X', 'X', ' ', ' ', ' ']
    self.assertTrue(gagnant(grille, 'X'))
    self.assertFalse(gagnant(grille, 'O'))

    # Simuler une victoire en colonne
    grille[0] = [' ', ' ', ' ', ' ', ' ', ' ', ' ']
    grille[1] = ['O', ' ', ' ', ' ', ' ', ' ', ' ']
    grille[2] = ['O', ' ', ' ', ' ', ' ', ' ', ' ']
    grille[3] = ['O', ' ', ' ', ' ', ' ', ' ', ' ']
    self.assertTrue(gagnant(grille, 'O'))
    self.assertFalse(gagnant(grille, 'X'))

    # Simuler une victoire en diagonale (haut-gauche vers bas-droite)
    grille[0] = [' ', ' ', 'X', ' ', ' ', ' ', ' ']
    grille[1] = [' ', 'X', ' ', ' ', ' ', ' ', ' ']
    grille[2] = ['X', ' ', ' ', ' ', ' ', ' ', ' ']
    grille[3] = [' ', ' ', ' ', ' ', ' ', ' ', ' ']
    self.assertTrue(gagnant(grille, 'X'))
    self.assertFalse(gagnant(grille, 'O'))

    # Simuler une victoire en diagonale (bas-gauche vers haut
