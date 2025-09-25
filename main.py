import pygame
import math
import sys
import numpy as np
import cv2
from update_parking_function import update_parking
from typing import List, Dict, Tuple
from GlobalConstants import Constants
from CarWorker import CarWorker
from LicensePlateDetector import LicensePlateDetector
import multiprocessing as mp

pygame.init()

font1 = pygame.font.SysFont(None, 60)
parking: Dict[str, List[int]] = {
    'A8': [37, 30, 463, 200, 1, 426, 170],
    'A3': [36, 200, 465, 368, 1, 429, 168],
    'B2': [33, 369, 466, 544, 1, 433, 175],
    'C2': [35, 545, 468, 713, 1, 433, 168],
    'D2': [36, 713, 471, 883, 1, 435, 170],
    'E1': [35, 882, 475, 1063, 1, 440, 181],
    'A1': [798, 192, 1218, 362, 1, 420, 170],
    'A5': [800, 362, 1220, 544, 1, 420, 182],
    'B3': [801, 543, 1220, 707, 1, 419, 164],
    'C3': [802, 706, 1220, 880, 1, 418, 174],
    'A2': [1220, 192, 1633, 363, 1, 413, 171],
    'A6': [1218, 362, 1635, 543, 1, 417, 181],
    'B4': [1221, 544, 1636, 711, 1, 415, 167],
    'C4': [1218, 708, 1636, 882, 1, 418, 174],
    'A7': [2007, 30, 2465, 194, 1, 458, 164],
    'A4': [2007, 192, 2465, 360, 1, 458, 168],
    'B1': [2008, 359, 2466, 539, 1, 458, 180],
    'C1': [2007, 538, 2466, 707, 1, 459, 169],
    'D1': [2008, 707, 2465, 882, 1, 457, 175],
    'E2': [2007, 882, 2466, 1056, 1, 459, 174]
}


def dibujar_boton(superficie, rect, texto, color_base, color_hover):
    raton = pygame.mouse.get_pos()
    if rect.collidepoint(raton):
        color = color_hover
    else:
        color = color_base
    pygame.draw.rect(superficie, color, rect, border_radius=15)
    texto_render = font1.render(texto, True, Constants.WHITE)
    superficie.blit(texto_render, (rect.x + 20, rect.y + 15))
 

def create_rect_text(window, coordinates: Tuple[int], font, text: str = None,
                     occupied_spots=None, license: bool = True, enter="Enter"):
    pygame.draw.rect(window, Constants.BRIGHT_RED, coordinates, border_radius=15)
    if license:
        texto_render = font.render(f"{enter} license:\n{text}", True, Constants.WHITE)
    else: 
        texto_render = font.render(f"Sitios libres: {20-len(occupied_spots)}/20", True, Constants.WHITE)
    
    # Ajustar posición para que no se corte al saltar de línea
    lines = (f"{enter} license:", text) if license else (f"Sitios libres: {20-len(occupied_spots)}/20",)
    y_offset = coordinates[1] + 10
    for line in lines:
        texto_render = font.render(line, True, Constants.WHITE)
        window.blit(texto_render, (coordinates[0]+10, y_offset))
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


