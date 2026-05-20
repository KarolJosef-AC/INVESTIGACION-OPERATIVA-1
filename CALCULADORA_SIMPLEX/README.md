# 🐔 Simplex - Calculadora de Programación Lineal

## Formulación de raciones alimenticias para Pollos Parrilleros (Fase Inicial)

---

## 📑 Tabla de Contenidos

- [Descripción](#-descripción)
- [Características](#-características)
- [Instalación](#-instalación)
- [Uso](#-uso)
- [Estructura del Proyecto](#-estructura-del-proyecto)
- [Modelo Matemático](#-modelo-matemático)
- [Arquitectura MVC](#-arquitectura-mvc)
- [Resultado Esperado](#-resultado-esperado)
- [Tecnologías](#-tecnologías)
- [Autores](#-autores)
- [Licencia](#-licencia)
- [Referencias](#-referencias)

---

# 📖 Descripción

Software de escritorio desarrollado en **Python** que implementa el:

- Método Simplex Estándar
- Método Simplex Gran M

para resolver problemas de **Programación Lineal**, específicamente orientado a la formulación de raciones alimenticias de mínimo costo para pollos parrilleros en fase inicial (0–21 días).

El sistema permite resolver modelos con restricciones mixtas de tipo:

- ≤ (menor o igual)
- ≥ (mayor o igual)
- = (igualdad)

El programa procesa automáticamente las iteraciones del algoritmo Simplex, mostrando paso a paso:

- tablas iterativas,
- pivotes,
- razones de factibilidad,
- operaciones Gauss-Jordan,
- y solución óptima final.

Además, el software permite:

- ✅ Visualizar iteración por iteración el procedimiento completo
- ✅ Detectar soluciones infactibles
- ✅ Detectar problemas no acotados
- ✅ Mostrar operaciones Gauss-Jordan
- ✅ Calcular automáticamente el costo mínimo en bolivianos (Bs)

---

#  Características

- ✅ Implementación del Método Simplex Estándar y Método Gran M
- ✅ Resolución de problemas de minimización
- ✅ Manejo de restricciones mixtas (≤, ≥, =)
- ✅ Visualización iteración por iteración de tablas Simplex
- ✅ Identificación automática de pivotes
- ✅ Operaciones Gauss-Jordan paso a paso
- ✅ Detección de problemas infactibles
- ✅ Detección de problemas no acotados
- ✅ Interfaz gráfica moderna con tema oscuro
- ✅ Arquitectura MVC organizada
- ✅ Carga automática del modelo del proyecto

---

#  Instalación

## Requisitos previos

- Python 3.10 o superior
- Tkinter (incluido por defecto en Python)

## Clonar el repositorio

```bash
git clone https://github.com/KarolJosef-AC/INVESTIGACION-OPERATIVA-1.git
cd INVESTIGACION-OPERATIVA-1
```

## Ejecutar el programa

```bash
python main.py
```

**Nota:** No se requieren dependencias externas adicionales.

---

#  Uso

## Paso a paso

1. Ejecuta:
   ```bash
   python main.py
   ```

2. La ventana se abrirá maximizada con 3 paneles:
   - **Izquierda:** Formulario del problema
   - **Centro:** Tablas de iteraciones
   - **Derecha:** Solución y operaciones

3. Haz clic en **"Cargar Modelo del Proyecto"**

4. Verifica los datos cargados:
   - Función objetivo con 5 variables
   - 5 restricciones (4 ≥ y 1 ≤)

5. Presiona **"CALCULAR"**

6. Observa en el panel central:
   - Tabla inicial
   - Filas Z y M
   - Pivotes resaltados
   - Iteraciones completas

7. Revisa en el panel derecho:
   - Valor óptimo de Z
   - Variables solución
   - Razones de factibilidad
   - Operaciones Gauss-Jordan

---

# 📁 Estructura del Proyecto

```
INVESTIGACION-OPERATIVA-1/
│
├── main.py
├── README.md
│
├── controllers/
│   └── app_controller.py
│
├── models/
│   ├── estructuras.py
│   ├── simplex_motor.py
│   └── ejemplos.py
│
├── utils/
│   ├── matematica.py
│   └── tema.py
│
└── views/
    ├── base_widget.py
    ├── vista_principal.py
    │
    └── componentes/
        ├── encabezado.py
        ├── panel_problema.py
        ├── panel_tablas.py
        ├── panel_resultado.py
        └── pie_pagina.py
```

---

#  Modelo Matemático

## Variables de decisión

| Variable | Ingrediente | Costo (Bs/kg) |
|----------|-------------|---------------|
| x₁ | Maíz Amarillo | 2.39 |
| x₂ | Harina de Soja | 4.16 |
| x₃ | Sorgo | 2.06 |
| x₄ | Carbonato de Calcio | 0.80 |
| x₅ | Afrecho de Trigo | 1.80 |

## Composición nutricional

| Ingrediente | Proteína (%) | Energía (%) | Calcio (%) | Fósforo (%) |
|-------------|-------------|-----------|----------|-----------|
| Maíz (x₁) | 8.5 | 72.0 | 0.02 | 0.28 |
| Soja (x₂) | 48.0 | 30.0 | 0.30 | 0.65 |
| Sorgo (x₃) | 8.0 | 70.0 | 0.03 | 0.30 |
| Carbonato (x₄) | 0.0 | 0.0 | 38.0 | 0.00 |
| Afrecho (x₅) | 15.0 | 55.0 | 0.13 | 0.90 |

## Restricciones nutricionales

| Nutriente | Requerimiento | Tipo |
|-----------|---------------|------|
| Proteína Cruda | ≥ 200 kg | ≥ |
| Energía Metabolizable | ≥ 550 kg | ≥ |
| Calcio (Ca) | ≥ 10.5 kg | ≥ |
| Fósforo Disponible | ≥ 5.0 kg | ≥ |
| Peso Total | ≤ 1000 kg | ≤ |

## Función Objetivo

```
Min Z = 2.39x₁ + 4.16x₂ + 2.06x₃ + 0.80x₄ + 1.80x₅
```

## Forma estándar — Método Gran M

```
Min Z = 2.39x₁ + 4.16x₂ + 2.06x₃ + 0.80x₄ + 1.80x₅ + M(a₁ + a₂ + a₃ + a₄)
```

**Sujeto a:**

```
(R1)  0.085x₁ + 0.48x₂ + 0.08x₃ + 0.15x₅ - s₁ + a₁ = 200

(R2)  0.72x₁ + 0.30x₂ + 0.70x₃ + 0.55x₅ - s₂ + a₂ = 550

(R3)  0.0002x₁ + 0.003x₂ + 0.0003x₃ + 0.38x₄ + 0.0013x₅ - s₃ + a₃ = 10.5

(R4)  0.0028x₁ + 0.0065x₂ + 0.003x₃ + 0.009x₅ - s₄ + a₄ = 5.0

(R5)  x₁ + x₂ + x₃ + x₄ + x₅ + s₅ = 1000

      xᵢ, sᵢ, aᵢ ≥ 0
```

---

#  Arquitectura MVC

```
┌────────────────────────────────────────────┐
│                 CONTROLLER                 │
│            app_controller.py               │
└───────────────┬────────────────────────────┘
                │
        ┌───────┴────────┐
        ▼                ▼
┌──────────────┐   ┌──────────────┐
│     VIEW     │   │    MODEL     │
│              │   │              │
│ views/       │   │ models/      │
│ interfaz GUI │   │ lógica simplex│
└──────────────┘   └──────────────┘
```

## Flujo de ejecución

1. El usuario ingresa los datos
2. El controlador valida el problema
3. El modelo ejecuta el Método Simplex
4. El controlador recibe los resultados
5. La vista renderiza tablas y solución

---

#  Algoritmo Simplex Gran M

1. **Construcción de la tabla inicial**
   - Variables de holgura
   - Variables superfluas
   - Variables artificiales

2. **Selección de columna pivote**
   - Prioridad fila M
   - Luego fila Z

3. **Selección de fila pivote**
   - Razón mínima positiva

4. **Aplicación de Gauss-Jordan**
   - Normalización
   - Eliminación por filas

5. **Actualización de base**

6. **Verificación de factibilidad**

7. **Lectura de solución óptima**

---

# 📊 Resultado Esperado

Al ejecutar el modelo para pollos parrilleros en fase inicial se obtiene:

**Z mín = 2604.32 Bs**

## Solución óptima

| Variable | Ingrediente | Cantidad |
|----------|-------------|----------|
| x₁ | Maíz Amarillo | 189.23 kg |
| x₂ | Harina de Soja | 268.35 kg |
| x₃ | Sorgo | 322.59 kg |
| x₄ | Carbonato de Calcio | 24.49 kg |
| x₅ | Afrecho de Trigo | 195.35 kg |
| | **Total** | **1000.00 kg** |

## Interpretación de resultados

- El Sorgo domina la mezcla debido a su bajo costo y alto aporte energético.
- La Harina de Soja se utiliza para satisfacer la proteína mínima requerida.
- El Carbonato de Calcio cubre eficientemente la restricción de calcio.
- El Afrecho de Trigo complementa energía y proteína a bajo costo.

---

#  Tecnologías

| Componente | Tecnología |
|-----------|-----------|
| Lenguaje | Python 3.10+ |
| GUI | Tkinter |
| Arquitectura | MVC |
| Estructuras | Dataclasses |
| Control de versiones | Git |

---

# 👥 Autores

| Nombre |
|--------|
| Condori Hurtado Gabriel |
| Aramayo Calle Karol Josef |

**Docente:** Ing. Sánchez Hervas José Gabriel  
**Materia:** MAT329 - Investigación de Operaciones  
**Universidad:** Universidad Autónoma Gabriel René Moreno  
**Facultad:** Ingeniería de Ciencias de la Comunicación y Telecomunicaciones  
**Gestión:** 1/2026

---

# 📄 Licencia

Proyecto desarrollado con fines académicos para la materia:

**MAT329 — Investigación de Operaciones**

---

# 📚 Referencias

- Guía Práctica para el Productor de Pollos Parrilleros (AIESRP)
- Salvador, 2018 — Estándares de calidad para ingredientes de alimentación animal
- Método Simplex Gran M — Investigación de Operaciones