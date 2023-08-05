import pygame
import random

pygame.init()

pygame.display.set_caption('Flappy Bird')
schermata_play=pygame.image.load('immagini/schermata_play.png')
sfondo=pygame.image.load('immagini/sfondo.png')
uccello=pygame.image.load('immagini/uccello.png')
base=pygame.image.load('immagini/base.png')
gameover=pygame.image.load('immagini/gameover.png')
tubo_inferiore=pygame.image.load('immagini/tubo.png')
tubo_superiore=pygame.transform.flip(tubo_inferiore,False,True)

suono_punti=pygame.mixer.Sound('suoni/score.mp3')
suono_haiperso=pygame.mixer.Sound('suoni/hit.mp3')
suono_nuova_partita=pygame.mixer.Sound('suoni/button-press.mp3')


DISPLAY=pygame.display.set_mode((288,512))
FPS=50
FONT=pygame.font.SysFont('Comic Sans MS',50,bold=True)
VELOCITA_AVANZAMENTO=3

larghezza_immagine_uccello=uccello.get_width()
larghezza_immagine_tubo=tubo_inferiore.get_width()
altezza_immagine_uccello=uccello.get_height()

class tubi_classe:

    def __init__(self):
        self.x=300
        self.y=random.randint(-75,150)

    def avanza_e_disegna(self):
        self.x-=VELOCITA_AVANZAMENTO
        DISPLAY.blit(tubo_inferiore,(self.x,self.y+210))
        DISPLAY.blit(tubo_superiore,(self.x,self.y-210))

    def collisione(self,uccello,uccellox,uccelloy):
        tolleranza=5
        uccello_lato_dx=uccellox+larghezza_immagine_uccello-tolleranza
        uccello_lato_sx=uccellox+tolleranza
        tubi_lato_dx=self.x+larghezza_immagine_tubo
        tubi_lato_sx=self.x
        uccello_lato_superiore=uccelloy+tolleranza
        uccello_lato_inferiore=uccelloy+altezza_immagine_uccello-tolleranza
        tubi_lato_superiore=self.y+110
        tubi_lato_inferiore=self.y+210
        if uccello_lato_dx>tubi_lato_sx and uccello_lato_sx<tubi_lato_dx:
            if uccello_lato_superiore<tubi_lato_superiore or uccello_lato_inferiore>tubi_lato_inferiore:
                hai_perso()

    def fra_i_tubi(self,uccello,uccellox):
        tolleranza=5
        uccello_lato_dx=larghezza_immagine_uccello-tolleranza
        uccello_lato_sx=uccellox+tolleranza
        tubi_lato_dx=self.x+larghezza_immagine_tubo
        tubi_lato_sx=self.x
        if uccello_lato_dx>tubi_lato_sx and uccello_lato_sx<tubi_lato_dx:
            return True


def disegna_oggetti():
    DISPLAY.blit(sfondo,(0,0))
    for tubo in tubi:
        tubo.avanza_e_disegna()
    DISPLAY.blit(uccello,(uccellox,uccelloy))
    DISPLAY.blit(base,(basex,400))
    reinderizzazione_punti=FONT.render(str(punti),1,(0,0,0))
    DISPLAY.blit(reinderizzazione_punti,(144,0))

def aggiorna():
    pygame.display.update()
    pygame.time.Clock().tick(FPS)

def inizializza():
    global uccellox,uccelloy,accellerazione_verticale
    global basex,tubi,punti,fra_i_tubi
    suono_nuova_partita.play()
    uccellox,uccelloy=60,150
    accellerazione_verticale=0
    basex=0
    punti=0
    tubi=[]
    tubi.append(tubi_classe())
    fra_i_tubi=False

def schermata_iniziale():
    DISPLAY.blit(schermata_play,(0,0))
    aggiorna()
    intro=False
    while not intro:
        for event in pygame.event.get():
            if event.type==pygame.KEYDOWN and event.key==pygame.K_SPACE:
                intro=True
            if event.type==pygame.KEYDOWN and event.key==pygame.K_ESCAPE:
                 quit() #pygame.quit()
                 exit()
            if event.type==pygame.QUIT:
                quit() #pygame.quit()
                exit()

def hai_perso():
    suono_haiperso.play()
    DISPLAY.blit(gameover,(-140,15)) #50,180
    aggiorna()
    perso=True
    while perso:
        for event in pygame.event.get():
            if event.type==pygame.KEYDOWN and event.key==pygame.K_SPACE:
                suono_nuova_partita.play()
                inizializza()
                perso=False
            if event.type==pygame.KEYDOWN and event.key==pygame.K_ESCAPE:
                quit() #pygame.quit()
                exit()
            if event.type==pygame.QUIT:
                quit() #pygame.quit()
                exit()
            if event.type==pygame.KEYDOWN and event.key==pygame.K_RETURN:
                schermata_iniziale()
                break
            break

schermata_iniziale()
inizializza()

while True:
    basex-=VELOCITA_AVANZAMENTO
    if basex<-45:
        basex=0
    accellerazione_verticale+=1
    uccelloy+=accellerazione_verticale
    for event in pygame.event.get():
        if (event.type==pygame.KEYDOWN and event.key==pygame.K_UP):
            accellerazione_verticale=-10
        if event.type==pygame.KEYDOWN and event.key==pygame.K_ESCAPE:
            quit() #pygame.quit()
            exit()
        if event.type==pygame.QUIT:
            quit() #pygame.quit()
            exit()
    if tubi[-1].x<150:
        tubi.append(tubi_classe())
    for tubo in tubi:
        tubo.collisione(uccello,uccellox,uccelloy)
    if not fra_i_tubi:
        for tubo in tubi:
            if tubo.fra_i_tubi(uccello,uccellox):
                fra_i_tubi=True
                break
    if fra_i_tubi:
        fra_i_tubi=False
        for tubo in tubi:
            if tubo.fra_i_tubi(uccello,uccellox):
                fra_i_tubi=True
                break
        if not fra_i_tubi:
            punti+=1
            suono_punti.play()
    if uccelloy>380:
        hai_perso()

        
    disegna_oggetti()
    aggiorna()
