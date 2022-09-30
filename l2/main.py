import tkinter as tk
from math import sin, cos
import math
import numpy as np
from itertools import *
import matplotlib.pyplot as plt
import random
import time
from tkinter import *

height = 800
width = 800


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
        canvas.create_line(y[i, 0], y[i, 1], y[i + 1, 0], y[i + 1, 1], width=1, fill="grey")
        canvas.create_text(y[i, 0] - 4, y[i, 1], text=str(int((i - 2) / 2)))

    canvas.create_text(y[1, 0] - 15, y[1, 1], text=name, font=("DejavuSansLight", 15, 'bold'), fill="grey")


def draw_XYZ(canvas, length=height / 2, period=20, mode="iso"):
    y = osY_matrix(length=length, period=period)
    y = y * Tx(180)

    x = y * Tz(90) * Tx(90)
    z = x * Ty(90)
    y = y * Ty(-45)

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

def middle_line(p1, p2):
    return (p2 + p1)/2


def bez3(u, x):
    U = np.matrix([u ** 3, u ** 2, u, 1])
    M = np.matrix([[-1, 3, -3, 1],
                   [3, -6, 3, 0],
                   [-3, 3, 0, 0],
                   [1, 0, 0, 0]])
    return U * M * x


def x_middle_points(x):
    x_new = []
    for i in range(len(x)):
        x_new.append(x[i].tolist()[0])
        if (i != 0) & ((i) % 2 == 0) & (i + 1 < len(x)):
            m = middle_line(x[i], x[i + 1])
            x_new.append(m.tolist()[0])
            x_new.append(m.tolist()[0])

    for i in range(4 - len(x_new) % 4):
        x_new.append(x_new[-1])

    return np.matrix(x_new)


def bez_u(x, length=100):
    p = []

    for i in range(0, int(len(x)), 4):
        x_i = x[i:i + 4]
        i -= 1
        for j in range(length + 1):
            if p == []:
                p = (bez3(j / length, x_i))
            else:
                p = np.vstack([p, (bez3(j / length, x_i))])

    return p


def draw_bez(p, canvas, x, period=40, mode="iso"):
    p = p * period
    p = p * Tx(180)
    p = metric(p, mode)

    for i in range(len(p) - 1):
        canvas.create_line(p[i, 0], p[i, 1], p[i + 1, 0], p[i + 1, 1], width=2, fill="red")

    r = period / 10
    x = x * period
    x = x * Tx(180)
    x = metric(x, mode)
    for i in range(len(x)):
        canvas.create_oval(x[i, 0] - r, x[i, 1] - r, x[i, 0] + r, x[i, 1] + r)
        if i < len(x) - 1:
            # m = middle_line(x[i], x[i+1]
            # canvas.create_oval(m[0, 0]-r, m[0, 1]-r, m[0, 0]+r, m[0, 1]+r)
            canvas.create_line(x[i, 0], x[i, 1], x[i + 1, 0], x[i + 1, 1], width=1, fill="gray", dash=(4, 2))
        canvas.create_text(x[i, 0] + 12, x[i, 1], text=str(i + 1), font=("DejavuSansLight", 15, 'bold'))


def rand_x(N=4, A=0, B=9):
    X = []
    for i in range(N):
        x = random.randint(A, B)
        y = random.randint(A, B)
        z = random.randint(A, B)
        X.append([x, y, z, 1])

    return np.matrix(X)


def do_one_frame(n, x_orig, canvas):
    canvas.delete('all')
    draw_XYZ(canvas, height / 2, period=50)

    x = x_middle_points(x_orig)
    p = bez_u(x)

    draw_bez(p, canvas, x_orig, period=50)
    # window.after(1000, do_one_frame, n)


def get_x(n, entry, canvas):
    x = []
    for i in range(n):
        x.append([int(entry[i][0].get()), int(entry[i][1].get()), int(entry[i][2].get()), 1])
    print(11)
    do_one_frame(n, np.matrix(x), canvas)

    return x


def insert_x(x, entry, n):
    for i in range(n):
        entry[i][0].insert(0, str(x[i, 0]))
        entry[i][1].insert(0, str(x[i, 1]))
        entry[i][2].insert(0, str(x[i, 2]))


def main_window(ent):
    n = int(ent.get())
    x_orig = rand_x(n)
    root.destroy()
    window = tk.Tk()
    window.title('Безье')

    canvas = tk.Canvas(window, width=width, height=height, bg="white",
                       cursor="pencil")
    ##########################################

    Label(text="X").grid(row=0, column=1, sticky=N)
    Label(text="Y").grid(row=0, column=2, sticky=N)
    Label(text="Z").grid(row=0, column=3, sticky=N)

    entry = []
    for i in range(n):
        x = tk.Entry(width=4)
        y = tk.Entry(width=4)
        z = tk.Entry(width=4)
        entry.append([x, y, z])
        Label(text=str(i + 1)).grid(row=i + 1, column=0, sticky=N)
        x.grid(row=i + 1, column=1, sticky=N)
        y.grid(row=i + 1, column=2, sticky=N)
        z.grid(row=i + 1, column=3, sticky=N)

    for i in range(n + 2, n + 5):
        Label(text=' ').grid(row=i + 1, column=0, sticky=N)

    insert_x(x_orig, entry, n)

    but = tk.Button(text="Изменить",
                    command=lambda: get_x(n, entry, canvas))

    but.grid(row=n + 1, column=2, sticky=W)

    do_one_frame(n, x_orig, canvas)
    canvas.grid(row=0, column=4, rowspan=n + 5)

    ############################################
    window.mainloop()

root = tk.Tk()

lbl = Label(text="Число точек")

ent = tk.Entry(width=4)

btn = tk.Button(root, text="Построить")
btn.config(command=lambda: main_window(ent = ent))

lbl.pack()
ent.pack(padx=120, pady=30)
btn.pack(padx=240, pady=30)

root.title("Безье")
root.mainloop()