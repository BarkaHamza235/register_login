from tkinter import *
from PIL import Image, ImageTk
from tkinter import messagebox, ttk 
import time
import os
import pymysql
import sqlite3


class Employe:
    def __init__(self, root):
        self.root = root
        self.root.title("Employe")
        self.root.geometry("1920x1040+0+0")
        self.root.config(bg="white")
        self.root.focus_force()
        
        #Date base avec sqlite3
        con = sqlite3.connect(database=r"D:\Python_projects\gestion_magasin\Donnee\magasinbase.db")
        cur = con.cursor()
        """con = pymysql.connect(host="localhost", user="root", password="", database="magasinbase")
        cur = con.cursor()"""
        cur.execute("CREATE TABLE IF NOT EXISTS employe (eid text PRIMARY KEY, nom text, email text, sexe text, contact text, naissance text, adhesion text, password text, type text, adresse text, salaire text)")
        con.commit()


        #Les variables
        self.var_reche_Option = StringVar()
        self.var_ecri_recherche = StringVar()
        self.var_emp_id = StringVar()
        self.var_sexe = StringVar()
        self.var_contact = StringVar()
        self.var_nom = StringVar()
        self.var_naissance = StringVar()
        self.var_adhesion = StringVar()
        self.var_email = StringVar()
        self.var_password = StringVar()
        self.var_type = StringVar()
        self.var_salaire = StringVar()
        
        #Rechercher Employe
        reche_Frame = LabelFrame(self.root, text="Rechercher Employe", font=("goudy old style", 20), bd=2, relief=RIDGE, bg="white")
        reche_Frame.place(x=400, y=20, width=750, height=90)

        #option de recherche
        reche_Option = ttk.Combobox(reche_Frame, textvariable=self.var_reche_Option, values=("nom","email","contact"), font=("times new roman",20), state="r", justify=CENTER)
        reche_Option.current(0)
        reche_Option.place(x=10, y=10, width=200)
        
        ecri_recherche = Entry(reche_Frame, textvariable=self.var_ecri_recherche, font=("times new roman",20), bg="lightyellow")
        ecri_recherche.place(x=235, y=10, width=200)

        #Bouton recherche et tous
        btn_recherche = Button(reche_Frame, command=self.recherche, text="Recherche", font=("times new roman",20), cursor="hand2", bg="blue",fg="white").place(x=450, y=5, height=40)
        btn_tous = Button(reche_Frame, command=self.affiche_resultat, text="Tous", font=("times new roman",20), cursor="hand2", bg="lightgray").place(x=600, y=5, height=40)

        #Title 
        title = Label(self.root, text="Formulaire Employe", font=("times new roman",20,"bold"), bg="cyan", fg="black").place(x=0, y=150, width=1499)

        #Contenu formulaire
        #ligne 1
        emp_id = Label(self.root, text="ID Employe", font=("goudy old style",20), bg="white").place(x=50, y=220, width=200)
        sexe = Label(self.root, text="Sexe", font=("goudy old style",20), bg="white").place(x=500, y=220, width=200)
        contact = Label(self.root, text="Contact", font=("goudy old style",20,), bg="white").place(x=900, y=220, width=200)
        
        self.ecri_emp_id = Entry(self.root, textvariable=self.var_emp_id, font=("goudy old style",20), bg="lightyellow")
        self.ecri_emp_id.place(x=250, y=220, width=250)
        ecri_sexe = ttk.Combobox(self.root, textvariable=self.var_sexe, values=("Homme","Femme"),  font=("goudy old style",20,), state="r", justify=CENTER)
        ecri_sexe.current(0)
        ecri_sexe.place(x=680, y=220, width=250)
        ecri_contact = Entry(self.root, textvariable=self.var_contact, font=("goudy old style",20), bg="lightyellow")
        ecri_contact.place(x=1100, y=220, width=250)

        #ligne 2
        nom = Label(self.root, text="Nom", font=("goudy old style",20), bg="white").place(x=50, y=290, width=200)
        date_naiss = Label(self.root, text="Date Naissance", font=("goudy old style",20), bg="white").place(x=500, y=290, width=200)
        adhesion = Label(self.root, text="Date Adhesion", font=("goudy old style",20), bg="white").place(x=910, y=290, width=200)
        
        ecri_nom = Entry(self.root, textvariable=self.var_nom, font=("goudy old style",20), bg="lightyellow").place(x=250, y=290, width=250)
        ecri_date_naiss = Entry(self.root, textvariable=self.var_naissance, font=("goudy old style",20), bg="lightyellow").place(x=680, y=290, width=250)
        ecri_adhesion = Entry(self.root, textvariable=self.var_adhesion, font=("goudy old style",20), bg="lightyellow").place(x=1100, y=290, width=250)

        #ligne 3
        email = Label(self.root, text="E-mail", font=("goudy old style",20), bg="white").place(x=50, y=360, width=200)
        password = Label(self.root, text="Password", font=("goudy old style",20), bg="white").place(x=500, y=360, width=200)
        type = Label(self.root, text="Type", font=("goudy old style",20), bg="white").place(x=910, y=360, width=200)
        
        ecri_email = Entry(self.root, textvariable=self.var_email, font=("goudy old style",20), bg="lightyellow").place(x=250, y=360, width=250)
        ecri_password = Entry(self.root, textvariable=self.var_password, show="*", font=("goudy old style",20), bg="lightyellow").place(x=680, y=360, width=250)
        ecri_type = ttk.Combobox(self.root, textvariable=self.var_type, values=("Admin","Employe"),  font=("goudy old style",20), state="r", justify=CENTER)
        ecri_type.current(0)
        ecri_type.place(x=1100, y=360, width=250)

        #ligne 4
        adresse = Label(self.root, text="Adresse", font=("goudy old style",20), bg="white").place(x=50, y=430, width=200)
        salaire = Label(self.root, text="Salaire", font=("goudy old style",20), bg="white").place(x=500, y=430, width=200)
        
        self.ecri_adresse = Text(self.root, font=("goudy old style",20), bg="lightyellow")
        self.ecri_adresse.place(x=250, y=430, width=250, height=115)
        ecri_salaire = Entry(self.root, textvariable=self.var_salaire, font=("goudy old style",20), bg="lightyellow").place(x=680, y=430, width=250)

        #Boutons
        self.ajout_btn = Button(self.root, command=self.ajout_employe, state="normal", text="Ajouter", cursor="hand2", font=("times new roman",20,"bold"), bg="green")
        self.ajout_btn.place(x=570, y=500, height=40)
        self.modifier_btn = Button(self.root, command=self.modifier, text="Modifier", state="disabled", cursor="hand2", font=("times new roman",20,"bold"), bg="yellow")
        self.modifier_btn.place(x=750, y=500, height=40)
        self.supprimer_btn = Button(self.root, command=self.supprimer, text="Supprimer", state="disabled", cursor="hand2", font=("times new roman",20,"bold"), bg="red")
        self.supprimer_btn.place(x=930, y=500, height=40)
        effacer_btn = Button(self.root, command=self.effacer, text="Effacer", cursor="hand2", font=("times new roman",20,"bold"), bg="lightgray").place(x=1110, y=500, height=40)

        #Liste Employe
        liste_Frame = Frame(self.root, bd=3, relief=RIDGE)
        liste_Frame.place(x=0, y=550, relwidth=1, height=225)
        
        scroll_y = Scrollbar(liste_Frame, orient=VERTICAL)
        scroll_y.pack(side=RIGHT, fill=Y)

        scroll_x = Scrollbar(liste_Frame, orient=HORIZONTAL)
        scroll_x.pack(side=BOTTOM, fill=X)

        self.employeliste = ttk.Treeview(liste_Frame, columns=("eid", "nom", "email", "sexe", "contact", "naissance", "adhesion","password", "type", "adresse", "salaire"), yscrollcommand=scroll_y.set, xscrollcommand=scroll_x.set)

        scroll_x.config(command=self.employeliste.xview)
        scroll_y.config(command=self.employeliste.yview)

        self.employeliste.heading("eid", text="ID")
        self.employeliste.heading("nom", text="Nom")
        self.employeliste.heading("email", text="E-mail")
        self.employeliste.heading("sexe", text="Sexe")
        self.employeliste.heading("contact", text="Contact")
        self.employeliste.heading("naissance", text="Date Naissance")
        self.employeliste.heading("adhesion", text="Date Adhesion")
        self.employeliste.heading("password", text="Password")
        self.employeliste.heading("type", text="Type")
        self.employeliste.heading("adresse", text="Adresse")
        self.employeliste.heading("salaire", text="Salaire")

        self.employeliste["show"] = "headings" 
        self.employeliste.bind("<ButtonRelease-1>", self.information)

        self.employeliste.pack(fill=BOTH, expand=1)

        self.affiche_resultat()

        #Les fonctions
    def ajout_employe(self):
        con = sqlite3.connect(database=r"D:\Python_projects\gestion_magasin\Donnee\magasinbase.db")
        cur = con.cursor()
        """con = pymysql.connect(host="localhost", user="root", password="", database="magasinbase")
        cur = con.cursor()"""

        try:
            if self.var_emp_id.get() =="" or self.var_password.get() =="" or self.var_type.get() =="":
                messagebox.showerror("Erreur", "Veuillez mettre un ID password et type  !")
            else:
                cur.execute("select * from employe where eid=?", (self.var_emp_id.get(),))
                row = cur.fetchone()
                if row != None: 
                    messagebox.showerror("Erreur","L'ID employe existe deja !")
                else:
                    cur.execute("insert into employe (eid, nom, email, sexe, contact, naissance, adhesion, password, type, adresse, salaire) values(?,?,?,?,?,?,?,?,?,?,?)", (
                        self.var_emp_id.get(),
                        self.var_nom.get(),
                        self.var_email.get(),
                        self.var_sexe.get(),
                        self.var_contact.get(),
                        self.var_naissance.get(),
                        self.var_adhesion.get(),
                        self.var_password.get(),
                        self.var_type.get(),
                        self.ecri_adresse.get("1.0", END),
                        self.var_salaire.get()
                    ))
                    con.commit()
                    self.affiche_resultat()
                    self.effacer()
                    messagebox.showinfo("Succes", "Ajout Effectue avec succes !")

        except Exception as ex:
                messagebox.showerror("Erreur", f"Erreur de connexion: {str(ex)} !")

    def affiche_resultat(self):
        con = sqlite3.connect(database=r"D:\Python_projects\gestion_magasin\Donnee\magasinbase.db")
        cur = con.cursor()
        """con = pymysql.connect(host="localhost", user="root", password="", database="magasinbase")
        cur = con.cursor()"""
        try:
            cur.execute("select * from employe")
            rows = cur.fetchall()
            self.employeliste.delete(*self.employeliste.get_children())
            for row in rows:
                self.employeliste.insert("", END, values=row)

        except Exception as ex:
                messagebox.showerror("Erreur", f"Erreur de connexion: {str(ex)} !")

             
    
    def information(self, ev):
        self.ajout_btn.config(state="disabled") #desactiver le bouton ajouter
        self.modifier_btn.config(state="normal") #activer le bouton modifier
        self.supprimer_btn.config(state="normal") #activer le bouton supprimer
        self.ecri_emp_id.config(state="readonly") # ID en mode read only

        r = self.employeliste.focus()
        contenu = self.employeliste.item(r)

        row = contenu["values"]
        self.var_emp_id.set(row[0]),
        self.var_nom.set(row[1]),
        self.var_email.set(row[2]),
        self.var_sexe.set(row[3]),
        self.var_contact.set(row[4]),
        self.var_naissance.set(row[5]),
        self.var_adhesion.set(row[6]),
        self.var_password.set(row[7]),
        self.var_type.set(row[8]),
        self.ecri_adresse.delete("1.0", END),
        self.ecri_adresse.insert(END, row[9]),
        self.var_salaire.set(row[10])


    def modifier(self):
        con = sqlite3.connect(database=r"D:\Python_projects\gestion_magasin\Donnee\magasinbase.db")
        cur = con.cursor()
        """con = pymysql.connect(host="localhost", user="root", password="", database="magasinbase")
        cur = con.cursor()"""
        try:
            cur.execute("update employe set nom=?, email=?, sexe=?, contact=?, naissance=?, adhesion=?, password=?, type=?, adresse=?, salaire=? where eid=?",
                        (
                        self.var_nom.get(),
                        self.var_email.get(),
                        self.var_sexe.get(),
                        self.var_contact.get(),
                        self.var_naissance.get(),
                        self.var_adhesion.get(),
                        self.var_password.get(),
                        self.var_type.get(),
                        self.ecri_adresse.get("1.0", END),
                        self.var_salaire.get(),
                        self.var_emp_id.get()
                        ))
            con.commit()
            self.affiche_resultat()
            self.effacer()

            messagebox.showinfo("Succes", "Modification Effectue avec succes !")
            
           
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
                cur.execute("delete from employe where eid=?", self.var_emp_id.get())
                con.commit()
                self.affiche_resultat()
                self.effacer()
                messagebox.showinfo("Succes", "Suppression Effectue !")



        except Exception as ex:
            messagebox.showerror("Erreur", f"Erreur de connexion: {str(ex)} !")
        
        

    def effacer(self):
        self.ecri_emp_id.config(state="normal")
        self.ajout_btn.config(state="normal") #desactiver le bouton ajouter
        self.modifier_btn.config(state="disabled") #activer le bouton modifier
        self.supprimer_btn.config(state="disabled") #activer le bouton supprimer
        
        self.var_nom.set(""),
        self.var_email.set(""),
        self.var_sexe.set("Homme"),
        self.var_contact.set(""),
        self.var_naissance.set(""),
        self.var_adhesion.set(""),
        self.var_password.set(""),
        self.var_type.set("Admin"),
        self.ecri_adresse.delete("1.0", END),
        self.var_salaire.set(""),
        self.var_emp_id.set("")
        self.var_ecri_recherche.set("")
        self.var_reche_Option.set("nom")
    
    def recherche(self):
        con = sqlite3.connect(database=r"D:\Python_projects\gestion_magasin\Donnee\magasinbase.db")
        cur = con.cursor()
        """con = pymysql.connect(host="localhost", user="root", password="", database="magasinbase")
        cur = con.cursor()"""

        try:
            if self.var_ecri_recherche.get()=="":
                messagebox.showerror("Erreur", "Veuillez saisir dans le champ recherche !")
            else:
                cur.execute("select * from employe where "+self.var_reche_Option.get()+" LIKE '%"+self.var_ecri_recherche.get()+"%'")
                rows = cur.fetchall()
                if len(rows) !=0:
                    self.employeliste.delete(*self.employeliste.get_children())
                    for row in rows:
                        self.employeliste.insert("", END, values=row)
                else:
                    messagebox.showerror("Erreur", "Aucun resultat trouve !")

        except Exception as ex:
            messagebox.showerror("Erreur", f"Erreur de connexion: {str(ex)} !")
        


        

   

if __name__=="__main__":
    root = Tk()
    obj = Employe(root)
    root.mainloop()