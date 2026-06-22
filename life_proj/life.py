import argparse
from pathlib import Path
from PIL import Image, ImageDraw


COLORS = {
    "red": (255, 0, 0),
    "green": (0, 255, 0),
    "blue": (0, 0, 255),
    "yellow": (255, 255, 0),
    "cyan": (0, 255, 255),
    "magenta": (255, 0, 255),
}


def read_field(filename):
    with open(filename, "r", encoding="utf-8") as file:
        lines = [line.strip() for line in file if line.strip()]

    if not lines:
        raise ValueError("Файл пустой")

    width, height = map(int, lines[0].split())

    if len(lines[1:]) != height:
        raise ValueError("Количество строк поля не совпадает с указанной высотой")

    field = []

    for line in lines[1:height + 1]:
        if len(line) != width:
            raise ValueError("Длина строки поля не совпадает с указанной шириной")

        row = []

        for cell in line:
            if cell == "O":
                row.append(1)
            elif cell == ".":
                row.append(0)
            else:
                raise ValueError("Поле может содержать только символы 'O' и '.'")

        field.append(row)

    return field


def count_neighbors(field, y, x):
    height = len(field)
    width = len(field[0])
    count = 0

    for dy in (-1, 0, 1):
        for dx in (-1, 0, 1):
            if dy == 0 and dx == 0:
                continue

            ny = y + dy
            nx = x + dx

            if 0 <= ny < height and 0 <= nx < width:
                if field[ny][nx] > 0:
                    count += 1

    return count


def next_generation(field):
    height = len(field)
    width = len(field[0])

    new_field = [[0] * width for _ in range(height)]

    for y in range(height):
        for x in range(width):
            neighbors = count_neighbors(field, y, x)
            age = field[y][x]

            if age > 0 and neighbors in (2, 3):
                new_field[y][x] = age + 1
            elif age == 0 and neighbors == 3:
                new_field[y][x] = 1

    return new_field


def field_to_text(field):
    lines = []

    for row in field:
        line = "".join("O" if cell > 0 else "." for cell in row)
        lines.append(line)

    return "\n".join(lines)


def age_color(base_color, age):
    factor = max(0.25, 1 - age * 0.08)

    return tuple(int(channel * factor) for channel in base_color)


def save_image(field, filename, base_color, cell_size=20):
    height = len(field)
    width = len(field[0])

    image = Image.new(
        "RGB",
        (width * cell_size, height * cell_size),
        "white"
    )

    draw = ImageDraw.Draw(image)

    for y in range(height):
        for x in range(width):
            age = field[y][x]

            if age > 0:
                color = age_color(base_color, age)

                left = x * cell_size
                top = y * cell_size
                right = left + cell_size - 1
                bottom = top + cell_size - 1

                draw.rectangle(
                    [left, top, right, bottom],
                    fill=color,
                    outline="gray"
                )

    image.save(filename)


def main():
    parser = argparse.ArgumentParser(
        description="Консольная реализация игры Жизнь"
    )

    parser.add_argument("input_file")
    parser.add_argument("--steps", type=int, required=True)
    parser.add_argument("--output", default="result.txt")
    parser.add_argument("--images", default="images")
    parser.add_argument("--color", default="green", choices=COLORS.keys())
    parser.add_argument("--cell-size", type=int, default=20)

    args = parser.parse_args()

    if args.steps < 0:
        raise ValueError("Количество шагов не может быть отрицательным")

    if args.cell_size <= 0:
        raise ValueError("Размер клетки должен быть положительным")

    field = read_field(args.input_file)
    base_color = COLORS[args.color]

    images_dir = Path(args.images)
    images_dir.mkdir(parents=True, exist_ok=True)

    with open(args.output, "w", encoding="utf-8") as file:
        for generation in range(args.steps + 1):
            file.write(f"Generation {generation}\n")
            file.write(field_to_text(field))
            file.write("\n\n")

            image_name = images_dir / f"generation_{generation}.png"
            save_image(field, image_name, base_color, args.cell_size)

            field = next_generation(field)

    print("Готово!")


if __name__ == "__main__":
    main()