import time
import tkinter as tk
from tkinter import messagebox

import serial


class StepperControlApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Control de Motor Stepper")
        
        self.ser = serial.Serial('COM8', 9600)
        time.sleep(2)  # Espera a que la conexión se establezca
        
        self.create_widgets()
        
    def create_widgets(self):
        self.forward_button = tk.Button(self.root, text="Mover Adelante", command=self.move_forward)
        self.forward_button.pack(pady=10)

        self.backward_button = tk.Button(self.root, text="Mover Atrás", command=self.move_backward)
        self.backward_button.pack(pady=10)

        self.steps_entry = tk.Entry(self.root)
        self.steps_entry.insert(0, "100")
        self.steps_entry.pack(pady=10)
        
        self.status_label = tk.Label(self.root, text="Estado: Listo")
        self.status_label.pack(pady=10)

    def move_motor(self, steps):
        command = f'M{steps}\n'
        self.ser.write(command.encode())
        
        # Espera la confirmación de Arduino
        while True:
            if self.ser.in_waiting > 0:
                response = self.ser.readline().decode().strip()
                if response == "Done":
                    self.status_label.config(text="Estado: Movimiento completado")
                    break

    def move_forward(self):
        try:
            steps = int(self.steps_entry.get())
            self.status_label.config(text="Estado: Moviendo adelante")
            self.move_motor(steps)
        except ValueError:
            messagebox.showerror("Error", "Por favor, ingresa un número válido de pasos")

    def move_backward(self):
        try:
            steps = int(self.steps_entry.get())
            self.status_label.config(text="Estado: Moviendo atrás")
            self.move_motor(-steps)
        except ValueError:
            messagebox.showerror("Error", "Por favor, ingresa un número válido de pasos")

    def on_closing(self):
        self.ser.close()
        self.root.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = StepperControlApp(root)
    root.protocol("WM_DELETE_WINDOW", app.on_closing)
    root.mainloop()

