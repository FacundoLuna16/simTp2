import customtkinter as ctk


class ScrollableGrid:
    def __init__(self, parent):
        self.parent = parent
        self.frame_interior = ctk.CTkFrame(self.parent)
        self.frame_interior.pack(expand=True, fill="both")

    def render_data(self, data: list[int]):
        # Limpiar el frame antes de renderizar nuevos datos
        for widget in self.frame_interior.winfo_children():
            widget.destroy()

        # Crear un Text widget para mostrar el texto
        text_widget = ctk.CTkTextbox(self.frame_interior, wrap="word")
        text_widget.pack(expand=True, fill="both")
        text_widget.insert("0.0", "\n".join(map(str, data)))
