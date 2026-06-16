import math

d1 = float(input())
d2 = float(input())
h = float(input())
v_sand = float(input())
n = float(input())
theta1 = float(input())

d1 *= 3
h *= 3

theta1_rad = theta1 * math.pi / 180

x = d1 * math.tan(theta1_rad)

L1 = (x ** 2 + d1 ** 2) ** 0.5
L2 = ((h - x) ** 2 + d2 ** 2) ** 0.5

v_sand = v_sand * 5280 / 3600

t = (L1 + n * L2) / v_sand

print(
    f"Если спасатель начнёт движение под углом theta1, "
    f"равным {int(theta1)} градусам, "
    f"он достигнет утопающего через {t:.1f} секунд"
)