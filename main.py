##Alexander Sinisterra Moreno
##Estructura de Datos
# main.py
import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime

# Clase que almacena los datos del participante y calcula el costo
class GestionParticipantes:
    def __init__(self, identificacion, nombre, genero, tecnica, costo_por_clase, num_clases, fecha_registro=None):
        self.identificacion = str(identificacion)
        self.nombre = nombre
        self.genero = genero
        self.tecnica = tecnica
        self.costo_por_clase = int(costo_por_clase)
        self.num_clases = int(num_clases)
        self.fecha_registro = fecha_registro if fecha_registro else datetime.now()

    def calcular_costo(self):
        return self.num_clases * self.costo_por_clase


# Diccionario con los valores por técnica (según el anexo)
VALORES_POR_TECNICA = {
    "Dibujo": 70000,
    "Pintura": 85000,
    "Escritura": 100000,
    "Fotografía": 90000,
    "Grabado": 75000,
}

class AppGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Melodías Perfectas - Acceso")
        self.participantes = []  # lista para almacenar objetos GestionParticipantes
        self._build_login()

    def _build_login(self):
        # Pantalla de acceso
        frm = ttk.Frame(self.root, padding=20)
        frm.grid()

        ttk.Label(frm, text="Autor: Tu Nombre Aquí").grid(column=0, row=0, columnspan=2, sticky="w")
        ttk.Label(frm, text="Aplicación: Melodías Perfectas").grid(column=0, row=1, columnspan=2, sticky="w")
        ttk.Label(frm, text="Ingrese la contraseña:").grid(column=0, row=2, pady=(10,2), sticky="w")

        self.pass_var = tk.StringVar()
        entry_pass = ttk.Entry(frm, textvariable=self.pass_var, show="*")
        entry_pass.grid(column=0, row=3, sticky="w")
        entry_pass.focus()

        btn_ingresar = ttk.Button(frm, text="Ingresar", command=self._verificar_password)
        btn_ingresar.grid(column=1, row=3, padx=(10,0))

        # Info de ayuda
        ttk.Label(frm, text="(contraseña genérica: 123)").grid(column=0, row=4, columnspan=2, sticky="w", pady=(8,0))

        # permitir salir
        btn_salir = ttk.Button(frm, text="Salir", command=self.root.quit)
        btn_salir.grid(column=0, row=5, columnspan=2, pady=(12,0))

    def _verificar_password(self):
        pw = self.pass_var.get().strip()
        if pw == "123":
            self._abrir_registro()
        else:
            messagebox.showerror("Acceso denegado", "Contraseña incorrecta. Intenta de nuevo.")

    def _abrir_registro(self):
        # Nueva ventana principal (registro)
        for widget in self.root.winfo_children():
            widget.destroy()
        self.root.title("Melodías Perfectas - Registro de Participantes")

        frm = ttk.Frame(self.root, padding=12)
        frm.grid(sticky="nsew")
        # Layout
        ttk.Label(frm, text="Registro de Participantes", font=("TkDefaultFont", 14)).grid(column=0, row=0, columnspan=4, pady=(0,10))

        # Identificación
        ttk.Label(frm, text="Identificación:").grid(column=0, row=1, sticky="e")
        self.ident_var = tk.StringVar()
        ttk.Entry(frm, textvariable=self.ident_var).grid(column=1, row=1, sticky="w")

        # Nombre completo
        ttk.Label(frm, text="Nombre completo:").grid(column=0, row=2, sticky="e")
        self.nombre_var = tk.StringVar()
        ttk.Entry(frm, textvariable=self.nombre_var, width=40).grid(column=1, row=2, columnspan=3, sticky="w")

        # Género (radio)
        ttk.Label(frm, text="Género:").grid(column=0, row=3, sticky="e")
        self.genero_var = tk.StringVar(value="M")
        rb_m = ttk.Radiobutton(frm, text="Masculino", variable=self.genero_var, value="M")
        rb_f = ttk.Radiobutton(frm, text="Femenino", variable=self.genero_var, value="F")
        rb_m.grid(column=1, row=3, sticky="w")
        rb_f.grid(column=2, row=3, sticky="w")

        # Técnica artística (combobox)
        ttk.Label(frm, text="Técnica artística:").grid(column=0, row=4, sticky="e")
        self.tecnica_var = tk.StringVar()
        cb = ttk.Combobox(frm, textvariable=self.tecnica_var, state="readonly", values=list(VALORES_POR_TECNICA.keys()))
        cb.grid(column=1, row=4, sticky="w")
        cb.bind("<<ComboboxSelected>>", self._actualizar_costo_por_clase)

        # Costo por clase (deshabilitado)
        ttk.Label(frm, text="Costo por clase:").grid(column=0, row=5, sticky="e")
        self.costo_var = tk.StringVar(value="0")
        ent_costo = ttk.Entry(frm, textvariable=self.costo_var, state="disabled")
        ent_costo.grid(column=1, row=5, sticky="w")

        # Número de clases
        ttk.Label(frm, text="Número de clases:").grid(column=0, row=6, sticky="e")
        self.num_clases_var = tk.StringVar(value="1")
        ttk.Entry(frm, textvariable=self.num_clases_var, width=6).grid(column=1, row=6, sticky="w")

        # Fecha de registro (autogenerada, deshabilitada)
        ttk.Label(frm, text="Fecha de registro:").grid(column=0, row=7, sticky="e")
        self.fecha_var = tk.StringVar(value=datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        ttk.Entry(frm, textvariable=self.fecha_var, state="disabled", width=22).grid(column=1, row=7, sticky="w")

        # Botones: Guardar, Calcular/Mostrar Reporte, Salir
        btn_guardar = ttk.Button(frm, text="Guardar Registro", command=self.guardar_registro)
        btn_guardar.grid(column=0, row=8, pady=(12,0))

        btn_calcular = ttk.Button(frm, text="Calcular Costo / Mostrar Reporte", command=self.calcular_y_mostrar)
        btn_calcular.grid(column=1, row=8, columnspan=2, pady=(12,0), sticky="w")

        btn_salir = ttk.Button(frm, text="Salir de la Aplicación", command=self.confirmar_salir)
        btn_salir.grid(column=3, row=8, pady=(12,0), sticky="e")

        # Mensaje / lista rápida de participantes guardados
        ttk.Label(frm, text="Participantes guardados:").grid(column=0, row=9, columnspan=4, sticky="w", pady=(10,0))
        self.lista_text = tk.Text(frm, height=6, width=60, state="disabled")
        self.lista_text.grid(column=0, row=10, columnspan=4, pady=(4,0))

    def _actualizar_costo_por_clase(self, event=None):
        tecnica = self.tecnica_var.get()
        if tecnica in VALORES_POR_TECNICA:
            self.costo_var.set(str(VALORES_POR_TECNICA[tecnica]))
        else:
            self.costo_var.set("0")

    def guardar_registro(self):
        # Validaciones básicas
        ident = self.ident_var.get().strip()
        nombre = self.nombre_var.get().strip()
        genero = self.genero_var.get()
        tecnica = self.tecnica_var.get()
        costo = self.costo_var.get()
        num_clases = self.num_clases_var.get().strip()
        fecha = self.fecha_var.get()

        if not ident or not nombre or not tecnica:
            messagebox.showwarning("Faltan datos", "Debes completar identificación, nombre y técnica.")
            return

        try:
            num_clases_int = int(num_clases)
            if num_clases_int <= 0:
                raise ValueError()
        except:
            messagebox.showwarning("Dato inválido", "El número de clases debe ser un entero positivo.")
            return

        participante = GestionParticipantes(
            identificacion=ident,
            nombre=nombre,
            genero=genero,
            tecnica=tecnica,
            costo_por_clase=int(costo),
            num_clases=num_clases_int,
            fecha_registro=datetime.now()
        )

        self.participantes.append(participante)
        self._actualizar_lista_text()
        messagebox.showinfo("Guardado", f"Registro guardado para {nombre}.")

    def _actualizar_lista_text(self):
        self.lista_text.config(state="normal")
        self.lista_text.delete("1.0", tk.END)
        for p in self.participantes:
            linea = f"{p.identificacion} - {p.nombre} - {p.tecnica} - clases: {p.num_clases}\n"
            self.lista_text.insert(tk.END, linea)
        self.lista_text.config(state="disabled")

    def calcular_y_mostrar(self):
        # Si ya hay participantes guardados, mostrar el último (o podrías pedir que el usuario seleccione)
        if not self.participantes:
            messagebox.showwarning("Sin registros", "No hay participantes guardados. Guarda uno primero.")
            return

        # Por simplicidad muestro el último guardado
        participante = self.participantes[-1]
        total = participante.calcular_costo()

        # Ventana de reporte
        rep = tk.Toplevel(self.root)
        rep.title("Reporte - Valor a Pagar")
        frm = ttk.Frame(rep, padding=12)
        frm.grid()

        ttk.Label(frm, text="Reporte de Pago", font=("TkDefaultFont", 14)).grid(column=0, row=0, columnspan=2, pady=(0,8))

        datos = [
            ("Identificación:", participante.identificacion),
            ("Nombre:", participante.nombre),
            ("Género:", "Masculino" if participante.genero == "M" else "Femenino"),
            ("Técnica:", participante.tecnica),
            ("Costo por clase:", f"$ {participante.costo_por_clase:,}".replace(",", ".")),
            ("Número de clases:", str(participante.num_clases)),
            ("Fecha de registro:", participante.fecha_registro.strftime("%Y-%m-%d %H:%M:%S")),
            ("Valor total a pagar:", f"$ {total:,}".replace(",", "."))
        ]

        for i, (etq, val) in enumerate(datos, start=1):
            ttk.Label(frm, text=etq).grid(column=0, row=i, sticky="e", padx=(0,8))
            ttk.Label(frm, text=val).grid(column=1, row=i, sticky="w")

        ttk.Button(frm, text="Cerrar", command=rep.destroy).grid(column=0, row=len(datos)+1, columnspan=2, pady=(10,0))

    def confirmar_salir(self):
        if messagebox.askyesno("Confirmar salida", "¿Seguro que quieres salir de la aplicación?"):
            self.root.quit()


if __name__ == "__main__":
    root = tk.Tk()
    app = AppGUI(root)
    root.mainloop()
