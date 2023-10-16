from tkinter import *
from PIL import Image, ImageTk
from tkinter import ttk, messagebox
import time
import os
import pymysql, sqlite3


class Fournisseur:
    def __init__(self, root):
        self.root = root
        self.root.title("Fournisseur")
        self.root.geometry("1920x1040+0+0")
        self.root.config(bg="white")
        self.root.focus_force()

        #Date base avec sqlite3
        con = sqlite3.connect(database=r"D:\Python_projects\gestion_magasin\Donnee\magasinbase.db")
        cur = con.cursor()
        """con = pymysql.connect(host="localhost", user="root", password="", database="magasinbase")
        cur = con.cursor()"""
        cur.execute("CREATE TABLE IF NOT EXISTS fournisseur (forid text PRIMARY KEY, nom text, contact text, description text)")
        con.commit()
        
        #Les variables
        self.var_recherche = StringVar()
        self.var_fourni_id = StringVar()
        self.var_nom = StringVar()
        self.var_contact = StringVar()

        #Rechercher Fournisseur
        reche_Option = Label(self.root, text="Rechercher par ID Fournisseur", font=("times new roman", 15), bg="white")
        reche_Option.place(x=700, y=80)
        self.ecri_recherche = Entry(self.root, textvariable=self.var_recherche, font=("times new roman",15), bg="lightyellow")
        self.ecri_recherche.place(x=950, y=80, height=40)

        #Bouton recherche et tous
        btn_recherche = Button(self.root, command=self.recherche, text="Recherche", font=("times new roman",15, ""), cursor="hand2", bg="blue",fg="white").place(x=1170, y=80, height=40)
        btn_tous = Button(self.root, command=self.affiche_resultat, text="Tous", font=("times new roman",15, ""), cursor="hand2", bg="lightgray",fg="black").place(x=1280, y=80, height=40)
        
        #Title 
        title = Label(self.root, text="Formulaire Fournisseur", font=("times new roman",20,"bold"), bg="cyan", fg="black").place(x=0, y=0, width=1499)

        #Contenu formulaire
        #ligne 1
        four_id = Label(self.root, text="ID Fournisseur", font=("goudy old style",20), bg="white").place(x=50, y=70)
        self.ecri_four_id = Entry(self.root, textvariable=self.var_fourni_id, font=("goudy old style",20), bg="lightyellow")
        self.ecri_four_id.place(x=250, y=70, width=250)

        #ligne 2
        nom = Label(self.root, text="Nom", font=("goudy old style",20), bg="white").place(x=50, y=140)
        ecri_nom = Entry(self.root, textvariable=self.var_nom, font=("goudy old style",20), bg="lightyellow").place(x=250, y=140, width=250)

        #ligne 3
        contact = Label(self.root, text="Contact", font=("goudy old style",20,), bg="white").place(x=50, y=210)
        ecri_contact = Entry(self.root, textvariable=self.var_contact, font=("goudy old style",20), bg="lightyellow").place(x=250, y=210, width=250)
        
        #ligne 4
        description = Label(self.root, text="Description", font=("goudy old style",20), bg="white").place(x=50, y=280)
        self.ecri_description = Text(self.root, font=("goudy old style",20), bg="lightyellow")
        self.ecri_description.place(x=250, y=280, width=600, height=180)

        #Boutons
        self.ajout_btn = Button(self.root, command=self.ajout_fournisseur, state="normal", text="Ajouter", cursor="hand2", font=("times new roman",20,"bold"), bg="green")
        self.ajout_btn.place(x=100, y=500, width=150, height=40)

        self.modifier_btn = Button(self.root, command=self.modifier, text="Modifier", state="disabled", cursor="hand2", font=("times new roman",20,"bold"), bg="yellow")
        self.modifier_btn.place(x=300, y=500, width=150, height=40)
        self.supprimer_btn = Button(self.root, command=self.supprimer, text="Supprimer", state="disabled", cursor="hand2", font=("times new roman",20,"bold"), bg="red")
        self.supprimer_btn.place(x=500, y=500, width=150, height=40)
        self.effacer_btn = Button(self.root, command=self.effacer, text="Effacer", cursor="hand2", font=("times new roman",20,"bold"), bg="lightgray")
        self.effacer_btn.place(x=700, y=500, width=150, height=40)


         #Liste Fournisseur
        liste_Frame = Frame(self.root, bd=3, relief=RIDGE)
        liste_Frame.place(x=900, y=150, width=600, height=500)
        
        scroll_y = Scrollbar(liste_Frame, orient=VERTICAL)
        scroll_y.pack(side=RIGHT, fill=Y)

        scroll_x = Scrollbar(liste_Frame, orient=HORIZONTAL)
        scroll_x.pack(side=BOTTOM, fill=X)

        self.fournisseurliste = ttk.Treeview(liste_Frame, columns=("forid", "nom", "contact", "description"), yscrollcommand=scroll_y.set, xscrollcommand=scroll_x.set)

        scroll_x.config(command=self.fournisseurliste.xview)
        scroll_y.config(command=self.fournisseurliste.yview)

        self.fournisseurliste.heading("forid", text="ID")
        self.fournisseurliste.heading("nom", text="Nom")
        self.fournisseurliste.heading("contact", text="Contact")
        self.fournisseurliste.heading("description", text="Description")

        self.fournisseurliste["show"] = "headings" 
        self.fournisseurliste.bind("<ButtonRelease-1>")

        self.fournisseurliste.pack(fill=BOTH, expand=1)

        self.fournisseurliste.bind("<ButtonRelease-1>", self.information)


        self.affiche_resultat()

        #Les fonctions
    def ajout_fournisseur(self):
        con = sqlite3.connect(database=r"D:\Python_projects\gestion_magasin\Donnee\magasinbase.db")
        cur = con.cursor()
        """con = pymysql.connect(host="localhost", user="root", password="", database="magasinbase")
        cur = con.cursor()"""

        try:
            if self.var_fourni_id.get() =="" or self.var_nom.get() =="" or self.var_contact.get() =="":
                messagebox.showerror("Erreur", "Veuillez mettre un ID nom et contact  !")
            else:
                cur.execute("select * from fournisseur where forid=?", (self.var_fourni_id.get(),))
                row = cur.fetchone()
                if row != None: 
                    messagebox.showerror("Erreur","L'ID Fournisseur existe deja !")
                else:
                    cur.execute("insert into fournisseur (forid, nom, contact, description) values(?,?,?,?)", (
                        self.var_fourni_id.get(),
                        self.var_nom.get(),
                        self.var_contact.get(),
                        self.ecri_description.get("1.0", END)
                    ))
                    con.commit()
                    self.affiche_resultat()
                    messagebox.showinfo("Succes", "Ajout Effectue avec succes !")

        except Exception as ex:
                messagebox.showerror("Erreur", f"Erreur de connexion: {str(ex)} !")

        
        
    def affiche_resultat(self):
        con = sqlite3.connect(database=r"D:\Python_projects\gestion_magasin\Donnee\magasinbase.db")
        cur = con.cursor()
        """con = pymysql.connect(host="localhost", user="root", password="", database="magasinbase")
        cur = con.cursor()"""
        try:
            cur.execute("select * from fournisseur")
            rows = cur.fetchall()
            self.fournisseurliste.delete(*self.fournisseurliste.get_children())
            for row in rows:
                self.fournisseurliste.insert("", END, values=row)

        except Exception as ex:
                messagebox.showerror("Erreur", f"Erreur de connexion: {str(ex)} !")

             
    
    def information(self, ev):
        self.ajout_btn.config(state="disabled") #desactiver le bouton ajouter
        self.modifier_btn.config(state="normal") #activer le bouton modifier
        self.supprimer_btn.config(state="normal") #activer le bouton supprimer
        self.ecri_four_id.config(state="readonly") # ID en mode read only
        
        r = self.fournisseurliste.focus()
        contenu = self.fournisseurliste.item(r)

        row = contenu["values"]
        self.var_fourni_id.set(row[0]),
        self.var_nom.set(row[1]),
        self.var_contact.set(row[2]),
        self.ecri_description.delete("1.0", END)
        self.ecri_description.insert("1.0", row[3]), 
        

    def modifier(self):
        con = sqlite3.connect(database=r"D:\Python_projects\gestion_magasin\Donnee\magasinbase.db")
        cur = con.cursor()
        """con = pymysql.connect(host="localhost", user="root", password="", database="magasinbase")
        cur = con.cursor()"""
        try:
            cur.execute("update fournisseur set nom=?, contact=?, description=? where forid=?",
                        (
                        self.var_nom.get(),
                        self.var_contact.get(),
                        self.ecri_description.get("1.0", END),
                        self.var_fourni_id.get(),

                        ))
            con.commit()
            self.affiche_resultat()
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
                cur.execute("delete from fournisseur where forid=?", self.var_fourni_id.get())
                con.commit()
                self.affiche_resultat()
                messagebox.showinfo("Succes", "Suppression Effectue !")
                

        except Exception as ex:
            messagebox.showerror("Erreur", f"Erreur de connexion: {str(ex)} !")
        
        

    def effacer(self):
        self.ecri_four_id.config(state="normal") # mettre id en mode normale
        self.ajout_btn.config(state="normal") #desactiver le bouton ajouter
        self.modifier_btn.config(state="disabled") #activer le bouton modifier
        self.supprimer_btn.config(state="disabled") #activer le bouton supprimer

        self.var_fourni_id.set("")
        self.var_nom.set("")
        self.var_contact.set("")
        self.var_recherche.set("")
        self.ecri_description.delete("1.0", END)

    
    def recherche(self):
        con = sqlite3.connect(database=r"D:\Python_projects\gestion_magasin\Donnee\magasinbase.db")
        cur = con.cursor()
        """con = pymysql.connect(host="localhost", user="root", password="", database="magasinbase")
        cur = con.cursor()"""

        try:
            if self.var_recherche.get()=="":
                messagebox.showerror("Erreur", "Qu'est-ce que vous rechercher ?")
            else:
                cur.execute("select * from fournisseur where forid=?", (self.var_recherche.get(),))
                row = cur.fetchone()
                if row !=None:
                    self.fournisseurliste.delete(*self.fournisseurliste.get_children())
                    self.fournisseurliste.insert("", END, values=row)

                else:
                    messagebox.showerror("Erreur", "Aucun resultat trouve !")

        except Exception as ex:
            messagebox.showerror("Erreur", f"Erreur de connexion: {str(ex)} !")
        

        

        
if __name__=="__main__":
    root = Tk()
    obj = Fournisseur(root)
    root.mainloop()