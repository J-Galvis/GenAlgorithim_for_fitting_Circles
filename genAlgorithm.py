"""
Algoritmo genético

De : Juan Camilo Galvis Agudelo

Se realizaron los siguientes cambios en el código GA (uno por uno) y estos serían los resultados.

    Cambiar los puntos de partida iniciales (soluciones iniciales) diez veces:
    Esto llevo a ningun cambio en el resultado final.

    Cambiar la probabilidad de cruce dos veces:
    Afecta la consistencia del algoritmo, ya que en ocasiones llegará al resultado más optimo, 
    y en otras al no haber pocos cruces lleva a poca mutación, lo que nos da discos con radios pequeños.

    Cambiar la probabilidad de mutación dos veces:
    Esto afecta la consistencia del algoritmo, ya que en ocasiones llegará al resultado más optimo, 
    y en otras al no haber poca mutación nos da discos con radios pequeños.

    Cambiar el tamaño de la población dos veces:
    Esto afecta la capacidad de resolución del problema, dandonos discos más pequeños.

    Cambie la semilla del número aleatorio diez veces: 
    Al hacer esto se demostro que el algoritmo cumple con encontrar el disco de mayor radio 
    que se puede colocar entre estos discos independientemente de su posición.

"""

from circleCreator  import *

import random
import numpy

from deap import algorithms
from deap import base
from deap import creator
from deap import tools

seed = 1220 # Con seed garantizo que los random sean replicables
NGen = 1000
population = 100

obstacles = randomCircles(seed,10) # Creo los "obstáculos", que son los circulos blancos.

def evalCircle(individual):
    sum_ = 0
    x,y,radius = individual
    newCircle = Circle((x,y),radius, facecolor = "Red", edgecolor = "Black")

    if validCircle(newCircle) == True: # Así me aseguro que siempre que el circulo sea válido, se evalue su radio.
        sum_ = radius

    return (sum_,)

creator.create("FitnessMin", base.Fitness, weights=(1,))
creator.create("Individual", list, fitness=creator.FitnessMin)

toolbox = base.Toolbox()
toolbox.register("permutation", random.sample, range(height), 3)
toolbox.register("individual", tools.initIterate, creator.Individual, toolbox.permutation)
toolbox.register("population", tools.initRepeat, list, toolbox.individual)
toolbox.register("evaluate", evalCircle)

# Executes a two-point crossover on the input sequence individuals. The two individuals are modified in place and both keep their original length.
toolbox.register("mate",tools.cxOnePoint)

#Mutate an individual by replacing attributes, with probability indpb, by a integer uniformly drawn between low and up inclusively.
toolbox.register("mutate", tools.mutUniformInt, low=0, up=height, indpb=0.5)
toolbox.register("select", tools.selTournament, tournsize=int(population/3))

def main(seed=0):
    random.seed(seed)
    
    pop = toolbox.population(population)
    hof = tools.HallOfFame(1)
    stats = tools.Statistics(lambda ind: ind.fitness.values)
    stats.register("Avg", numpy.mean)
    stats.register("Std", numpy.std)
    stats.register("Min", numpy.min)
    stats.register("Max", numpy.max)

    algorithms.eaSimple(pop, toolbox, cxpb=0.5, mutpb=0.5, ngen=NGen, stats=stats,halloffame=hof, verbose=True)

    return hof

if __name__ == "__main__":
    x,y,radius = main()[0]
    newCircle = Circle((x,y),radius, facecolor = "Red", edgecolor = "Black")
    solidCircles.append(newCircle)
    texto = "Radio : " + str(newCircle.radius) +"\n         Centro : "+ str(newCircle.center) 
    plotCircles(obstacles,len(solidCircles),texto)