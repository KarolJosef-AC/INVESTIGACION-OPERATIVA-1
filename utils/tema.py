"""
utils/tema.py
=============
Paleta de colores, fuentes y constantes visuales.
Cambiar aquí afecta toda la interfaz.
"""

# ── Colores ──────────────────────────────────────────────────────
FONDO        = "#0d0f14"
FONDO2       = "#13161e"
FONDO3       = "#1a1e29"
BORDE        = "#252a38"
AZUL         = "#4f8ef7"
VERDE        = "#22c55e"
ROJO         = "#ef4444"
AMARILLO     = "#f59e0b"
TEXTO        = "#e8eaf0"
TEXTO2       = "#8b90a0"
TEXTO3       = "#3d4255"

# ── Fuentes ───────────────────────────────────────────────────────
FUENTE_MONO    = ("Courier New", 10)
FUENTE_MONO_SM = ("Courier New", 9)
FUENTE_MONO_LG = ("Courier New", 12)
FUENTE_TITULO  = ("Georgia", 13, "italic")
FUENTE_TITULO_LG = ("Georgia", 18, "bold")
FUENTE_TABLA   = ("Courier New", 8)
FUENTE_TABLA_BOLD = ("Courier New", 8, "bold")

# ── Radios y espaciados ──────────────────────────────────────────
PADDING   = 12
PAD_SM    = 6
PAD_LG    = 18
REDONDEO  = 8

# ── Tamaños de columna (en píxeles) ─────────────────────────────
ANCHO_COL_IZQ = 380
ANCHO_COL_DER = 320

# ── Constantes del algoritmo ─────────────────────────────────────
MAX_VARIABLES     = 6
MIN_VARIABLES     = 2
MAX_RESTRICCIONES = 8
MIN_RESTRICCIONES = 1
MAX_ITERACIONES   = 50