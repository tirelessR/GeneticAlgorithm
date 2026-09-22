from math import sin, cos
import random

# Определение максимальных констант
MAX_X = 5
MAX_Y = 5
# Определение минимальных констант
MIN_X = -5
MIN_Y = -5
# Шаг инверсии
EPS = 0.2

# Определение функции
def func(x, y):
    return sin(x) * cos(y) + x

# Создаём случайную особь
def create_individual():
    individual = [random.uniform(MIN_X, MAX_X),
                  random.uniform(MIN_Y, MAX_Y)]
    return individual

# Кроссовер
def crossover(parent1, parent2):
    child = [(parent1[0] + parent2[0]) / 2,
             (parent1[1] + parent2[1]) / 2]
    return child

# Мутация
def mutation():
    return create_individual()

# Инверсия
def inversion(ind, eps):
    sign_x = random.choice([-1, 1])
    new_x = ind[0] + sign_x * eps
    new_x = max(MIN_X, min(MAX_X, new_x))

    sign_y = random.choice([-1, 1])
    new_y = ind[1] + sign_y * eps
    new_y = max(MIN_Y, min(MAX_Y, new_y))

    return [new_x, new_y]

#
# Реализация самого ГА
#
# Функция селекции (выбор k случайных особей из популяции)
def select(population, fitness, k=5):
    best = None
    best_f = float('inf')

    for _ in range(k):
        i = random.randrange(len(population))
        if fitness[i] < best_f:
            best_f = fitness[i]
            best = population[i]
    return best