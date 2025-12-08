# Generated an artistic representation of the night sky from data taken from audio features within a given Spotify playlist

import random
import pygame
import csv


from visual_objects import Moon, Star

# if __main__ statement used - entry point
if __name__ == "__main__":
    pygame.init()

    #set up the display
    width, height = 800, 600
    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption("Betelgeuse")

    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)

    # Created the lists for the columns of csv data used from Spotify playlist tracks

    danceability = []
    key = []
    energy = []
    tempo = []

    # Importing csv dataset of Spotify audio features of songs from a given playlist "2025"

    with open('2025.csv', newline='') as csvfile:
        file = csv.reader(csvfile, delimiter=',', quotechar='"')
        next(file)
        for row in file:
            danceability.append(float(row[12]))
            key.append(int(row[14]))
            energy.append(float(row[13]))
            tempo.append(float(row[22]))

        # dance is column #12
        # energy is #13
        # tempo is #22
        # key is 14
        # speechiness is 17

    StarList = []

    for i in range(len(danceability)): # goes through every row in csv file, pulls danceability & key values, then uses the class, Star, inputs those things (4) into the parameters from the class
        dance = danceability[i] 
        key_value = key[i]
        new_star = Star(random.randint(0, width), random.randint(0, height), key_value, dance)
        StarList.append(new_star) # adds a new star to the end of the list for every song in  csv file

    # defining (inatializing) variables of average energy and average tempo from the sum of all the energy and tempo values respectively

    sum_energy = sum(energy)
    sum_tempo = sum(tempo)

    average_energy = sum_energy / len(energy)
    average_tempo = sum_tempo / len(tempo)

    # for testing
    # print("Avg energy:", average_energy)
    # print("Avg tempo:", average_tempo)

    # creating an instance of the Moon
    moon = Moon(average_energy * width, average_energy * height, average_tempo)

    # Game loop (main loop)
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        
        screen.fill((0, 0, 10))

        for star in StarList:
            star.update()
            star.display(screen)

        # getting the time in milliseconds (found function in pygame website resource) used to help animate the Moon
        moon.update(pygame.time.get_ticks())
        moon.display(screen)

        pygame.display.flip() 

    pygame.quit()