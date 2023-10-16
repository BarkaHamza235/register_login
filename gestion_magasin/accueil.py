from tkinter import *
from PIL import Image, ImageTk
from tkinter import ttk, messagebox
import time
import os
import subprocess



class Acceuil:
    def __init__(self, root):
        self.root = root
        self.root.title("Acceuil")
        self.root.geometry("1920x1040+0+0")
        self.root.config(bg="white")
        
        self.icon_title = ImageTk.PhotoImage(file=r"D:\Python_projects\gestion_magasin\image\logo.png")

        #Title
        title = Label(self.root, text="Gestion Magasin ", image=self.icon_title, font=("times new roman",40,"bold"), bg="cyan", anchor="w", padx=20, compound=LEFT).place(x=0, y=0, relwidth=1, height=100)

        #Bouton deconnecter
        btn_deconnecter = Button(self.root, text="Deconnexion", command=self.deconnecter, cursor="hand2", font=("times new roman",20,"bold"), bg="orange").place(x=1150, y=20)

        #Heure
        self.heure = Label(self.root, text="Bienvenue chez Hamza Magasin\t\t Date : DD-MM-YYYY\t\t Heure : HH:MM:SS ", font=("times new roman",15), bg="black", fg="white").place(x=0, y=100, relwidth=1, height=40)

        #Menu
        self.logomenu = Image.open(r"D:\Python_projects\gestion_magasin\image\menu.jpg")
        self.logomenu = self.logomenu.resize((450,300))
        self.logomenu = ImageTk.PhotoImage(self.logomenu)

        menu_frame = Frame(self.root,bd=2, relief=RIDGE, bg="white")
        menu_frame.place(x=0, y=140, width=450, height=850)
        label_logomenu = Label(menu_frame, image=self.logomenu)
        label_logomenu.pack(side=TOP, fill=X)

        self.icon_menu = ImageTk.PhotoImage(file=r"D:\Python_projects\gestion_magasin\image\side.png")

        label_menu = Label(menu_frame, text="Menu", font=("times new roman",40,"bold"), bg="orange").pack(side=TOP, fill=X)

        #Boutons pour Employe, Fournisseur, Categorie, Produit, Vente, Quitter
        btn_employe = Button(menu_frame, image=self.icon_menu, text="Employe", command=self.employe, cursor="hand2", font=("times new roman",20),bd=5, bg="white",  anchor="w", padx=10, compound=LEFT).pack(side=TOP, fill=X)
        btn_fournisseur = Button(menu_frame, image=self.icon_menu, text="Fournisseur", command=self.fournisseur, cursor="hand2", font=("times new roman",20),bd=5, bg="white",  anchor="w", padx=10, compound=LEFT).pack(side=TOP, fill=X)
        btn_categorie = Button(menu_frame, image=self.icon_menu, text="Categorie", command=self.categorie, cursor="hand2", font=("times new roman",20),bd=5, bg="white",  anchor="w", padx=10, compound=LEFT).pack(side=TOP, fill=X)
        btn_produit = Button(menu_frame, image=self.icon_menu, text="Produit", command=self.produit, cursor="hand2", font=("times new roman",20),bd=5, bg="white",  anchor="w", padx=10, compound=LEFT).pack(side=TOP, fill=X)
        btn_vendeur = Button(menu_frame, image=self.icon_menu, text="Vente", command=self.vente, cursor="hand2", font=("times new roman",20),bd=5, bg="white",  anchor="w", padx=10, compound=LEFT).pack(side=TOP, fill=X)
        btn_quitter = Button(menu_frame, image=self.icon_menu, text="Quitter", command=self.quitter, cursor="hand2", font=("times new roman",20),bd=5, bg="white",  anchor="w", padx=10, compound=LEFT).pack(side=TOP, fill=X)
        
        #Contenu
        self.label_employe = Label(self.root, text="Total Employe \n[0]", font=("goudy old style",20,"bold"), bg="green", bd=5, relief=RIDGE).place(x=500, y=200, width=300, height=150)
        self.label_fournisseur = Label(self.root, text="Total Fournisseur \n[0]", font=("goudy old style",20,"bold"), bg="red", bd=5, relief=RIDGE).place(x=850, y=200, width=300, height=150)
        self.label_categorie = Label(self.root, text="Total Categorie \n[0]", font=("goudy old style",20,"bold"), bg="gold", bd=5, relief=RIDGE).place(x=1200, y=200, width=300, height=150)
        self.label_produit = Label(self.root, text="Total Produit \n[0]", font=("goudy old style",20,"bold"), bg="gray", bd=5, relief=RIDGE).place(x=1550, y=200, width=300, height=150)
        self.label_vente = Label(self.root, text="Total Vente \n[0]", font=("goudy old style",20,"bold"), bg="blue", bd=5, relief=RIDGE).place(x=1000, y=400, width=300, height=150)

        #Footer
        label_footer = Label(self.root, text="Develloper par Hamza Barka\t\t\t barkahamza454@gmail.com\t\t\t +221 70 847 03 94\t\tCopyright 2023", font=("times new roman",15,"bold"), bg="black", fg="white").pack(side=BOTTOM, fill=X)


        #Fonctions
    def employe(self):
        self.obj = os.system("python D:\Python_projects\gestion_magasin\employe.py")

    def vente(self):
        self.obj = os.system("python D:\Python_projects\gestion_magasin\_vente.py")
    
    def fournisseur(self):
        self.obj = os.system("python D:\Python_projects\gestion_magasin\_fournisseur.py")

    def categorie(self):
        self.obj = os.system("python D:\Python_projects\gestion_magasin\categorie.py")

    def produit(self):
        self.obj = os.system("python D:\Python_projects\gestion_magasin\produit.py")

    def quitter(self):
        self.root.destroy()

    def deconnecter(self):
        self.root.destroy()
        self.obj = os.system("python D:\Python_projects\gestion_magasin\login.py")



if __name__=="__main__":
    root = Tk()
    obj = Acceuil(root)
    root.mainloop()