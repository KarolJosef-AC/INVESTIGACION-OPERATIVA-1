"""
Columna central: muestra las tablas Simplex de cada iteración.
"""

import tkinter as tk
from typing import List, Optional

import utils.tema as T
from views.base_widget import BaseWidget
from models.estructuras import PasoSimplex, ResultadoSimplex
from utils.matematica import redondear, formatear_numero


class VistaPanelTablas(BaseWidget):
    """Panel central que renderiza las iteraciones del Simplex."""

    def __init__(self, parent: tk.Widget):
        self._frame_raiz = self._construir(parent)

    def _construir(self, parent) -> tk.Frame:
        outer = self.frame(parent, bg=T.FONDO2)

        self._construir_titulo_panel(outer)
        self.separador(outer).pack(fill="x")

        wrapper, canvas, frame_int = self.canvas_scroll_xy(outer, bg=T.FONDO2)
        wrapper.pack(fill="both", expand=True)

        self._frame_contenido = frame_int
        self._mostrar_espera()
        return outer

    def _construir_titulo_panel(self, parent) -> None:
        f = self.frame(parent, bg=T.FONDO2)
        f.pack(fill="x", padx=T.PADDING, pady=(T.PADDING, T.PAD_SM))

        punto = tk.Frame(f, bg=T.VERDE, width=7, height=7)
        punto.pack(side="left", padx=(0, 8))
        punto.pack_propagate(False)

        self.label_titulo(f, "Iteraciones",
                          bg=T.FONDO2, fg=T.TEXTO).pack(side="left")

    def _limpiar_contenido(self) -> None:
        for w in self._frame_contenido.winfo_children():
            w.destroy()

    def _mostrar_espera(self) -> None:
        self._limpiar_contenido()
        f = self.frame(self._frame_contenido, bg=T.FONDO2)
        f.pack(expand=True, pady=60)
        self.label(f, "∑", fg=T.TEXTO3,
                   font=("Courier New", 36)).pack()
        self.label(f, "INGRESA LOS DATOS Y PRESIONA CALCULAR",
                   fg=T.TEXTO3, font=T.FUENTE_MONO_SM).pack(pady=6)

    def mostrar_error(self, mensaje: str) -> None:
        self._limpiar_contenido()
        frame_err = self.frame(self._frame_contenido, bg="#1c0d0d")
        frame_err.pack(fill="x", padx=T.PADDING, pady=T.PADDING,
                       ipadx=T.PADDING, ipady=T.PADDING)
        self.label(frame_err, f"⚠  {mensaje}",
                   bg="#1c0d0d", fg=T.ROJO,
                   font=T.FUENTE_MONO_SM,
                   wraplength=500, justify="left").pack(anchor="w")

    def limpiar(self) -> None:
        self._mostrar_espera()

    def mostrar_resultado(self, resultado: ResultadoSimplex,
                          tipo: str) -> None:
        self._limpiar_contenido()
        c = self._frame_contenido
        c.configure(padx=T.PADDING, pady=T.PADDING)
        self._mostrar_iteraciones(c, resultado, tipo)

    def _mostrar_iteraciones(self, parent, resultado: ResultadoSimplex,
                             tipo: str) -> None:
        for paso in resultado.pasos:
            self._construir_bloque_paso(parent, paso,
                                        resultado.total_columnas,
                                        tipo)

    def _construir_bloque_paso(self, parent, paso: PasoSimplex,
                               total_columnas: int, tipo: str) -> None:
        bloque = self.frame(parent, bg=T.FONDO2)
        bloque.pack(fill="both", expand=True, pady=(0, T.PAD_LG))
        self._construir_descripcion_paso(bloque, paso)
        self._construir_tabla(bloque, paso, total_columnas)
        if tipo == "min" and paso.numero > 0:
            self._construir_nota_z(bloque)

    def _construir_descripcion_paso(self, parent,
                                    paso: PasoSimplex) -> None:
        self.label(
            parent, paso.descripcion.upper(),
            fg=T.AZUL, font=T.FUENTE_MONO_SM
        ).pack(anchor="w", pady=(0, 4))

    def _construir_nota_z(self, parent) -> None:
        self.label(
            parent, "* Z negativo indica minimización",
            fg=T.TEXTO3, font=T.FUENTE_MONO_SM
        ).pack(anchor="w", pady=(2, 0))

    def _construir_tabla(self, parent, paso: PasoSimplex,
                         total_columnas: int) -> None:
        encabezados = self._generar_encabezados(paso, total_columnas)
        frame_tabla = self.frame(parent, bg=T.FONDO3)
        frame_tabla.pack(fill="x", pady=(0, 2))

        self._fila_encabezados(frame_tabla, encabezados, paso, total_columnas)

        for i, fila in enumerate(paso.filas):
            self._fila_datos(frame_tabla, i, fila, paso, total_columnas,
                             paso.variables_en_base[i].nombre)

        self._fila_z(frame_tabla, paso, total_columnas)

        if any(v != 0 for v in paso.fila_m):
            self._fila_m(frame_tabla, paso, total_columnas)

    def _generar_encabezados(self, paso: PasoSimplex,
                             total_columnas: int) -> List[str]:
        enc = []
        for j in range(total_columnas):
            if j < 5:
                enc.append(f"x{j+1}")
            elif j < 9:
                enc.append(f"s{j-4}")
            elif j < 13:
                enc.append(f"a{j-8}")
            else:
                enc.append(f"h{j-12}")
        enc.append("B")
        return enc

    def _celda(self, parent, text: str, row: int, col: int,
               bg=T.FONDO2, fg=T.TEXTO,
               font=None, width: int = 7) -> tk.Label:
        lbl = tk.Label(
            parent, text=text, width=width,
            bg=bg, fg=fg,
            font=font or T.FUENTE_TABLA,
            relief="flat", bd=0,
            padx=1, pady=1
        )
        lbl.grid(row=row, column=col, sticky="nsew", padx=1, pady=1)
        return lbl

    def _fila_encabezados(self, parent, encabezados: List[str],
                          paso: PasoSimplex,
                          total_columnas: int) -> None:
        self._celda(parent, "Base", 0, 0,
                    bg=T.FONDO3, fg=T.TEXTO2,
                    font=T.FUENTE_TABLA_BOLD)

        for j, titulo in enumerate(encabezados):
            eliminada = j in paso.columnas_eliminadas
            es_pivote = (j == paso.columna_pivote)
            bg = T.FONDO3
            fg = T.TEXTO3 if eliminada else (T.AMARILLO if es_pivote else T.TEXTO2)
            self._celda(parent, titulo, 0, j + 1,
                        bg=bg, fg=fg,
                        font=T.FUENTE_TABLA_BOLD)

    def _fila_datos(self, parent, fila_idx: int,
                    fila: List[float], paso: PasoSimplex,
                    total_columnas: int, nombre_base: str) -> None:
        row = fila_idx + 1
        es_fila_pivote = (fila_idx == paso.fila_pivote)
        bg_fila = "#141820" if es_fila_pivote else T.FONDO2

        self._celda(parent, nombre_base, row, 0,
                    bg=bg_fila, fg=T.TEXTO2)

        for j, val in enumerate(fila):
            eliminada = j in paso.columnas_eliminadas
            es_pivote_c = (j == paso.columna_pivote)
            es_pivote_celda = es_fila_pivote and es_pivote_c

            if eliminada:
                bg, fg = bg_fila, T.TEXTO3
            elif es_pivote_celda:
                bg, fg = "#2a2000", T.AMARILLO
            elif es_pivote_c:
                bg, fg = "#1d1800", T.AMARILLO
            else:
                bg, fg = bg_fila, T.TEXTO

            self._celda(parent, formatear_numero(val),
                        row, j + 1, bg=bg, fg=fg)

    def _fila_z(self, parent, paso: PasoSimplex,
                total_columnas: int) -> None:
        row = len(paso.filas) + 1
        self._celda(parent, "Z", row, 0,
                    bg="#0d1520", fg=T.AZUL,
                    font=T.FUENTE_TABLA_BOLD)

        for j, val in enumerate(paso.fila_z):
            eliminada = j in paso.columnas_eliminadas
            es_pivote = (j == paso.columna_pivote)
            fg = T.TEXTO3 if eliminada else (T.AMARILLO if es_pivote else T.AZUL)
            self._celda(parent, formatear_numero(val),
                        row, j + 1, bg="#0d1520", fg=fg)

    def _fila_m(self, parent, paso: PasoSimplex,
                total_columnas: int) -> None:
        row = len(paso.filas) + 2
        self._celda(parent, "M", row, 0,
                    bg="#1a1500", fg=T.AMARILLO,
                    font=T.FUENTE_TABLA_BOLD)

        for j, val in enumerate(paso.fila_m):
            eliminada = j in paso.columnas_eliminadas
            es_pivote = (j == paso.columna_pivote)
            fg = T.TEXTO3 if eliminada else (T.AMARILLO if es_pivote else T.AMARILLO)
            self._celda(parent, formatear_numero(val),
                        row, j + 1, bg="#1a1500", fg=fg)

    def get_frame(self) -> tk.Frame:
        return self._frame_raiz