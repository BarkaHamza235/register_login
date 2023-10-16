from tkinter import *
from tkinter import ttk, messagebox
import pymysql
import os

class Formulaire:
    def __init__(self, root):
        self.root = root
        self.root.title("Formulaire")
        self.root.geometry("1920x1080+0+0")

        #Champts du formulaire
        frame1 = Frame(self.root, bg="grey")
        frame1.place(x=500, y=200, width=700, height=500)

        #Title
        title = Label(frame1, text="Creer un compte", font=("algerian",20,"bold"), bg="grey", fg="orange").place(x=50, y=30)
        #Prenom
        prenom = Label(frame1, text="Prenom", font=("times new roman",15,"bold"), bg="grey", fg="black").place(x=50, y=100)
        self.ecri_prenom = Entry(frame1, font=("times new roman",15), bg="lightgrey")
        self.ecri_prenom.place(x=50, y=130, width=250)

        #Nom
        nom = Label(frame1, text="Nom", font=("times new roman",15,"bold"), bg="grey", fg="black").place(x=370, y=100)
        self.ecri_nom = Entry(frame1, font=("times new roman",15), bg="lightgrey")
        self.ecri_nom.place(x=370, y=130, width=250)

        #Telephone
        prenom = Label(frame1, text="Telephone", font=("times new roman",15,"bold"), bg="grey", fg="black").place(x=50, y=160)
        self.ecri_telephone = Entry(frame1, font=("times new roman",15), bg="lightgrey")
        self.ecri_telephone.place(x=50, y=190, width=250)

        #Email
        email = Label(frame1, text="Email", font=("times new roman",15,"bold"), bg="grey", fg="black").place(x=370, y=160)
        self.ecri_email = Entry(frame1, font=("times new roman",15), bg="lightgrey")
        self.ecri_email.place(x=370, y=190, width=250)
        
        #Question
        question = Label(frame1, text="Selectionnez une Question", font=("times new roman",15,"bold"), bg="grey", fg="black").place(x=50, y=220)
        self.ecri_question = ttk.Combobox(frame1, font=("times new roman", 15), state="readonly")
        self.ecri_question["values"] = ("Select", "Ton surnom", "Lieu de naissance", "Meilleur ami", "Film prefere")
        self.ecri_question.place(x=50, y=250, width=250)
        self.ecri_question.current(0)

        #Reponse
        reponse = Label(frame1, text="Repondre", font=("times new roman",15,"bold"), bg="grey", fg="black").place(x=370, y=220)
        self.ecri_reponse = Entry(frame1, font=("times new roman",15), bg="lightgrey")
        self.ecri_reponse.place(x=370, y=250, width=250)

         #Password
        password = Label(frame1, text="Password", font=("arial",15,"bold"), bg="grey", fg="black").place(x=50, y=280)
        self.ecri_password = Entry(frame1, font=("times new roman",15), show="*", bg="lightgrey")
        self.ecri_password.place(x=50, y=310, width=250)

        #Confirm password
        confirmpassword = Label(frame1, text="Confirme password", font=("times new roman",15,"bold"), bg="grey", fg="black").place(x=370, y=280)
        self.ecri_confirmpassword = Entry(frame1, font=("times new roman",15), show="*", bg="lightgrey")
        self.ecri_confirmpassword.place(x=370, y=310, width=250)
        
        # les termes et conditions
        self.var_chek = IntVar()
        chk = Checkbutton(frame1, variable=self.var_chek, onvalue=1, offvalue=0, text="J'accepte les termes et conditions", cursor="hand2", font=("times new roman",12), bg="grey").place(x=50, y=370)

        # Les boutons de validation et connexion
        btn1 = Button(frame1, text="Creer", command=self.creer, cursor="hand2", font=("times new roman",15,"bold"), bg="cyan", fg="black").place(x=250, y=430, width=250)
        btn2 = Button(frame1, text="Connexion", command=self.page_connexion, cursor="hand2", font=("times new roman",15,"bold"), bg="cyan", fg="black").place(x=550, y=50, width=150)


    def creer(self):
        if self.ecri_prenom.get()=="" or self.ecri_nom.get()=="" or self.ecri_email.get()=="" or self.ecri_question.get()=="" or self.ecri_reponse.get()=="" or self.ecri_password.get()=="" or self.ecri_confirmpassword.get()=="":
            messagebox.showerror("Erreur","Tous les champs sont obligatoirs !", parent=self.root)
        elif self.ecri_password.get()!=self.ecri_confirmpassword.get():
            messagebox.showerror("Erreur","Les deux mots de passe ne sont pas coformes !", parent=self.root)
        elif self.var_chek.get()==0:
            messagebox.showerror("Erreur","Veuillez accepter les termes et conditions !", parent=self.root)
        else:
            try:
                con = pymysql.connect(host="localhost", user="root", password="", database="creer")
                cur = con.cursor()
                cur.execute("select * from compte where email = %s", self.ecri_email.get())
                row = cur.fetchone()
                if row != None: 
                    messagebox.showerror("Erreur","Ce email existe deja !", parent=self.root)
                else:
                    cur.execute("insert into compte(prenom, nom, telephone, email, question, reponse, password) VALUES(%s, %s, %s, %s, %s, %s, %s)",
                        (
                            self.ecri_prenom.get(),
                            self.ecri_nom.get(),
                            self.ecri_telephone.get(), 
                            self.ecri_email.get(),
                            self.ecri_question.get(), 
                            self.ecri_reponse.get(), 
                            self.ecri_password.get()
                        ))
                    messagebox.showinfo("Succes", f"Votre compte a ete cree !", parent=self.root)
                con.commit()
                self.reini()
                con.close()
            except Exception as ex:
                messagebox.showerror("Erreur", f"Erreur de connexion: {str(ex)} !", parent=self.root)

    def reini(self):
        self.ecri_prenom.delete(0, END),
        self.ecri_nom.delete(0, END),
        self.ecri_telephone.delete(0, END),
        self.ecri_email.delete(0, END),
        self.ecri_question.delete(0, END),
        self.ecri_reponse.delete(0, END),
        self.ecri_password.delete(0, END)
        self.ecri_confirmpassword.delete(0, END)


    def page_connexion(self):
        self.root.destroy()
        import login


root = Tk()
obj = Formulaire(root)
root.mainloop()