def main(parking):
    ventana = pygame.display.set_mode((Constants.WIN_WIDTH, Constants.WIN_HEIGHT))
    pygame.display.set_caption("Parking simulation")
    fondo = pygame.image.load("data_images/A1.png")
    fondo = pygame.transform.scale(fondo, (Constants.WIN_WIDTH, Constants.WIN_HEIGHT))
    coche_original = pygame.image.load("data_images/coche_mio_2.png")
    coche_original = pygame.transform.scale(coche_original, (750, 450)) 
    boton_rect = pygame.Rect(Constants.WIN_WIDTH - 200, 40, 150, 70) 

    car_worker = CarWorker()
    car_worker.create_process()
    car_worker.activate_deamon()
    car_worker.start_process()

    license_plate1 = LicensePlateDetector()
    license_plate2 = LicensePlateDetector()

    sitios_ocupados = None
    texto_license1 = ""
    texto_license2 = ""
    itera = 0
    car_results = []
    x, y = 200, Constants.WIN_HEIGHT-120
    clock = pygame.time.Clock()

    pygame.draw.rect(fondo, Constants.GREEN, (Constants.X1,Constants.Y1,Constants.X2-Constants.X1,Constants.Y2-Constants.Y1), 5)
    pygame.draw.rect(fondo, Constants.GREEN, (Constants.Z1,Constants.W1,Constants.Z2-Constants.Z1,Constants.W2-Constants.W1), 5)

    pygame.draw.rect(fondo, Constants.BRIGHT_RED, (Constants.SX1, Constants.SY1, Constants.SX2-Constants.SX1, Constants.SY2-Constants.SY1), 5) 
    pygame.draw.rect(fondo, Constants.BRIGHT_RED, (Constants.SSX1, Constants.SSY1, Constants.SSX2-Constants.SSX1, Constants.SSY2-Constants.SSY1), 5) 
                        
    
    while True:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                car_worker.stop()
                pygame.quit()
                sys.exit()

            if evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
                if boton_rect.collidepoint(evento.pos):
                    car_worker.stop()
                    pygame.quit()
                    sys.exit()   

        ventana.blit(fondo, (0, 0))

        # teclas presionadas
        teclas = pygame.key.get_pressed()
        if teclas[pygame.K_a]:
            Constants.ANGLE += 3  # girar a la izquierda
        if teclas[pygame.K_d]:
            Constants.ANGLE -= 3  # girar a la derecha
        if teclas[pygame.K_s]:
            x += Constants.VELOCITY * math.cos(math.radians(-Constants.ANGLE))
            y += Constants.VELOCITY * math.sin(math.radians(-Constants.ANGLE))
        if teclas[pygame.K_w]:
            x -= Constants.VELOCITY * math.cos(math.radians(-Constants.ANGLE))
            y -= Constants.VELOCITY * math.sin(math.radians(-Constants.ANGLE))

        # rotar coche
        coche_rotado = pygame.transform.rotate(coche_original, Constants.ANGLE)
        rect = coche_rotado.get_rect(center=(x, y))
        ventana.blit(coche_rotado, rect.topleft)

        wind_piece = pygame.surfarray.array3d(ventana)
        wind_piece = np.transpose(wind_piece, (1, 0, 2))
        wind_piece = cv2.cvtColor(wind_piece, cv2.COLOR_BGR2RGB)
        wind_piece_license1 = wind_piece[Constants.Y1:Constants.Y2,Constants.X1:Constants.X2]
        wind_piece_license2 = wind_piece[Constants.W1:Constants.W2,Constants.Z1:Constants.Z2]
        
        if itera % 20 == 0 and check_limit((Constants.SX1,Constants.SY1,Constants.SX2,Constants.SY2),car_results):
            license_text1, license_frame1 = license_plate1.get_license_plate(wind_piece_license1, enter=True)
            if license_text1:
                texto_license1 = license_text1

        if itera % 30 == 0 and check_limit((Constants.SSX1,Constants.SSY1,Constants.SSX2,Constants.SSY2),car_results):
            license_text2, license_frame2 = license_plate2.get_license_plate(wind_piece_license2, enter=False)
            if license_text2:
                texto_license2 = license_text2
        
        if itera % 20 == 0 and car_worker.frame_queue_empty():  
            car_worker.put_frames(wind_piece)

        if itera % 15 == 0 and not car_worker.results_queue_empty():
            car_results = car_worker.get_results()
            sitios_ocupados, parking = update_parking(car_results, parking)
        
        for center in car_results:
            pygame.draw.circle(ventana, color=Constants.BRIGHT_RED, center=center, radius=2)

        create_rect_text(ventana, Constants.LICENSE1_COORDINATES, font1, text=texto_license1) 
        create_rect_text(ventana, Constants.LICENSE2_COORDINATES, font1, text=texto_license2) 

        if sitios_ocupados is not None:
            create_rect_text(ventana, Constants.CAR_COORDINATES, font1, occupied_spots=sitios_ocupados, license=False)

        itera+=1

        for value in parking.values():
            if value[4]: 
                pygame.draw.rect(ventana, Constants.GREEN, (value[0], value[1], value[-2], value[-1]), 5)
            else:
                pygame.draw.rect(ventana, Constants.RED, (value[0], value[1], value[-2], value[-1]), 5)
        
        # dibujar botón
        dibujar_boton(ventana, boton_rect, "Exit", Constants.RED, Constants.BRIGHT_RED)
        pygame.display.update()
        clock.tick(30)

if __name__ == "__main__":
    main(parking)