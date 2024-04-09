import customtkinter as ctk
from vistaGenerador import VentanaGenerador
from frameGrilla import ScrollableGrid


class VentanaPrincipal(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Simulacion tp 2 - Grupo 8")
        self.geometry("800x600")

        self.tabview = ctk.CTkTabview(self, height=700, width=600)
        self.tabview.pack(expand=True, fill="both")

        #Configuramos el tamanio que ocupara cada columna y fila
        self.vista1 = self.tabview.add("Generar Numeros Aleatorios")
        self.vista1.grid_columnconfigure(0, weight=1)
        self.vista1.grid_columnconfigure(1, weight=1)
        self.vista1.grid_rowconfigure(0, weight=1)
        # self.vista2 = self.tabview.add("Vista 2")
        # self.vista3 = self.tabview.add("Vista 3")

        # armamos 2 frame para dividir la vista 1 en 2 de forma vertical
        # Crea dos frames dentro de la vista "Generar Numeros Aleatorios"
        self.frame1 = ctk.CTkFrame(self.vista1)
        self.frame1.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
        self.frame2 = ctk.CTkFrame(self.vista1)
        self.frame2.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")

        VentanaGenerador(self.frame1, ScrollableGrid(self.frame2))


if __name__ == "__main__":
    app = VentanaPrincipal()
    app.mainloop()
