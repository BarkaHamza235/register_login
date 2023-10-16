from tkinter import *
from PIL import Image, ImageTk
from tkinter import ttk, messagebox
import time
import os
import sqlite3, pymysql

class Produit:
    def __init__(self, root):
        self.root = root
        self.root.title("Produit")
        self.root.geometry("1920x1040+0+0")
        self.root.config(bg="white")
        self.root.focus_force()

        #Date base avec sqlite3
        con = sqlite3.connect(database=r"D:\Python_projects\gestion_magasin\Donnee\magasinbase.db")
        cur = con.cursor()
        """con = pymysql.connect(host="localhost", user="root", password="", database="magasinbase")
        cur = con.cursor()"""
        cur.execute("CREATE TABLE IF NOT EXISTS produit (pid INTEGER PRIMARY KEY AUTOINCREMENT, categorie text, fournisseur text, nom text, prix text, quantite text, status text)")
        con.commit()

        #Les variables
        self.var_ecri_recherche = StringVar()
        self.var_ecri_recher_option = StringVar()
        self.var_pid = StringVar()
        self.var_categorie = StringVar()
        self.var_fournisseur = StringVar()
        self.var_nomProduit = StringVar()
        self.var_prix = StringVar()
        self.var_quantite = StringVar()
        self.var_status = StringVar()

        self.fourni_liste = []
        self.liste_fournisseur()
        
        produit_frame = Frame(self.root,bd=2, relief=RIDGE, bg="white")
        produit_frame.place(x=10, y=10, width=650, height=750)
        
        #Title 
        title = Label(produit_frame, text="Details Produit", font=("goudy old style",25,"bold"), bg="cyan", relief=RIDGE).pack(side=TOP, fill=X)
        
        categorie = Label(produit_frame, text="Categorie", font=("goudy old style",25), bg="white").place(x=30, y=80)
        fournisseur = Label(produit_frame, text="Fournisseur", font=("goudy old style",25), bg="white").place(x=30, y=150)
        nomProduit = Label(produit_frame, text="Nom", font=("goudy old style",25), bg="white").place(x=30, y=220)
        prix = Label(produit_frame, text="Prix", font=("goudy old style",25), bg="white").place(x=30, y=290)
        quantite = Label(produit_frame, text="Quantite", font=("goudy old style",25), bg="white").place(x=30, y=360)
        status = Label(produit_frame, text="Status", font=("goudy old style",25), bg="white").place(x=30, y=430)

        #Date base avec sqlite3
        con = sqlite3.connect(database=r"D:\Python_projects\gestion_magasin\Donnee\magasinbase.db")
        cur = con.cursor()
        """con = pymysql.connect(host="localhost", user="root", password="", database="magasinbase")
        cur = con.cursor()"""
        cur.execute("select nom from categorie")
        rows = cur.fetchall()

        ecri_categorie = ttk.Combobox(produit_frame, textvariable=self.var_categorie, values=rows, font=("goudy old style",20), state="r", justify=CENTER)
        ecri_categorie.set("Select")
        ecri_categorie.place(x=210, y=80, width=250)

        #Date base avec sqlite3
        con = sqlite3.connect(database=r"D:\Python_projects\gestion_magasin\Donnee\magasinbase.db")
        cur = con.cursor()
        """con = pymysql.connect(host="localhost", user="root", password="", database="magasinbase")
        cur = con.cursor()"""
        cur.execute("select nom from fournisseur")
        rows = cur.fetchall()

        ecri_fournisseur = ttk.Combobox(produit_frame, textvariable=self.var_fournisseur, values=self.fourni_liste, font=("goudy old style",20), state="r", justify=CENTER)
        ecri_fournisseur.current(0)
        ecri_fournisseur.place(x=210, y=150, width=250)

        ecri_nomProduit = Entry(produit_frame, textvariable=self.var_nomProduit, font=("goudy old style",20), bg="lightyellow").place(x=210, y=230)
        ecri_prix = Entry(produit_frame, textvariable=self.var_prix, font=("goudy old style",20), bg="lightyellow").place(x=210, y=300)
        ecri_quantite = Entry(produit_frame, textvariable=self.var_quantite, font=("goudy old style",20), bg="lightyellow").place(x=210, y=370)

        ecri_status = ttk.Combobox(produit_frame, textvariable=self.var_status, values=["Active","Inactive"], font=("goudy old style",20), state="r", justify=CENTER)
        ecri_status.current(0)
        ecri_status.place(x=210, y=430, width=250)

        self.ajout_btn = Button(produit_frame, command=self.ajout_produit, text="Ajouter", state="normal", cursor="hand2", font=("times new roman",20), bg="green")
        self.ajout_btn.place(x=10, y=500, width=145, height=60)

        self.modifier_btn = Button(self.root, command=self.modifier, text="Modifier", state="disabled", cursor="hand2", font=("times new roman",20), bg="yellow")
        self.modifier_btn.place(x=180, y=510, width=145, height=60)
        self.supprimer_btn = Button(self.root, command=self.supprimer, text="Supprimer", state="disabled", cursor="hand2", font=("times new roman",20), bg="red")
        self.supprimer_btn.place(x=340, y=510, width=145, height=60)
        self.effacer_btn = Button(self.root, command=self.effacer, text="Effacer", cursor="hand2", font=("times new roman",20), bg="lightgray")
        self.effacer_btn.place(x=500, y=510, width=145, height=60)

        #Rechercher Employe
        reche_Frame = LabelFrame(self.root, text="Rechercher Produit", font=("goudy old style", 20), bd=2, relief=RIDGE, bg="white")
        reche_Frame.place(x=700, y=10, width=750, height=90)

        ecri_recher_option = ttk.Combobox(reche_Frame, textvariable=self.var_ecri_recher_option, values=["Categorie","Fournisseur","Nom"], font=("goudy old style",20), state="r", justify=CENTER)
        ecri_recher_option.current(0)
        ecri_recher_option.place(x=10, y=10, width=200)

        ecri_recherche = Entry(reche_Frame, textvariable=self.var_ecri_recherche, font=("goudy old style",20), bg="lightyellow").place(x=225, y=10, width=240)

        #Bouton recherche et tous
        btn_recherche = Button(reche_Frame, command=self.recherche, text="Recherche", font=("times new roman",15, ""), cursor="hand2", bg="blue",fg="white").place(x=480, y=5, height=40)
        btn_tous = Button(reche_Frame, command=self.affiche_resultat, text="Tous", font=("times new roman",15, ""), cursor="hand2", bg="lightgray",fg="black").place(x=590, y=5, height=40)


        #Liste Produit
        liste_Frame = Frame(self.root, bd=3, relief=RIDGE)
        liste_Frame.place(x=680, y=120, width=800, height=580)
        
        scroll_y = Scrollbar(liste_Frame, orient=VERTICAL)
        scroll_y.pack(side=RIGHT, fill=Y)

        scroll_x = Scrollbar(liste_Frame, orient=HORIZONTAL)
        scroll_x.pack(side=BOTTOM, fill=X)

        self.produitliste = ttk.Treeview(liste_Frame, columns=("pid","categorie", "fournisseur", "nom", "prix", "quantite", "status"), yscrollcommand=scroll_y.set, xscrollcommand=scroll_x.set)

        scroll_x.config(command=self.produitliste.xview)
        scroll_y.config(command=self.produitliste.yview)

        self.produitliste.heading("pid", text="ID")
        self.produitliste.heading("categorie", text="Categorie")
        self.produitliste.heading("fournisseur", text="Fournisseur")
        self.produitliste.heading("nom", text="Nom")
        self.produitliste.heading("prix", text="Prix")
        self.produitliste.heading("quantite", text="Quantite")
        self.produitliste.heading("status", text="Status")
        
        self.produitliste["show"] = "headings" 

        self.produitliste.pack(fill=BOTH, expand=1)
        
        self.produitliste.bind("<ButtonRelease-1>", self.information)

        self.affiche_resultat()


    def liste_fournisseur(self):
        self.fourni_liste.append("Vide")
        #Date base avec sqlite3
        con = sqlite3.connect(database=r"D:\Python_projects\gestion_magasin\Donnee\magasinbase.db")
        cur = con.cursor()
        """con = pymysql.connect(host="localhost", user="root", password="", database="magasinbase")
        cur = con.cursor()"""
        try:
            cur.execute("select nom from fournisseur")
            four = cur.fetchall()
            if len(four) >0:
                 del self.fourni_liste[:]
                 self.fourni_liste.append("Select")
                 for i in four:
                    self.fourni_liste.append(i[0])

                 
        except Exception as ex:
                messagebox.showerror("Erreur", f"Erreur de connexion: {str(ex)} !")


    
    #Les fonctions
    def ajout_produit(self):
        con = sqlite3.connect(database=r"D:\Python_projects\gestion_magasin\Donnee\magasinbase.db")
        cur = con.cursor()
        """con = pymysql.connect(host="localhost", user="root", password="", database="magasinbase")
        cur = con.cursor()"""

        try:
            if self.var_categorie.get() =="Select" or self.var_fournisseur.get() =="Select" or self.var_nomProduit.get() =="":
                messagebox.showerror("Erreur", "Saisir les champs obligatoires(categorie, fournisseur et nom produit) !")
            else:
                cur.execute("select * from produit where nom=?", (self.var_nomProduit.get(),))
                row = cur.fetchone()
                if row != None: 
                    messagebox.showerror("Erreur","Produit existe deja !")
                else:
                    cur.execute("insert into produit (categorie, fournisseur, nom, prix, quantite, status) values(?,?,?,?,?,?)", (
                        self.var_categorie.get(),
                        self.var_fournisseur.get(),
                        self.var_nomProduit.get(),
                        self.var_prix.get(),
                        self.var_quantite.get(),
                        self.var_status.get(),
                    ))
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
            cur.execute("select * from produit")
            rows = cur.fetchall()
            self.produitliste.delete(*self.produitliste.get_children())
            for row in rows:
                self.produitliste.insert("", END, values=row)

        except Exception as ex:
                messagebox.showerror("Erreur", f"Erreur de connexion: {str(ex)} !")


    def information(self, ev):
        self.ajout_btn.config(state="disabled") #desactiver le bouton ajouter
        self.modifier_btn.config(state="normal") #activer le bouton modifier
        self.supprimer_btn.config(state="normal") #activer le bouton supprimer
        
        r = self.produitliste.focus()
        contenu = self.produitliste.item(r)

        row = contenu["values"]
        self.var_pid.set(row[0]),
        self.var_categorie.set(row[1]),
        self.var_fournisseur.set(row[2]),
        self.var_nomProduit.set(row[3]),
        self.var_prix.set(row[4]),
        self.var_quantite.set(row[5]),
        self.var_status.set(row[6]),


    def modifier(self):
        con = sqlite3.connect(database=r"D:\Python_projects\gestion_magasin\Donnee\magasinbase.db")
        cur = con.cursor()
        """con = pymysql.connect(host="localhost", user="root", password="", database="magasinbase")
        cur = con.cursor()"""
        
        try:
            if self.var_pid.get() =="":
                messagebox.showerror("Erreur", "Selectioner un ID")
            else:
                cur.execute("select * from produit where pid=?", (self.var_pid.get(),))
                row = cur.fetchone()
                if row == None: 
                    messagebox.showerror("Erreur","Veuillez selectionner un produit sur la liste !")
                else:
                    cur.execute("update produit set categorie=?, fournisseur=?, nom=?, prix=?, quantite=?, status=? where pid=?", (
                    self.var_categorie.get(),
                    self.var_fournisseur.get(),
                    self.var_nomProduit.get(),
                    self.var_prix.get(),
                    self.var_quantite.get(),
                    self.var_status.get(),
                    self.var_pid.get(),
                ))
            con.commit()
            self.affiche_resultat()
            self.effacer()

            messagebox.showinfo("Succes", "Modification Effectuee avec succes !")
            
           
        except Exception as ex:
            messagebox.showerror("Erreur", f"Erreur de connexion: {str(ex)} !")



    
    def supprimer(self):
        con = sqlite3.connect(database=r"D:\Python_projects\gestion_magasin\Donnee\magasinbase.db")
        cur = con.cursor()
        """con = pymysql.connect(host="localhost", user="root", password="", database="magasinbase")
        cur = con.cursor()"""
        try:
            ok = messagebox.askyesno("Voullez-vous vraiment supprimer ?")
            if ok == True:
                cur.execute("delete from produit where pid=?", self.var_pid.get())
                con.commit()
                self.affiche_resultat()
                self.effacer()
                messagebox.showinfo("Succes", "Suppression Effectue !")
                

        except Exception as ex:
            messagebox.showerror("Erreur", f"Erreur de connexion: {str(ex)} !")
    

    def effacer(self):
        self.ajout_btn.config(state="normal") #desactiver le bouton ajouter
        self.modifier_btn.config(state="disabled") #activer le bouton modifier
        self.supprimer_btn.config(state="disabled") #activer le bouton supprimer

        self.var_pid.set(""),
        self.var_categorie.set("Select"),
        self.var_fournisseur.set("Select"),
        self.var_nomProduit.set(""),
        self.var_prix.set(""),
        self.var_quantite.set(""),
        self.var_status.set("Active"),
        self.var_ecri_recherche.set(""),



    def recherche(self):
        con = sqlite3.connect(database=r"D:\Python_projects\gestion_magasin\Donnee\magasinbase.db")
        cur = con.cursor()
        """con = pymysql.connect(host="localhost", user="root", password="", database="magasinbase")
        cur = con.cursor()"""

        try:
            if self.var_ecri_recherche.get()=="":
                messagebox.showerror("Erreur", "Qu'est-ce que vous voulez rechercher ?")
            else:
                cur.execute("select * from produit where "+self.var_ecri_recher_option.get()+" LIKE '%"+self.var_ecri_recherche.get()+"%'")
                rows = cur.fetchall()
                if len(rows) !=0:
                    self.produitliste.delete(*self.produitliste.get_children())
                    for row in rows:
                        self.produitliste.insert("", END, values=row)
                else:
                    messagebox.showerror("Erreur", "Aucun resultat trouve !")

        except Exception as ex:
            messagebox.showerror("Erreur", f"Erreur de connexion: {str(ex)} !")



if __name__=="__main__":
    root = Tk()
    obj = Produit(root)
    root.mainloop()