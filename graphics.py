from tkinter import *

canvas_size = [900, 900]

root = Tk()
root.title("Battle")
canvas = Canvas(root, width=canvas_size[0], height=canvas_size[1], bg="white")
canvas.grid(row=0, column=0, rowspan=20)


# [Work in progress] Plots the course of missile / ship if action is executed.
def plot_course():
    course = True
    # draw()


# Populates map.
def draw(particles, canvas):
    canvas.delete("all")
    for particle in particles:
        x = particle.x
        y = canvas_size[1] - particle.y
        vx = particle.velx
        vy = - particle.vely
        if particle.faction == "USSR":
            fill = "red"
        elif particle.faction == "USA":
            fill = "blue"
        else:
            fill = "grey"
        if particle.p_type == "ship":
            size = 3
            if particle.faction != "dead":
                canvas.create_text(x + 20, y, text=round(particle.dv, 1))
                canvas.create_text(x - 20, y, text=particle.missiles)
                canvas.create_text(x , y + 15, text=particle.mdef, fill="cornflower blue")
            canvas.create_line(x, y, x, y - 50, fill=fill)
            canvas.create_line(x, y, x + vx * 1000, y + vy * 1000, dash=(5, 5), fill=fill)
            canvas.create_line(x, y, x + vx * 10, y + vy * 10, fill=fill, width=3)
            particle.icon = canvas.create_rectangle(x - size, y - size, x + size, y + size, fill=fill)
        elif particle.p_type == "missile":
            size = 2
            canvas.create_text(x + 20, y, text=round(particle.dv, 1))
            canvas.create_text(x - 20, y - 7, text=particle.missiles)
            if particle.m_req != "na":
                canvas.create_text(x - 20, y + 7, text=round(particle.m_req, 1), fill="red")
            points = (x - size, y - size, x, y + size, x + size, y - size)
            canvas.create_line(x, y, x, y - 25, fill=fill)
            canvas.create_line(x, y, x + vx * 1000, y + vy * 1000, dash=(10, 10), fill=fill)
            canvas.create_line(x, y, x + vx * 10, y + vy * 10, fill=fill, width=2)
            particle.icon = canvas.create_rectangle(x - size, y - size, x + size, y + size, fill=fill)
