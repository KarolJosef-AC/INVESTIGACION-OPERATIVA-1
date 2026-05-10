"""
Simplex — Calculadora de Programación Lineal
=============================================
Punto de entrada de la aplicación de escritorio.
Ejecutar:  python main.py
"""

import sys
import os

# Asegurar que el directorio raíz esté en el path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import tkinter as tk
from controllers.app_controller import AppController


def main() -> None:
    root = tk.Tk()
    root.title("Simplex — Calculadora de Programación Lineal")
    root.resizable(True, True)

    # Tamaño mínimo razonable
    root.minsize(1900, 1000)

    controller = AppController(root)
    controller.iniciar()

    root.mainloop()


if __name__ == "__main__":
    main()
