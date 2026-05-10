"""
Barra superior de la aplicación.
"""

import tkinter as tk
import utils.tema as T
from views.base_widget import BaseWidget


class VistaEncabezado(BaseWidget):
    """Encabezado con título y subtítulo."""

    def __init__(self, parent: tk.Widget):
        self.frame_raiz = self._construir(parent)

    def _construir(self, parent) -> tk.Frame:
        frame = self.frame(parent, bg=T.FONDO)
        self._separador_sup = self.separador(frame, bg=T.BORDE)
        self._separador_sup.pack(fill="x", side="bottom")

        inner = self.frame(frame, bg=T.FONDO)
        inner.pack(fill="x", padx=T.PAD_LG, pady=(T.PADDING, T.PADDING))

        self._construir_titulo(inner)
        self._construir_subtitulo(inner)
        self._construir_tipo(inner)
        return frame

    def _construir_titulo(self, parent) -> None:
        frame_t = self.frame(parent, bg=T.FONDO)
        frame_t.pack(side="left", anchor="s")

        lbl = tk.Label(
            frame_t,
            text="Sim",
            bg=T.FONDO, fg=T.TEXTO,
            font=("Georgia", 22, "bold")
        )
        lbl.pack(side="left")

        lbl2 = tk.Label(
            frame_t,
            text="plex",
            bg=T.FONDO, fg=T.AZUL,
            font=("Georgia", 22, "bold")
        )
        lbl2.pack(side="left")

    def _construir_subtitulo(self, parent) -> None:
        lbl = tk.Label(
            parent,
            text="Formulación de raciones alimenticias para Pollos Parrilleros (Fase Inicial)",
            bg=T.FONDO, fg=T.TEXTO2,
            font=("Courier New", 9)
        )
        lbl.pack(side="left", padx=(T.PAD_SM, 0), anchor="s",
                 pady=(0, 3))

    def _construir_tipo(self, parent) -> None:
        lbl3 = tk.Label(
            parent,
            text="MINIMIZACIÓN",
            bg=T.FONDO, fg=T.AZUL,
            font=("Georgia", 10, "bold")
        )
        lbl3.pack(side="right", padx=(0, T.PAD_SM))

    def get_frame(self) -> tk.Frame:
        return self.frame_raiz