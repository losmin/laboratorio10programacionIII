import tkinter as tk

import serial
from serial.tools.list_ports import comports


class ServoControlApp(tk.Tk):
    def __init__(self, arduino_port):
        super().__init__()
        self.title("Laboratorio 10 ServoMotor")
        self.geometry("300x400")
        self.arduino = serial.Serial(arduino_port, 9600, timeout=1)
        self.create_widgets()

    def create_widgets(self):
        self.columnconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)

        titulo = tk.Label(self, text="Control de Servomotor", font=("Arial", 16))
        titulo.grid(row=0, column=0, pady=10)

        botones_frame = tk.Frame(self)
        botones_frame.grid(row=1, column=0, padx=10, pady=10)

        btn_texts = ["Girar Derecha", "Girar 90 Grados", "Girar 180 Grados", "Girar 270 Grados", "Girar 360 Grados", "Girar Izquierda"]
        btn_commands = ['1', '3', '4', '5', '6', '2']

        for i, (text, command) in enumerate(zip(btn_texts, btn_commands)):
            btn = tk.Button(botones_frame, text=text, command=lambda cmd=command: self.enviar_comando(cmd))
            btn.grid(row=i, column=0, pady=5, sticky="ew")

        # Añadir entrada para ángulo personalizado
        self.custom_angle_label = tk.Label(botones_frame, text="Ángulo Personalizado:")
        self.custom_angle_label.grid(row=6, column=0, pady=5)
        self.custom_angle_entry = tk.Entry(botones_frame)
        self.custom_angle_entry.grid(row=7, column=0, pady=5)
        self.custom_angle_btn = tk.Button(botones_frame, text="Girar", command=self.enviar_angulo_personalizado)
        self.custom_angle_btn.grid(row=8, column=0, pady=5)

    def enviar_comando(self, comando):
        try:
            self.arduino.write(comando.encode())
        except serial.SerialException:
            print("Error: No se pudo enviar el comando.")

    def enviar_angulo_personalizado(self):
        try:
            angulo = int(self.custom_angle_entry.get())
            if 0 <= angulo <= 360:
                comando = f"A{angulo}"
                self.arduino.write(comando.encode())
            else:
                print("El ángulo debe estar entre 0 y 360 grados.")
        except ValueError:
            print("Por favor, introduzca un número válido.")

def encontrar_puerto_arduino():
    puertos_disponibles = [p.device for p in comports()]
    return puertos_disponibles[0] if puertos_disponibles else None

def main():
    puerto_arduino = encontrar_puerto_arduino()
    if puerto_arduino:
        app = ServoControlApp(puerto_arduino)
        app.mainloop()
    else:
        print("No se encontró ningún dispositivo Arduino conectado.")

if __name__ == "__main__":
    main()
