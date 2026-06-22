import math


# Перевод ярдов в футы
def yards_to_feet(yards):
    return yards * 3


# Перевод скорости из миль/час в футы/секунду
def speed_to_feet_per_second(speed):
    return speed * 5280 / 3600


# Вычисление времени для одного угла
def calculate_time(d1, d2, h, v_sand, n, theta):
    d1 = yards_to_feet(d1)
    h = yards_to_feet(h)

    theta = math.radians(theta)

    x = d1 * math.tan(theta)

    l1 = math.sqrt(x ** 2 + d1 ** 2)
    l2 = math.sqrt((h - x) ** 2 + d2 ** 2)

    v_sand = speed_to_feet_per_second(v_sand)

    t = (l1 + n * l2) / v_sand

    return t


# Подбор лучшего угла обычным перебором
def find_best_angle_by_loop(d1, d2, h, v_sand, n, step):
    d1_feet = yards_to_feet(d1)
    h_feet = yards_to_feet(h)

    max_angle = math.degrees(math.atan(h_feet / d1_feet))

    best_angle = 0
    best_time = calculate_time(d1, d2, h, v_sand, n, best_angle)

    angle = 0

    while angle <= max_angle:
        current_time = calculate_time(d1, d2, h, v_sand, n, angle)

        if current_time < best_time:
            best_time = current_time
            best_angle = angle

        angle += step

    # на всякий случай проверяем самый последний возможный угол
    current_time = calculate_time(d1, d2, h, v_sand, n, max_angle)

    if current_time < best_time:
        best_time = current_time
        best_angle = max_angle

    return best_angle, best_time


# Левая часть аналитической формулы:
# h = d1 * tg(theta) + d2 * sin(theta) / sqrt(n^2 - sin^2(theta))
def formula_left_part(d1_feet, d2_feet, n, theta):
    s = math.sin(theta)

    result = (
        d1_feet * math.tan(theta)
        + d2_feet * s / math.sqrt(n ** 2 - s ** 2)
    )

    return result


# Угол по аналитической формуле
# Здесь мы не перебираем все углы, а ищем ответ по формуле методом половинного деления
def find_angle_by_formula(d1, d2, h, n):
    d1_feet = yards_to_feet(d1)
    h_feet = yards_to_feet(h)

    if h_feet == 0:
        return 0

    left = 0
    right = math.atan(h_feet / d1_feet)

    for i in range(100):
        middle = (left + right) / 2

        value = formula_left_part(d1_feet, d2, n, middle)

        if value < h_feet:
            left = middle
        else:
            right = middle

    theta = (left + right) / 2

    return math.degrees(theta)


# Тесты
assert yards_to_feet(1) == 3
assert yards_to_feet(5) == 15

assert round(speed_to_feet_per_second(1), 3) == 1.467

assert round(
    calculate_time(8, 10, 50, 5, 2, 39.413),
    1
) == 39.9

test_angle, test_time = find_best_angle_by_loop(8, 10, 50, 5, 2, 0.01)
assert round(test_angle, 1) == 80.6
assert round(test_time, 1) == 23.1

test_formula_angle = find_angle_by_formula(8, 10, 50, 2)
assert round(test_formula_angle, 1) == 80.6

print("Тесты пройдены")


# Ввод данных
d1 = float(input(
    "Введите кратчайшее расстояние между спасателем и кромкой воды, d1 (ярды) => "
))

d2 = float(input(
    "Введите кратчайшее расстояние от утопающего до берега, d2 (футы) => "
))

h = float(input(
    "Введите боковое смещение между спасателем и утопающим, h (ярды) => "
))

v_sand = float(input(
    "Введите скорость движения спасателя по песку, v_sand (мили в час) => "
))

n = float(input(
    "Введите коэффициент замедления спасателя при движении в воде, n => "
))


if d1 <= 0 or d2 <= 0 or h < 0 or v_sand <= 0 or n < 1:
    print("Ошибка: d1, d2, v_sand должны быть больше 0, h не меньше 0, n не меньше 1")
else:
    step = 0.01

    best_angle, best_time = find_best_angle_by_loop(d1, d2, h, v_sand, n, step)

    formula_angle = find_angle_by_formula(d1, d2, h, n)
    formula_time = calculate_time(d1, d2, h, v_sand, n, formula_angle)

    print()
    print("Численное решение перебором:")
    print(f"Лучший угол: {best_angle:.3f} градусов")
    print(f"Минимальное время: {best_time:.1f} секунд")

    print()
    print("Решение по аналитической формуле:")
    print(f"Угол: {formula_angle:.3f} градусов")
    print(f"Время: {formula_time:.1f} секунд")

    print()
    print("Сравнение:")
    print(f"Разница углов: {abs(best_angle - formula_angle):.6f} градусов")
    print(f"Разница времени: {abs(best_time - formula_time):.6f} секунд")