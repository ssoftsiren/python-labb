import math
import zip_util


EARTH_RADIUS_MILES = 3959.2


def is_good_zip(zip_code):
    return len(zip_code) == 5 and zip_code.isdigit()


def make_dictionaries(zip_codes):
    zip_by_code = {}
    zip_by_city_state = {}

    for row in zip_codes:
        zip_code = row[0]
        latitude = row[1]
        longitude = row[2]
        city = row[3]
        state = row[4]
        county = row[5]

        data = {
            "zip_code": zip_code,
            "latitude": latitude,
            "longitude": longitude,
            "city": city,
            "state": state,
            "county": county
        }

        zip_by_code[zip_code] = data

        key = (city.lower(), state.lower())

        if key not in zip_by_city_state:
            zip_by_city_state[key] = []

        zip_by_city_state[key].append(zip_code)

    return zip_by_code, zip_by_city_state


def decimal_to_dms(number, is_latitude):
    if is_latitude:
        direction = "N" if number >= 0 else "S"
    else:
        direction = "E" if number >= 0 else "W"

    number = abs(number)

    total_seconds = round(number * 3600, 2)

    degrees = int(total_seconds // 3600)
    total_seconds = total_seconds - degrees * 3600

    minutes = int(total_seconds // 60)
    seconds = total_seconds - minutes * 60

    return f"{degrees:03d}°{minutes:02d}'{seconds:05.2f}\"{direction}"


def command_loc(zip_by_code):
    zip_code = input("Enter a ZIP Code to lookup => ").strip()

    if not is_good_zip(zip_code):
        print("Invalid ZIP Code")
        return

    if zip_code not in zip_by_code:
        print("ZIP Code not found")
        return

    data = zip_by_code[zip_code]

    latitude = decimal_to_dms(data["latitude"], True)
    longitude = decimal_to_dms(data["longitude"], False)

    print(
        f"ZIP Code {zip_code} is in "
        f"{data['city']}, {data['state']}, {data['county']} county,"
    )
    print(f"coordinates: ({latitude},{longitude})")


def command_zip(zip_by_city_state):
    city = input("Enter a city name to lookup => ").strip()
    state = input("Enter the state name to lookup => ").strip()

    key = (city.lower(), state.lower())

    if key not in zip_by_city_state:
        print("No ZIP Code found")
        return

    zip_codes = sorted(zip_by_city_state[key])

    print(
        f"The following ZIP Code(s) found for "
        f"{city.title()}, {state.upper()}: {', '.join(zip_codes)}"
    )


def calculate_distance(lat1, lon1, lat2, lon2):
    lat1 = math.radians(lat1)
    lon1 = math.radians(lon1)
    lat2 = math.radians(lat2)
    lon2 = math.radians(lon2)

    delta_lat = lat2 - lat1
    delta_lon = lon2 - lon1

    a = (
        math.sin(delta_lat / 2) ** 2
        + math.cos(lat1) * math.cos(lat2) * math.sin(delta_lon / 2) ** 2
    )

    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

    return EARTH_RADIUS_MILES * c


def command_dist(zip_by_code):
    zip_code_1 = input("Enter the first ZIP Code => ").strip()
    zip_code_2 = input("Enter the second ZIP Code => ").strip()

    if not is_good_zip(zip_code_1) or not is_good_zip(zip_code_2):
        print("Invalid ZIP Code")
        return

    if zip_code_1 not in zip_by_code or zip_code_2 not in zip_by_code:
        print("ZIP Code not found")
        return

    data_1 = zip_by_code[zip_code_1]
    data_2 = zip_by_code[zip_code_2]

    distance = calculate_distance(
        data_1["latitude"],
        data_1["longitude"],
        data_2["latitude"],
        data_2["longitude"]
    )

    print(
        f"The distance between {zip_code_1} and {zip_code_2} "
        f"is {distance:.2f} miles"
    )


def main():
    zip_codes = zip_util.read_zip_all()
    zip_by_code, zip_by_city_state = make_dictionaries(zip_codes)

    while True:
        command = input("Command ('loc', 'zip', 'dist', 'end') => ").strip().lower()

        if command == "loc":
            command_loc(zip_by_code)
        elif command == "zip":
            command_zip(zip_by_city_state)
        elif command == "dist":
            command_dist(zip_by_code)
        elif command == "end":
            print("Done")
            break
        else:
            print("Invalid command, ignoring")


main()