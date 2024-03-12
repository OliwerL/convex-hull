import numpy as np
import matplotlib.pyplot as plt


class Tiger:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.b = 2
        self.beta = np.random.randint(0, 31) * (np.pi / 180)
        self.gama = np.random.randint(0, 46) * (np.pi / 180)
        self.a = np.random.randint(1, 11)
        self.alfa = np.random.randint(0, 360) * (np.pi / 180)
        self.points = self.generate_points()


    def get_position(self):
        """Zwraca aktualną pozycję Tigera."""
        return (f'{self.x}, {self.y}')

    def generate_points(self):
        original_points = [
            (self.x + self.a, self.y + self.a),
            (self.x - self.a, self.y + self.a),
            (self.x, self.y),
        ]
        original_points_2 = [
            (self.x + self.b, self.y + self.b),

        ]
        original_points_3 = [
            (self.x + self.b, self.y + self.b),
        ]

        rotated_points = []
        for x, y in original_points:
            # Przesunięcie punktów, aby środek obrotu był w (0,0)
            x_shifted, y_shifted = x - self.x, y - self.y
            print(x_shifted, y_shifted)

            # Rotacja
            x_rotated = x_shifted * np.cos(self.alfa) - y_shifted * np.sin(self.alfa)
            y_rotated = x_shifted * np.sin(self.alfa) + y_shifted * np.cos(self.alfa)

            # Przesunięcie z powrotem
            x_rotated += self.x
            y_rotated += self.y

            rotated_points.append((x_rotated, y_rotated))

        for x, y in original_points_2:
            # Przesunięcie punktów, aby środek obrotu był w (0,0)
            x_shifted, y_shifted = x - self.x, y - self.y
            print(x_shifted, y_shifted)

            # Rotacja
            x_rotated = x_shifted * np.cos(self.alfa + self.gama + np.pi/2) - y_shifted * np.sin(self.alfa + self.gama + np.pi/2)
            y_rotated = x_shifted * np.sin(self.alfa + self.gama + np.pi/2) + y_shifted * np.cos(self.alfa + self.gama + np.pi/2)

            # Przesunięcie z powrotem
            x_rotated += self.x
            y_rotated += self.y

            x2_rotated = x_shifted * np.cos(self.alfa + self.gama + np.pi) - y_shifted * np.sin(self.alfa + self.gama + np.pi)
            y2_rotated = x_shifted * np.sin(self.alfa + self.gama + np.pi) + y_shifted * np.cos(self.alfa + self.gama + np.pi)
            x2_rotated += self.x
            y2_rotated += self.y
            xs = self.x
            ys = self.y
            rotated_points.append((x_rotated, y_rotated))
            rotated_points.append((x2_rotated, y2_rotated))
            rotated_points.append((xs,ys))

        for x, y in original_points_3:
            x_shifted, y_shifted = x - self.x, y - self.y
            print(x_shifted, y_shifted)

            x_rotated = x_shifted * np.cos(self.alfa - self.gama) - y_shifted * np.sin(
                self.alfa - self.gama)
            y_rotated = x_shifted * np.sin(self.alfa - self.gama) + y_shifted * np.cos(
                self.alfa - self.gama)

            x_rotated += self.x
            y_rotated += self.y

            x2_rotated = x_shifted * np.cos(self.alfa - self.gama - np.pi/2) - y_shifted * np.sin(
                self.alfa - self.gama - np.pi/2)
            y2_rotated = x_shifted * np.sin(self.alfa - self.gama - np.pi/2) + y_shifted * np.cos(
                self.alfa - self.gama - np.pi/2)
            x2_rotated += self.x
            y2_rotated += self.y
            xs = self.x
            ys = self.y
            rotated_points.append((x_rotated, y_rotated))
            rotated_points.append((x2_rotated, y2_rotated))
            rotated_points.append((xs, ys))

        return rotated_points

    def move_points(self):
        moved_points = []
        for x, y in self.points:
            dx = np.cos(self.alfa) * 10
            dy = np.sin(self.alfa) * 10

            moved_x = x + dx
            moved_y = y + dy

            moved_points.append((moved_x, moved_y))

        return moved_points


