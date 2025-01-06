import random 
import math
import matplotlib.pyplot as plt
from matplotlib.patches import Circle

numCircles = 20
width = 50
height = 50
solidCircles = []

def validateCollision(newCircle : Circle): # Averigua si se choca el nuevo circulo con alguno existente
    for oldCircle in solidCircles:
        x1,y1 = newCircle.center
        x2,y2 = oldCircle.center
        a = abs(x1 - x2)
        b = abs(y1 - y2)
        distance = math.sqrt(a**2 + b**2)
        if distance <= (newCircle.radius + oldCircle.radius):
            return True
    return False

def validCircle(newCircle : Circle): # Valida el radio y posición de un circulo
    x,y = newCircle.center
    aboveAxis = (y + newCircle.radius)>=height or (x + newCircle.radius)>=width # Valida que no se pase de la altura y anchura maximos
    belowAxis = (y - newCircle.radius)<=0 or (x - newCircle.radius)<=0 # Valida que el circulo no pase de los limites inferiores
    if belowAxis or aboveAxis or validateCollision(newCircle):
        return False
    else:
        return True

def createCircle(radius : float): # Crea un circulo con un radio máximo
    newCircle = Circle((random.randrange(width),random.randrange(height)),random.randrange(1,radius), facecolor = "White", edgecolor = "Black")
    if validCircle(newCircle) == False:
        newCircle = createCircle(radius)
    return newCircle

def randomCircles(seed :int , radius : float):
    (random.seed(numCircles),random.seed(seed)) # Con esto hago que los circulos generdos por randomCircles sean replicables
    for _ in range(numCircles):
        newCircle = createCircle(radius)
        solidCircles.append(newCircle)
        # print(newCircle.center)
    return solidCircles

def plotCircles(obstacles: list,num: int,text: str): 
    fig, ax = plt.subplots(figsize=(5, 5))
    for i in range(num): # Ciclo que va colocando los circulos en el plot
        obstacle = list(obstacles)[i]
        ax.add_patch(obstacle)
    plt.xlim(0, width)
    plt.ylim(0, height) 
    text_kwargs = dict(ha='center', va='center', fontsize=10, color='BLack')
    plt.text(0, height+3, text, **text_kwargs)
    ax.set_aspect('equal', adjustable='box')
    plt.show()

if __name__== "__main__":
    obstacles = randomCircles(1234,10)
    plotCircles(obstacles,numCircles,"")