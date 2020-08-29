#Importiamo i pacchetti necessari
from tkinter import *
from PIL import ImageTk,Image
import sqlite3
import random
#Impostiamo le dimensioni dell'interfaccia, il logo, il nome ed il colore
root = Tk()
root.geometry("1800x1800")
root.title("BIBDA Park")
root.iconbitmap(r'C:\Users\Pasqui\Desktop\Master\Progetti\Ps4\logo.ico')
root.configure(background="black")

#Messaggio di benvenuto e spiegazione all'utente
Welcome = Label(root, text= """Dear Gamer welcome in our Park and we hope you enjoyed our new Gaming Hub.\n
If you are reading this messagge, you decided to play our #GuessthegameChallange\n\n
After pressing the button below\n you will display 10 words related to a famous scene image of a Game present in this Hub.\n
Choose the game from our Menu to discover if you WON!""", fg="White", bg="black",font="Helvetica 20 bold")
Welcome.pack()
#Impostiamo la connessione al DB dei giochi (185)
conn = sqlite3.connect(r'C:\Users\Pasqui\Desktop\Master\Progetti\Ps4\Fact\Ft_games_images.db')
c = conn.cursor()
lista_ID=[]
concepts=[]
titles=[]
#Verifichiamo il numero di ID presenti nel DB che corrisponderà ad un immagine del gioco ed ai 10 concetti
for i in c.execute("SELECT DISTINCT ID FROM Ft_games_images"):
    lista_ID.append(i[0])

Numero_id = int(len(lista_ID))
titolo_vincente=''
#A sorte estraiamo un numero compreso tra 1 ed il count degli ID
numero_casuale = random.randint(1, Numero_id)
#Utilizziamo il numero casuale come indice per estrarre un ID dalla lista
Id_casuale = str(lista_ID[numero_casuale])
#Utilizziamo l'ID estratto come filtro del DB ed isoliamo i 10 concetti precedentemente generati da Clarifai ed anche il titolo del gioco
for j in c.execute("SELECT concept, title FROM Ft_games_images where ID = ?",(Id_casuale,)):
    concepts.append((j[0]))
    concepts.append("-")
    titolo_vincente=j[1]
#Cancelliamo l'ultimo trattino della lista che non ci interessa
del concepts[-1]
#Isoliamo in una lista tutti i titoli dei giochi
for i in c.execute("SELECT concept, Title FROM Ft_games_images"):
    titles.append(i[1])
#Rendiamo i titoli dei giochi univoci
titles=list(dict.fromkeys(titles))
titles.sort()
#Li trasformiamo in Maiuscolo
concepts = list(map(lambda x:x.upper(),concepts))
#Definiamo la funzione per giocare che fa apparire i 10 concetti e la lista dei giochi da cui scegliere
def gioca():
    Welcome.destroy()
    global Display_conce
    Display_conce = Label(root, text = concepts, fg="White", bg="black", font="Helvetica 14")
    Display_conce.pack(side=TOP, anchor="s",pady=50)
    giocaButton.destroy()
    drop_sport.pack()
    clicked.set(titles[0])
    Button_final.pack(padx=50,pady=50)


giocaButton= Button(root, text="LET'S PLAY", bg="white", command=gioca)

#Attribuiamo al bottone gioca un'immagine
img_play = Image.open(r'C:\Users\Pasqui\Desktop\Master\Progetti\Ps4\play.png')
img_play= img_play.resize((85,85),Image.ANTIALIAS)
img_play = ImageTk.PhotoImage(img_play)
giocaButton.config(image=img_play)
giocaButton.pack()

#Creiamo la lista dei giochi
var= StringVar()
clicked= StringVar()
drop_sport = OptionMenu(root, clicked,*titles)
drop_sport.config(width="40",bg="blue",font="bold")
print(Id_casuale)
#Creiamo la funzione per verificare di aver scelto il gioco corretto associato ai 10 concetti e plottiamo l'immagine del gioco vincente
def verifica():
    drop_sport.destroy()
    Display_conce.destroy()
    Button_final.destroy()
    if clicked.get()==titolo_vincente:
        label_win=Label(root, text="YOU WIN!!!!", font="Helvetica 30 bold",bg="black",fg="white")
        label_win.pack()
    else:
        label_lose=Label(root, text="YOU Lose :(", font="Helvetica 30 bold",bg="black",fg="white")
        label_lose.pack()
    global Image_game
    Image_game=Image.open(r'C:\Users\Pasqui\Desktop\Master\Progetti\Ps4\Immagini_copertina\img_' + Id_casuale +'.jpg')
    Image_game = Image_game.resize((400,400),Image.ANTIALIAS)
    Image_game  = ImageTk.PhotoImage(Image_game)
    Canvas_image = Canvas(root, width = 400 , height = 400,borderwidth=0, highlightthickness=0)
    Canvas_image.pack(padx=40, pady=40)
    Canvas_image.create_image(200,200,image = Image_game)
    if clicked.get()==titolo_vincente:
        label_win=Label(root, text="The winning game was '" + titolo_vincente + "'\n Go to the infopoint and receive a copy of the game!\n Register on your Social Netork using the challange #", font="Helvetica 30 bold",bg="black",fg="white")
        label_win.pack()
    else:
        label_win=Label(root, text="The winning game was '" + titolo_vincente + "'\n We hope you had a lot of fun here and...\n see you soon next time!", font="Helvetica 20 bold",bg="black",fg="white")
        label_win.pack()

Button_final = Button(root, text="PRESS ME", command=verifica, bg="blue",width = "34",font="bold")
print(titolo_vincente)
root.mainloop()
