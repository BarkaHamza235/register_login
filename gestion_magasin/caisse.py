from tkinter import *
from PIL import Image, ImageTk
from tkinter import ttk, messagebox
import time
import os
import pymysql, sqlite3
import tempfile


class Caisse:
    def __init__(self, root):
        self.root = root
        self.root.title("Caisse")
        self.root.geometry("1920x1040+0+0")
        self.root.config(bg="white")
        
        #Cart liste
        self.cart_liste = []
        self.ck_print = 0

        #Title
        self.icon_title = ImageTk.PhotoImage(file=r"D:\Python_projects\gestion_magasin\image\logo.png")

        title = Label(self.root, text="Caisse Magasin ", image=self.icon_title, font=("times new roman",40,"bold"), bg="cyan", fg="black", anchor="w", padx=20, compound=LEFT).place(x=0, y=0, relwidth=1, height=100)

        #Bouton deconnecter
        btn_deconnecter = Button(self.root, command=self.deconnecter, text="Deconnexion", cursor="hand2", font=("times new roman",20,"bold"), bg="orange").place(x=1150, y=20)

        #Heure
        self.heure = Label(self.root, text="Bienvenue chez Hamza Magasin\t\t Date : DD-MM-YYYY\t\t Heure : HH:MM:SS ", font=("times new roman",15), bg="black", fg="white")
        self.heure.place(x=0, y=100, relwidth=1, height=40)
        self.modif_heure()
        
        #Produit Frame
        self.var_nomP = StringVar()

        produit_frame1 = Frame(self.root, bd=4, relief=RIDGE, bg="white")
        produit_frame1.place(x=10, y=150, width=700, height=810)
        
        #produit titre
        p_title = Label(produit_frame1, text="Tous les produits", font=("goudy old style",20,"bold"), bg="cyan", bd=3, relief=RIDGE).pack(side=TOP, fill=X)

        produit_frame2 = Frame(produit_frame1, bd=4, relief=RIDGE, bg="white")
        produit_frame2.place(x=5, y=40, width=680, height=150)
        
        #Rechercher Fournisseur
        recherche = Label(produit_frame2, text="Rechercher Produit | par Nom", font=("goudy old style", 20, "bold"), bg="green", fg="white", bd=3, relief=RIDGE).place(x=2, y=20)
        nomP = Label(produit_frame2, text="Nom Produit", font=("goudy old style", 20, "bold"), bg="white").place(x=2, y=80)
        ecri_nomP = Entry(produit_frame2, textvariable=self.var_nomP, font=("goudy old style", 20, "bold"), bg="lightyellow").place(x=160, y=80, width=180)
        #self.ecri_recherche = Entry(self.root, textvariable=self.var_recherche, font=("times new roman",15), bg="lightyellow")
        #self.ecri_recherche.place(x=950, y=80, height=40)

        #Bouton recherche et tous
        btn_recherche = Button(produit_frame2, command=self.recherche, text="Recherche", font=("times new roman",15, ""), cursor="hand2", bg="green",fg="white").place(x=350, y=80, width=140, height=35)
        tous = Button(produit_frame2, command=self.affiche_resultat, text="Tous", font=("times new roman",15, ""), cursor="hand2", bg="lightgray",fg="black").place(x=500, y=80, width=140, height=35)

        #Liste Produit
        produit_frame3 = Frame(produit_frame1, bd=3, relief=RIDGE)
        produit_frame3.place(x=2, y=200, relwidth=1, height=350)
        
        scroll_y = Scrollbar(produit_frame3, orient=VERTICAL)
        scroll_y.pack(side=RIGHT, fill=Y)

        scroll_x = Scrollbar(produit_frame3, orient=HORIZONTAL)
        scroll_x.pack(side=BOTTOM, fill=X)

        self.produit_table = ttk.Treeview(produit_frame3, columns=("pid", "nom", "prix", "quantite", "status"), yscrollcommand=scroll_y.set, xscrollcommand=scroll_x.set)

        scroll_x.config(command=self.produit_table.xview)
        scroll_y.config(command=self.produit_table.yview)

        self.produit_table.heading("pid", text="ID", anchor="w")
        self.produit_table.heading("nom", text="Nom", anchor="w")
        self.produit_table.heading("prix", text="Prix", anchor="w")
        self.produit_table.heading("quantite", text="Quantite", anchor="w")
        self.produit_table.heading("status", text="Status", anchor="w")
        
        self.produit_table["show"] = "headings" 

        self.produit_table.pack(fill=BOTH, expand=1)

        self.produit_table.bind("<ButtonRelease-1>", self.information)

        self.affiche_resultat()

        #Note
        note = Label(produit_frame1, text="Note : 'Entrer 0 Quantite pour retirer les produits du panier'", anchor="w", font=("times new roman",15), bg="white", fg="red").pack(side=BOTTOM, fill=X)

        #Client Frame
        client_frame = Frame(self.root, bd=4, relief=RIDGE, bg="white")
        client_frame.place(x=730, y=150, width=600, height=90)

        #Client
        self.var_cli_nom = StringVar()
        self.var_cli_contact = StringVar()


        Cli_title = Label(client_frame, text="Details du Client", font=("goudy old style",15,"bold"), bg="gold", bd=3, relief=RIDGE).pack(side=TOP, fill=X)
        
        cli_nom = Label(client_frame, text="Nom", font=("goudy old style",15), bg="white").place(x=15, y=40)
        ecri_cli_nom = Entry(client_frame, textvariable=self.var_cli_nom, font=("goudy old style",15), bg="lightyellow").place(x=80, y=40, width=180)

        cli_contact = Label(client_frame, text="Contact", font=("goudy old style",15), bg="white").place(x=290, y=40)
        ecri_cli_contact = Entry(client_frame, textvariable=self.var_cli_contact, font=("goudy old style",15), bg="lightyellow").place(x=400, y=40, width=180)
        
        #Calculatrice
        self.var_calcul = StringVar()

        calcul_cart_frame = Frame(self.root, bd=4, relief=RIDGE, bg="white")
        calcul_cart_frame.place(x=730, y=250, width=600, height=470)

        calcul_frame = Frame(calcul_cart_frame, bd=4, relief=RIDGE, bg="white")
        calcul_frame.place(x=10, y=10, width=280, height=480)

        self.calcul = Entry(calcul_frame, textvariable=self.var_calcul, font=("arial",15, "bold"), bg="lightyellow", justify=RIGHT, bd=10, relief=GROOVE, state="readonly")
        self.calcul.grid(row=0, columnspan=4)

        #Boutons
        self.btn_7 = Button(calcul_frame, text="7", font=("arial",15, "bold"), bg="gray", cursor="hand2", width=5,  pady=30, command=lambda:self.get_input_cal(7)).grid(row=1, column=0)
        self.btn_8 = Button(calcul_frame, text="8", font=("arial",15, "bold"), bg="gray", cursor="hand2", width=5,  pady=30, command=lambda:self.get_input_cal(8)).grid(row=1, column=1)
        self.btn_9 = Button(calcul_frame, text="9", font=("arial",15, "bold"), bg="gray", cursor="hand2", width=5,  pady=30, command=lambda:self.get_input_cal(9)).grid(row=1, column=2)
        self.btn_plus = Button(calcul_frame, text="+", font=("arial",15, "bold"), bg="gray", cursor="hand2", width=5,  pady=30, command=lambda:self.get_input_cal("+")).grid(row=1, column=3)

        self.btn_4 = Button(calcul_frame, text="4", font=("arial",15, "bold"), bg="gray", cursor="hand2", width=5,  pady=30, command=lambda:self.get_input_cal(4)).grid(row=2, column=0)
        self.btn_5 = Button(calcul_frame, text="5", font=("arial",15, "bold"), bg="gray", cursor="hand2", width=5,  pady=30, command=lambda:self.get_input_cal(5)).grid(row=2, column=1)
        self.btn_6 = Button(calcul_frame, text="6", font=("arial",15, "bold"), bg="gray", cursor="hand2", width=5,  pady=30, command=lambda:self.get_input_cal(6)).grid(row=2, column=2)
        self.btn_mois = Button(calcul_frame, text="-", font=("arial",15, "bold"), bg="gray", cursor="hand2", width=5,  pady=30, command=lambda:self.get_input_cal("-")).grid(row=2, column=3)

        self.btn_1 = Button(calcul_frame, text="1", font=("arial",15, "bold"), bg="gray", cursor="hand2", width=5,  pady=30, command=lambda:self.get_input_cal(1)).grid(row=3, column=0)
        self.btn_2 = Button(calcul_frame, text="2", font=("arial",15, "bold"), bg="gray", cursor="hand2", width=5,  pady=30, command=lambda:self.get_input_cal(2)).grid(row=3, column=1)
        self.btn_3 = Button(calcul_frame, text="3", font=("arial",15, "bold"), bg="gray", cursor="hand2", width=5,  pady=30, command=lambda:self.get_input_cal(3)).grid(row=3, column=2)
        self.btn_fois = Button(calcul_frame, text="*", font=("arial",15, "bold"), bg="gray", cursor="hand2", width=5,  pady=30, command=lambda:self.get_input_cal("*")).grid(row=3, column=3)

        self.btn_0 = Button(calcul_frame, text="0", font=("arial",15, "bold"), bg="gray", cursor="hand2", width=5,  pady=30, command=lambda:self.get_input_cal(0)).grid(row=4, column=0)
        self.btn_clear = Button(calcul_frame, text="c", font=("arial",15, "bold"), bg="gray", cursor="hand2", width=5,  pady=30, command=self.clear_cal).grid(row=4, column=1)
        self.btn_egal = Button(calcul_frame, text="=", font=("arial",15, "bold"), bg="gray", cursor="hand2", width=5,  pady=30, command=self.resultat).grid(row=4, column=2)
        self.btn_div = Button(calcul_frame, text="/", font=("arial",15, "bold"), bg="gray", cursor="hand2", width=5,  pady=30, command=lambda:self.get_input_cal("/")).grid(row=4, column=3)


        panier_cart_frame = Frame(calcul_cart_frame, bd=3, relief=RIDGE)
        panier_cart_frame.place(x=290, y=10, width=300, height=450)

        self.panier_title = Label(panier_cart_frame, text="Produit \t Total du panier  : [0]", font=("goudy old style",15,"bold"), bg="gold", bd=3, relief=RIDGE)
        self.panier_title.pack(side=TOP, fill=X)

        scroll_y = Scrollbar(panier_cart_frame, orient=VERTICAL)
        scroll_y.pack(side=RIGHT, fill=Y)

        scroll_x = Scrollbar(panier_cart_frame, orient=HORIZONTAL)
        scroll_x.pack(side=BOTTOM, fill=X)

        self.cart_table = ttk.Treeview(panier_cart_frame, columns=("pid", "nom", "prix", "quantite", "status"), yscrollcommand=scroll_y.set, xscrollcommand=scroll_x.set)

        scroll_x.config(command=self.cart_table.xview)
        scroll_y.config(command=self.cart_table.yview)

        self.cart_table.heading("pid", text="ID", anchor="w")
        self.cart_table.heading("nom", text="Nom", anchor="w")
        self.cart_table.heading("prix", text="Prix", anchor="w")
        self.cart_table.heading("quantite", text="Quantite", anchor="w")
        self.cart_table.heading("status", text="Status", anchor="w")
        
        self.cart_table["show"] = "headings" 

        self.cart_table.pack(fill=BOTH, expand=1)

        self.cart_table.bind("<ButtonRelease-1>", self.information_cart)


        #Les variables Ajouter bouton cart
        self.var_pid = StringVar()
        self.var_nomProduit = StringVar()
        self.var_prix = StringVar()
        self.var_quantite = StringVar()
        self.var_stock = StringVar()

        btn_frame = Frame(self.root, bd=4, relief=RIDGE, bg="white")
        btn_frame.place(x=20, y=560, width=600, height=150)

        Prod_nom = Label(btn_frame, text="Nom Produit", font=("goudy old style",15), bg="white").place(x=5, y=5)
        ecri_Prod_nom = Entry(btn_frame, textvariable=self.var_nomProduit, font=("goudy old style",17), bg="lightyellow", state="readonly").place(x=5, y=40, width=180, height=30)

        prix = Label(btn_frame, text="Prix Produit", font=("goudy old style",15), bg="white").place(x=205, y=5)
        ecri_prix = Entry(btn_frame, textvariable=self.var_prix, font=("goudy old style",20), bg="lightyellow", state="readonly").place(x=205, y=40, width=180, height=30)
        
        quantite = Label(btn_frame, text="Quantite Produit", font=("goudy old style",15), bg="white").place(x=400, y=5)
        quantite = Entry(btn_frame, textvariable=self.var_quantite, font=("goudy old style",20), bg="lightyellow").place(x=400, y=40, width=180, height=30)
        
        self.stock = Label(btn_frame, text="En Stock", font=("goudy old style",15), bg="white")
        self.stock.place(x=5, y=80)

        btn_clear_cart = Button(btn_frame, command=self.clear_cart, text="Clear", font=("times new roman",20), cursor="hand2", bg="lightgray",fg="black").place(x=180, y=80, width=150)
        btn_miseajour = Button(btn_frame, command=self.ajout_modifier, text="Ajouter | Modifie", font=("times new roman",20), cursor="hand2", bg="orange",fg="black").place(x=360, y=80)
        
        #Facture
        facture_frame = Frame(self.root, bd=4, relief=RIDGE, bg="white")
        facture_frame.place(x=20, y=0, width=550, height=300)

        f_title = Label(facture_frame, text="Zone de Facture Client", font=("goudy old style",20,"bold"), bg="lightblue", bd=3, relief=RIDGE).pack(side=TOP, fill=X)

        scroll_y = Scrollbar(facture_frame, orient=VERTICAL)
        scroll_y.pack(side=RIGHT, fill=Y)

        self.ecri_space_fact = Text(facture_frame, yscrollcommand=scroll_y.set)
        self.ecri_space_fact.pack(fill=BOTH, expand=1)
        scroll_y.config(command=self.ecri_space_fact.yview)

        #boutons
        fact_Menu_frame = Frame(self.root, bd=4, relief=RIDGE, bg="white")
        fact_Menu_frame.place(x=700, y=540, width=550, height=150)

        self.montant = Label(fact_Menu_frame, text="Montant Facture \n [0]", font=("goudy old style",15,"bold"), bg="#3f51b5", fg="white")
        self.montant.place(x=20, y=5, width=150, height=70)

        self.remise = Label(fact_Menu_frame, text="Remise \n [0]", font=("goudy old style",15,"bold"), bg="#8bc34a", fg="white")
        self.remise.place(x=180, y=5, width=150, height=70)

        self.net_payer = Label(fact_Menu_frame, text="Net a Payer \n [0]", font=("goudy old style",15,"bold"), bg="#607d8b", fg="white")
        self.net_payer.place(x=345, y=5, width=185, height=70)

        btn_imprimer = Button(fact_Menu_frame, command=self.imprimer_facture, text="Imprimer", font=("goudy old style",15, "bold"), cursor="hand2", bg="lightgreen").place(x=20, y=80, width=150, height=40)
        btn_effacer = Button(fact_Menu_frame, command=self.clear_all, text="Reinitialiser Tous", font=("goudy old style",15, "bold"), cursor="hand2", bg="lightgray").place(x=180, y=80, width=150, height=40)
        btn_generer = Button(fact_Menu_frame, command=self.generer_facture, text="Generer", font=("goudy old style",15, "bold"), cursor="hand2", bg="yellow").place(x=345, y=80, width=150, height=40)



        #Footer
        label_footer = Label(self.root, text="Develloper par Hamza Barka\t\t\t barkahamza454@gmail.com\t\t\t +221 70 847 03 94\t\tCopyright 2023", font=("times new roman",15,"bold"), bg="black", fg="white").pack(side=BOTTOM, fill=X)


        #Fonctions 
    def get_input_cal(self, num):
        xnum = self.var_calcul.get()+str(num)
        self.var_calcul.set(xnum)

    def clear_cal(self):
        self.var_calcul.set("")
    
    def resultat(self):
        resultat = self.calcul.get()
        self.var_calcul.set(eval(resultat))

    def affiche_resultat(self):
        con = sqlite3.connect(database=r"D:\Python_projects\gestion_magasin\Donnee\magasinbase.db")
        cur = con.cursor()
        """con = pymysql.connect(host="localhost", user="root", password="", database="magasinbase")
        cur = con.cursor()"""
        try:
            cur.execute("select pid, nom, prix, quantite, status from produit where status='Active'")
            rows = cur.fetchall()
            self.produit_table.delete(*self.produit_table.get_children())
            for row in rows:
                self.produit_table.insert("", END, values=row)

        except Exception as ex:
                messagebox.showerror("Erreur", f"Erreur de connexion: {str(ex)} !")
    

    def recherche(self):
        con = sqlite3.connect(database=r"D:\Python_projects\gestion_magasin\Donnee\magasinbase.db")
        cur = con.cursor()
        """con = pymysql.connect(host="localhost", user="root", password="", database="magasinbase")
        cur = con.cursor()"""

        try:
            if self.var_nomP.get()=="":
                messagebox.showerror("Erreur", "Saisir le produit a rechercher ?")
            else:
                cur.execute("select pid, nom, prix, quantite, status from produit where nom  LIKE '%"+self.var_nomP.get()+"%' and status='Active'")
                rows = cur.fetchall()
                if len(rows) !=0:
                    self.produit_table.delete(*self.produit_table.get_children())
                    for row in rows:
                        self.produit_table.insert("", END, values=row)
                else:
                    messagebox.showerror("Erreur", "Aucun resultat trouve !")

        except Exception as ex:
            messagebox.showerror("Erreur", f"Erreur de connexion: {str(ex)} !")


    def information(self, ev):
        r = self.produit_table.focus()
        contenu = self.produit_table.item(r)

        row = contenu["values"]
        self.var_pid.set(row[0]),
        self.var_nomProduit.set(row[1]),
        self.var_prix.set(row[2]),
        self.stock.config(text=f"En Stock : {str(row[3])}")
        self.var_stock.set(row[3]),
        self.var_quantite.set(1),
    
    def information_cart(self, ev):
        r = self.cart_table.focus()
        contenu = self.cart_table.item(r)

        row = contenu["values"]
        self.var_pid.set(row[0]),
        self.var_nomProduit.set(row[1]),
        self.var_prix.set(row[2]),
        self.var_quantite.set(row[3]),
        self.stock.config(text=f"En Stock : {str(row[4])}")
        self.var_stock.set(row[4]),

    def ajout_modifier(self):
        if self.var_pid.get()=="":
            messagebox.showerror("Erreur", "Selectionner Un Produit !")
        elif self.var_quantite.get()=="":
            messagebox.showerror("Erreur", "Donner la quantite !")
        elif int(self.var_quantite.get()) > int(self.var_stock.get()):
            messagebox.showerror("Erreur", "La quantite demandee n'est pas disponible !")
        else:
            prix_cal= self.var_prix.get()
            cart_donnee = [self.var_pid.get(), self.var_nomProduit.get(), self.var_prix.get(), self.var_quantite.get(), self.var_stock.get()]

            present = "non"
            index_ = 0
            for row in self.cart_liste:
                if self.var_pid.get()==row[0]:
                    present = "oui"
                    break
                else:
                    index_ +=1
            if present =="oui":
                ok = messagebox.askyesno("Confirmer", "Le produit est deja present \nTu veux vraiment modifier | supprimer de la liste?")
                if ok == True:
                    if self.var_quantite.get()=="0":
                        self.cart_liste.pop(index_)
                    else:
                        self.cart_liste[index_][3] = self.var_quantite.get()
            else:
                self.cart_liste.append(cart_donnee)
            self.affiche_cart()
            self.facture_modifier()

    def affiche_cart(self):
        try:
            self.cart_table.delete(*self.cart_table.get_children())
            for row in self.cart_liste:
                self.cart_table.insert("", END, values=row)

        except Exception as ex:
                messagebox.showerror("Erreur", f"Erreur de connexion: {str(ex)} !")

    def facture_modifier(self):
        self.montant_facture = 0
        self.net_payer_facture = 0
        self.remise_facture = 0

        for row in self.cart_liste:
            self.montant_facture = self.montant_facture + (float(row[2])*int(row[3]))

        self.remise_facture = (self.montant_facture *5)/100

        self.net_payer_facture = self.montant_facture - self.remise_facture

        self.montant.config(text=f"Montant Facture \n [{str(self.montant_facture)}]")
        self.net_payer.config(text=f"Net a Payer \n [{str(self.net_payer_facture)}]")
        self.remise.config(text=f"Remise \n [{str(self.remise_facture)}]")
        self.panier_title.config(text=f"Produit \t Total du panier : [{str(len(self.cart_liste))}]")
        
    def generer_facture(self):
        if self.var_cli_nom.get()=="":
            messagebox.showerror("Erreur", "Saisir le nom du client ")
        elif len(self.cart_liste)==0:
            messagebox.showerror("Erreur", "Ajouter des produits dans le panier ")
        else:
            self.header_facture()
            self.body_facture()
            self.footer_facture()
            fp = open(fr"D:\Python_projects\gestion_magasin\facture\{str(self.facture)}.txt","w")
            fp.write(self.ecri_space_fact.get("1.0", END))
            fp.close
            messagebox.showinfo("Sauvegarder", "Enregistrement/Generer Effectue avec succes !")
            self.ck_print = 1

    def header_facture(self):
        self.facture = int(time.strftime("%H%M%S"))+int(time.strftime("%d%m%Y"))
        facture_entete = f'''
\t\t\tMagasin Hamza Barka 
\tTel:  +221 70 847 03 94 Adresse : Liberte 5 Dakar 
{str("="*57)}
Nom du Client : {self.var_cli_nom.get()}
Tel du Client : {self.var_cli_contact.get()}
Numero Facture : {str(self.facture)}\t\tDate : {str(time.strftime("%d%m%Y"))}
{str("="*57)}
Nom Produit\t\t\t\tQuantite\t\tPrix
{str("="*57)}
        '''
        self.ecri_space_fact.delete("1.0", END)
        self.ecri_space_fact.insert("1.0", facture_entete)




    def body_facture(self):
        con = sqlite3.connect(database=r"D:\Python_projects\gestion_magasin\Donnee\magasinbase.db")
        cur = con.cursor()
        """con = pymysql.connect(host="localhost", user="root", password="", database="magasinbase")
        cur = con.cursor()"""
        try:
            for row in self.cart_liste:
                pid = row[0]
                nom = row[1]
                quantite = int(row[4])-int(row[3])
                if int(row[3])==int(row[4]):
                    status = "Inactive"
                if int(row[3])!=int(row[4]):
                    status = "Active"
                
                prix = float(row[2])*float(row[3])
                prix = str(prix)
                
                self.ecri_space_fact.insert(END, "\n\t"+nom+"\t\t\t"+row[3]+"\t\t"+prix)

                cur.execute("update produit set  quantite=?, status=? where pid=?", (
                    quantite,
                    status,
                    pid
                ))
                con.commit()
            con.close()
            self.affiche_resultat()

        except Exception as ex:
                messagebox.showerror("Erreur", f"Erreur de connexion: {str(ex)} !")

    
    def footer_facture(self):
        facture_pied = f'''
{str("="*57)}
Montant Facture :\t\t\t\t {self.montant_facture}
Remise :\t\t\t\t {self.remise_facture}
Net a Payer :\t\t\t\t {self.net_payer_facture}
{str("="*57)}
'''     
        self.ecri_space_fact.insert(END, facture_pied)
        

    def clear_cart(self):
        self.var_pid.set("")
        self.var_nomProduit.set("")
        self.var_prix.set("")
        self.var_quantite.set("")
        self.stock.config(text="En Stock")
        self.var_stock.set("")

    def clear_all(self):
        del self.cart_liste[:]
        self.var_cli_nom.set("")
        self.var_cli_contact.set("")
        self.ecri_space_fact.delete("1.0", END)
        self.panier_title.config(text="Produit \t Total du panier  : [0]")
        self.var_nomP.set("")
        self.ck_print = 0
        self.clear_cart()
        self.affiche_resultat()
        self.affiche_cart()
        

    def imprimer_facture(self):
        if self.ck_print == 1:
            messagebox.showinfo("Imprimer", "Veuillez Pacienter Padant l'Impression !")
            fichier = tempfile.mktemp(".txt")
            open(fichier, "w").write(self.ecri_space_fact.get("1.0", END))
            os.startfile(fichier, "print")
        else:
            messagebox.showerror("Erreur","Veuillez Generer la Facture !")
    
    def modif_heure(self):
        heure_ = (time.strftime("%H:%M:%S"))
        date_ = (time.strftime("%d-%m-%Y"))
        self.heure.config(text=f"Bienvenue chez Hamza Magasin\t\t Date : {str(date_)}\t\t Heure : {str(heure_)} ")
        self.heure.after(200, self.modif_heure)


    def deconnecter(self):
        self.root.destroy()
        self.obj = os.system("python D:\Python_projects\gestion_magasin\login.py")
        
        


if __name__=="__main__":
    root = Tk()
    obj = Caisse(root)
    root.mainloop()