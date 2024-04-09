import customtkinter as ctk
from funciones import GeneradorAleatorio
import matplotlib.pyplot as plt
import numpy as np
import tkinter as tk
from tkinter import ttk


class VentanaGenerador():
    def __init__(self, vista, grilla):
        self.vista = vista
        self.grilla = grilla
        self.bandera = False
        self.datos = []
        # creamos un lbl con el texto "Distribución" y un select con las opciones "Uniforme", "Exponencial" y "Normal"
        # Setemos la opción "Uniforme" como la opción seleccionada por defecto
        self.label_distribucion = ctk.CTkLabel(self.vista, text="Distribución:")
        self.label_distribucion.grid(row=0, column=0, padx=10, pady=5)

        self.combobox_distribucion = ctk.CTkComboBox(self.vista,
                                                     values=["uniforme", "exponencial", "normal"],
                                                     command=self.handle_selection)
        self.combobox_distribucion.grid(row=0, column=1, padx=10, pady=5)

        # Agremamos un frame que contenga 2 lables con sus respectivas entradas de texto, este debe mantener siempre
        # el mismo tamaño
        self.frame_inputs = ctk.CTkFrame(self.vista)
        self.frame_inputs.grid(row=1, column=0, columnspan=3, padx=10, pady=5, sticky="nsew")

        # LABEL Y ENTRY PARA PARAMETRO 1
        self.label_parametro1 = ctk.CTkLabel(self.frame_inputs)
        self.label_parametro1.grid(row=0, column=0, padx=10, pady=5, sticky="nsew")
        self.entry_parametro1 = ctk.CTkEntry(self.frame_inputs)
        self.entry_parametro1.grid(row=0, column=1, padx=10, pady=5, sticky="nsew")

        # LABEL Y ENTRY PARA PARAMETRO 2
        self.label_parametro2 = ctk.CTkLabel(self.frame_inputs)
        self.label_parametro2.grid(row=1, column=0, padx=10, pady=5, sticky="nsew")
        self.entry_parametro2 = ctk.CTkEntry(self.frame_inputs)
        self.entry_parametro2.grid(row=1, column=1, padx=10, pady=5, sticky="nsew")

        self.laber_parametro_cantidad = ctk.CTkLabel(self.vista, text="Cantidad de números a generar:")
        self.laber_parametro_cantidad.grid(row=2, column=0, padx=10, pady=5)
        self.entry_parametro_cantidad = ctk.CTkEntry(self.vista)
        self.entry_parametro_cantidad.grid(row=2, column=1, padx=10, pady=5)

        self.btn_generar = ctk.CTkButton(self.vista, text="Generar números", command=self.generar_numeros)
        self.btn_generar.grid(row=3, column=1, columnspan=2, pady=10)

        # Cantidad de intervalos del histograma
        self.label_cantidad_intervalos = ctk.CTkLabel(self.vista, text="Cantidad de intervalos del histograma:")
        self.label_cantidad_intervalos.grid(row=4, column=0, padx=10, pady=5)
        self.entry_cantidad_intervalos = ctk.CTkEntry(self.vista)
        self.entry_cantidad_intervalos.grid(row=4, column=1, padx=10, pady=5)

        # Botón para generar el histograma
        self.btn_generar_histograma = ctk.CTkButton(self.vista, text="Generar histograma",
                                                    command=self.generar_histograma)
        self.btn_generar_histograma.grid(row=5, column=1, columnspan=2, pady=10)

        self.handle_selection("uniforme")  # Seteamos los campos para la distribución uniforme

        # Vincular la función de validación a la CTkEntry
        self.entry_parametro1.bind("<KeyRelease>", self.verificar_campos_generador_numeros)
        self.entry_parametro2.bind("<KeyRelease>", self.verificar_campos_generador_numeros)
        self.entry_parametro_cantidad.bind("<KeyRelease>", self.verificar_campos_generador_numeros)
        # Vincular la función de validación a la CTkEntry
        self.entry_cantidad_intervalos.bind("<KeyRelease>", self.verificar_campo_cantidad_intervalos)

        # Verificar los campos inicialmente
        self.verificar_campos_generador_numeros()
        self.verificar_campo_cantidad_intervalos()

    def verificar_campo_cantidad_intervalos(self, event=None):
        valor_cantidad_intervalos = self.entry_cantidad_intervalos.get()

        # Verificar si el valor es un entero
        if not valor_cantidad_intervalos.isdigit():
            self.btn_generar_histograma.configure(state="disabled")
            return

        # Convertir el valor a entero
        valor_cantidad_intervalos = int(valor_cantidad_intervalos)

        # Verificar si el valor es mayor a 0
        if valor_cantidad_intervalos > 0 and self.bandera:
            self.btn_generar_histograma.configure(state="normal")
        else:
            self.btn_generar_histograma.configure(state="disabled")

    def verificar_campos_generador_numeros(self, event=None):
        valor_parametro1 = self.entry_parametro1.get()
        valor_parametro2 = self.entry_parametro2.get()
        valor_cantidad = self.entry_parametro_cantidad.get()

        # Obtener el valor del campo de entrada
        if self.combobox_distribucion.get() == "exponencial" and valor_parametro1 and valor_cantidad:
            if not valor_parametro1.isdigit() or not valor_cantidad.isdigit():
                self.btn_generar.configure(state="disabled")
                return
            self.btn_generar.configure(state="normal")
            return

        # Verificar si los valores son enteros
        if not (valor_parametro1.isdigit() and valor_parametro2.isdigit() and valor_cantidad.isdigit()):
            self.btn_generar.configure(state="disabled")
            return

        # Convertir los valores a enteros
        valor_parametro1 = int(valor_parametro1)
        valor_parametro2 = int(valor_parametro2)
        valor_cantidad = int(valor_cantidad)

        # Verificar si los tres parámetros están presentes y si el parámetro 2 es mayor que el parámetro 1
        if valor_parametro1 and valor_parametro2 and valor_cantidad and valor_parametro2 > valor_parametro1:
            self.btn_generar.configure(state="normal")
        else:
            self.btn_generar.configure(state="disabled")

    def generar_histograma(self):
        intervalos = int(self.entry_cantidad_intervalos.get())
        # Calcular límites de los intervalos
        min_valor = min(self.datos)
        max_valor = max(self.datos)
        rango = max_valor - min_valor
        ancho_intervalo = rango / intervalos
        limites_intervalos = [min_valor + i * ancho_intervalo for i in range(intervalos + 1)]

        # Calcular frecuencias
        frecuencias, _ = np.histogram(self.datos, bins=limites_intervalos)

        # Crear tabla de frecuencias
        tabla_frecuencias = []
        for i in range(intervalos):
            intervalo = f"{limites_intervalos[i]:.2f} - {limites_intervalos[i + 1]:.2f}"
            tabla_frecuencias.append((intervalo, frecuencias[i]))

        # Mostrar tabla de frecuencias en una ventana
        self.mostrar_tabla_frecuencias(tabla_frecuencias)

        # Graficar histograma
        plt.figure(figsize=(10, 6))
        plt.hist(self.datos, bins=limites_intervalos, edgecolor='black')
        plt.title("Histograma de Frecuencias")
        plt.xlabel("Intervalos")
        plt.ylabel("Frecuencia")
        plt.grid(True)
        plt.xticks(limites_intervalos, rotation=45)
        plt.show()

    def mostrar_tabla_frecuencias(self, tabla_frecuencias):
        # Crear ventana
        ventana = tk.Toplevel()
        ventana.title("Tabla de Frecuencias")

        # Crear tabla
        tabla = ttk.Treeview(ventana, columns=("Intervalo", "Frecuencia"), show="headings")
        tabla.heading("Intervalo", text="Intervalo")
        tabla.heading("Frecuencia", text="Frecuencia")
        tabla.pack(expand=True, fill=tk.BOTH)

        # Insertar datos en la tabla
        for intervalo, frecuencia in tabla_frecuencias:
            tabla.insert("", "end", values=(intervalo, frecuencia))

    def generar_numeros(self):
        # datos del 1 al 100
        datos = []
        generador = GeneradorAleatorio(12)
        distribucion = self.combobox_distribucion.get()
        cantidad = int(self.entry_parametro_cantidad.get())
        if distribucion == "uniforme":
            a = int(self.entry_parametro1.get())
            b = int(self.entry_parametro2.get())
            datos = generador.generar_numeros_uniformes(a, b, cantidad)
        elif distribucion == "exponencial":
            media = int(self.entry_parametro1.get())
            datos = generador.generar_numeros_exponenciales(media, cantidad)
        elif distribucion == "normal":
            media = int(self.entry_parametro1.get())
            desviacion = int(self.entry_parametro2.get())
            datos = generador.generar_normales(media, desviacion, cantidad)
        self.bandera = True
        self.datos = datos
        self.grilla.render_data(datos)  # Renderizamos los datos en la grilla
        self.verificar_campo_cantidad_intervalos()

    def handle_selection(self, distribucion):
        if distribucion == "uniforme":
            self.label_parametro1.configure(text="Mínimo(a):", state="normal")
            self.label_parametro2.grid(row=1, column=0, padx=10)
            self.label_parametro2.configure(text="Máximo(b):", state="normal")
            self.entry_parametro2.grid(row=1, column=1, padx=10)

        elif distribucion == "exponencial":
            self.label_parametro1.configure(text=":Lambda")
            self.label_parametro2.grid_remove()
            self.entry_parametro2.grid_remove()

        elif distribucion == "normal":
            self.label_parametro1.configure(text="Media:", state="normal")
            self.label_parametro2.grid(row=1, column=0, padx=10)
            self.label_parametro2.configure(text="Desviación estándar:", state="normal")
            self.entry_parametro2.grid(row=1, column=1, padx=10)

        self.verificar_campos_generador_numeros()
