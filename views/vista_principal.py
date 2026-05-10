"""
Vista principal: ensambla todos los componentes en el layout de 3 columnas.
No contiene lógica de negocio; solo construye y expone los subcomponentes.
"""

import tkinter as tk
from typing import Callable

import utils.tema as T
from views.base_widget import BaseWidget
from views.componentes.encabezado    import VistaEncabezado
from views.componentes.panel_problema import VistaPanelProblema
from views.componentes.panel_tablas   import VistaPanelTablas
from views.componentes.panel_resultado import VistaPanelResultado
from views.componentes.pie_pagina      import VistaPiePagina


class VistaPrincipal(BaseWidget):
    """
    Layout de 3 columnas:
      [Problema | Iteraciones | Solución/Operaciones]
    """

    def __init__(self, root: tk.Tk,
                 on_generar:  Callable,
                 on_calcular: Callable,
                 on_limpiar:  Callable,
                 on_ejemplo:  Callable[[int], None]):

        self._root = root
        self._root.configure(bg=T.FONDO)

        self._construir_layout(on_generar, on_calcular,
                               on_limpiar, on_ejemplo)

    # ════════════════════════════════════════════════════════════
    # CONSTRUCCIÓN DEL LAYOUT
    # ════════════════════════════════════════════════════════════

    def _construir_layout(self, on_generar, on_calcular,
                          on_limpiar, on_ejemplo) -> None:
        """Encabezado → contenido (3 cols) → pie de página."""

        # ── Encabezado ───────────────────────────────────────────
        self._encabezado = VistaEncabezado(self._root)
        self._encabezado.get_frame().pack(fill="x", side="top")

        # ── Pie ──────────────────────────────────────────────────
        self._pie = VistaPiePagina(self._root)
        self._pie.get_frame().pack(fill="x", side="bottom")

        # ── Contenido central (3 columnas) ───────────────────────
        frame_contenido = self.frame(self._root, bg=T.FONDO)
        frame_contenido.pack(fill="both", expand=True,
                             padx=T.PAD_SM, pady=T.PAD_SM)

        self._construir_columna_izquierda(
            frame_contenido, on_generar, on_calcular,
            on_limpiar, on_ejemplo
        )
        self._construir_columna_derecha(frame_contenido)
        self._construir_columna_central(frame_contenido)

    def _construir_columna_izquierda(self, parent,
                                      on_generar, on_calcular,
                                      on_limpiar, on_ejemplo) -> None:
        """Panel del problema (ancho fijo)."""
        frame = self.frame(parent, bg=T.FONDO2,
                           width=T.ANCHO_COL_IZQ)
        frame.pack(side="left", fill="both", expand=False,
                   padx=(0, T.PAD_SM))
        
        self._panel_problema = VistaPanelProblema(
            frame, on_generar, on_calcular, on_limpiar, on_ejemplo
        )
        self._panel_problema.get_frame().pack(fill="both", expand=True)

    def _construir_columna_central(self, parent) -> None:
        """Panel de iteraciones (crece)."""
        frame = self.frame(parent, bg=T.FONDO2)
        frame.pack(side="left", fill="both", expand=True)

        self._panel_tablas = VistaPanelTablas(frame)
        self._panel_tablas.get_frame().pack(fill="both", expand=True)

    def _construir_columna_derecha(self, parent) -> None:
        """Panel de solución + operaciones (ancho fijo)."""
        frame = self.frame(parent, bg=T.FONDO)
        frame.pack(side="right", fill="both", expand=False)
        frame.pack(side="right", fill="y")
        
        #frame.pack_propagate(False)

        self._panel_resultado = VistaPanelResultado(frame)
        self._panel_resultado.get_frame().pack(fill="both", expand=True)

    # ════════════════════════════════════════════════════════════
    # ACCESO A LOS PANELES (para el controlador)
    # ════════════════════════════════════════════════════════════

    @property
    def panel_problema(self) -> VistaPanelProblema:
        return self._panel_problema

    @property
    def panel_tablas(self) -> VistaPanelTablas:
        return self._panel_tablas

    @property
    def panel_resultado(self) -> VistaPanelResultado:
        return self._panel_resultado
