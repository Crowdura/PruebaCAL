
import pathlib as patlb
from datetime import datetime
from tkinter import filedialog
import customtkinter as CustKinder
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import sympy as sp


class createAnalysis:
  def __init__(self):
    self.main_process()

  def main_process(self):
    self.view()
    self.show()

  def view(self):
    self.lv_view = CustKinder.CTk()
    self.lv_view.title("Vista de análisis de datos")
    self.lv_view.geometry("1000x650")

    # Panel lateral izquierdo (Controles)
    self.frame_controles = CustKinder.CTkFrame(self.lv_view, width=300)
    self.frame_controles.pack(side="left", fill="y", padx=10, pady=10)

    self.lv_input = CustKinder.CTkEntry(
        self.frame_controles, placeholder_text="Selección de archivo"
    )
    self.lv_input.pack(pady=10, fill="x", padx=10)

    lv_button = CustKinder.CTkButton(
        self.frame_controles,
        text="Seleccionar Archivo Excel",
        command=self.hadlderEventFil,
    )
    lv_button.pack(pady=5, fill="x", padx=10)

    self.lv_input2 = CustKinder.CTkEntry(
        self.frame_controles, placeholder_text="Carpeta de guardado"
    )
    self.lv_input2.pack(pady=10, fill="x", padx=10)

    lv_button2 = CustKinder.CTkButton(
        self.frame_controles,
        text="Carpeta de Guardado",
        command=self.hadlderEventDil,
    )
    lv_button2.pack(pady=5, fill="x", padx=10)

    lv_button3 = CustKinder.CTkButton(
        self.frame_controles,
        text="Realizar Análisis",
        command=self.calCulos,
        fg_color="green",
    )
    lv_button3.pack(pady=20, fill="x", padx=10)

    # Panel derecho para el gráfico 3D
    self.frame_grafica = CustKinder.CTkFrame(self.lv_view)
    self.frame_grafica.pack(
        side="right", fill="both", expand=True, padx=10, pady=10
    )

  def limpiar_numero(self, val):
    """Limpia cadenas numéricas de Excel y las convierte a float continuo."""
    if isinstance(val, (int, float)):
      return float(val)
    if isinstance(val, str):
      # Remueve puntos de miles y cambia comas por puntos decimales
      val_clean = val.replace(".", "").replace(",", ".")
      return float(val_clean)
    return float(val)

  def analysisExcel(self, file_path, num_rows: int):
    try:
      df = pd.read_excel(file_path)
      idx = num_rows - 2

      if idx < 0 or idx >= len(df):
        print("El número indexado está fuera del rango de la data")

      self.__res = df.iloc[idx].to_dict()

    except Exception as e:
      self.__res = f"Error al analizar el archivo: {e}"

  def creatDocument(self, dir_path, strText: str):
    lv_carpeta = (
        dir_path / "Registro de analisis" / datetime.now().strftime("%Y%m%d")
    )
    lv_archivo = lv_carpeta / "Analisis.txt"
    lv_carpeta.mkdir(parents=True, exist_ok=True)
    lv_content = "Analisis\n" + strText

    with lv_archivo.open("a", encoding="utf-8") as f:
      f.write(lv_content + "\n")

  def hadlderEventFil(self):
    lo_carpeta = filedialog.askopenfile(
        title="Selecciona archivo de datos",
        filetypes=[("Excel files", "*.xlsx *.xls")],
    )
    if lo_carpeta:
      self.ruta = patlb.Path(lo_carpeta.name)
      self.lv_input.delete(0, "end")
      self.lv_input.insert(0, str(self.ruta))

  def hadlderEventDil(self):
    lo_carpeta = filedialog.askdirectory(title="Selecciona carpeta destino")
    if lo_carpeta:
      self.ruta2 = patlb.Path(lo_carpeta)
      self.lv_input2.delete(0, "end")
      self.lv_input2.insert(0, str(self.ruta2))

  def calCulos(self):
    self.analysisExcel(self.ruta, 10)
    self.calProcess()

    val_x = self.limpiar_numero(self.__res["Actividades primarias"])
    val_y = self.limpiar_numero(self.__res["Actividades industriales"])
    val_z = self.limpiar_numero(self.__res["Actividades de servicios"])

    self.creatDocument(
        self.ruta2,
        self.genInforme(
            val_x=val_x,
            val_y=val_y,
            val_z=val_z,
            cm_x=self.lv_costo_marginal_x,
            cm_y=self.lv_costo_marginal_y,
            cm_z=self.lv_costo_marginal_z,
        ),
    )

  def calProcess(self):
    X, Y, Z = sp.symbols("X Y Z")

    # Función estandarizada de costo total
    self.C = (
        0.00001 * X**2
        + 0.000005 * Y**2
        + 0.000005 * Z**2
        + 0.5 * X
        + 0.8 * Y
        + 0.6 * Z
        + 100000
    )

    # Derivadas Parciales (Costos Marginales)
    lv_dC_dx = sp.diff(self.C, X)
    lv_dC_dy = sp.diff(self.C, Y)
    lv_dC_dz = sp.diff(self.C, Z)

    # Conversión a funciones numéricas
    lv_f_dC_dx = sp.lambdify((X, Y, Z), lv_dC_dx, "numpy")
    lv_f_dC_dy = sp.lambdify((X, Y, Z), lv_dC_dy, "numpy")
    lv_f_dC_dz = sp.lambdify((X, Y, Z), lv_dC_dz, "numpy")

    # Obtención de valores numéricos limpios
    val_x = self.limpiar_numero(self.__res["Actividades primarias"])
    val_y = self.limpiar_numero(self.__res["Actividades industriales"])
    val_z = self.limpiar_numero(self.__res["Actividades de servicios"])

    # Evaluación del costo marginal
    self.lv_costo_marginal_x = float(lv_f_dC_dx(val_x, val_y, val_z))
    self.lv_costo_marginal_y = float(lv_f_dC_dy(val_x, val_y, val_z))
    self.lv_costo_marginal_z = float(lv_f_dC_dz(val_x, val_y, val_z))

    # Matriz Hessiana
    lv_hessian = sp.hessian(self.C, (X, Y, Z))
    self.H_eval = np.array(lv_hessian).astype(np.float64)

    # Criterio de Sylvester
    lv_D1 = self.H_eval[0, 0]
    lv_D2 = np.linalg.det(self.H_eval[:2, :2])
    lv_D3 = np.linalg.det(self.H_eval)

    self.es_convexo = lv_D1 > 0 and lv_D2 > 0 and lv_D3 > 0

    # Crear Figura y Axes 3D con estilo oscuro
    self.fig = plt.Figure(figsize=(6, 5), dpi=100, facecolor="#2b2b2b")
    self.ax = self.fig.add_subplot(111, projection="3d", facecolor="#2b2b2b")

    # Limpiar Widgets antiguos en el Frame si re-ejecutas la función
    for widget in self.frame_grafica.winfo_children():
      widget.destroy()

    # Trazar la gráfica
    self.drawGraph(val_x, val_y, val_z)

    # Vincular Canvas
    self.canvas = FigureCanvasTkAgg(self.fig, master=self.frame_grafica)
    self.canvas.draw()
    self.canvas.get_tk_widget().pack(fill="both", expand=True, padx=5, pady=5)

  def drawGraph(self, val_x, val_y, val_z):
    self.ax.clear()

    # Estilo de ejes
    self.ax.tick_params(colors="white", labelsize=8)
    self.ax.xaxis.label.set_color("white")
    self.ax.yaxis.label.set_color("white")
    self.ax.zaxis.label.set_color("white")

    # Encofrar límites explícitos para no dejar la vista vacía
    self.ax.set_xlim(0, val_x * 1.3)
    self.ax.set_ylim(0, val_y * 1.3)
    self.ax.set_zlim(0, val_z * 1.3)

    # Desactivar notación científica
    self.ax.xaxis.get_major_formatter().set_useOffset(False)
    self.ax.xaxis.get_major_formatter().set_scientific(False)
    self.ax.yaxis.get_major_formatter().set_useOffset(False)
    self.ax.yaxis.get_major_formatter().set_scientific(False)
    self.ax.zaxis.get_major_formatter().set_useOffset(False)
    self.ax.zaxis.get_major_formatter().set_scientific(False)

    # 1. Punto de producción en R3
    self.ax.scatter(
        [val_x],
        [val_y],
        [val_z],
        color="red",
        s=80,
        label="Vector de Producción (X)",
    )

    # 2. Proyecciones ortogonales
    self.ax.plot(
        [val_x, val_x],
        [val_y, val_y],
        [0, val_z],
        color="gray",
        linestyle="--",
    )
    self.ax.plot(
        [val_x, val_x], [0, val_y], [0, 0], color="gray", linestyle="--"
    )
    self.ax.plot(
        [0, val_x], [val_y, val_y], [0, 0], color="gray", linestyle="--"
    )

    # 3. Vector Gradiente con Deltas Proporcionales por Eje
    factor_escala = 0.15
    delta_x = val_x * factor_escala if self.lv_costo_marginal_x != 0 else 0
    delta_y = val_y * factor_escala if self.lv_costo_marginal_y != 0 else 0
    delta_z = val_z * factor_escala if self.lv_costo_marginal_z != 0 else 0

    x_fin = val_x + delta_x
    y_fin = val_y + delta_y
    z_fin = val_z + delta_z

    self.ax.plot(
        [val_x, x_fin],
        [val_y, y_fin],
        [val_z, z_fin],
        color="#0066ff",
        linewidth=2.5,
        label="Vector Gradiente ∇C",
    )
    self.ax.scatter([x_fin], [y_fin], [z_fin], color="#0066ff", marker="^", s=40)

    # Títulos y etiquetas
    self.ax.set_title(
        "Ubicación del Vector de Producción en R³", color="white"
    )
    self.ax.set_xlabel("Sector Primario (x)")
    self.ax.set_ylabel("Sector Industrial (y)")
    self.ax.set_zlabel("Sector Servicios (z)")
    self.ax.legend(loc="upper right", fontsize=8)

  def genInforme(self, val_x, val_y, val_z, cm_x, cm_y, cm_z):
    reporte_texto = f"""
        1. Vector de Producción Bruta X (DANE):
        • Primario (x): $ {val_x:,.0f} M
        • Industrial (y): $ {val_y:,.0f} M
        • Servicios (z): $ {val_z:,.0f} M

        2. Costos Marginales [∇C(X)]:
        • ∂C/∂x: $ {cm_x:,.4f}
        • ∂C/∂y: $ {cm_y:,.4f}
        • ∂C/∂z: $ {cm_z:,.4f}

        3. Análisis de Matriz Hessiana H(C):
        • Menor Principal D1: {self.H_eval[0, 0]:.6f}
        • Menor Principal D2: {np.linalg.det(self.H_eval[:2, :2]):.10f}
        • Menor Principal D3: {np.linalg.det(self.H_eval):.14f}

        4. Validación de Mínimo (Sylvester):
        • Estado: {"Estrictamente Convexa" if self.es_convexo else "No Convexa"}
        • Conclusión: {"Garantiza Mínimo Global de Costos" if self.es_convexo else "Punto Silla / Sin Mínimo"}
        """
    return reporte_texto

  def show(self):
    self.lv_view.mainloop()


if __name__ == "__main__":
  lo_MainProcessShow = createAnalysis()