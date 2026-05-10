"""
Barra inferior de la aplicación.
"""

import tkinter as tk
import utils.tema as T
from views.base_widget import BaseWidget


class VistaPiePagina(BaseWidget):
    """Pie de página con información del proyecto."""

    def __init__(self, parent: tk.Widget):
        self.frame_raiz = self._construir(parent)

    def _construir(self, parent) -> tk.Frame:
        frame = self.frame(parent, bg=T.FONDO)
        self.separador(frame, bg=T.BORDE).pack(fill="x", side="top")

        inner = self.frame(frame, bg=T.FONDO)
        inner.pack(fill="x", padx=T.PAD_LG,
                   pady=(T.PAD_SM, T.PAD_SM))

        self._construir_izquierda(inner)
        self._construir_derecha(inner)

        return frame

    def _construir_izquierda(self, parent) -> None:
        self.label(parent, "Método Simplex — Gran M",
                   bg=T.FONDO, fg=T.TEXTO3,
                   font=T.FUENTE_MONO_SM).pack(side="left")

    def _construir_derecha(self, parent) -> None:
        self.label(parent, "Investigación Operativa 1",
                   bg=T.FONDO, fg=T.TEXTO3,
                   font=T.FUENTE_MONO_SM).pack(side="right")

    def get_frame(self) -> tk.Frame:
        return self.frame_raiz
