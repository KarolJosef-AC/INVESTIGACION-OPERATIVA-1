"""
Controlador principal (MVC).
Coordina la vista, el motor Simplex y los modelos.
"""

import tkinter as tk
import tkinter.messagebox as mb

from models.estructuras import Problema, Restriccion
from models.simplex_motor import MotorSimplex
from models.ejemplos import EJEMPLOS
from views.vista_principal import VistaPrincipal


class AppController:
    """
    Controlador MVC.
    Recibe eventos de la vista → invoca el motor → actualiza la vista.
    """

    def __init__(self, root: tk.Tk):
        self._root  = root
        self._motor = MotorSimplex()

        # Construir la vista con los callbacks hacia este controlador
        self._vista = VistaPrincipal(
            root,
            on_generar  = self._on_generar,
            on_calcular = self._on_calcular,
            on_limpiar  = self._on_limpiar,
            on_ejemplo  = self._on_ejemplo
        )

    def iniciar(self) -> None:
        """Llama al controlador tras crear la ventana."""
        pass

    # ════════════════════════════════════════════════════════════
    # CALLBACKS (eventos de la vista)
    # ════════════════════════════════════════════════════════════

    def _on_generar(self) -> None:
        """Regenera el formulario con los parámetros actuales."""
        self._vista.panel_problema.regenerar()
        self._vista.panel_tablas.limpiar()
        self._vista.panel_resultado.limpiar()

    def _on_calcular(self) -> None:
        """Lee el formulario, ejecuta Simplex y muestra el resultado."""
        problema = self._leer_problema()
        if problema is None:
            return

        resultado = self._motor.resolver(problema)

        if not resultado.exitoso:
            self._vista.panel_tablas.mostrar_error(resultado.error)
            self._vista.panel_resultado.limpiar()
            return

        self._vista.panel_tablas.mostrar_resultado(resultado, problema.tipo)
        self._vista.panel_resultado.mostrar_resultado(resultado, problema.tipo)

    def _on_limpiar(self) -> None:
        """Regenera el formulario limpio."""
        self._vista.panel_problema.regenerar()
        self._vista.panel_tablas.limpiar()
        self._vista.panel_resultado.limpiar()

    def _on_ejemplo(self, numero: int) -> None:
        """Carga un problema de ejemplo en el formulario."""
        if numero not in EJEMPLOS:
            return
        problema = EJEMPLOS[numero]
        self._vista.panel_problema.cargar_problema(problema)
        self._vista.panel_tablas.limpiar()
        self._vista.panel_resultado.limpiar()

    # ════════════════════════════════════════════════════════════
    # LECTURA Y VALIDACIÓN DEL FORMULARIO
    # ════════════════════════════════════════════════════════════

    def _leer_problema(self) -> Problema | None:
        """
        Lee los datos del formulario y construye un Problema.
        Muestra un diálogo de error si la validación falla.
        Retorna None si hay errores.
        """
        panel = self._vista.panel_problema

        tipo = panel.leer_tipo()

        objetivo = panel.leer_objetivo()
        if objetivo is None:
            mb.showerror(
                "Error de entrada",
                "Revisa los coeficientes de la función objetivo.\n"
                "Todos deben ser números válidos."
            )
            return None

        restricciones_raw = panel.leer_restricciones()
        if restricciones_raw is None:
            mb.showerror(
                "Error de entrada",
                "Revisa los coeficientes y límites de las restricciones.\n"
                "Todos deben ser números válidos."
            )
            return None

        restricciones = [
            Restriccion(
                coeficientes=r["coeficientes"],
                signo=r["signo"],
                limite=r["limite"]
            )
            for r in restricciones_raw
        ]

        return Problema(tipo=tipo, objetivo=objetivo,
                        restricciones=restricciones)
