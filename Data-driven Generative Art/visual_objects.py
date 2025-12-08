from math import sin
import random
import pygame

WHITE = (255, 255, 255)

class Star:
    """
    1st class created to represent the visual element of "Stars"
    The size of the star is based off of the numeric value of the key of the audio track (but multiplied by 0.16 and 1 is added, as some songs key is "0")
    The brightness of the star is determined by the danceability
    To make the stars "twinkle", brightness is updated by an additional attribute (max brightness - also determined by danceability) - but then a random integer is chosen based off of this value
    """
    def __init__(self, x, y, key, danceability):
        self.x = x
        self.y = y
        self.diameter = (key*0.16) + 1
        self.max_brightness = int(danceability * 255)
        self.brightness = (danceability*255, danceability*255, danceability*255)

    def display(self, screen):
        pygame.draw.circle(screen, self.brightness, (self.x, self.y), self.diameter)

    def update(self):
        new_brightness = random.randint(0, self.max_brightness)
        self.brightness = (new_brightness, new_brightness, new_brightness)

class Moon:
    """
    2nd class created to represent the visual element of a "Moon"
    The position of the Moon is determined by the average energy of the audio tracks
    Created an animation of the moon rising and setting - used Claude to give example snippet 
    """
    def __init__(self, energy_x, energy_y, avg_tempo):
        self.x = energy_x
        self.y = energy_y

        self.y_offset = 0
        self.avg_tempo = avg_tempo

    def display(self, screen):
        pygame.draw.circle(screen, WHITE, (self.x, self.y + self.y_offset), 40)

    def update(self, time):
         self.y_offset = sin(time * 0.001) * self.avg_tempo