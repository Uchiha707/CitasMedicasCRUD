import tkinter as tk  # Importar el módulo tkinter para crear la interfaz gráfica
from tkinter import ttk  # Importar ttk para usar widgets mejorados de tkinter
from tkinter import messagebox as messagebox  # Importar messagebox para mostrar mensajes emergentes
import sqlite3  # Importar sqlite3 para manejar la base de datos

# Clase para manejar la base de datos de citas médicas
class MedicalAppointmentDB:
    def __init__(self, db_name):
        # Establecer conexión con la base de datos SQLite
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()
        self.create_table()  # Llamar a la función para crear la tabla si no existe

    # Función para crear la tabla 'citas_médicas' si no existe
    def create_table(self):
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS citas_médicas (
                id INTEGER PRIMARY KEY,
                nombre TEXT,
                fecha TEXT,
                hora TEXT,
                descripcion TEXT
            )
        """)
        self.conn.commit()  # Guardar los cambios

    # Función para agregar una nueva cita médica a la base de datos
    def add_appointment(self, nombre, fecha, hora, descripcion):
        self.cursor.execute("INSERT INTO citas_médicas (nombre, fecha, hora, descripcion) VALUES (?, ?, ?, ?)",
                            (nombre, fecha, hora, descripcion))
        self.conn.commit()  # Guardar los cambios

    # Función para obtener todas las citas médicas desde la base de datos
    def get_appointments(self):
        self.cursor.execute("SELECT * FROM citas_médicas")
        return self.cursor.fetchall()  # Retornar todas las filas como una lista de tuplas

    # Función para actualizar una cita médica
    def update_appointment(self, appointment_id, nombre, fecha, hora, descripcion):
        self.cursor.execute("UPDATE citas_médicas SET nombre = ?, fecha = ?, hora = ?, descripcion = ? WHERE id = ?",
                            (nombre, fecha, hora, descripcion, appointment_id))
        self.conn.commit()  # Guardar los cambios

    # Función para eliminar una cita médica
    def delete_appointment(self, appointment_id):
        self.cursor.execute("DELETE FROM citas_médicas WHERE id = ?", (appointment_id,))
        self.conn.commit()  # Guardar los cambios

# Clase para manejar la interfaz gráfica
class MedicalAppointmentApp:
    def __init__(self, root):
        self.root = root  # Ventana principal de la aplicación
        self.root.title("Gestión de Citas Médicas")  # Título de la ventana
        self.db = MedicalAppointmentDB("citas_medicas.db")  # Crear la instancia de la base de datos

        # Crear la tabla visual para mostrar las citas médicas
        self.tree = ttk.Treeview(root, columns=("ID", "Nombre", "Fecha", "Hora", "Descripción"), show="headings")
        self.tree.heading("ID", text="ID")
        self.tree.heading("Nombre", text="Nombre")
        self.tree.heading("Fecha", text="Fecha")
        self.tree.heading("Hora", text="Hora")
        self.tree.heading("Descripción", text="Descripción")
        self.tree.pack(padx=10, pady=10)  # Empaquetar la tabla con un espacio alrededor

        # Crear un contenedor frame para alinear los campos a la izquierda
        form_frame = ttk.Frame(root)
        form_frame.pack(padx=10, pady=10, anchor='w')  # Alinear todo el contenedor a la izquierda

        # Crear etiquetas y entradas para agregar nuevas citas
        self.name_label = ttk.Label(form_frame, text="Nombre del Paciente:")
        self.name_label.grid(row=0, column=0, sticky='w', pady=5)  # Alinear a la izquierda
        self.name_entry = ttk.Entry(form_frame)
        self.name_entry.grid(row=0, column=1, pady=5)  # Campo para ingresar el nombre del paciente

        self.date_label = ttk.Label(form_frame, text="Fecha:")
        self.date_label.grid(row=1, column=0, sticky='w', pady=5)  # Alinear a la izquierda
        self.date_entry = ttk.Entry(form_frame)
        self.date_entry.grid(row=1, column=1, pady=5)  # Campo para ingresar la fecha

        self.time_label = ttk.Label(form_frame, text="Hora:")
        self.time_label.grid(row=2, column=0, sticky='w', pady=5)  # Alinear a la izquierda
        self.time_entry = ttk.Entry(form_frame)
        self.time_entry.grid(row=2, column=1, pady=5)  # Campo para ingresar la hora

        self.description_label = ttk.Label(form_frame, text="Descripción:")
        self.description_label.grid(row=3, column=0, sticky='w', pady=5)  # Alinear a la izquierda
        self.description_entry = ttk.Entry(form_frame)
        self.description_entry.grid(row=3, column=1, pady=5)  # Campo para ingresar la descripción

        # Crear botones para las acciones (Agregar, Actualizar, Eliminar)
        button_frame = ttk.Frame(root)
        button_frame.pack(pady=10, anchor='w')  # Alinear los botones a la izquierda

        # Botón para agregar una cita
        self.add_button = ttk.Button(button_frame, text="Agregar Cita", command=self.add_appointment)
        self.add_button.grid(row=0, column=0, padx=5)

        # Botón para actualizar una cita seleccionada
        self.update_button = ttk.Button(button_frame, text="Actualizar Cita", command=self.update_appointment)
        self.update_button.grid(row=0, column=1, padx=5)

        # Botón para eliminar una cita seleccionada
        self.delete_button = ttk.Button(button_frame, text="Eliminar Cita", command=self.delete_appointment)
        self.delete_button.grid(row=0, column=2, padx=5)

        # Cargar las citas médicas existentes al iniciar la aplicación
        self.load_appointments()

    # Función para agregar una cita médica a la base de datos
    def add_appointment(self):
        nombre = self.name_entry.get()  # Obtener el nombre del campo de entrada
        fecha = self.date_entry.get()  # Obtener la fecha del campo de entrada
        hora = self.time_entry.get()  # Obtener la hora del campo de entrada
        descripcion = self.description_entry.get()  # Obtener la descripción del campo de entrada

        # Validar que todos los campos estén llenos
        if not (nombre and fecha and hora and descripcion):
            messagebox.showerror("Error", "Todos los campos son obligatorios")  # Mostrar error si falta un campo
            return

        # Agregar la cita médica a la base de datos
        self.db.add_appointment(nombre, fecha, hora, descripcion)
        messagebox.showinfo("Éxito", "Cita médica agregada")  # Mostrar mensaje de éxito
        self.load_appointments()  # Recargar las citas en la tabla visual

        # Limpiar los campos de entrada
        self.name_entry.delete(0, tk.END)
        self.date_entry.delete(0, tk.END)
        self.time_entry.delete(0, tk.END)
        self.description_entry.delete(0, tk.END)

    # Función para actualizar una cita médica seleccionada
    def update_appointment(self):
        selected_item = self.tree.selection()  # Obtener la cita seleccionada en la tabla
        if not selected_item:
            messagebox.showerror("Error", "Selecciona una cita médica")  # Mostrar error si no se selecciona nada
            return

        # Obtener el ID de la cita seleccionada
        appointment_id = self.tree.item(selected_item)["values"][0]
        nombre = self.name_entry.get()  # Obtener el nuevo nombre
        fecha = self.date_entry.get()  # Obtener la nueva fecha
        hora = self.time_entry.get()  # Obtener la nueva hora
        descripcion = self.description_entry.get()  # Obtener la nueva descripción

        # Validar que todos los campos estén llenos
        if not (nombre and fecha and hora and descripcion):
            messagebox.showerror("Error", "Todos los campos son obligatorios")  # Mostrar error si falta un campo
            return

        # Actualizar la cita médica en la base de datos
        self.db.update_appointment(appointment_id, nombre, fecha, hora, descripcion)
        messagebox.showinfo("Éxito", "Cita médica actualizada")  # Mostrar mensaje de éxito
        self.load_appointments()  # Recargar las citas en la tabla visual

        # Limpiar los campos de entrada
        self.name_entry.delete(0, tk.END)
        self.date_entry.delete(0, tk.END)
        self.time_entry.delete(0, tk.END)
        self.description_entry.delete(0, tk.END)

    # Función para eliminar una cita médica seleccionada
    def delete_appointment(self):
        selected_item = self.tree.selection()  # Obtener la cita seleccionada en la tabla
        if not selected_item:
            messagebox.showerror("Error", "Selecciona una cita médica")  # Mostrar error si no se selecciona nada
            return

        # Obtener el ID de la cita seleccionada
        appointment_id = self.tree.item(selected_item)["values"][0]
        # Eliminar la cita médica de la base de datos
        self.db.delete_appointment(appointment_id)
        messagebox.showinfo("Éxito", "Cita médica eliminada")  # Mostrar mensaje de éxito
        self.load_appointments()  # Recargar las citas en la tabla visual

    # Función para cargar y mostrar todas las citas médicas en la tabla visual
    def load_appointments(self):
        # Limpiar la tabla actual
        for row in self.tree.get_children():
            self.tree.delete(row)

        # Obtener las citas desde la base de datos
        appointments = self.db.get_appointments()
        # Insertar cada cita en la tabla visual
        for appointment in appointments:
            self.tree.insert("", tk.END, values=appointment)

# Crear la ventana principal de la aplicación
root = tk.Tk()
app = MedicalAppointmentApp(root)  # Crear una instancia de la aplicación
root.mainloop()  # Ejecutar el bucle principal de la aplicación



 

