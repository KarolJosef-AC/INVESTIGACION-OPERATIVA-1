import tkinter as tk
import utils.tema as T
import tkinter.ttk as ttk

class BaseWidget:
    """Mixin con utilidades de construcción de widgets."""

    # ── Frames con fondo ─────────────────────────────────────────

    @staticmethod
    def frame(parent, bg=T.FONDO2, **kwargs) -> tk.Frame:
        return tk.Frame(parent, bg=bg, **kwargs)

    @staticmethod
    def label_frame(parent, text: str, bg=T.FONDO2) -> tk.LabelFrame:
        return tk.LabelFrame(
            parent, text=text,
            bg=bg, fg=T.TEXTO2,
            font=T.FUENTE_MONO_SM,
            bd=1, relief="flat",
            labelanchor="nw"
        )

    # ── Etiquetas ────────────────────────────────────────────────

    @staticmethod
    def label(parent, text: str, bg=T.FONDO2,
              fg=T.TEXTO, font=None, **kwargs) -> tk.Label:
        return tk.Label(
            parent, text=text,
            bg=bg, fg=fg,
            font=font or T.FUENTE_MONO,
            **kwargs
        )

    @staticmethod
    def label_titulo(parent, text: str, bg=T.FONDO2,
                     fg=T.TEXTO, **kwargs) -> tk.Label:
        return tk.Label(
            parent, text=text,
            bg=bg, fg=fg,
            font=T.FUENTE_TITULO,
            **kwargs
        )

    @staticmethod
    def label_seccion(parent, text: str, bg=T.FONDO2) -> tk.Label:
        """Etiqueta de sección en mayúsculas, estilo subtítulo."""
        return tk.Label(
            parent, text=text.upper(),
            bg=bg, fg=T.TEXTO3,
            font=T.FUENTE_MONO_SM
        )

    # ── Entradas ─────────────────────────────────────────────────

    @staticmethod
    def entry_numero(parent, width: int = 6,
                     textvariable=None) -> tk.Entry:
        return tk.Entry(
            parent,
            width=width,
            bg=T.FONDO3, fg=T.TEXTO,
            insertbackground=T.TEXTO,
            relief="flat",
            font=T.FUENTE_MONO,
            bd=1,
            highlightthickness=1,
            highlightbackground=T.BORDE,
            highlightcolor=T.AZUL,
            textvariable=textvariable,
            justify="center"
        )

    @staticmethod
    def entry_spinbox(parent, from_: int, to: int,
                      textvariable=None, width: int = 5) -> tk.Spinbox:
        return tk.Spinbox(
            parent,
            from_=from_, to=to,
            width=width,
            bg=T.FONDO3, fg=T.TEXTO,
            buttonbackground=T.FONDO3,
            insertbackground=T.TEXTO,
            relief="flat",
            font=T.FUENTE_MONO,
            bd=1,
            highlightthickness=1,
            highlightbackground=T.BORDE,
            highlightcolor=T.AZUL,
            textvariable=textvariable,
            justify="center"
        )

    @staticmethod
    def combo(parent, values: list,
              textvariable=None, width: int = 6):
        import tkinter.ttk as ttk
        cb = ttk.Combobox(
            parent, values=values,
            textvariable=textvariable,
            width=width, state="readonly",
            font=T.FUENTE_MONO
        )
        return cb

    # ── Botones ──────────────────────────────────────────────────

    @staticmethod
    def boton(parent, text: str,
              command=None,
              bg=T.AZUL, fg="#ffffff",
              **kwargs) -> tk.Button:
        return tk.Button(
            parent, text=text,
            command=command,
            bg=bg, fg=fg,
            activebackground=T.FONDO3,
            activeforeground=T.TEXTO,
            relief="flat",
            font=T.FUENTE_MONO,
            cursor="hand2",
            padx=10, pady=5,
            **kwargs
        )

    @staticmethod
    def boton_secundario(parent, text: str,
                         command=None, **kwargs) -> tk.Button:
        return tk.Button(
            parent, text=text,
            command=command,
            bg=T.FONDO3, fg=T.TEXTO2,
            activebackground=T.BORDE,
            activeforeground=T.TEXTO,
            relief="flat",
            font=T.FUENTE_MONO,
            cursor="hand2",
            padx=8, pady=5,
            **kwargs
        )

    # ── Separadores ──────────────────────────────────────────────

    @staticmethod
    def separador(parent, bg=T.BORDE,
                  orient="horizontal") -> tk.Frame:
        if orient == "horizontal":
            return tk.Frame(parent, bg=bg, height=1)
        return tk.Frame(parent, bg=bg, width=1)

    # ── Canvas con scroll ────────────────────────────────────────

    @staticmethod
    def canvas_scroll(parent, bg=T.FONDO2):
        """Devuelve (canvas, scrollbar_v, frame_interior)."""
        canvas = tk.Canvas(parent, bg=bg,
                           highlightthickness=0, bd=0)
        sb = tk.Scrollbar(parent, orient="vertical",
                          command=canvas.yview)
        canvas.configure(yscrollcommand=sb.set)

        frame_int = tk.Frame(canvas, bg=bg)
        win_id    = canvas.create_window((0, 0),
                                         window=frame_int,
                                         anchor="nw")

        def _on_configure(event):
            canvas.configure(scrollregion=canvas.bbox("all"))

        def _on_canvas_resize(event):
            canvas.itemconfig(win_id, width=event.width)

        frame_int.bind("<Configure>", _on_configure)
        canvas.bind("<Configure>", _on_canvas_resize)

        # Scroll con rueda del mouse
        def _on_mouse_wheel(event):
            canvas.yview_scroll(-1 * int(event.delta / 120), "units")

        canvas.bind_all("<MouseWheel>", _on_mouse_wheel)

        return canvas, sb, frame_int

    @staticmethod
    def canvas_scroll_xy(parent, bg=T.FONDO2):
        """Devuelve (marco_contenedor, canvas, frame_interior) con scroll X e Y estilizado."""
        wrapper = tk.Frame(parent, bg=bg)
        wrapper.grid_rowconfigure(0, weight=1)
        wrapper.grid_columnconfigure(0, weight=1)

        style = ttk.Style()
        style.theme_use('clam') 

        style.configure("Oscuro.Vertical.TScrollbar",
                        troughcolor=T.FONDO,     
                        background=T.FONDO3,      
                        bordercolor=T.BORDE,     
                        arrowcolor=T.AZUL,      
                        relief="flat")
        
        style.configure("Oscuro.Horizontal.TScrollbar",
                        troughcolor=T.FONDO,
                        background=T.FONDO3,
                        bordercolor=T.BORDE,
                        arrowcolor=T.AZUL,
                        relief="flat")

        style.map("Oscuro.Vertical.TScrollbar",
                background=[('active', T.AZUL)])
        style.map("Oscuro.Horizontal.TScrollbar",
                background=[('active', T.AZUL)])

        canvas = tk.Canvas(wrapper, bg=bg, highlightthickness=0, bd=0)
        
        sb_y = ttk.Scrollbar(wrapper, orient="vertical", command=canvas.yview, 
                            style="Oscuro.Vertical.TScrollbar")
        sb_x = ttk.Scrollbar(wrapper, orient="horizontal", command=canvas.xview, 
                            style="Oscuro.Horizontal.TScrollbar")
        
        canvas.configure(yscrollcommand=sb_y.set, xscrollcommand=sb_x.set)

        canvas.grid(row=0, column=0, sticky="nsew")
        sb_y.grid(row=0, column=1, sticky="ns")
        sb_x.grid(row=1, column=0, sticky="ew")

        frame_int = tk.Frame(canvas, bg=bg)
        canvas.create_window((0, 0), window=frame_int, anchor="nw")

        def _on_configure(event):
            canvas.configure(scrollregion=canvas.bbox("all"))

        frame_int.bind("<Configure>", _on_configure)

        def _on_mouse_wheel(event):
            canvas.yview_scroll(-1 * int(event.delta / 120), "units")
            
        def _on_shift_mouse_wheel(event):
            canvas.xview_scroll(-1 * int(event.delta / 120), "units")

        canvas.bind_all("<MouseWheel>", _on_mouse_wheel)
        canvas.bind_all("<Shift-MouseWheel>", _on_shift_mouse_wheel)

        return wrapper, canvas, frame_int