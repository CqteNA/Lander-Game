import tkinter as tk
import random

# Game settings
WIDTH, HEIGHT = 500, 500
GRAVITY = 0.005
THRUST = -0.02
THRUST_SIDE = 0.01
FUEL_USAGE = 0.1

class LunarLanderGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Lunar Lander")

        # Create canvas
        self.canvas = tk.Canvas(root, width=WIDTH, height=HEIGHT, bg="black")
        self.canvas.pack()

        # Create UI for restarting
        self.restart_button = tk.Button(root, text="Restart", command=self.restart_game)
        self.restart_button.pack()

        self.setup_game()

        # Key bindings
        self.root.bind("<Left>", self.thrust_left)
        self.root.bind("<Right>", self.thrust_right)
        self.root.bind("<Up>", self.thrust_up)
        self.root.bind("<KeyRelease>", self.stop_thrust)

    def setup_game(self):
        """ Initializes the game variables and resets the lander. """
        self.canvas.delete("all")

        # Landing Platform
        self.platform_x = random.randint(50, 450)
        self.platform = self.canvas.create_rectangle(self.platform_x, 490, self.platform_x + 100, 510, fill="red")

        # Lander
        self.lander = self.canvas.create_rectangle(230, 50, 270, 90, fill="yellow")

        # Movement variables
        self.lander_xv = 0
        self.lander_yv = 0
        self.fuel = 100
        self.thrusting_up = False
        self.thrusting_left = False
        self.thrusting_right = False

        # Start the game loop
        self.update_game()

    def update_game(self):
        """ Moves the lander and checks for collisions. """
        if self.fuel > 0:
            if self.thrusting_up:
                self.lander_yv += THRUST
                self.fuel -= FUEL_USAGE
            if self.thrusting_left:
                self.lander_xv -= THRUST_SIDE
                self.fuel -= FUEL_USAGE
            if self.thrusting_right:
                self.lander_xv += THRUST_SIDE
                self.fuel -= FUEL_USAGE

        # Apply gravity
        self.lander_yv += GRAVITY

        # Move the lander
        self.canvas.move(self.lander, self.lander_xv, self.lander_yv)

        # Get new position
        x1, y1, x2, y2 = self.canvas.coords(self.lander)

        # Check if lander touches the ground
        if y2 >= HEIGHT:
            self.handle_landing(x1, y1, x2, y2)
            return

        # Schedule next update
        self.root.after(20, self.update_game)

    def handle_landing(self, x1, y1, x2, y2):
        """ Checks if the landing is safe or a crash. """
        speed = abs(self.lander_yv)

        # Check if landed on platform
        if self.platform_x <= x1 and x2 <= self.platform_x + 100 and speed <= 1:
            message = "Safe Landing!"
        else:
            message = "jajajjajaja you l0se!"

        self.canvas.create_text(WIDTH//2, HEIGHT//2, text=message, fill="white", font=("Arial", 24))

    def restart_game(self):
        """ Restarts the game by resetting variables. """
        self.setup_game()

    def thrust_up(self, event):
        self.thrusting_up = True

    def thrust_left(self, event):
        self.thrusting_left = True

    def thrust_right(self, event):
        self.thrusting_right = True

    def stop_thrust(self, event):
        """ Stops thrust when keys are released. """
        if event.keysym == "Up":
            self.thrusting_up = False
        elif event.keysym == "Left":
            self.thrusting_left = False
        elif event.keysym == "Right":
            self.thrusting_right = False

# Run the game
if __name__ == "__main__":
    root = tk.Tk()
    game = LunarLanderGame(root)
    root.mainloop()
