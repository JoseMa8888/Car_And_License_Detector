import pygame
import math
import sys
import numpy as np
import cv2
from update_parking_function import update_parking
from typing import List, Dict, Tuple
from GlobalConstants import Constants
from LicensePlateDetector import LicensePlateDetector
from CarDetector import CarDetector

pygame.init()

constants = Constants(1080, 720)
constants.activate_parking()

font1 = pygame.font.SysFont(None, constants.FONTSIZE)


def dibujar_boton(superficie, rect, texto, color_base, color_hover, font):
    raton = pygame.mouse.get_pos()
    if rect.collidepoint(raton):
        color = color_hover
    else:
        color = color_base
    pygame.draw.rect(superficie, color, rect, border_radius=constants.bottonY)
    texto_render = font.render(texto, True, constants.WHITE)
    superficie.blit(texto_render, (rect.x + constants.bottonX, rect.y + constants.bottonY))
 

def create_rect_text(window, coordinates: Tuple[int], font, text: str = None,
                     occupied_spots=None, license: bool = True, enter="Enter"):
    pygame.draw.rect(window, constants.BRIGHT_RED, coordinates, border_radius=constants.bottonY)
    if license:
        texto_render = font.render(f"{enter} license:\n{text}", True, constants.WHITE)
    else: 
        texto_render = font.render(f"Sitios libres: {20-len(occupied_spots)}/20", True, constants.WHITE)
    
    # Ajustar posición para que no se corte al saltar de línea
    lines = (f"{enter} license:", text) if license else (f"Sitios libres: {20-len(occupied_spots)}/20",)
    y_offset = coordinates[1] + constants.tenY 
    for line in lines:
        texto_render = font.render(line, True, constants.WHITE)
        window.blit(texto_render, (coordinates[0]+constants.tenY, y_offset))
        y_offset += font.get_linesize()


def check_limit(limit, centers):
    if centers:
        i = 0
        found = False
        while not found and i < len(centers):
            centerx, centery = centers[i]
            found = ((limit[0] < centerx < limit[2]) and (limit[1] < centery < limit[3]))
            i+=1
        return found
    return False


def main():
    #constants.activate_constants()
    #print(constants.CAR_HEIGHT_IMAGE)
    parking = constants.parking.copy()
    ventana = pygame.display.set_mode((constants.WIN_WIDTH, constants.WIN_HEIGHT))
    pygame.display.set_caption("Parking simulation")
    fondo = pygame.image.load("data_images/A1.png")
    fondo = pygame.transform.scale(fondo, (constants.WIN_WIDTH, constants.WIN_HEIGHT))
    coche_original = pygame.image.load("data_images/coche_mio_2.png")
    coche_original = pygame.transform.scale(coche_original, (constants.original_carX, constants.original_carY)) 
    boton_rect = pygame.Rect(*constants.exit_botton_coordinates) 

    car_detector = CarDetector(model_path=constants.CAR_AI_MODEL_FILE)
    license_plate1 = LicensePlateDetector()
    license_plate2 = LicensePlateDetector()

    sitios_ocupados = None
    texto_license1 = ""
    texto_license2 = ""
    itera = 0
    car_results = []
    clock = pygame.time.Clock()
    x, y = constants.x, constants.y 

    pygame.draw.rect(fondo, constants.GREEN, (constants.X1,constants.Y1,constants.X2-constants.X1,constants.Y2-constants.Y1), 5)
    pygame.draw.rect(fondo, constants.GREEN, (constants.Z1,constants.W1,constants.Z2-constants.Z1,constants.W2-constants.W1), 5)

    pygame.draw.rect(fondo, constants.BRIGHT_RED, (constants.SX1, constants.SY1, constants.SX2-constants.SX1, constants.SY2-constants.SY1), 5) 
    pygame.draw.rect(fondo, constants.BRIGHT_RED, (constants.SSX1, constants.SSY1, constants.SSX2-constants.SSX1, constants.SSY2-constants.SSY1), 5) 
                        
    
    while True:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
                if boton_rect.collidepoint(evento.pos):
                    pygame.quit()
                    sys.exit()   

        ventana.blit(fondo, (0, 0))

        # teclas presionadas
        teclas = pygame.key.get_pressed()
        if teclas[pygame.K_a]:
            constants.ANGLE += 3  # girar a la izquierda
        if teclas[pygame.K_d]:
            constants.ANGLE -= 3  # girar a la derecha
        if teclas[pygame.K_s]:
            x += constants.VELOCITY * math.cos(math.radians(-constants.ANGLE))
            y += constants.VELOCITY * math.sin(math.radians(-constants.ANGLE))
        if teclas[pygame.K_w]:
            x -= constants.VELOCITY * math.cos(math.radians(-constants.ANGLE))
            y -= constants.VELOCITY * math.sin(math.radians(-constants.ANGLE))

        #2500 rotar coche
        coche_rotado = pygame.transform.rotate(coche_original, constants.ANGLE)
        rect = coche_rotado.get_rect(center=(x, y))
        ventana.blit(coche_rotado, rect.topleft)

        wind_piece = pygame.surfarray.array3d(ventana)
        wind_piece = np.transpose(wind_piece, (1, 0, 2))
        wind_piece = cv2.cvtColor(wind_piece, cv2.COLOR_BGR2RGB)
        wind_piece_license1 = wind_piece[constants.Y1:constants.Y2,constants.X1:constants.X2]
        wind_piece_license2 = wind_piece[constants.W1:constants.W2,constants.Z1:constants.Z2]
        
        if itera % 40 == 0 and check_limit((constants.SX1,constants.SY1,constants.SX2,constants.SY2),car_results):
            license_text1, license_frame1 = license_plate1.get_license_plate(wind_piece_license1, enter=True)
            if license_text1:
                texto_license1 = license_text1

        if itera % 40 == 0 and check_limit((constants.SSX1,constants.SSY1,constants.SSX2,constants.SSY2),car_results):
            license_text2, license_frame2 = license_plate2.get_license_plate(wind_piece_license2, enter=False)
            if license_text2:
                texto_license2 = license_text2
        
        if itera % 40 == 0:
            car_results = car_detector.detect_car(wind_piece, constants) 
            sitios_ocupados, parking = update_parking(car_results, parking)
        
        create_rect_text(ventana, constants.LICENSE1_COORDINATES, font1, text=texto_license1) 
        create_rect_text(ventana, constants.LICENSE2_COORDINATES, font1, text=texto_license2) 

        if sitios_ocupados is not None:
            create_rect_text(ventana, constants.CAR_COORDINATES, font1, occupied_spots=sitios_ocupados, license=False)

        itera+=1

        for value in parking.values():
            if value[4]: 
                pygame.draw.rect(ventana, constants.GREEN, (value[0], value[1], value[-2], value[-1]), 5)
            else:
                pygame.draw.rect(ventana, constants.RED, (value[0], value[1], value[-2], value[-1]), 5)
        
        # dibujar botón
        dibujar_boton(ventana, boton_rect, "Exit", constants.RED, constants.BRIGHT_RED, font1)
        pygame.display.update()
        clock.tick(30)

if __name__ == "__main__":
    main()