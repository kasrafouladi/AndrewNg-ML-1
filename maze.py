import tkinter as tk
import time
import random

class MazeGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Maze Game")
        self.root.geometry("600x600")
        
        self.canvas = tk.Canvas(self.root, bg="white", height=600, width=600)
        self.canvas.pack()
        
        self.timer_label = tk.Label(self.root, text="Time: 0s", font=("Arial", 16))
        self.timer_label.pack()

        self.cell_size = 20
        self.rows = 30
        self.cols = 30
        
        self.maze = self.generate_maze()
        self.draw_maze()
        
        self.player = self.canvas.create_text(10, 10, text="A", font=("Arial", 16), fill="blue")
        self.root.bind("<KeyPress>", self.move_player)
        
        self.start_time = time.time()
        self.update_timer()
        
    def generate_maze(self):
        maze = [[1 for _ in range(self.cols)] for _ in range(self.rows)]
        stack = [(0, 0)]
        visited = set((0, 0))
        
        while stack:
            current = stack[-1]
            x, y = current
            maze[y][x] = 0
            neighbors = []
            
            for dx, dy in [(-2, 0), (2, 0), (0, -2), (0, 2)]:
                nx, ny = x + dx, y + dy
                if 0 <= nx < self.cols and 0 <= ny < self.rows and (nx, ny) not in visited:
                    neighbors.append((nx, ny))
            
            if neighbors:
                next_cell = random.choice(neighbors)
                stack.append(next_cell)
                visited.add(next_cell)
                mx, my = (x + next_cell[0]) // 2, (y + next_cell[1]) // 2
                maze[my][mx] = 0
            else:
                stack.pop()
        
        return maze
    
    def draw_maze(self):
        for y in range(self.rows):
            for x in range(self.cols):
                if self.maze[y][x] == 1:
                    self.canvas.create_text(
                        x * self.cell_size + 10, y * self.cell_size + 10,
                        text="#", font=("Arial", 16), fill="black"
                    )
                else:
                    self.canvas.create_text(
                        x * self.cell_size + 10, y * self.cell_size + 10,
                        text=".", font=("Arial", 16), fill="black"
                    )
    
    def move_player(self, event):
        x, y = self.canvas.coords(self.player)
        new_x, new_y = x, y
        
        if event.keysym == 'Up':
            new_y -= 20
        elif event.keysym == 'Down':
            new_y += 20
        elif event.keysym == 'Left':
            new_x -= 20
        elif event.keysym == 'Right':
            new_x += 20
        
        if 0 <= new_x < self.cols * self.cell_size and 0 <= new_y < self.rows * self.cell_size:
            if self.maze[int(new_y / self.cell_size)][int(new_x / self.cell_size)] == 0:
                self.canvas.coords(self.player, new_x, new_y)

    def update_timer(self):
        elapsed_time = int(time.time() - self.start_time)
        self.timer_label.config(text=f"Time: {elapsed_time}s")
        self.root.after(1000, self.update_timer)

if __name__ == "__main__":
    root = tk.Tk()
    game = MazeGame(root)
    root.mainloop()