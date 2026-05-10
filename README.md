# 🐔 Simplex - Calculadora de Programación Lineal

## Formulación de raciones alimenticias para Pollos Parrilleros (Fase Inicial)
---

##  Tabla de Contenidos

- [Descripción](#descripción)
- [Características](#características)
- [Instalación](#instalación)
- [Uso](#uso)
- [Estructura del Proyecto](#estructura-del-proyecto)
- [Modelo Matemático](#modelo-matemático)
- [Arquitectura MVC](#arquitectura-mvc)
- [Resultado Esperado](#resultado-esperado)
- [Tecnologías](#tecnologías)
- [Autores](#autores)

---

##  Descripción

Software de escritorio que implementa el **Método Simplex Gran M** para resolver problemas de programación lineal, específicamente diseñado para la **formulación de raciones alimenticias de mínimo costo** para pollos parrilleros en fase inicial (0–21 días).

El programa permite:

- Ingresar problemas de PL con restricciones mixtas (≤, ≥, =)
- Visualizar paso a paso cada iteración del algoritmo Simplex
- Identificar pivotes, razones y operaciones de Gauss-Jordan
- Detectar problemas infactibles o no acotados
- Cálculo automático del costo mínimo en bolivianos (Bs)

---

##  Características

-  **Método Simplex Gran M** para minimización con variables artificiales
-  **Visualización iteración por iteración** de tablas Simplex completas
-  **Interfaz oscura moderna** con resaltado de pivotes en amarillo
-  **Panel de operaciones** con razones y filas pivote normalizadas
-  **Carga de ejemplos precargados** (modelo del proyecto)
-  **Detección de infactibilidad** y problemas no acotados
-  **Scrollbars estilizados** acordes al tema oscuro
-  **Layout de 3 columnas**: Problema | Iteraciones | Solución

---

##  Instalación

### Requisitos previos

- **Python 3.10 o superior**
- **Tkinter** (incluido por defecto en Python)

##  Instalación
### Clonar el repositorio
```bash
git clone [https://github.com/KarolJosef-AC/INVESTIGACION-OPERATIVA-1.git](https://github.com/KarolJosef-AC/INVESTIGACION-OPERATIVA-1.git)
cd INVESTIGACION-OPERATIVA-1
```

### Ejecutar

```bash
python main.py
```

> **Nota:** No se requieren dependencias externas adicionales. Solo Python estándar.

---

##  Uso

### Paso a paso

1. Ejecuta `python main.py`
2. La ventana se abrirá maximizada con 3 paneles:
   - **Izquierda:** Formulario del problema
   - **Centro:** Tablas de iteraciones
   - **Derecha:** Solución y operaciones
3. Haz clic en **"Cargar Modelo del Proyecto"** para cargar el ejemplo de pollos parrilleros
4. Verifica los datos cargados:
   - Función objetivo con 5 variables
   - 5 restricciones (4 ≥ y 1 ≤)
5. Presiona **"CALCULAR"**
6. Observa en el panel central:
   - Tabla inicial con filas Z y M
   - Cada iteración con el pivote resaltado en amarillo
   - Columnas eliminadas atenuadas
7. Revisa en el panel derecho:
   - Z mín = costo total en bolivianos
   - x₁, x₂, x₃, x₄, x₅ = kg de cada ingrediente
   - Razones de factibilidad por iteración
   - Filas pivote normalizadas

---

## 📁 Estructura del Proyecto

```
simplex_python/
│
├── main.py                          # Punto de entrada de la aplicación
├── README.md                        # Este archivo
│
├── utils/                           # Utilidades y configuración
│   ├── matematica.py               # Redondeo, validación numérica, constantes
│   └── tema.py                     # Paleta de colores, fuentes, dimensiones
│
├── models/                          # Lógica de negocio y estructuras de datos
│   ├── estructuras.py              # Dataclasses: Problema, Restriccion, PasoSimplex, etc.
│   ├── simplex_motor.py            # Motor Simplex Gran M (algoritmo completo)
│   └── ejemplos.py                 # Datos del problema de pollos parrilleros
│
├── controllers/                     # Controladores (patrón MVC)
│   └── app_controller.py           # Controlador principal: coordina vista y motor
│
└── views/                           # Interfaz gráfica (Tkinter)
    ├── base_widget.py              # Widgets base reutilizables y canvas con scroll
    ├── vista_principal.py          # Layout principal de 3 columnas
    └── componentes/
        ├── encabezado.py           # Barra superior con título y tipo
        ├── panel_problema.py       # Panel izquierdo: formulario de entrada
        ├── panel_tablas.py         # Panel central: tablas Simplex
        ├── panel_resultado.py      # Panel derecho: solución y operaciones
        └── pie_pagina.py           # Barra inferior informativa
```

---

##  Modelo Matemático

### Datos del problema

| Ingrediente        | Variable | Costo (Bs/kg) |
|--------------------|----------|---------------|
| Maíz Amarillo      | x₁       | 2.39          |
| Harina de Soja     | x₂       | 4.16          |
| Sorgo              | x₃       | 2.06          |
| Carbonato de Calcio| x₄       | 0.80          |
| Afrecho de Trigo   | x₅       | 1.80          |

### Composición nutricional (por kg de ingrediente)

| Ingrediente   | Proteína (%) | Energía (%) | Calcio (%) | Fósforo (%) |
|---------------|-------------|-------------|-----------|------------|
| Maíz (x₁)    | 8.5         | 72.0        | 0.02      | 0.28       |
| Soja (x₂)    | 48.0        | 30.0        | 0.30      | 0.65       |
| Sorgo (x₃)   | 8.0         | 70.0        | 0.03      | 0.30       |
| Carbonato (x₄)| 0.0        | 0.0         | 38.0      | 0.00       |
| Afrecho (x₅) | 15.0        | 55.0        | 0.13      | 0.90       |

### Restricciones nutricionales (en 1000 kg de mezcla)

| Nutriente                  | Requerimiento   | Tipo |
|----------------------------|-----------------|------|
| Proteína Cruda             | ≥ 200 kg (20%)  | ≥    |
| Energía Metabolizable      | ≥ 550 kg (55%)  | ≥    |
| Calcio (Ca)                | ≥ 10.5 kg (1.05%)| ≥   |
| Fósforo Disponible (P)     | ≥ 5.0 kg (0.50%)| ≥    |
| Peso Total                 | ≤ 1000 kg       | ≤    |

### Función Objetivo

```
Min Z = 2.39x₁ + 4.16x₂ + 2.06x₃ + 0.80x₄ + 1.80x₅
```

### Forma estándar (Gran M)

```
Min Z = 2.39x₁ + 4.16x₂ + 2.06x₃ + 0.80x₄ + 1.80x₅ + M(a₁+a₂+a₃+a₄)

Sujeto a:
  0.085x₁ + 0.48x₂  + 0.08x₃  + 0.00x₄ + 0.15x₅   - s₁ + a₁ = 220
  0.72x₁  + 0.30x₂  + 0.70x₃  + 0.00x₄ + 0.55x₅   - s₂ + a₂ = 590
  0.0002x₁+ 0.003x₂ + 0.0003x₃+ 0.38x₄ + 0.0013x₅  - s₃ + a₃ = 10.5
  0.0028x₁+ 0.0065x₂+ 0.003x₃ + 0.00x₄ + 0.009x₅   - s₄ + a₄ = 5.0
  x₁      + x₂      + x₃      + x₄     + x₅         + s₅       = 1000
  xᵢ, sᵢ, aᵢ ≥ 0
```

---

##  Arquitectura MVC

```
┌─────────────────────────────────────────────────────────┐
│                      CONTROLLER                         │
│                 app_controller.py                       │
│                                                         │
│  _leer_problema()  →  lee formulario                    │
│  _on_calcular()    →  ejecuta motor y actualiza vista   │
│  _on_ejemplo()     →  carga datos precargados           │
└──────────┬──────────────────────────┬──────────────────┘
           │                          │
           ▼                          ▼
┌──────────────────┐       ┌──────────────────────┐
│      VIEW        │       │        MODEL         │
│                  │       │                      │
│ vista_principal  │       │ estructuras.py       │
│ panel_problema   │◄─────►│ simplex_motor.py     │
│ panel_tablas     │       │ ejemplos.py          │
│ panel_resultado  │       │                      │
│ encabezado       │       └──────────────────────┘
│ pie_pagina       │
└──────────────────┘
```

### Flujo de ejecución

1. **Vista** → El usuario ingresa datos o carga un ejemplo
2. **Controlador** → Lee y valida los datos del formulario
3. **Modelo** → `MotorSimplex.resolver()` ejecuta el algoritmo
4. **Controlador** → Recibe el `ResultadoSimplex` con todos los pasos
5. **Vista** → Renderiza tablas, solución y operaciones

### Algoritmo Simplex Gran M

```
1. CONSTRUIR TABLA INICIAL
   - Agregar variables de holgura (≤), superfluas (≥) y artificiales (≥, =)
   - Calcular filas Z y M según minimización

2. MIENTRAS haya coeficientes negativos en M o Z:

   a. SELECCIONAR COLUMNA PIVOTE
      - Prioridad: valor más negativo en fila M (si hay artificiales)
      - Luego: valor más negativo en fila Z

   b. SELECCIONAR FILA PIVOTE
      - Prueba del cociente mínimo: B ÷ columna pivote

   c. APLICAR GAUSS-JORDAN
      - Normalizar fila pivote
      - Eliminar en todas las demás filas (incluyendo Z y M)

   d. ACTUALIZAR BASE
      - La variable entrante reemplaza a la saliente
      - Si sale una artificial, se elimina su columna

3. VERIFICAR FACTIBILIDAD
   - Si alguna artificial queda en la base con valor > 0 → INFACTIBLE

4. LEER SOLUCIÓN
   - Variables básicas con sus valores
   - Z = Σ(coeficiente × valor) para variables originales
```

---

##  Resultado Esperado

Al ejecutar el modelo de pollos parrilleros, se obtiene:

```
Z mín  = 2604.32 Bs  (para 1000 kg de alimento)

x₁ (Maíz)       = 189.23 kg
x₂ (Soja)       = 268.35 kg
x₃ (Sorgo)      = 322.59 kg
x₄ (Carbonato)  =  24.49 kg
x₅ (Afrecho)    = 195.35 kg
─────────────────────────────
Total            = 1000.00 kg ✓
```

### Iteraciones del algoritmo

| Iteración | Entra | Sale | Pivote |
|-----------|-------|------|--------|
| 1         | x₁    | a₂   | 0.72   |
| 2         | x₂    | a₁   | 0.48   |
| 3         | x₃    | a₄   | 0.38   |
| 4         | x₅    | a₃   | 0.76   |
| 39        | —     | —    | Óptimo |

---

##  Tecnologías

| Componente         | Tecnología                      |
|--------------------|---------------------------------|
| Lenguaje           | Python 3.10+                    |
| GUI                | Tkinter (nativo)                |
| Arquitectura       | MVC (Modelo-Vista-Controlador)  |
| Estructuras        | Dataclasses                     |
| Control de versiones | Git                           |

---

##  Autores

| Nombre                    | 
|---------------------------|
| Condori Hurtado Gabriel   | 
| Aramayo Calle Karol Josef |

**Docente:** Ing. Sánchez Hervas José Gabriel  
**Materia:** MAT329 - Investigación de Operaciones  
**Universidad:** Universidad Autónoma Gabriel René Moreno  
**Facultad:** Ingeniería de Ciencias de la Comunicación y Telecomunicaciones  
**Gestión:** 1/2026

---

##  Licencia
Este proyecto es de uso académico para la materia MAT329.

---

##  Referencias

- Guía Práctica para el Productor de Pollos Parrilleros (AIESRP)
- Salvador, 2018 — Estándares de calidad para ingredientes de alimentación animal
- Método Simplex Gran M — Investigación de Operaciones