import tkinter as tk
from math import sin, cos
import math
import numpy as np

height = 600
width = 600


def shift(num=4, dist=height / 2):
    m = np.matrix([[dist, dist, 0, 0]])
    for i in range(num - 1):
        m = np.vstack([m, [dist, dist, 0, 0]])

    return m

def Ty(Q):
    Q = math.radians(Q)
    return np.matrix([[cos(Q), 0, -sin(Q), 0],
                [0, 1, 0, 0],
                [sin(Q), 0, cos(Q), 0],
                [0, 0, 0, 1]])

def Tx(Q):
    Q = math.radians(Q)
    return np.matrix([[1, 0, 0, 0],
                [0, cos(Q), sin(Q), 0],
                [0, -sin(Q), cos(Q), 0],
                [0, 0, 0, 1]])

def Tz(Q):
    Q = math.radians(Q)
    return np.matrix([[cos(Q), sin(Q), 0, 0],
                [-sin(Q), cos(Q), 0, 0],
                [0, 0, 1, 0],
                [0, 0, 0, 1]])

def T0():
    return np.matrix([[1,0,0,0],
                      [0,1,0,0],
                      [0,0,0,0],
                      [0,0,0,1]])

def osY_matrix(length=300, arrow=10, period=20):
    m = np.matrix([[0, 0, 0, 1],
                   [0, length, 0, 1],
                   [-10, length - arrow, 0, 1],
                   [10, length - arrow, 0, 1], ])

    for i in range(1, round(length // period)):
        m = np.vstack([m, [-arrow / 2, i * period, 0, 1]])
        m = np.vstack([m, [arrow / 2, i * period, 0, 1]])

    return m


def draw_os(y, canvas, name, length=height / 2):
    canvas.create_line(y[0, 0], y[0, 1], y[1, 0], y[1, 1], width=2, fill="grey")
    canvas.create_line(y[2, 0], y[2, 1], y[1, 0], y[1, 1], width=2, fill="grey")
    canvas.create_line(y[3, 0], y[3, 1], y[1, 0], y[1, 1], width=2, fill="grey")

    for i in range(4, len(y), 2):
        canvas.create_line(y[i, 0], y[i, 1], y[i + 1, 0], y[i + 1, 1], width=2, fill="grey")
        canvas.create_text(y[i, 0] - 4, y[i, 1], text=str(int((i - 2) / 2)))

    canvas.create_text(y[1, 0] - 15, y[1, 1], text=name, font=("DejavuSansLight", 15, 'bold'))


def draw_XYZ(canvas, length=height / 2, period=20, mode="iso"):
    y = osY_matrix(length=length, period=period)
    y = y * Tx(180)

    x = y * Tz(90) * Tx(90)
    z = x * Ty(90)
    y = y * Ty(-45)

    z[0, 2] = 120
    x = metric(x, mode)
    y = metric(y, mode)
    z = metric(z, mode)

    draw_os(y, canvas, 'y', length)
    draw_os(x, canvas, 'x', length)
    draw_os(z, canvas, 'z', length)

    canvas.create_text(y[0, 0] - 8, y[0, 1], text=str(0))


def metric(obj, mode = "iso"):
    if mode == 'iso':
        return obj*Ty(45)*Tx(35.2) + shift(len(obj))
    else:
        return obj*Ty(22.208)*Tx(20.705) + shift(len(obj))


def draw_parallelepiped(canvas, period=40, mode="iso"):
    m = np.matrix([[0, 0, 0, 1],
                   [0, 1, 0, 1],
                   [1, 1, 0, 1],
                   [1, 0, 0, 1],
                   [0, 0, 1, 1],
                   [0, 1, 1, 1],
                   [1, 1, 1, 1],
                   [1, 0, 1, 1], ]) * period
    m = m * Tx(180)
    m = metric(m, mode)

    canvas.create_line(m[0, 0], m[0, 1], m[1, 0], m[1, 1], width=2, fill="black")
    canvas.create_line(m[1, 0], m[1, 1], m[2, 0], m[2, 1], width=2, fill="black")
    canvas.create_line(m[2, 0], m[2, 1], m[3, 0], m[3, 1], width=2, fill="black")
    canvas.create_line(m[3, 0], m[3, 1], m[0, 0], m[0, 1], width=2, fill="black")

    canvas.create_line(m[4, 0], m[4, 1], m[5, 0], m[5, 1], width=2, fill="black")
    canvas.create_line(m[5, 0], m[5, 1], m[6, 0], m[6, 1], width=2, fill="black")
    canvas.create_line(m[6, 0], m[6, 1], m[7, 0], m[7, 1], width=2, fill="black")
    canvas.create_line(m[7, 0], m[7, 1], m[4, 0], m[4, 1], width=2, fill="black")

    canvas.create_line(m[0, 0], m[0, 1], m[4, 0], m[4, 1], width=2, fill="black")
    canvas.create_line(m[1, 0], m[1, 1], m[5, 0], m[5, 1], width=2, fill="black")
    canvas.create_line(m[2, 0], m[2, 1], m[6, 0], m[6, 1], width=2, fill="black")
    canvas.create_line(m[3, 0], m[3, 1], m[7, 0], m[7, 1], width=2, fill="black")

    return m


def draw_cat(canvas, period=40, mode="iso"):
    cat = np.matrix([
        [0.5, 1, 0, 1],
        [2, 0, 0, 1],
        [7, 0, 0, 1],
        [8, 1, 0, 1],
        [8, 2.5, 0, 1],
        [7, 2, 0, 1],
        [6.5, 1, 0, 1],
        [5, 6, 0, 1],
        [4, 5, 0, 1],
        [3, 5, 0, 1],
        [2, 6, 0, 1],

        [0.5, 1, 1, 1],
        [2, 0, 1, 1],
        [7, 0, 1, 1],
        [8, 1, 1, 1],
        [8, 2.5, 1, 1],
        [7, 2, 1, 1],
        [6.5, 1, 1, 1],
        [5, 6, 1, 1],
        [4, 5, 1, 1],
        [3, 5, 1, 1],
        [2, 6, 1, 1],

        [2, 2, 1, 1],
        [2, 0, 1, 1],
        [3, 0, 1, 1],
        [3, 2, 1, 1],

        [4, 2, 1, 1],
        [4, 0, 1, 1],
        [5, 0, 1, 1],
        [5, 2, 1, 1],

        [6.5, 1, 1, 1],

        [2, 4.5, 1, 1],
        [2.5, 4, 1, 1],
        [3, 4.5, 1, 1],

        [4, 4.5, 1, 1],
        [4.5, 4, 1, 1],
        [5, 4.5, 1, 1],

        [3, 4, 1, 1],
        [4, 4, 1, 1],
        [3, 3, 1, 1],
        [4, 3, 1, 1]

    ])
    delta = [[0.5, 0, 1, 0]]
    for i in range(len(cat) - 1):
        delta = np.vstack([delta, [0.5, 0, 1, 0]])

    cat = cat - delta
    cat = cat * period
    cat = cat * Tx(180)
    cat = metric(cat, mode)
    cat = cat * T0()

    for i in range(0, 10):
        canvas.create_line(cat[i, 0], cat[i, 1], cat[i + 1, 0], cat[i + 1, 1], width=2, fill="black")
    canvas.create_line(cat[10, 0], cat[10, 1], cat[0, 0], cat[0, 1], width=2, fill="black")

    for i in range(11, 21):
        canvas.create_line(cat[i, 0], cat[i, 1], cat[i + 1, 0], cat[i + 1, 1], width=2, fill="black")
    canvas.create_line(cat[21, 0], cat[21, 1], cat[11, 0], cat[11, 1], width=2, fill="black")

    for i in range(0, 11):
        canvas.create_line(cat[i, 0], cat[i, 1], cat[i + 11, 0], cat[i + 11, 1], width=2, fill="black")

    for i in range(22, 25):
        canvas.create_line(cat[i, 0], cat[i, 1], cat[i + 1, 0], cat[i + 1, 1], width=2, fill="black")

    for i in range(26, 29):
        canvas.create_line(cat[i, 0], cat[i, 1], cat[i + 1, 0], cat[i + 1, 1], width=2, fill="black")

    canvas.create_line(cat[30, 0], cat[30, 1], cat[28, 0], cat[28, 1], width=2, fill="black")

    for i in range(31, 33):
        canvas.create_line(cat[i, 0], cat[i, 1], cat[i + 1, 0], cat[i + 1, 1], width=2, fill="black")
    canvas.create_line(cat[33, 0], cat[33, 1], cat[31, 0], cat[31, 1], width=2, fill="black")

    for i in range(34, 36):
        canvas.create_line(cat[i, 0], cat[i, 1], cat[i + 1, 0], cat[i + 1, 1], width=2, fill="black")
    canvas.create_line(cat[34, 0], cat[34, 1], cat[36, 0], cat[36, 1], width=2, fill="black")

    for i in range(37, 39):
        canvas.create_line(cat[i, 0], cat[i, 1], cat[i + 1, 0], cat[i + 1, 1], width=2, fill="black")

    canvas.create_line(cat[37, 0], cat[37, 1], cat[40, 0], cat[40, 1], width=2, fill="black")

    return cat

def picture(mode = "iso"):
    window = tk.Tk()
    window.title('Проекция')

    canvas = tk.Canvas(window,width=width,height=height,bg="white",
              cursor="pencil")
    ##########################################

    draw_XYZ(canvas, height/2, mode=mode, period = 30)
    draw_cat(canvas, mode=mode, period = 30)
    ############################################
    canvas.pack()
    window.mainloop()

def main():
    root = tk.Tk()
    btn = tk.Button(root, text="Диметрическая проекция")
    btn.config(command=lambda: picture("dim"))
    btn.pack(padx=120, pady=30)

    btn = tk.Button(root, text="Изометрическая проекция")
    btn.config(command=lambda: picture("iso"))
    btn.pack(padx=240, pady=30)

    root.title("Проекции")
    root.mainloop()

main()