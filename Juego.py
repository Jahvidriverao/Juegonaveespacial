
from pickle import TRUE
import pygame
import random
import math
from pygame import mixer

# Iniciar programa
pygame.init()

#Crear la pantalla
pantalla = pygame.display.set_mode((800, 600))

#Titulo e Icono
pygame.display.set_caption("Invasión Espacial")
icono = pygame.image.load("ovni.png")
pygame.display.set_icon(icono)
fondo = pygame.image.load('Fondo.jpg')


#agregar musica

mixer.music.load('MusicaFondo.mp3')
mixer.music.set_volume(0.2)
mixer.music.play(-1)

#Variables del jugador
img_jugador = pygame.image.load("astronave.png")
jugador_x = 368
jugador_y = 500
jugador_x_cambio = 0
#Variables del enemigo
img_enemigo = []
enemigo_x = []
enemigo_y =  []
enemigo_x_cambio = []
enemigo_y_cambio = []
cantidad_enemigos = 10

for e in range(cantidad_enemigos):
    img_enemigo.append(pygame.image.load("enemigo.png"))
    enemigo_x.append(random.randint(0, 730))
    enemigo_y.append(random.randint(50, 200))
    enemigo_x_cambio.append(0.5)
    enemigo_y_cambio.append(30)

#Variables de la bala
img_bala= pygame.image.load("bala.png")
bala_x = 0
bala_y =  500
bala_x_cambio = 0
bala_y_cambio = 1.5
bala_visible = False

#variable puntaje
puntaje = 0
fuente = pygame.font.Font ('freesansbold.ttf', 32)
texto_x = 10
texto_y= 10

#texto final de juego
fuente_final = pygame.font.Font('freesansbold.ttf', 40)

def texto_final():
    mi_fuente_final = fuente_final.render("GAMER OVER", True, (255,255,255))
    pantalla.blit(mi_fuente_final, (275,300))

#funcion mostrar puntaje
def mostrar_puntaje(x, y): 
    texto = fuente.render(f"puntaje: { puntaje}", True, (255, 255, 255) )
    pantalla.blit(texto, (x, y))

#funcion jugador 
def jugador(x, y):
    pantalla.blit(img_jugador, (x, y))

#funcion enemigo
def enemigo(x, y, ene):
    pantalla.blit(img_enemigo[ene], (x, y))

#funcion dispara bala
def disparar_bala(x, y):
    global bala_visible
    bala_visible = True
    pantalla.blit(img_bala, (x + 16 , y + 10))
#funcion detectar colisiones
def hay_colision(x_1, y_1, x_2, y_2):
    distacia = math.sqrt(math.pow(x_1 - x_2, 2)+ math.pow(y_2 - y_1, 2))
    if distacia <27:
        return True
    else:
        return False
#Loop del juego
se_ejecuta = True
while se_ejecuta:
    #Fondo imagen
    pantalla.blit(fondo, (0, 0))

    for evento in pygame.event.get():
        #Evento cerrar
        if evento.type == pygame.QUIT:
            se_ejecuta = False
     
      #Movimiento 
        if evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_LEFT:
                jugador_x_cambio = -0.5
            if evento.key == pygame.K_RIGHT:
                jugador_x_cambio = 0.5
            if evento.key == pygame.K_SPACE:
                sonido_bala= mixer.Sound('disparo.mp3')
                sonido_bala.play()
                if not bala_visible:
                    bala_x = jugador_x
                    disparar_bala(bala_x, bala_y)

            
    #evento soltar tecla
        if evento.type == pygame.KEYUP:
            if evento.key == pygame.K_LEFT or evento.key == pygame.K_RIGHT:
                jugador_x_cambio = 0
    #Modificar Ubicacion del jugador
    jugador_x += jugador_x_cambio

    #mantener dentro de bordes
    if jugador_x <= 0:
        jugador_x = 0
    elif jugador_x >=738:
        jugador_x = 738

    #Modificar Ubicacion del enemigo
    for e in range(cantidad_enemigos):
        #fin del juego
        if enemigo_y[e] >400:
            for k in range(cantidad_enemigos):
                enemigo_y[k] = 1000
            texto_final()
            break


        enemigo_x[e] += enemigo_x_cambio[e]

    #mantener dentro de bordes al enemigo
        if enemigo_x [e]<= 0:
            enemigo_x_cambio[e] = 0.5
            enemigo_y[e] += enemigo_y_cambio[e]
        elif enemigo_x [e]>=738:
            enemigo_x_cambio[e] = -0.5
            enemigo_y[e] += enemigo_y_cambio[e]

            #colision
        colision = hay_colision(enemigo_x[e], enemigo_y[e],bala_x, bala_y)
        if colision:
            sonido_colision = mixer.Sound('Golpe.mp3')
            sonido_bala.play()
            bala_y = 500
            bala_visible = False
            puntaje += 1
            enemigo_x [e]= random.randint(0, 730)
            enemigo_y [e]=  random.randint(50, 200)

        enemigo(enemigo_x[e], enemigo_y[e], e )

    #movimiento bala
    if bala_y <= -64:
        bala_y = 500
        bala_visible = False

    if bala_visible:
        disparar_bala(bala_x, bala_y)
        bala_y -= bala_y_cambio




#Modificar ubicacion

    jugador(jugador_x, jugador_y)
    
    mostrar_puntaje(texto_x, texto_y)

    #actualizar al jugador 
    pygame.display.update()

