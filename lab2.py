import math


# Перевод ярдов в футы
def yards_to_feet(yards):
    return yards * 3


# Перевод скорости из миль/час в футы/секунду
def speed_to_feet_per_second(speed):
    return speed * 5280 / 3600


# Вычисление времени
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


# Тесты
assert yards_to_feet(1) == 3
assert yards_to_feet(5) == 15

assert round(speed_to_feet_per_second(1), 3) == 1.467

assert round(
    calculate_time(8, 10, 50, 5, 2, 39.413),
    1
) == 39.9

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

theta1 = float(input(
    "Введите направление движения спасателя по песку, theta1 (градусы) => "
))


# Вычисление и вывод результата
time = calculate_time(d1, d2, h, v_sand, n, theta1)

print(
    f"Если спасатель начнёт движение под углом theta1, "
    f"равным {int(theta1)} градусам, "
    f"он достигнет утопающего через {time:.1f} секунд"
)
