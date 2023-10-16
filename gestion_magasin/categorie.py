from tkinter import *
from PIL import Image, ImageTk
from tkinter import ttk, messagebox
import time
import os
import sqlite3, pymysql


class Categorie:
    def __init__(self, root):
        self.root = root
        self.root.title("Categorie")
        self.root.geometry("1500x780+400+200")
        self.root.config(bg="white")
        self.root.focus_force()
        

        #Les variables
        self.var_cat_id = StringVar()
        self.var_nom = StringVar()

         #Date base avec sqlite3
        con = sqlite3.connect(database=r"D:\Python_projects\gestion_magasin\Donnee\magasinbase.db")
        cur = con.cursor()
        """con = pymysql.connect(host="localhost", user="root", password="", database="magasinbase")
        cur = con.cursor()"""
        cur.execute("CREATE TABLE IF NOT EXISTS categorie (cid INTEGER PRIMARY KEY AUTOINCREMENT, nom text)")
        con.commit()

        #Title 
        title = Label(self.root, text="Gestion Categorie Produit", font=("goudy old style",40,"bold"), bg="cyan", bd=3, relief=RIDGE).pack(side=TOP, fill=X, padx=10, pady=10)
            
        #contenu
        categorie = Label(self.root, text="Saisir Categorie Produit", font=("times new roman",30), bg="white").place(x=50, y=150)
        ecri_categorie = Entry(self.root, textvariable=self.var_nom, font=("times new roman",30), bg="lightyellow").place(x=50, y=230, width=380)

        #Boutons
        self.ajout_btn = Button(self.root, command=self.ajout_categorie, text="Ajouter", cursor="hand2", font=("times new roman",30,"bold"), bg="green")
        self.ajout_btn.place(x=450, y=230, width=160, height=50)

        self.supprimer_btn = Button(self.root, command=self.supprimer, text="Supprimer", cursor="hand2", font=("times new roman",30,"bold"), bg="red")
        self.supprimer_btn.place(x=630, y=230, width=200, height=50)

         #Liste Categorie
        liste_Frame = Frame(self.root, bd=3, relief=RIDGE)
        liste_Frame.place(x=900, y=100, width=600, height=180)
        
        scroll_y = Scrollbar(liste_Frame, orient=VERTICAL)
        scroll_y.pack(side=RIGHT, fill=Y)

        scroll_x = Scrollbar(liste_Frame, orient=HORIZONTAL)
        scroll_x.pack(side=BOTTOM, fill=X)

        self.categorieliste = ttk.Treeview(liste_Frame, columns=("cid", "nom"), yscrollcommand=scroll_y.set, xscrollcommand=scroll_x.set)

        scroll_x.config(command=self.categorieliste.xview)
        scroll_y.config(command=self.categorieliste.yview)

        self.categorieliste.heading("cid", text="ID")
        self.categorieliste.heading("nom", text="Nom")
        
        self.categorieliste["show"] = "headings" 

        self.categorieliste.pack(fill=BOTH, expand=1)

        self.categorieliste.bind("<ButtonRelease-1>", self.information)


        self.affiche_resultat()

         #Images
        self.cat1 = Image.open(r"D:\Python_projects\gestion_magasin\image\cat1.png")
        self.cat1 = self.cat1.resize((700,400))
        self.cat1 = ImageTk.PhotoImage(self.cat1)

        label_cat1 = Label(self.root, bd=7, relief=RAISED, image=self.cat1)
        label_cat1.place(x=50, y=300)

        self.cat2 = Image.open(r"D:\Python_projects\gestion_magasin\image\cat2.jpg")
        self.cat2 = self.cat2.resize((700,400))
        self.cat2 = ImageTk.PhotoImage(self.cat2)

        label_cat2 = Label(self.root, bd=7, relief=RAISED, image=self.cat2)
        label_cat2.place(x=770, y=300)


        #Les fonctions
    def ajout_categorie(self):
        con = sqlite3.connect(database=r"D:\Python_projects\gestion_magasin\Donnee\magasinbase.db")
        cur = con.cursor()
        """con = pymysql.connect(host="localhost", user="root", password="", database="magasinbase")
        cur = con.cursor()"""

        try:
            if self.var_nom.get() =="" :
                messagebox.showerror("Erreur", "Veuillez saisir une categorie de produit !")
            else:
                cur.execute("select * from categorie where nom=?", (self.var_nom.get(),))
                row = cur.fetchone()
                if row != None: 
                    messagebox.showerror("Erreur","La Categorie existe deja !")
                else:
                    cur.execute("insert into categorie (nom) values(?)", (self.var_nom.get(),))
                    con.commit()
                    self.affiche_resultat()
                    self.effacer()
                    messagebox.showinfo("Succes", "Enregistrement Effectue avec succes !")

        except Exception as ex:
                messagebox.showerror("Erreur", f"Erreur de connexion: {str(ex)} !")


    def affiche_resultat(self):
        con = sqlite3.connect(database=r"D:\Python_projects\gestion_magasin\Donnee\magasinbase.db")
        cur = con.cursor()
        """con = pymysql.connect(host="localhost", user="root", password="", database="magasinbase")
        cur = con.cursor()"""
        try:
            cur.execute("select * from categorie")
            rows = cur.fetchall()
            self.categorieliste.delete(*self.categorieliste.get_children())
            for row in rows:
                self.categorieliste.insert("", END, values=row)

        except Exception as ex:
                messagebox.showerror("Erreur", f"Erreur de connexion: {str(ex)} !")


    def information(self, ev):
        r = self.categorieliste.focus()
        contenu = self.categorieliste.item(r)
        row = contenu["values"]
        self.var_cat_id.set(row[0])
        self.var_nom.set(row[1])


    def supprimer(self):
        con = sqlite3.connect(database=r"D:\Python_projects\gestion_magasin\Donnee\magasinbase.db")
        cur = con.cursor()
        """con = pymysql.connect(host="localhost", user="root", password="", database="magasinbase")
        cur = con.cursor()"""
        try:
            if self.var_cat_id.get() =="":
                messagebox.showerror("Erreur","Veuillez selectionner une categorie a partir de la liste !")
            else:
                cur.execute("select * from categorie where cid=?", (self.var_cat_id.get(),))
                row = cur.fetchone()
                if row == None: 
                    messagebox.showerror("Erreur","L'id Categorie n'existe pas !")
                else:
                    ok = messagebox.askyesno("Voullez-vous vraiment supprimer ?")
                    if ok == True:
                        cur.execute("delete from categorie where cid=?", self.var_cat_id.get())
                        con.commit()
                        self.affiche_resultat()
                        self.effacer()
                        messagebox.showinfo("Succes", "Suppression Effectue !")
                        

        except Exception as ex:
            messagebox.showerror("Erreur", f"Erreur de connexion: {str(ex)} !")
        

    def effacer(self):
        self.var_cat_id.set("")
        self.var_nom.set("")
        

if __name__=="__main__":
    root = Tk()
    obj = Categorie(root)
    root.mainloop()