from tkinter import *
from tkinter import ttk, messagebox
import pymysql
from pymysql import cursors

class Etudiant:
    def __init__(self, root):
        self.root = root
        self.root.title("Inscription")
        self.root.geometry("1930x1080+0+0")

        #Champts du formulaire
        gestion_frame = Frame(self.root, bd=5, relief=GROOVE, bg="cyan")
        gestion_frame.place(x=30, y=50, width=600, height=700)

        #Title
        title = Label(gestion_frame, text="Information de l'etudiant", font=("times new roman",30,"bold"), bg="cyan").place(x=50, y=50)

        #Id
        idEtudiant = Label(gestion_frame, text="ID Etudiant", font=("times new roman",20,"bold"), bg="cyan").place(x=50, y=150)
        self.ecri_idEtudiant = Entry(gestion_frame, font=("times new roman",20), bg="lightgrey")
        self.ecri_idEtudiant.place(x=220, y=150)

        #Nom complet
        nomComplet = Label(gestion_frame, text="Nom complet", font=("times new roman",20,"bold"), bg="cyan").place(x=50, y=210)
        self.ecri_nomComplet = Entry(gestion_frame, font=("times new roman",20), bg="lightgrey")
        self.ecri_nomComplet.place(x=220, y=210)

        #E-mail
        email = Label(gestion_frame, text="E-mail", font=("times new roman",20,"bold"), bg="cyan").place(x=50, y=260)
        self.ecri_email = Entry(gestion_frame, font=("times new roman",20), bg="lightgrey")
        self.ecri_email.place(x=220, y=260)

        #Sexe
        sexe = Label(gestion_frame, text="Sexe", font=("times new roman",20,"bold"), bg="cyan").place(x=50, y=310)
        self.ecri_sexe = ttk.Combobox(gestion_frame, font=("times new roman",20), state="readonly")
        self.ecri_sexe["values"] = ("Homme", "Femme")
        self.ecri_sexe.place(x=220, y=310, width=285)
        self.ecri_sexe.current(0)

        #Contact
        contact = Label(gestion_frame, text="Contact", font=("times new roman",20,"bold"), bg="cyan").place(x=50, y=360)
        self.ecri_contact = Entry(gestion_frame, font=("times new roman",20), bg="lightgrey")
        self.ecri_contact.place(x=220, y=360)

        #Date naissance
        date = Label(gestion_frame, text="Date Naissance", font=("times new roman",20,"bold"), bg="cyan").place(x=50, y=410)
        self.ecri_date = Entry(gestion_frame, font=("times new roman",20), bg="lightgrey")
        self.ecri_date.place(x=220, y=410)

        #Adresse
        adresse = Label(gestion_frame, text="Adresse", font=("times new roman",20,"bold"), bg="cyan").place(x=50, y=460)
        self.ecri_adresse = Text(gestion_frame, font=("times new roman",15))
        self.ecri_adresse.place(x=220, y=460, width=285, height=60)
        
        #Bouton ajouter
        ajouter_btn = Button(gestion_frame, text="Ajouter", command=self.ajout_etudiant, cursor="hand2", font=("times new roman",15,"bold"), relief=GROOVE, bd=10, bg="green").place(x=10, y=570, width=120)

        #Bouton modifier
        modifier_btn = Button(gestion_frame, text="Modifier", command=self.modifier, cursor="hand2", font=("times new roman",15,"bold"), relief=GROOVE, bd=10, bg="yellow").place(x=150, y=570, width=120)

        #Bouton supprimer
        supprimer_btn = Button(gestion_frame, text="Supprimer", command=self.supprimer, cursor="hand2", font=("times new roman",15,"bold"), relief=GROOVE, bd=10, bg="red").place(x=300, y=570, width=120)

        #Bouton effacer
        effacer_btn = Button(gestion_frame, text="Effacer", command=self.effacer, cursor="hand2", font=("times new roman",15,"bold"), relief=GROOVE, bd=10, bg="grey").place(x=450, y=570, width=120)


        #Recherche
        details_frame = Frame(self.root, bd=5, relief=GROOVE, bg="cyan")
        details_frame.place(x=660, y=50, width=1100, height=700)
        
        type_rech = Label(details_frame, text="Recherche par", font=("times new roman",20,"bold"), bg="cyan").place(x=10, y=50)
        self.ecri_type_rech = ttk.Combobox(details_frame, font=("times new roman",20), state="readonly")
        self.ecri_type_rech["values"] = ("id", "nom", "contact")
        self.ecri_type_rech.place(x=190, y=55, width=70, height=35)
        self.ecri_type_rech.current(0)

        self.ecri_recherche = Entry(details_frame, font=("times new roman", 20), bd=5, relief=GROOVE)
        self.ecri_recherche.place(x=270, y=55, width=150, height=35)

        #Boutons Recherche et Afficher
        recherche_btn = Button(details_frame, text="Rechercher", command=self.recherche_info, cursor="hand2", font=("times new roman",15,"bold"), relief=GROOVE, bd=10, bg="grey", fg="white").place(x=430, y=55, width=120, height=35)
        afficher_btn = Button(details_frame, text="Afficher", command=self.affiche_resultat, cursor="hand2", font=("times new roman",15,"bold"), relief=GROOVE, bd=10, bg="grey", fg="white").place(x=570, y=55, width=120, height=35)

        #Affichage
        resultat_frame = Frame(details_frame, bd=5, relief=GROOVE, bg="cyan")
        resultat_frame.place(x=10, y=110, width=1070, height=570)

        scroll_x = Scrollbar(resultat_frame, orient=HORIZONTAL)
        scroll_y = Scrollbar(resultat_frame, orient=VERTICAL)
        self.tab_resultat = ttk.Treeview(resultat_frame, columns=("id", "nom","email", "sexe", "contact", "date", "adresse"), xscrollcommand=scroll_x.set, yscrollcommand=scroll_y.set)

        scroll_x.pack(side=BOTTOM, fill=X)
        scroll_y.pack(side=RIGHT, fill=Y)

        self.tab_resultat.heading("id", text="ID Etudiant")
        self.tab_resultat.heading("nom", text="Nom Complet")
        self.tab_resultat.heading("email", text="E-mail")
        self.tab_resultat.heading("sexe", text="Sexe")
        self.tab_resultat.heading("contact", text="contact")
        self.tab_resultat.heading("date", text="date")
        self.tab_resultat.heading("adresse", text="adresse")

        self.tab_resultat["show"] = "headings"

        self.tab_resultat.column("id", width=100)
        self.tab_resultat.column("nom", width=150)
        self.tab_resultat.column("email", width=150)
        self.tab_resultat.column("sexe", width=150)
        self.tab_resultat.column("contact", width=150)
        self.tab_resultat.column("date", width=150)
        self.tab_resultat.column("adresse", width=200)

        self.tab_resultat.pack()
        self.tab_resultat.bind("<ButtonRelease-1>", self.information)

        self.affiche_resultat()


    def ajout_etudiant(self):
        if self.ecri_idEtudiant.get()=="" or self.ecri_nomComplet.get()=="" or self.ecri_email.get()=="":
            messagebox.showerror("Erreur","Vous n'avez pas rempli les champs obligatoires !", parent=self.root)
        else:
            con = pymysql.connect(host="localhost", user="root", password="", database="creer")
            cur = con.cursor()
            cur.execute("insert into etudiant_inscrit VALUES(%s, %s, %s, %s, %s, %s, %s)",
                        (
                            self.ecri_idEtudiant.get(),
                            self.ecri_nomComplet.get(),
                            self.ecri_email.get(), 
                            self.ecri_sexe.get(), 
                            self.ecri_contact.get(), 
                            self.ecri_date.get(),
                            self.ecri_adresse.get("1.0", END)
                        ))
                               
            con.commit()
            self.affiche_resultat()
            self.effacer()
            con.close()
            messagebox.showinfo("Succes", "Enregistrement Effectue !", parent=self.root)

                    
    def affiche_resultat(self):
        con = pymysql.connect(host="localhost", user="root", password="", database="creer")
        cur = con.cursor()
        cur.execute("select * from etudiant_inscrit")
        rows = cur.fetchall()
        if len(rows) != 0:
            self.tab_resultat.delete(*self.tab_resultat.get_children())
            for row in rows:
                self.tab_resultat.insert("", END, values=row)
        con.commit()
        con.close()       

    def effacer(self):
        self.ecri_idEtudiant.delete(0, END),
        self.ecri_nomComplet.delete(0, END),
        self.ecri_email.delete(0, END),
        self.ecri_sexe.delete(0, END),
        self.ecri_contact.delete(0, END),
        self.ecri_date.delete(0, END),
        self.ecri_adresse.delete("1.0", END)     
        

    def information(self, ev):
        cursors_row = self.tab_resultat.focus()
        contents = self.tab_resultat.item(cursors_row)   

        row = contents["values"]
        self.ecri_idEtudiant.insert(END, row[0]),
        self.ecri_nomComplet.insert(END, row[1]),
        self.ecri_email.insert(END, row[2]),
        self.ecri_sexe.insert(END, row[3]),
        self.ecri_contact.insert(END, row[4]),
        self.ecri_date.insert(END, row[5]),
        self.ecri_adresse.delete("1.0", END)
        self.ecri_adresse.insert(END, row[6])



    def modifier(self):
        con = pymysql.connect(host="localhost", user="root", password="", database="creer")
        cur = con.cursor()
        cur.execute("update etudiant_inscrit set nom=%s, email=%s, sexe=%s, contact=%s, date=%s, adresse=%s where id=%s",
                        (
                            self.ecri_nomComplet.get(),
                            self.ecri_email.get(), 
                            self.ecri_sexe.get(), 
                            self.ecri_contact.get(), 
                            self.ecri_date.get(),
                            self.ecri_adresse.get("1.0", END),
                            self.ecri_idEtudiant.get()
                        ))
        con.commit()
        self.affiche_resultat()
        self.effacer()
        con.close()
        messagebox.showinfo("Succes", "Modification Effectue !", parent=self.root)



    def supprimer(self):
        con = pymysql.connect(host="localhost", user="root", password="", database="creer")
        cur = con.cursor()
        cur.execute("delete from etudiant_inscrit where id=%s", self.ecri_idEtudiant.get())
        con.commit()
        self.affiche_resultat()
        self.effacer()
        con.close()
        messagebox.showinfo("Succes", "Suppression Effectue !", parent=self.root)


    def recherche_info(self):
        con = pymysql.connect(host="localhost", user="root", password="", database="creer")
        cur = con.cursor()
        cur.execute("select * from etudiant_inscrit where "+str(self.ecri_type_rech.get())+" LIKE '%"+str(self.ecri_recherche.get())+"%'")
        rows = cur.fetchall()
        if len(rows) != 0:
            self.tab_resultat.delete(*self.tab_resultat.get_children())
            for row in rows:
                self.tab_resultat.insert('', END, values=row)
        con.commit()
        con.close()   

            




root = Tk()
obj = Etudiant(root)
root.mainloop()