from math import sin, cos
import random

# Определение максимальных констант
MAX_X = 5
MAX_Y = 5

# Определение минимальных констант
MIN_X = -5
MIN_Y = -5

# Определение функции
def func(x, y):
    return sin(x) * cos(y) + x

# Создаём случайную особь
def create_individual():
    individual = [random.uniform(MIN_X, MAX_X),
                  random.uniform(MIN_Y, MAX_Y)]
    return individual

def crossover(parent1, parent2):
    child = [(parent1[0] + parent2[0]) / 2,
             (parent1[1] + parent2[1]) / 2]
    return child

