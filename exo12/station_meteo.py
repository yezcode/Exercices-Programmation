exercice1.py
# importer le module sense hat
from sense_hat import SenseHat
import math

# creer une variable qui va stocker la couleur bleu
blue_color = [27, 176, 241]
orange_color = [241, 69, 27]
black_color = [0, 0, 0]

# creer une variable sense_hat 
sense = SenseHat()

# afficher "Station méteo"
sense.show_message("Station meteo", text_colour=blue_color, scroll_speed=0.05)

# creer une variable temperature
temperature = math.ceil(sense.get_temperature())

sense.set_pixel(0, 0, orange_matrice)


exercice2.py
# importer le module sense hat
from sense_hat import SenseHat
import math

# creer une variable qui va stocker la couleur bleu
blue_color = [27, 176, 241]
orange_color = [241, 69, 27]
black_color = [0, 0, 0]
red_color = [236, 25, 12]

# creer une variable sense_hat 
sense = SenseHat()

# afficher "Station méteo"
# sense.show_message("Station meteo", text_colour=blue_color, scroll_speed=0.05)

# boucle infini
while True:

  # creer une variable temperature
  temperature = math.ceil(sense.get_temperature())
  
  
  # verifier la temperature 
  if temperature <= 15:
    blue_matrice = [blue_color] * 64
    sense.set_pixels(blue_matrice)
  elif temperature < 40:
    orange_matrice = [orange_color] * 64
    sense.set_pixels(orange_matrice)
  elif temperature >= 40:
    red_matrice = [red_color] * 64
    sense.set_pixels(red_matrice)

exercice3.py
# importer le module sense hat
from sense_hat import SenseHat
import math

# creer une variable qui va stocker la couleur bleu
blue_color = [27, 176, 241]
orange_color = [241, 69, 27]
black_color = [0, 0, 0]
red_color = [236, 25, 12]

# creer une variable sense_hat 
sense = SenseHat()

B = blue_color
O = orange_color
X = black_color
R = red_color

# afficher "Station méteo"
# sense.show_message("Station meteo", text_colour=blue_color, scroll_speed=0.05)

water_image = [
  X, X, X, X, X, X, X, X,
  X, X, X, B, B, X, X, X,
  X, X, X, B, B, X, X, X,
  X, X, B, B, B, B, X, X,
  X, X, B, B, B, B, X, X,
  X, X, B, B, B, B, X, X,
  X, X, X, B, B, X, X, X,
  X, X, X, X, X, X, X, X
]

# boucle infini
while True:

  # creer une variable pour recuperer l'humidité
  humidity = sense.get_humidity()
  
  if humidity > 45:
    # afficher une image de goutte d'eau
    sense.set_pixels(water_image)
  else:
    sense.clear()
    