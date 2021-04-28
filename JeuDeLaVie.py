from tkinter import *
import time 

class JeuDeLaVie(Frame):

	def __init__(self, parent):

		Frame.__init__(self, parent) 
		self.parent = parent
		self.nb_cell_x = 38 # nombre des cellules en largeur (nb de colonnes)
		self.nb_cell_y = 28 # nombre des cellules en hauteur (nb des lignes)
		self.grille_boutons = [] # array qui sera remplie par les boutons de la grille (les cellules)
		self.generer_suivant = True # variable bool pour la simulation et la réinitialisation du jeux
		self.interface_graphique()

	def interface_graphique(self):
		'''Interface graphique du jeux contenant le titre , la description , les boutons start et resest et la grille des cellules'''	
		self.parent.title("Jeux de la vie")

		# frame contenant le titre et la description
		self.frame_titre = Frame(self.parent)
		self.frame_titre.grid(row = 0, column = 0, columnspan = 4) 
		
		title = Label(self.frame_titre, text = "Jeux de la vie",  font = ("Arial Bold" , 15))
		title.pack(side = TOP)

		description = Label(self.frame_titre, text = "Cliquer sur les cellules pour créer la configuration du départ , puis sur le bouton Start Game pour débuter le jeux :")
		description.pack(side = BOTTOM)

		# frame contenant les boutons start et reset
		self.frame_boutons=Frame(self.parent)
		self.frame_boutons.grid(row = 1, column = 0, columnspan = 4)

		# bouton start pour lancer la simulation
		self.bouton_start = Button(self.frame_boutons, text = "Start Game", command = self.simuler_jeux)
		self.bouton_start.pack(side=LEFT)

		# bouton reset pour stopper la simulation et/ou réinitialiser le jeux
		self.bouton_reset = Button(self.frame_boutons, text = "Reset", state = DISABLED, command = self.reset_game)
		self.bouton_reset.pack(side=RIGHT)	

		# Constuction de la grille des cellules
		self.construire_grille()

	def construire_grille(self):
		'''Constuire la grille des cellules pour choisir la configutaion initiale avant de démarrer le jeux '''
		# frame contenant la grille des boutons du jeux
		self.game_frame = Frame(self.parent, width = self.nb_cell_x + 2, height = self.nb_cell_y+ 2, borderwidth = 1)
		self.game_frame.grid(row = 2, column = 0, columnspan = 4)
		
		# instancier des boutons dans l'array grille_boutons 
		self.grille_boutons = [[Button(self.game_frame, bg = "white", width = 2, height = 1) for i in range(self.nb_cell_x + 2)] for j in range(self.nb_cell_y + 2)]
		for i in range(1, self.nb_cell_y + 1):
			for j in range(1, self.nb_cell_x + 1):	
				self.grille_boutons[i][j].grid(row = i, column = j)
				# changer la couleur d'un bouton cliqué pour choisir la configuration initiale 
				self.grille_boutons[i][j]['command'] = lambda x=i, y=j:self.changer_couleur(self.grille_boutons[x][y])
				
	def simuler_jeux(self):
		'''la cellule morte ayant exactement 3 cellules voisines devient une cellule vivante 
		   et la cellule vivante ne possedant pas exactement 2 ou 3 cellules voisines devient une cellule morte
		   (La simulation s'exécute indéfiniment, jusqu'à ce qu'elle atteigne un état stable ou que vous réinitialisez le jeux (avec le bouton Reset))'''
		# desactiver les boutons
		self.desactiver_boutons()
		# liste de boutons dans la grille pour basculer
		boutons_a_changer = []
		
		for i in range(1, self.nb_cell_y + 1):
			for j in range(1, self.nb_cell_x + 1):
				# coordonnées des cellules tel que coord[0]=i et coord[1]=j pour les utiliser en dehors de la boucle
				coord = (i, j)
				# Une cellule morte (blanche) et ayant exactement 3 cellules voisines devient une cellule vivante (noire)
				if self.grille_boutons[i][j]['bg'] == "white" and self.compter_voisins(i, j) == 3:
					boutons_a_changer.append(coord)		
				# une cellule vivante (noire) ne possedant pas exactement 2 ou 3 cellules voisines devient une cellule morte (blanche)
				elif self.grille_boutons[i][j]['bg'] == "black" and self.compter_voisins(i, j) != 3 and self.compter_voisins(i, j) != 2:
					boutons_a_changer.append(coord)

		# changer la couleur des cellules mortes et vivantes qui necessitent un changement (placés dans boutons_a_changer) ensemble 
		for coord in boutons_a_changer:
			self.changer_couleur(self.grille_boutons[coord[0]][coord[1]])	

		# generer_suivant est initialisé a true dans le constructeur et ne devient false que si on clique sur reset pour stopper le jeux
		if self.generer_suivant == True : # si le bonton reset n'est pas cliqué faire une nouvelle simulation (apres 100 ms)
			self.after(100, self.simuler_jeux)
		else: # sinon (bouton reset cliqué) réinitialiser le jeux
			self.activer_boutons()
		
	
	def desactiver_boutons(self):
		'''descativer les boutons de la grille et le bouton start et activer le bouton reset'''
		if self.grille_boutons[1][1] != DISABLED:
			for i in range(0, self.nb_cell_y + 2):
				for j in range(0, self.nb_cell_x + 2):
					self.grille_boutons[i][j].configure(state = DISABLED)

			self.bouton_reset.configure(state = NORMAL)
			self.bouton_start.configure(state = DISABLED)

	def activer_boutons(self):
		'''réinitialiser le jeux (activer les boutons de la grille et le bouton start et desactiver le bouton reset)'''
		for i in range(0, self.nb_cell_y + 2):
			for j in range(0, self.nb_cell_x + 2):
				self.grille_boutons[i][j]['bg'] = "white"
				self.grille_boutons[i][j].configure(state = NORMAL)

		self.bouton_reset.configure(state = DISABLED)
		self.bouton_start.configure(state = NORMAL)
		# generer_suivant = True pour pouvoir faire de nouvelles simulations
		self.generer_suivant = True

	def compter_voisins(self, coord_x, coord_y):
		'''Prend en parametres les coordonnées x et y d'une cellules et retourne le nb des cellules voisines'''
		compteur = 0
		# parcourir 3 cellules en largeur et 3 cellules en hauteur et compter les cellules vivantes voisines (sans la cellule elle-meme)
		for i in range(coord_x - 1, coord_x + 2):
			for j in range(coord_y - 1, coord_y + 2):
				if (i != coord_x or j != coord_y) and self.grille_boutons[i][j]['bg'] == "black":
					compteur += 1

		return compteur

	def changer_couleur(self, cellule):
		'''une cellule morte (blanche) devient vivante (noire) et vice versa'''
		if cellule['bg'] == "white":
			cellule['bg'] = "black"
		else:
			cellule['bg'] = "white"

	def reset_game(self):
		''' appel de activer_boutons() pour réinitialiser le jeux''' 
		self.generer_suivant = False 
		
if __name__ == '__main__':
	window = Tk()
	window.resizable(False , False)
	window.geometry("+190+0")
	game = JeuDeLaVie(window)
	window.mainloop()

	