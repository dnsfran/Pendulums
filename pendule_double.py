import tkinter as tk
import math

class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def set_x(self, x):
        self.x = x
    
    def set_y(self, y):
        self.y = y

    def get_x(self):
        return self.x
    
    def get_y(self):
        return self.y

    def __str__(self):
        return f"({self.x}, {self.y})"

class DoublePendulum:
    def __init__(self, origin, l1, l2, a1, a2, a1_v = 0.0 , a2_v = 0.0,  m1=1.0, m2=1.0):
        self.origin = origin
        self.l1 = l1
        self.l2 = l2
        self.a1 = a1  # angle 1 (radians)
        self.a2 = a2  # angle 2 (radians)
        self.a1_v = a1_v # angular velocity 1
        self.a2_v = a2_v  # angular velocity 2
        self.m1 = m1
        self.m2 = m2
        self.g = 9.81

    def update(self, dt=0.05):
        # Equations of motion for double pendulum
        g = self.g
        m1 = self.m1
        m2 = self.m2
        l1 = self.l1
        l2 = self.l2
        a1 = self.a1
        a2 = self.a2
        a1_v = self.a1_v
        a2_v = self.a2_v

        num1 = -g * (2 * m1 + m2) * math.sin(a1)
        num2 = -m2 * g * math.sin(a1 - 2 * a2)
        num3 = -2 * math.sin(a1 - a2) * m2
        num4 = a2_v * a2_v * l2 + a1_v * a1_v * l1 * math.cos(a1 - a2)
        den = l1 * (2 * m1 + m2 - m2 * math.cos(2 * a1 - 2 * a2))
        a1_a = (num1 + num2 + num3 * num4) / den

        num1 = 2 * math.sin(a1 - a2)
        num2 = a1_v * a1_v * l1 * (m1 + m2)
        num3 = g * (m1 + m2) * math.cos(a1)
        num4 = a2_v * a2_v * l2 * m2 * math.cos(a1 - a2)
        den = l2 * (2 * m1 + m2 - m2 * math.cos(2 * a1 - 2 * a2))
        a2_a = (num1 * (num2 + num3 + num4)) / den

        self.a1_v += a1_a * dt
        self.a2_v += a2_a * dt
        self.a1 += self.a1_v * dt
        self.a2 += self.a2_v * dt
        
        # Ajout des frottements (damping)
        damping = 0.001
        self.a1_v *= (1 - damping)
        self.a2_v *= (1 - damping)

    def get_points(self):
        x0, y0 = self.origin.x, self.origin.y
        x1 = x0 + self.l1 * math.sin(self.a1)
        y1 = y0 + self.l1 * math.cos(self.a1)
        x2 = x1 + self.l2 * math.sin(self.a2)
        y2 = y1 + self.l2 * math.cos(self.a2)
        return (x0, y0, x1, y1, x2, y2)

class DoublePendulumApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Simulation de Double Pendule")
        self.geometry("1000x700")
        self.canvas = tk.Canvas(self, width=1000, height=700, bg="white")
        self.canvas.pack()
        self.pendule = DoublePendulum(Point(500, 300), 200, 50, math.pi , 0.1,  1.0, 0.0, 1.0, 5.0)
        self.animate()

    def animate(self):
        self.pendule.update(0.10)
        self.draw_pendulum(self.pendule)
        self.after(10, self.animate)

    def draw_pendulum(self, pendule):
        self.canvas.delete("all")
        x0, y0, x1, y1, x2, y2 = pendule.get_points()
        self.canvas.create_line(x0, y0, x1, y1, width=2)
        self.canvas.create_oval(x1-10, y1-10, x1+10, y1+10, fill="blue")
        self.canvas.create_line(x1, y1, x2, y2, width=2)
        self.canvas.create_oval(x2-10, y2-10, x2+10, y2+10, fill="red")

if __name__ == "__main__":
    app = DoublePendulumApp()
    app.mainloop()
