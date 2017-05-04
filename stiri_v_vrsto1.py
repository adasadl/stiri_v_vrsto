
import tkinter
import argparse
import logging

from razred_igra import *
from razred_clovek import *
from razred_racunalnik import *

MINIMAX_GLOBINA = 4

class Gui():
    TAG_FIGURA = "figura"
    TAG_OKVIR = "okvir"
    VELIKOST_POLJA = 60
    ODMIK = 0.5

    def __init__(self, master, globina):

        self.rdeci = None
        self.modri = None
        self.igra = None
        
        master.protocol("WM_DELETE_WINDOW", lambda: self.zapri_okno(master))

        glavni_menu = tkinter.Menu(master)
        master.config(menu = glavni_menu)

        podmenu = tkinter.Menu(glavni_menu)
        glavni_menu.add_cascade(label = "Možnosti", menu = podmenu)
        podmenu.add_command(label="Človek vs Človek",
                            command=lambda: self.nova_igra(Clovek(self), Clovek(self)))
        podmenu.add_command(label="Človek vs Računalnik",
                            command=lambda: self.nova_igra(Clovek(self), Racunalnik(self, Minimax(globina))))
        podmenu.add_command(label="Računalnik vs Človek",
                            command=lambda: self.nova_igra(Racunalnik(self, Minimax(globina)), Clovek(self)))
        

        self.plosca = tkinter.Canvas(master, width = (7 + 2*Gui.ODMIK)*Gui.VELIKOST_POLJA, height = (6+2*Gui.ODMIK)*Gui.VELIKOST_POLJA)
        self.plosca.grid(row = 1, column = 0)
         

        self.narisi_polje()
        
        self.plosca.bind("<Button-1>", self.plosca_klik)

        self.napis = tkinter.StringVar(master, value = "Igra 4 v vrsto se je pričela!")
        tkinter.Label(master, textvariable = self.napis, font = ("Fixedsys", 20)).grid(row = 0, column = 0)

        self.nova_igra(Clovek(self), Racunalnik(self, Minimax(globina)))

    def nova_igra(self, modri, rdeci):
        #prekinemo igralce
        self.prekini_igralce()
        # Pobrišemo vse figure s polja
        self.plosca.delete(Gui.TAG_FIGURA)
        # Ustvarimo novo igro
        self.igra = Igra()
        # Nastavimo igralce
        self.rdeci = rdeci
        self.modri = modri

        # Modri je prvi na potezi
        self.napis.set("Na potezi je MODRI.")
        self.modri.igraj()


    def koncaj_igro(self, zmagovalec, stirica):
        self.prekini_igralce()
        if zmagovalec == MODRI:
            self.napis.set("Zmagal je MODRI.")
            self.obkrozi_zmagovalno_stirico(zmagovalec, stirica)
            

        elif zmagovalec == RDECI:
            self.napis.set("Zmagal je RDECI.")
            self.obkrozi_zmagovalno_stirico(zmagovalec, stirica)
            

        else:
            self.napis.set("Neodločeno.")
            

    def prekini_igralce(self):
        """Sporoči igralcem, da morajo nehati razmišljati."""
        if self.modri: self.modri.prekini()
        if self.rdeci: self.rdeci.prekini()

    def zapri_okno(self, master):
        self.prekini_igralce()
        master.destroy()
    

    def narisi_polje(self):
        self.plosca.delete(Gui.TAG_OKVIR)
        d = Gui.VELIKOST_POLJA

        self.plosca.create_rectangle(Gui.ODMIK*d, Gui.ODMIK*d, (7+Gui.ODMIK)*d, (6+Gui.ODMIK)*d, tag = Gui.TAG_OKVIR, width = 1.5)
        for i in range(1, 7):  # navpicne crte
            self.plosca.create_line((i+Gui.ODMIK)*d, (Gui.ODMIK)*d, (i+Gui.ODMIK) *d, (6+Gui.ODMIK)*d, tag=Gui.TAG_OKVIR)
        for j in range(1, 6):  # vodoravne crte
            self.plosca.create_line(Gui.ODMIK*d, (Gui.ODMIK + j)*d, (7+Gui.ODMIK)*d, (Gui.ODMIK+j)*d, tag=Gui.TAG_OKVIR)

    def narisi_modri(self, p):
        x = p[0] * Gui.VELIKOST_POLJA
        y= 0
        sirina = 2
        d1 = Gui.VELIKOST_POLJA / 10
        d2 = Gui.VELIKOST_POLJA - d1

        (i, j) = p

        j = 5
        while j>=0:
            if self.igra.stolpci[i][j] == MODRI:
                self.plosca.create_oval(x + d1 + Gui.VELIKOST_POLJA * Gui.ODMIK, 0.5*Gui.VELIKOST_POLJA + j*2 * Gui.VELIKOST_POLJA * Gui.ODMIK + d1,
                                        x + d2 + Gui.VELIKOST_POLJA * Gui.ODMIK, 0.5*Gui.VELIKOST_POLJA + j*2 * Gui.VELIKOST_POLJA * Gui.ODMIK + d2, 
                                        width=sirina, tag=Gui.TAG_FIGURA,
                                        fill="royal blue", outline = "royal blue")
            j-=1

            
                 

    def narisi_rdeci(self, p):
        x = p[0] * Gui.VELIKOST_POLJA
        sirina = 2
        d1 = Gui.VELIKOST_POLJA / 10
        d2 = Gui.VELIKOST_POLJA - d1

        (i, j) = p
        j = 5
        while j>0:
            if self.igra.stolpci[i][j] == RDECI:
                self.plosca.create_oval(x + d1 + Gui.VELIKOST_POLJA * Gui.ODMIK, 0.5*Gui.VELIKOST_POLJA + j*2 * Gui.VELIKOST_POLJA * Gui.ODMIK + d1,
                                        x + d2 + Gui.VELIKOST_POLJA * Gui.ODMIK, 0.5*Gui.VELIKOST_POLJA + j*2 * Gui.VELIKOST_POLJA * Gui.ODMIK + d2, 
                                        width=sirina, tag=Gui.TAG_FIGURA,
                                        fill="orange red", outline = "orange red")
            j-=1


    def obkrozi_zmagovalno_stirico(self, zmagovalec, stirica):
        d = Gui.VELIKOST_POLJA
        r = Gui.ODMIK
        barva = "red"

        (j1, i1) = stirica[0]
        (j2, i2) = stirica[1]
        (j3, i3) = stirica[2]
        (j4, i4) = stirica[3]

        if zmagovalec == MODRI:
            barva = "navy"
        if j1==j2==j3==j4: #v primeru, da je zmagal s stolpcem
            self.plosca.create_rectangle((j1+r)* d, (i1+r) * d, (j1+1+r) * d , (i4 + 1+r) * d, width=5, outline = barva, tag = Gui.TAG_FIGURA) #Zakaj ne dela z drugim tagom?
        elif i1==i1==i3==i4: #zmagal z vrstico
            self.plosca.create_rectangle((j1+r) * d, (i1+1+r) * d, (j4+1+r) * d, (i1+r) * d, width=5, outline = barva, tag = Gui.TAG_FIGURA)
        else: #zmagal z diagonalo
            self.plosca.create_rectangle((j1+r) * d, (i1 + r) * d, (j1 + 1+r) * d, (i1 + 1+r) * d, width=5, outline=barva, tag=Gui.TAG_FIGURA)
            self.plosca.create_rectangle((j2+r) * d, (i2 + r) * d, (j2 + 1+r) * d, (i2 + 1+r) * d, width=5, outline=barva, tag=Gui.TAG_FIGURA)
            self.plosca.create_rectangle((j3+r) * d, (i3 + r) * d, (j3 + 1+r) * d, (i3 + 1+r) * d, width=5, outline=barva, tag=Gui.TAG_FIGURA)
            self.plosca.create_rectangle((j4+r) * d, (i4 + r) * d, (j4 + 1+r) * d, (i4 + 1+r) * d, width=5, outline=barva, tag=Gui.TAG_FIGURA)



    def plosca_klik(self, event):
        """Obdelaj klik na ploščo."""
        # Tistemu, ki je na potezi, povemo, da je uporabnik kliknil na ploščo.
        # Podamo mu potezo p.
        i = int((event.x - Gui.ODMIK * Gui.VELIKOST_POLJA) // Gui.VELIKOST_POLJA)
        j = event.y // Gui.VELIKOST_POLJA
        (novi_zmagovalec, nova_stirica) = self.igra.stanje_igre()
        if self.igra.stolpci[i][0] == 0 and nova_stirica == None: #to zagotovi, da če so vsa polja v nekem stolpcu že polna, se ne zgodi nič
            # print ("Klik na ({0}, {1}), polje ({2}, {3})".format(event.x, event.y, i, j))
            if self.igra.na_potezi == MODRI:
                self.modri.klik((i,j))
            elif self.igra.na_potezi == RDECI:
                self.rdeci.klik((i,j))
            else:
                # Nihče ni na potezi, ne naredimo nič
                pass
        else:
            # klik izven plošče
            pass

    def povleci_potezo(self, p):
        
        igralec = self.igra.na_potezi
        r = self.igra.povleci_potezo(p)
        print (self.igra.stolpci) #preverimo, da je pravilno zapisano v self.stolpci
        
        if r is None:
            # Poteza ni bila veljavna, nič se ni spremenilo
            pass
        else:
            # Poteza je bila veljavna, narišemo jo na zaslon
            if igralec == MODRI:
                self.narisi_modri(p)
            elif igralec == RDECI:
                self.narisi_rdeci(p)
            # Ugotovimo, kako nadaljevati
            (novi_zmagovalec, nova_stirica) = self.igra.stanje_igre()
            if novi_zmagovalec == NI_KONEC:
                # Igra se nadaljuje
                if self.igra.na_potezi == MODRI:
                    self.napis.set("Na potezi je MODRI.")
                    self.modri.igraj()
                elif self.igra.na_potezi == RDECI:
                    self.napis.set("Na potezi je RDECI.")
                    self.rdeci.igraj()

            else:
                self.koncaj_igro(novi_zmagovalec, nova_stirica)








if __name__ == "__main__":
    # Iz ukazne vrstice poberemo globino za minimax, uporabimo
    # modul argparse, glej https://docs.python.org/3.4/library/argparse.html

    # Opišemo argumente, ki jih sprejmemo iz ukazne vrstice
    parser = argparse.ArgumentParser(description="Igrica stiri v vrsto")
    # Argument --globina n, s privzeto vrednostjo MINIMAX_GLOBINA
    parser.add_argument('--globina',
                        default=MINIMAX_GLOBINA,
                        type=int,
                        help='globina iskanja za minimax algoritem')
    # Argument --debug, ki vklopi sporočila o tem, kaj se dogaja
    parser.add_argument('--debug',
                        action='store_true',
                        help='vklopi sporočila o dogajanju')

    # Obdelamo argumente iz ukazne vrstice
    args = parser.parse_args()

    # Vklopimo sporočila, če je uporabnik podal --debug
    if args.debug:
        logging.basicConfig(level=logging.DEBUG)

    # Naredimo glavno okno in nastavimo ime
    root = tkinter.Tk()
    root.title("Stiri v vrsto")

    # Naredimo objekt razreda Gui in ga spravimo v spremenljivko,
    # sicer bo Python mislil, da je objekt neuporabljen in ga bo pobrisal
    # iz pomnilnika.
    aplikacija = Gui(root, args.globina)

    # Kontrolo prepustimo glavnemu oknu. Funkcija mainloop neha
    # delovati, ko okno zapremo.
    root.mainloop()
