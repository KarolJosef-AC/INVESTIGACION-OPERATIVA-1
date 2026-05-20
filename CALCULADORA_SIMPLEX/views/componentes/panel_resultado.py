"""
Columna derecha: solución óptima y operaciones por iteración.
"""

import tkinter as tk
from typing import List

import utils.tema as T
from views.base_widget import BaseWidget
from models.estructuras import ResultadoSimplex, PasoSimplex
from utils.matematica import redondear, formatear_numero


class VistaPanelResultado(BaseWidget):
    """Panel derecho con la solución y el detalle de operaciones."""

    def __init__(self, parent: tk.Widget):
        self._frame_raiz = self._construir(parent)

    # ════════════════════════════════════════════════════════════
    # CONSTRUCCIÓN
    # ════════════════════════════════════════════════════════════

    def _construir(self, parent) -> tk.Frame:
        outer = self.frame(parent, bg=T.FONDO)
        outer.pack(fill="both", expand=True)

        # Panel solución 
        self._frame_solucion = self._construir_panel_solucion(outer)

        # Panel operaciones 
        self._frame_operaciones = self._construir_panel_operaciones(outer)

        return outer

    # ════════════════════════════════════════════════════════════
    # PANEL SOLUCIÓN
    # ════════════════════════════════════════════════════════════

    def _construir_panel_solucion(self, parent) -> tk.Frame:
        panel = self.frame(parent, bg=T.FONDO2)
        panel.pack(fill="x", pady=(0, T.PAD_SM))

        self._construir_titulo_solucion(panel)
        self.separador(panel).pack(fill="x")

        self._area_solucion = self.frame(panel, bg=T.FONDO2)
        self._area_solucion.pack(fill="x", padx=T.PADDING, pady=T.PADDING)

        self._mostrar_solucion_vacia()
        return panel

    def _construir_titulo_solucion(self, parent) -> None:
        f = self.frame(parent, bg=T.FONDO2)
        f.pack(fill="x", padx=T.PADDING, pady=(T.PADDING, T.PAD_SM))

        punto = tk.Frame(f, bg=T.AMARILLO, width=7, height=7)
        punto.pack(side="left", padx=(0, 8))
        punto.pack_propagate(False)

        self.label_titulo(f, "Solución",
                          bg=T.FONDO2, fg=T.TEXTO).pack(side="left")

    def _mostrar_solucion_vacia(self) -> None:
        for w in self._area_solucion.winfo_children():
            w.destroy()
        self.label(self._area_solucion, "—", fg=T.TEXTO3).pack()

    def _mostrar_solucion(self, resultado: ResultadoSimplex,
                          tipo: str) -> None:
        for w in self._area_solucion.winfo_children():
            w.destroy()
        self._construir_valor_z(resultado, tipo)
        self._construir_chips_variables(resultado)

    def _construir_valor_z(self, resultado: ResultadoSimplex,
                        tipo: str) -> None:
        subindice = "mín"
        f = self.frame(self._area_solucion, bg=T.FONDO2)
        f.pack(anchor="w", pady=(0, T.PAD_SM))
        self.label(f, f"Z{subindice} =",
                fg=T.VERDE, font=("Courier New", 11)).pack(side="left")
        self.label(f, f"{resultado.valor_z}",
                fg=T.TEXTO, font=("Courier New", 16, "bold")).pack(side="left")

    def _construir_chips_variables(self, resultado: ResultadoSimplex) -> None:
        """Muestra los valores de las variables, una debajo de otra."""
        f = self.frame(self._area_solucion, bg=T.FONDO2)
        f.pack(anchor="w", fill="x")
        
        for j in range(resultado.cant_variables):
            idx = next((i for i, v in
                        enumerate(resultado.variables_en_base_final)
                        if v.indice == j), -1)
            val = (redondear(resultado.filas_final[idx][resultado.total_columnas])
                if idx != -1 else 0.0)
            
            # Cada variable en su propia línea
            fila = self.frame(f, bg=T.FONDO2)
            fila.pack(fill="x", pady=1)
            
            self.label(fila, f"x{j+1} = {formatear_numero(val)}",
                    bg=T.FONDO2, fg=T.TEXTO,
                    font=T.FUENTE_MONO).pack(anchor="w")

    # ════════════════════════════════════════════════════════════
    # PANEL OPERACIONES 
    # ════════════════════════════════════════════════════════════

    def _construir_panel_operaciones(self, parent) -> tk.Frame:
        panel = self.frame(parent, bg=T.FONDO2)
        panel.pack(fill="both", expand=True)

        self._construir_titulo_operaciones(panel)
        self.separador(panel).pack(fill="x")

        wrapper, canvas, frame_int = self.canvas_scroll_xy(panel, bg=T.FONDO2)
        wrapper.pack(fill="both", expand=True)

        self._area_ops = frame_int
        return panel

    def _construir_titulo_operaciones(self, parent) -> None:
        f = self.frame(parent, bg=T.FONDO2)
        f.pack(fill="x", padx=T.PADDING, pady=(T.PADDING, T.PAD_SM))
        punto = tk.Frame(f, bg=T.VERDE, width=7, height=7)
        punto.pack(side="left", padx=(0, 8))
        punto.pack_propagate(False)
        self.label_titulo(f, "Operaciones",
                          bg=T.FONDO2, fg=T.TEXTO).pack(side="left")

    def _mostrar_operaciones_vacias(self) -> None:
        for w in self._area_ops.winfo_children():
            w.destroy()

    def _mostrar_operaciones(self, resultado: ResultadoSimplex) -> None:
        for w in self._area_ops.winfo_children():
            w.destroy()
        self._area_ops.configure(padx=T.PADDING, pady=T.PAD_SM)
        for paso in resultado.pasos:
            if paso.numero == 0:
                continue
            paso_anterior = resultado.pasos[paso.numero - 1]
            self._bloque_operacion_iter(paso, paso_anterior,
                                        resultado.total_columnas)

    def _bloque_operacion_iter(self, paso: PasoSimplex,
                               paso_anterior: PasoSimplex,
                               total_columnas: int) -> None:
        bloque = self.frame(self._area_ops, bg=T.FONDO3)
        bloque.pack(fill="x", pady=(0, T.PAD_SM),
                    ipadx=T.PAD_SM, ipady=T.PAD_SM)
        self._titulo_bloque(bloque, paso)
        self._seccion_razones(bloque, paso, paso_anterior, total_columnas)
        self._seccion_fila_pivote(bloque, paso, paso_anterior, total_columnas)

    def _titulo_bloque(self, parent, paso: PasoSimplex) -> None:
        f = self.frame(parent, bg=T.FONDO3)
        f.pack(fill="x", pady=(0, 4))
        self.label(f, f"ITERACIÓN {paso.numero}",
                   bg=T.FONDO3, fg=T.AZUL,
                   font=T.FUENTE_MONO_SM).pack(side="left")
        self.separador(parent, bg=T.BORDE).pack(fill="x", pady=2)

    def _seccion_razones(self, parent, paso: PasoSimplex,
                         paso_anterior: PasoSimplex,
                         total_columnas: int) -> None:
        self.label(parent, "Razones  B ÷ col.pivote",
                   bg=T.FONDO3, fg=T.TEXTO3,
                   font=T.FUENTE_MONO_SM).pack(anchor="w", pady=(2, 1))
        fp = paso.fila_pivote
        cp = paso.columna_pivote
        filas_antes = paso_anterior.filas
        for i, fila in enumerate(filas_antes):
            den = fila[cp]
            if den > 0:
                razon = redondear(fila[total_columnas] / den)
                es_menor = (i == fp)
                txt = (f"F{i+1}: {formatear_numero(fila[total_columnas])}"
                       f" ÷ {formatear_numero(den)} = {razon}"
                       + (" ←" if es_menor else ""))
                self.label(parent, txt,
                           bg=T.FONDO3,
                           fg=T.AMARILLO if es_menor else T.TEXTO,
                           font=T.FUENTE_MONO_SM).pack(anchor="w")
            else:
                self.label(parent, f"F{i+1}: descartada",
                           bg=T.FONDO3, fg=T.TEXTO3,
                           font=T.FUENTE_MONO_SM).pack(anchor="w")

    def _seccion_fila_pivote(self, parent, paso: PasoSimplex,
                             paso_anterior: PasoSimplex,
                             total_columnas: int) -> None:
        fp = paso.fila_pivote
        cp = paso.columna_pivote
        elem_piv = redondear(paso_anterior.filas[fp][cp])
        self.separador(parent, bg=T.BORDE).pack(fill="x", pady=3)
        self.label(parent, f"Fila pivote ÷ {elem_piv}",
                   bg=T.FONDO3, fg=T.TEXTO3,
                   font=T.FUENTE_MONO_SM).pack(anchor="w", pady=(0, 1))
        valores = " | ".join(
            formatear_numero(v / elem_piv)
            for v in paso_anterior.filas[fp]
        )
        self.label(parent, valores,
                   bg=T.FONDO3, fg=T.TEXTO,
                   font=T.FUENTE_MONO_SM,
                   wraplength=250, justify="left").pack(anchor="w")

    # ════════════════════════════════════════════════════════════

    def mostrar_resultado(self, resultado: ResultadoSimplex,
                          tipo: str) -> None:
        self._mostrar_solucion(resultado, tipo)
        self._mostrar_operaciones(resultado)

    def limpiar(self) -> None:
        self._mostrar_solucion_vacia()
        self._mostrar_operaciones_vacias()

    def get_frame(self) -> tk.Frame:
        return self._frame_raiz