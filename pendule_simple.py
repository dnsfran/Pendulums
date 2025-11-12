import tkinter as tk
import math 


class Point :
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


class Pendule:
    def __init__(self, origin, length, angle,weight=1.0):
        self.origin = origin
        self.length = length
        self.angle = angle  # in radians
        self.angle_velocity = 5.0
        self.weight = weight  # default weight

    def set_length(self, length):
        self.length = length
    
    def set_angle(self, angle):
        self.angle = angle
    
    def set_weight(self, weight):
        self.weight = weight

    def update_angle(self, dt):
        # Update the angle based on the angular velocity and time step
        self.angle += self.angle_velocity * dt

    def update_velocity(self, dt = 0.01, gravity=9.81):
        # Update the angular velocity based on the angular acceleration and time step
        angle_acceleration = -gravity / self.length * math.sin(self.angle)
        self.angle_velocity += angle_acceleration*dt

    def get_end_point(self):
        x = self.origin.x + self.length * math.sin(self.angle)
        y = self.origin.y + self.length * math.cos(self.angle)
        return Point(x, y)

class PenduleApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Simulation de Pendule")
        self.geometry("600x400")
        self.canvas = tk.Canvas(self, width=600, height=400, bg="white")
        self.canvas.pack()
        # Création du pendule
        self.pendule = Pendule(Point(300, 200), 150, math.pi / 4)
        self.animate()

    def animate(self):
        self.pendule.update_velocity(0.05)
        self.pendule.update_angle(0.05)
        self.draw_pendulum(self.pendule)
        self.after(20, self.animate)  # 50 FPS

    def draw_pendulum(self, pendule):
        self.canvas.delete("all")
        x0, y0 = pendule.origin.x, pendule.origin.y
        x1 = x0 + pendule.length * math.sin(pendule.angle)
        y1 = y0 + pendule.length * math.cos(pendule.angle)
        self.canvas.create_line(x0, y0, x1, y1, width=2)
        self.canvas.create_oval(x1-15, y1-15, x1+15, y1+15, fill="blue")




if __name__ == "__main__":
    app = PenduleApp()
    app.mainloop()

