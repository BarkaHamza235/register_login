from tkinter import *
from tkinter import ttk, messagebox
import pymysql
import os
class Login:
    def __init__(self, root):
        self.root = root
        self.root.title("Connexion")
        self.root.geometry("1500x780+230+250")
        self.root.config(bg="white")
        self.root.focus_force()

        login_frame = Frame(self.root, bg="cyan")
        login_frame.place(x=500, y=130, width=500, height=500)

        #Title 
        title = Label(login_frame, text="Connexion", font=("algerian",40,"bold"), bg="cyan", fg="black")
        title.pack(side=TOP, fill=X)

        #email
        email = Label(login_frame, text="E-mail", font=("times new roman",30,"bold"), bg="cyan", fg="black").place(x=150, y=100, width=200)
        self.ecri_email = Entry(login_frame, font=("times new roman",20), bg="lightgrey")
        self.ecri_email.place(x=50, y=160, width=400, height=30)

        #password
        password = Label(login_frame, text="Password", font=("times new roman",30,"bold"), bg="cyan", fg="black").place(x=150, y=200, width=200)
        self.ecri_password = Entry(login_frame, show="*", font=("times new roman",20), bg="lightgrey")
        self.ecri_password.place(x=50, y=270, width=400, height=30)

        # Les boutons de validation et connexion
        creer_btn = Button(login_frame, text="Creer un nouveau compte", command=self.page_formulaire, cursor="hand2", font=("times new roman",15,"bold"), bd=0, bg="cyan", fg="green").place(x=30, y=320)
        oubli_btn = Button(login_frame, text="Mot de passe oublie", command=self.password_oublie_fenetre, cursor="hand2", font=("times new roman",15,"bold"), bd=0, bg="cyan", fg="red").place(x=300, y=320)
        connexion_btn = Button(login_frame, text="Connexion", command=self.connexion, cursor="hand2", font=("times new roman",15,"bold"), bd=0, bg="lightgray", fg="green").place(x=190, y=370)

    def connexion(self):
        if  self.ecri_email.get()=="" or self.ecri_password.get()=="":
            messagebox.showerror("Erreur","Veuillez saisir email et mot de passe !", parent=self.root)
        else:
            try:
                con = pymysql.connect(host="localhost", user="root", password="", database="creer")
                cur = con.cursor()
                cur.execute("select * from compte where email = %s and password = %s", (self.ecri_email.get(), self.ecri_password.get()) )
                row = cur.fetchone()
                if row == None: 
                    messagebox.showerror("Erreur","Email et/ou Password invalide !", parent=self.root)
                else:
                    messagebox.showinfo("Succes", "Bienvenue !", parent=self.root)
                    self.root.destroy()
                    import students
                    con.close
            except Exception as ex:
                messagebox.showerror("Erreur", f"Erreur de connexion: {str(ex)} !", parent=self.root)

    
    def password_oublie_fenetre(self):
        if  self.ecri_email.get()=="":
            messagebox.showerror("Erreur","Veuillez donner un email valide !", parent=self.root)
        else:
            try:
                con = pymysql.connect(host="localhost", user="root", password="", database="creer")
                cur = con.cursor()
                cur.execute("select * from compte where email = %s", self.ecri_email.get())
                row = cur.fetchone()
                if row == None: 
                    messagebox.showerror("Erreur","Veuillez entrer un email invalide !", parent=self.root)
                else:                   
                    con.close()
                    self.root2 = Toplevel()
                    self.root2.title("Mot de passe oublie")
                    self.root2.geometry("400x400+800+500")
                    self.root2.config(bg="white")
                    self.root2.focus_force()
                    self.root2.grab_set()

                    #Title 
                    title = Label(self.root2, text="Mot de passe oublie", font=("algerian",20,"bold"), bg="red", fg="black")
                    title.pack(side=TOP, fill=X)

                    #Question
                    question = Label(self.root2, text="Selectionnez une Question", font=("times new roman",15,"bold"), bg="white", fg="black").place(x=70, y=50)
                    self.ecri_question = ttk.Combobox(self.root2, font=("times new roman", 15), state="readonly")
                    self.ecri_question["values"] = ("Select", "Ton surnom", "Lieu de naissance", "Meilleur ami", "Film prefere")
                    self.ecri_question.place(x=70, y=100, width=250)
                    self.ecri_question.current(0)

                    #Reponse
                    reponse = Label(self.root2, text="Repondre", font=("times new roman",15,"bold"), bg="white", fg="black").place(x=70, y=150)
                    self.ecri_reponse = Entry(self.root2, font=("times new roman",15), bg="lightgrey")
                    self.ecri_reponse.place(x=70, y=200, width=250)

                    #Changer mot de passe
                    new_password = Label(self.root2, text="Nouveau mot de passe", font=("times new roman",15,"bold"), bg="white", fg="black").place(x=70, y=250)
                    self.ecri_new_password= Entry(self.root2, show="*", font=("times new roman",15), bg="lightgrey")
                    self.ecri_new_password.place(x=70, y=300, width=250)

                    #Bouton changer mot de passe
                    changer_btn = Button(self.root2, text="Moifier", command=self.password_oublie, cursor="hand2", font=("times new roman",15,"bold"), bg="lightgray", fg="green").place(x=160, y=350)

            except Exception as ex:
                messagebox.showerror("Erreur", f"Erreur de connexion: {str(ex)} !", parent=self.root)


    def reini(self):
        self.ecri_question.delete(0, END),
        self.ecri_reponse.delete(0, END),
        self.ecri_new_password.delete(0, END)

    def password_oublie(self):
        if self.ecri_question.get()=="" or self.ecri_reponse.get()=="" or self.ecri_new_password.get()=="":
            messagebox.showerror("Erreur","Remplir tous les champs !", parent=self.root2)
        else:
            try:
                con = pymysql.connect(host="localhost", user="root", password="", database="creer")
                cur = con.cursor()
                cur.execute("select * from compte where email = %s and question = %s and reponse = %s", (self.ecri_email.get(), self.ecri_question.get(), self.ecri_reponse.get(),) )
                row = cur.fetchone()
                if row == None: 
                    messagebox.showerror("Erreur","Vous n'avez pas bien repondu a la question selectionne !", parent=self.root2)
                else:                   
                    cur.execute("update  compte set password = %s where email = %s", (self.ecri_new_password.get(), self.ecri_email.get()) )
                    con.commit()
                    con.close()
                    messagebox.showinfo("Succes", "Vous avez modifie votre mot de passe !", parent=self.root2)
                    self.reini()
                    self.root2.destroy()
            except Exception as ex:
                messagebox.showerror("Erreur", f"Erreur de connexion: {str(ex)} !", parent=self.root2)

    def page_formulaire(self):
        self.root.destroy()
        import register



root = Tk()
obj = Login(root)
root.mainloop()