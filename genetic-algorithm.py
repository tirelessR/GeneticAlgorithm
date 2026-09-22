import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from math import sin, cos
import random

# Определение максимальных констант
MAX_X = 5
MAX_Y = 5
# Определение минимальных констант
MIN_X = -5
MIN_Y = -5
EPS = 0.2 # Шаг инверсии
POP_SIZE = 100 # Макс. размер популяции
MAX_GEN = 200 # Макс. кол-во генераций
N_ELITE = 5 # Кол-во "элиты"
P_MUT = 0.10 # Шанс мутации
P_INV = 0.30 # Шанс инверсии
EPS_INV = 0.20 # Эпсилон инверсии

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
def select(population, fitness, k=N_ELITE):
    best = None
    best_f = float('inf')

    for _ in range(k):
        i = random.randrange(len(population))
        if fitness[i] < best_f:
            best_f = fitness[i]
            best = population[i]
    return best

# Генетический алгоритм
def genetic_algorithm():
    population = [create_individual() for _ in range(POP_SIZE)]
    history_best = []
    history_mean = []
    best_ever = None
    best_ever_f = float('inf')

    for generation in range(MAX_GEN):
        fitness = [func(ind[0], ind[1]) for ind in population]

        paired = sorted(zip(population, fitness), key=lambda p: p[1])
        population = [p[0] for p in paired]
        fitness = [p[1] for p in paired]

        if fitness[0] < best_ever_f:
            best_ever_f = fitness[0]
            best_ever = population[0]

        history_best.append(fitness[0])
        history_mean.append(sum(fitness) / len(fitness))

        new_population = population[:N_ELITE]
        while len(new_population) < POP_SIZE:
            p1 = select(population, fitness)
            p2 = select(population, fitness)
            child = crossover(p1, p2)

            r = random.random()
            if r < P_MUT:
                child = mutation()
            elif r < P_MUT + P_INV:
                child = inversion(child, EPS_INV)

            new_population.append(child)

        population = new_population

    return best_ever, best_ever_f, history_best, history_mean

best, best_f, hb, hm = genetic_algorithm()

print(f"Найденная точка: x = {best[0]:.4f}, y = {best[1]:.4f}")
print(f"Значение функции: f = {best_f:.4f}")
print(f"Поколений: {len(hb)}")


plt.rcParams['font.family'] = 'DejaVu Sans'
plt.rcParams['axes.unicode_minus'] = False


plt.figure(figsize=(11, 5))

plt.plot(hb, label='Лучшее значение в поколении',
         color='#1f77b4', linewidth=2)

plt.plot(hm, label='Среднее значение по популяции',
         color='#ff7f0e', linewidth=1.5, alpha=0.75)

plt.axhline(y=-5.9589, color='red', linestyle='--', linewidth=1,
            label='Теоретический минимум (-5.9589)')

plt.xlabel('Поколение (эпоха)')
plt.ylabel('f(x, y)')
plt.title('Сходимость генетического алгоритма по эпохам')
plt.legend(loc='upper right')
plt.grid(alpha=0.3)
plt.tight_layout()
plt.savefig("convergence.png", dpi=120, bbox_inches='tight')
plt.close()

fig = plt.figure(figsize=(12, 8))
ax = fig.add_subplot(111, projection='3d')

xs = np.linspace(MIN_X, MAX_X, 150)
ys = np.linspace(MIN_Y, MAX_Y, 150)
X, Y = np.meshgrid(xs, ys)
Z = np.sin(X) * np.cos(Y) + X

surf = ax.plot_surface(X, Y, Z,
                       cmap='viridis',
                       alpha=0.85,
                       linewidth=0,
                       antialiased=True,
                       rstride=2, cstride=2)

ax.scatter(best[0], best[1], best_f,
           color='red', s=120, edgecolor='black', linewidth=1.2,
           label=f'Найденный минимум ({best[0]:.2f}; {best[1]:.2f})',
           zorder=10)

ax.set_xlabel('x')
ax.set_ylabel('y')
ax.set_zlabel('f(x, y)')
ax.set_title('Поверхность f(x, y) = sin(x)·cos(y) + x')
ax.legend(loc='upper left')

fig.colorbar(surf, shrink=0.55, aspect=15, pad=0.1, label='f(x, y)')

plt.tight_layout()
plt.savefig("surface_3d.png", dpi=120, bbox_inches='tight')
plt.close()