def generate_random_tigers():
    points = np.random.rand(20, 2) * 100
    tigers = []
    for x, y in points:
        tigers.append(Tiger(int(x), int(y)))

    return tigers


def collect_all_points(random_tigers):
    all_points = []
    for tiger in random_tigers:
        all_points.extend(tiger.points)
    return all_points


def lowest_point(random_tigers):
    point = random_tigers[0]
    for tiger in random_tigers:
        if tiger.y < point.y:
            point = tiger
        elif tiger.y == point.y and tiger.x < point.x:
            point = tiger
    return point


def lowest_point_from_points(all_points):
    lowest_point = all_points[0]

    for point in all_points:

        if point[1] < lowest_point[1] or (point[1] == lowest_point[1] and point[0] < lowest_point[0]):
            lowest_point = point

    return lowest_point


def orientation(p1, p2, p3):
    first_diff = (p2.y - p1.y) * (p3.x - p2.x)
    second_diff = (p2.x - p1.x) * (p3.y - p2.y)
    value = first_diff - second_diff
    if value == 0:
        return 0
    elif value > 0:
        return 1
    else:
        return -1


def orientation_all_points(p1, p2, p3):
    x1, y1 = p1
    x2, y2 = p2
    x3, y3 = p3

    first_diff = (y2 - y1) * (x3 - x2)
    second_diff = (x2 - x1) * (y3 - y2)
    value = first_diff - second_diff

    if value == 0:
        return 0
    elif value > 0:
        return 1
    else:
        return -1




def find_next_point(start, tigers):
    p2 = tigers[0]
    if p2 == start:
        p2 = tigers[1]
    for p3 in tigers:
        if p3 == start or p3 == p2:
            continue
        # Sprawdź, czy p3 jest bardziej po prawej stronie niż p2 względem start
        # Używając orientation(start, p2, p3), 1 oznacza, że p3 jest po prawej
        if orientation_all_points(start, p2, p3) == 1:
            p2 = p3  # Jeśli tak, zaktualizuj p2 na p3

    return p2


def find_next_point_all(start, all_points):
    p2 = all_points[0]
    if p2 == start:
        p2 = all_points[1]
    for p3 in all_points:
        if p3 == start or p3 == p2:
            continue
        if orientation_all_points(start, p2, p3) == 1:
            p2 = p3
    return p2


def draw_point(tigers):
    x = []
    y = []
    for tiger in tigers:
        x.append(tiger.x)
        y.append(tiger.y)
    plt.scatter(x, y, color = 'blue')


def draw_line(x1, y1, x2, y2):
    plt.plot([x1, x2], [y1, y2], color='red')


def draw_tiger(tiger):
  points = tiger.points
  points.append(tiger.points[0])
  for i in range(len(points) - 1):
      x1, y1 = points[i]
      x2, y2 = points[i + 1]
      plt.plot([x1, x2], [y1, y2], color='green')


moving = True
random_tigers = generate_random_tigers()
while moving:
    all_points = collect_all_points(random_tigers)
    start_point = lowest_point_from_points(all_points)
    starting_point = start_point
    condition = True
    draw_point(random_tigers)
    for tiger in random_tigers:
        draw_tiger(tiger)

    while condition:
        # Wywołaj funkcję find_next_point, aby znaleźć kolejny punkt na prawo
        next_point = find_next_point_all(start_point, all_points)
        if not next_point or next_point == starting_point:
            draw_line(start_point[0], start_point[1], starting_point[0], starting_point[1])
            condition = False
        else:
            draw_line(start_point[0], start_point[1], next_point[0], next_point[1])
            start_point = next_point
    for tiger in random_tigers:
        tiger.points = tiger.move_points()
    plt.axis('equal')
    plt.show()

