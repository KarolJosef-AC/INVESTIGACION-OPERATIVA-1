"""
Columna izquierda: ingreso del problema.

Sub-funciones independientes para cada sección:
  · _seccion_parametros()   → tipo, variables, restricciones
  · _seccion_objetivo()     → coeficientes de Z
  · _seccion_restricciones()→ filas de restricciones
  · _seccion_botones()      → calcular, limpiar, ejemplos
"""

import tkinter as tk
import tkinter.ttk as ttk
from typing import Callable, Dict, List, Optional

import utils.tema as T
from views.base_widget import BaseWidget


class VistaPanelProblema(BaseWidget):
    """Panel izquierdo con el formulario del problema."""

    def __init__(self, parent: tk.Widget,
                 on_generar:  Callable,
                 on_calcular: Callable,
                 on_limpiar:  Callable,
                 on_ejemplo:  Callable[[int], None]):
        # Callbacks hacia el controlador
        self._on_generar  = on_generar
        self._on_calcular = on_calcular
        self._on_limpiar  = on_limpiar
        self._on_ejemplo  = on_ejemplo

        # Variables de control
        self._var_tipo        = tk.StringVar(value="min")
        self._var_variables   = tk.IntVar(value=2)
        self._var_restricciones = tk.IntVar(value=2)

        # Entradas dinámicas
        self._entradas_objetivo:     List[tk.Entry]       = []
        self._entradas_restricciones: List[Dict]          = []

        self._frame_raiz = self._construir(parent)
        self._generar_campos()

    # ════════════════════════════════════════════════════════════
    # CONSTRUCCIÓN DEL PANEL
    # ════════════════════════════════════════════════════════════

    def _construir(self, parent) -> tk.Frame:
        """Marco exterior con borde y scroll vertical."""
        outer = self.frame(parent, bg=T.FONDO2)
        outer.pack(fill="both", expand=False,
                   ipadx=0, ipady=0)

        # Título del panel
        self._construir_titulo_panel(outer)
        self.separador(outer).pack(fill="x")

        # Contenedor con scroll bidireccional
        wrapper, canvas, frame_int = self.canvas_scroll_xy(outer, bg=T.FONDO2)
        wrapper.pack(fill="both", expand=True)

        self._frame_contenido = frame_int
        return outer

    def _construir_titulo_panel(self, parent) -> None:
        """Encabezado del panel izquierdo."""
        f = self.frame(parent, bg=T.FONDO2)
        f.pack(fill="x", padx=T.PADDING, pady=(T.PADDING, T.PAD_SM))

        punto = tk.Frame(f, bg=T.AZUL, width=7, height=7)
        punto.pack(side="left", padx=(0, 8))
        punto.pack_propagate(False)

        self.label_titulo(f, "Problema", bg=T.FONDO2,
                          fg=T.TEXTO).pack(side="left")

    # ════════════════════════════════════════════════════════════
    # SECCIÓN 1: PARÁMETROS (tipo / variables / restricciones)
    # ════════════════════════════════════════════════════════════

    def _seccion_parametros(self, parent) -> None:
        """Dropdowns y spinboxes de configuración."""
        self.label_seccion(parent, "Parámetros").pack(
            anchor="w", pady=(T.PADDING, 4))

        frame_grid = self.frame(parent, bg=T.FONDO2)
        frame_grid.pack(fill="x", pady=(0, 4))

        # ── Tipo ─────────────────────────────────────────────────
        self._construir_campo_tipo(frame_grid)

        # ── Variables ────────────────────────────────────────────
        self._construir_campo_variables(frame_grid)

        # ── Restricciones ────────────────────────────────────────
        self._construir_campo_restricciones(frame_grid)

        # ── Botón generar ────────────────────────────────────────
        self._construir_boton_generar(parent)

    def _construir_campo_tipo(self, parent) -> None:
        f = self.frame(parent, bg=T.FONDO2)
        f.pack(side="left", padx=(0, T.PAD_SM))

        self.label(f, "Tipo", fg=T.TEXTO2,
                font=T.FUENTE_MONO_SM).pack(anchor="w")
        
        self.label(f, "Minimización", fg=T.VERDE,
                font=T.FUENTE_MONO_SM).pack(pady=(2, 0))

    def _construir_campo_variables(self, parent) -> None:
        f = self.frame(parent, bg=T.FONDO2)
        f.pack(side="left", padx=(0, T.PAD_SM))

        self.label(f, "Variables", fg=T.TEXTO2,
                   font=T.FUENTE_MONO_SM).pack(anchor="w")

        sp = self.entry_spinbox(
            f, from_=T.MIN_VARIABLES, to=T.MAX_VARIABLES,
            textvariable=self._var_variables, width=5
        )
        sp.pack()

    def _construir_campo_restricciones(self, parent) -> None:
        f = self.frame(parent, bg=T.FONDO2)
        f.pack(side="left")

        self.label(f, "Restricciones", fg=T.TEXTO2,
                   font=T.FUENTE_MONO_SM).pack(anchor="w")

        sp = self.entry_spinbox(
            f, from_=T.MIN_RESTRICCIONES, to=T.MAX_RESTRICCIONES,
            textvariable=self._var_restricciones, width=5
        )
        sp.pack()

    def _construir_boton_generar(self, parent) -> None:
        btn = self.boton(
            parent, "⟳  GENERAR CAMPOS",
            command=self._on_generar,
            bg=T.FONDO3, fg=T.AZUL
        )
        btn.pack(fill="x", pady=(4, 0))

    # ════════════════════════════════════════════════════════════
    # SECCIÓN 2: FUNCIÓN OBJETIVO
    # ════════════════════════════════════════════════════════════

    def _seccion_objetivo(self, parent, cant_var: int) -> None:
        """Entradas de coeficientes de Z."""
        self.separador(parent).pack(fill="x", pady=T.PADDING)
        self.label_seccion(parent, "Función Objetivo — Z").pack(
            anchor="w", pady=(0, 4))

        frame_campos = self.frame(parent, bg=T.FONDO2)
        frame_campos.pack(anchor="w")

        self._entradas_objetivo = []

        for i in range(cant_var):
            self._construir_campo_objetivo(frame_campos, i)

    def _construir_campo_objetivo(self, parent, indice: int) -> None:
        """Un par (etiqueta xᵢ + entrada) para el objetivo."""
        f = self.frame(parent, bg=T.FONDO2)
        f.pack(side="left", padx=(0, T.PAD_SM))

        self.label(f, f"x{indice + 1}", fg=T.TEXTO3,
                   font=T.FUENTE_MONO_SM).pack()

        entry = self.entry_numero(f, width=6)
        entry.insert(0, "0")
        entry.pack()

        self._entradas_objetivo.append(entry)

    # ════════════════════════════════════════════════════════════
    # SECCIÓN 3: RESTRICCIONES
    # ════════════════════════════════════════════════════════════

    def _seccion_restricciones(self, parent,
                                cant_rest: int, cant_var: int) -> None:
        """Filas de restricciones."""
        self.separador(parent).pack(fill="x", pady=T.PADDING)
        self.label_seccion(parent, "Restricciones").pack(
            anchor="w", pady=(0, 4))

        self._entradas_restricciones = []

        for i in range(cant_rest):
            self._construir_fila_restriccion(parent, i, cant_var)

    def _construir_fila_restriccion(self, parent,
                                    indice: int, cant_var: int) -> None:
        """Una fila completa Rᵢ: [coef…] [signo] [B]."""
        frame_fila = self.frame(parent, bg=T.FONDO3)
        frame_fila.pack(fill="x", pady=2, ipady=6, ipadx=6)

        # Etiqueta Rᵢ
        self.label(frame_fila, f"R{indice + 1}",
                   bg=T.FONDO3, fg=T.AZUL,
                   font=T.FUENTE_MONO_SM).pack(side="left", padx=(4, 6))

        # Coeficientes
        entradas_coef = []
        for j in range(cant_var):
            g = self.frame(frame_fila, bg=T.FONDO3)
            g.pack(side="left", padx=2)
            self.label(g, f"x{j+1}", bg=T.FONDO3,
                        fg=T.TEXTO3, font=("Courier New", 7)).pack()
            e = self.entry_numero(g, width=4)
            e.insert(0, "0")
            e.pack()
            entradas_coef.append(e)

        # Selector de signo
        var_signo = tk.StringVar(value="<=")
        style = ttk.Style()
        
        # 1. Configuración estática base para el identificador Sign.TCombobox
        style.configure(
            "Sign.TCombobox",
            fieldbackground=T.FONDO3,
            background=T.FONDO3,
            foreground=T.TEXTO,
            arrowcolor=T.TEXTO2,
            selectbackground=T.FONDO3,
            selectforeground=T.TEXTO,
        )
        
        # 2. Mapeo dinámico de estados para anular el renderizado nativo
        style.map(
            "Sign.TCombobox",
            fieldbackground=[("readonly", T.FONDO3)],
            selectbackground=[("readonly", T.FONDO3)],
            background=[("readonly", T.FONDO3)],
            foreground=[("readonly", T.TEXTO)]
        )

        cb_signo = ttk.Combobox(
            frame_fila, values=["<=", ">=", "="],
            textvariable=var_signo,
            width=3, state="readonly",
            font=T.FUENTE_MONO,
            style="Sign.TCombobox"
        )
        cb_signo.pack(side="left", padx=4)

        # Límite B
        g_b = self.frame(frame_fila, bg=T.FONDO3)
        g_b.pack(side="left", padx=2)
        self.label(g_b, "B", bg=T.FONDO3,
                   fg=T.TEXTO3, font=T.FUENTE_MONO_SM).pack()
        e_b = self.entry_numero(g_b, width=5)
        e_b.insert(0, "0")
        e_b.pack()

        self._entradas_restricciones.append({
            "coeficientes": entradas_coef,
            "signo":        var_signo,
            "limite":       e_b
        })

    # ════════════════════════════════════════════════════════════
    # SECCIÓN 4: BOTONES DE ACCIÓN
    # ════════════════════════════════════════════════════════════

    def _seccion_botones(self, parent) -> None:
        """Botones calcular, limpiar y ejemplos."""
        self.separador(parent).pack(fill="x", pady=T.PADDING)

        self._construir_botones_principales(parent)
        self._construir_botones_ejemplos(parent)

    def _construir_botones_principales(self, parent) -> None:
        f = self.frame(parent, bg=T.FONDO2)
        f.pack(fill="x", pady=(0, T.PAD_SM))

        self.boton(f, "CALCULAR",
                   command=self._on_calcular).pack(
                       side="left", fill="x", expand=True,
                       padx=(0, T.PAD_SM))

        self.boton_secundario(f, "LIMPIAR",
                              command=self._on_limpiar).pack(side="left")

    def _construir_botones_ejemplos(self, parent) -> None:
        f = self.frame(parent, bg=T.FONDO2)
        f.pack(fill="x")

        self.boton_secundario(
            f, "Cargar Modelo del Proyecto",
            command=lambda: self._on_ejemplo(1)
        ).pack(side="left", fill="x", expand=True, padx=(0, 4))
        
    # ════════════════════════════════════════════════════════════
    # GENERACIÓN / RECONSTRUCCIÓN DEL FORMULARIO
    # ════════════════════════════════════════════════════════════

    def _generar_campos(self) -> None:
        """Reconstruye el formulario con los parámetros actuales."""
        for widget in self._frame_contenido.winfo_children():
            widget.destroy()

        c = self._frame_contenido
        c.configure(padx=T.PADDING, pady=T.PADDING)

        nv = self._var_variables.get()
        nr = self._var_restricciones.get()

        self._seccion_parametros(c)
        self._seccion_objetivo(c, nv)
        self._seccion_restricciones(c, nr, nv)
        self._seccion_botones(c)

    def regenerar(self) -> None:
        """Llamado desde el controlador al presionar 'Generar campos'."""
        self._generar_campos()

    # ════════════════════════════════════════════════════════════
    # LECTURA DE DATOS
    # ════════════════════════════════════════════════════════════

    def leer_tipo(self) -> str:
        return "min"

    def leer_objetivo(self) -> Optional[List[float]]:
        """Devuelve lista de coeficientes o None si hay error."""
        vals = []
        for i, e in enumerate(self._entradas_objetivo):
            txt = e.get().strip()
            from utils.matematica import es_numero_valido
            if not es_numero_valido(txt):
                return None
            vals.append(float(txt))
        return vals

    def leer_restricciones(self):
        """
        Devuelve lista de dicts:
          {'coeficientes': [...], 'signo': str, 'limite': float}
        o None si hay error de validación.
        """
        from utils.matematica import es_numero_valido
        resultado = []
        for fila in self._entradas_restricciones:
            coefs = []
            for e in fila["coeficientes"]:
                txt = e.get().strip()
                if not es_numero_valido(txt):
                    return None
                coefs.append(float(txt))
            txt_b = fila["limite"].get().strip()
            if not es_numero_valido(txt_b):
                return None
            resultado.append({
                "coeficientes": coefs,
                "signo":        fila["signo"].get(),
                "limite":       float(txt_b)
            })
        return resultado

    # ════════════════════════════════════════════════════════════
    # CARGA DE EJEMPLO
    # ════════════════════════════════════════════════════════════

    def cargar_problema(self, problema) -> None:
        """Llena el formulario con los datos de un Problema."""
        from models.estructuras import Problema
        self._var_tipo.set(problema.tipo)
        self._var_variables.set(problema.cant_variables)
        self._var_restricciones.set(problema.cant_restricciones)
        self._generar_campos()

        # Esperar a que los widgets estén creados
        self._frame_contenido.update_idletasks()

        for i, val in enumerate(problema.objetivo):
            if i < len(self._entradas_objetivo):
                self._entradas_objetivo[i].delete(0, tk.END)
                self._entradas_objetivo[i].insert(0, str(val))

        for i, r in enumerate(problema.restricciones):
            if i < len(self._entradas_restricciones):
                fila = self._entradas_restricciones[i]
                for j, c in enumerate(r.coeficientes):
                    if j < len(fila["coeficientes"]):
                        fila["coeficientes"][j].delete(0, tk.END)
                        fila["coeficientes"][j].insert(0, str(c))
                fila["signo"].set(r.signo)
                fila["limite"].delete(0, tk.END)
                fila["limite"].insert(0, str(r.limite))

    # ── Acceso al frame raíz ─────────────────────────────────────

    def get_frame(self) -> tk.Frame:
        return self._frame_raiz
