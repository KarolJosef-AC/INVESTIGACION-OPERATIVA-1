"""
Motor Simplex Gran M 
"""

from models.estructuras import (
    Problema, ResultadoSimplex, PasoSimplex, VariableBase
)
from utils.matematica import redondear, MAX_ITERACIONES


class MotorSimplex:
    TOL = 1e-5

    def resolver(self, problema: Problema) -> ResultadoSimplex:
        try:
            return self._ejecutar(problema)
        except Exception as exc:
            import traceback
            traceback.print_exc()
            return ResultadoSimplex(
                pasos=[], valores_variables=[], valor_z=0,
                cant_variables=0, total_columnas=0,
                variables_en_base_final=[], filas_final=[],
                error=str(exc)
            )

    # ----------------------------------------------------------
    # CONSTRUCCIÓN DE LA TABLA INICIAL
    # ----------------------------------------------------------
    def _construir_tabla(self, problema: Problema):
        nv   = problema.cant_variables
        nr   = problema.cant_restricciones
        obj  = problema.objetivo
        tipo = problema.tipo

        # 1. Índices de variables auxiliares
        col_idx   = nv
        rest_info = []
        for r in problema.restricciones:
            if r.signo == "<=":
                rest_info.append({"tipo": "<=", "holgura": col_idx})
                col_idx += 1
            elif r.signo == ">=":
                rest_info.append({
                    "tipo":       ">=",
                    "superflua":  col_idx,
                    "artificial": col_idx + 1
                })
                col_idx += 2
            else:  # "="
                rest_info.append({"tipo": "=", "artificial": col_idx})
                col_idx += 1

        total_col = col_idx   # número de columnas sin B

        # 2. Matriz de restricciones + base inicial
        filas          = []
        variables_base = []
        cb_num = [0.0] * nr   # coef. numérico en FO de la variable básica
        cb_m   = [0.0] * nr   # 1 si la variable básica es artificial

        for i, r in enumerate(problema.restricciones):
            fila = [0.0] * (total_col + 1)
            for j in range(nv):
                fila[j] = r.coeficientes[j]

            info = rest_info[i]
            if info["tipo"] == "<=":
                h = info["holgura"]
                fila[h] = 1.0
                variables_base.append(
                    VariableBase(nombre=f"h{h+1}", indice=h, es_artificial=False))
                cb_num[i] = 0.0
                cb_m[i]   = 0.0

            elif info["tipo"] == ">=":
                s = info["superflua"]
                a = info["artificial"]
                fila[s] = -1.0
                fila[a] =  1.0
                variables_base.append(
                    VariableBase(nombre=f"a{a+1}", indice=a, es_artificial=True))
                cb_num[i] = 0.0
                cb_m[i]   = 1.0

            else:  # "="
                a = info["artificial"]
                fila[a] = 1.0
                variables_base.append(
                    VariableBase(nombre=f"a{a+1}", indice=a, es_artificial=True))
                cb_num[i] = 0.0
                cb_m[i]   = 1.0

            fila[total_col] = r.limite
            filas.append(fila)

        # 3. Coeficientes numéricos de la FO
        ct_num = [0.0] * total_col
        for j in range(nv):
            ct_num[j] = obj[j]

        # 4. Coeficientes M de la FO  ← CORRECCIÓN CLAVE
        #    ct_m[j] = 1 para columnas artificiales (MIN: penalización +M)
        #    ct_m[j] = 0 para todo lo demás
        ct_m_arr = [0.0] * total_col
        for info in rest_info:
            if "artificial" in info:
                ct_m_arr[info["artificial"]] = 1.0

        # 5. Fila Z y fila M iniciales
        fila_z = [0.0] * (total_col + 1)
        fila_m = [0.0] * (total_col + 1)

        for j in range(total_col + 1):
            s_num = sum(cb_num[i] * filas[i][j] for i in range(nr))
            s_m   = sum(cb_m[i]  * filas[i][j] for i in range(nr))
            ct_m_j = ct_m_arr[j] if j < total_col else 0.0

            fila_z[j] = (ct_num[j] - s_num) if j < total_col else -s_num
            fila_m[j] = ct_m_j - s_m
            
        hay_art   = any(v.es_artificial for v in variables_base)
        cols_elim = []

        return (filas, fila_z, fila_m, variables_base,
                total_col, hay_art, cols_elim)

    # ----------------------------------------------------------
    # SELECCIÓN DE COLUMNA PIVOTE
    # ----------------------------------------------------------
    def _columna_pivote(self, fila_z, fila_m, hay_art, total_col, cols_elim):

        def _mas_negativo(fila):
            col   = -1
            menor = -self.TOL  
            for j in range(total_col):
                if j in cols_elim:
                    continue
                if fila[j] < menor:
                    menor = fila[j]
                    col   = j
            return col

        if hay_art:
            col = _mas_negativo(fila_m)
            if col != -1:
                return col   # hay negativo en M → pivotear allí

        # Sin negativos en M (o sin artificiales): buscar en Z
        return _mas_negativo(fila_z)

    # ----------------------------------------------------------
    # SELECCIÓN DE FILA PIVOTE (cociente mínimo)
    # ----------------------------------------------------------
    def _fila_pivote(self, filas, col, total_col):
        fila  = -1
        menor = float('inf')
        for i, f in enumerate(filas):
            if f[col] > self.TOL:
                razon = f[total_col] / f[col]
                if razon < menor:
                    menor = razon
                    fila  = i
        return fila

    # ----------------------------------------------------------
    # GAUSS-JORDAN
    # ----------------------------------------------------------
    def _gauss_jordan(self, filas, fila_z, fila_m, fp, cp, total_col):
        piv = filas[fp][cp]
        # Normalizar fila pivote
        for j in range(total_col + 1):
            filas[fp][j] /= piv
        # Eliminar en todas las demás filas de restricciones
        for i in range(len(filas)):
            if i == fp:
                continue
            f = filas[i][cp]
            for j in range(total_col + 1):
                filas[i][j] -= f * filas[fp][j]
        # Eliminar en fila Z
        fz = fila_z[cp]
        for j in range(total_col + 1):
            fila_z[j] -= fz * filas[fp][j]
        # Eliminar en fila M
        fm = fila_m[cp]
        for j in range(total_col + 1):
            fila_m[j] -= fm * filas[fp][j]

    # ----------------------------------------------------------
    # SNAPSHOT
    # ----------------------------------------------------------
    def _snapshot(self, num, desc, filas, fila_z, fila_m,
                  vars_base, hay_art, cols_elim, cp, fp):
        return PasoSimplex(
            numero=num,
            descripcion=desc,
            filas=[list(f) for f in filas],
            fila_z=list(fila_z),
            fila_m=list(fila_m),
            variables_en_base=[VariableBase(**v.__dict__) for v in vars_base],
            hay_artificiales=hay_art,
            columnas_eliminadas=list(cols_elim),
            columna_pivote=cp,
            fila_pivote=fp
        )

    # ----------------------------------------------------------
    # BUCLE PRINCIPAL
    # ----------------------------------------------------------
    def _ejecutar(self, problema: Problema) -> ResultadoSimplex:
        (filas, fz, fm, vars_base,
         total_col, hay_art, cols_elim) = self._construir_tabla(problema)

        pasos = []
        pasos.append(self._snapshot(
            0, "Tabla inicial",
            filas, fz, fm, vars_base, hay_art, cols_elim, -1, -1
        ))

        for it in range(1, MAX_ITERACIONES + 1):

            # Elegir columna pivote
            cp = self._columna_pivote(fz, fm, hay_art, total_col, cols_elim)
            if cp == -1:
                break   # óptimo alcanzado

            # Elegir fila pivote
            fp = self._fila_pivote(filas, cp, total_col)
            if fp == -1:
                return ResultadoSimplex(
                    pasos=pasos, valores_variables=[], valor_z=0,
                    cant_variables=problema.cant_variables,
                    total_columnas=total_col,
                    variables_en_base_final=[], filas_final=[],
                    error="Problema no acotado."
                )

            var_sale = vars_base[fp]
            if var_sale.es_artificial:
                cols_elim.append(var_sale.indice)

            pasos.append(self._snapshot(
                it,
                f"Iteración {it} — entra x{cp+1}, sale {var_sale.nombre} (PIVOTE)",
                filas, fz, fm,
                vars_base, hay_art, cols_elim,
                cp, fp
            ))

            # Actualizar base y aplicar Gauss-Jordan
            vars_base[fp] = VariableBase(
                nombre=f"x{cp+1}", indice=cp, es_artificial=False)
            self._gauss_jordan(filas, fz, fm, fp, cp, total_col)

            hay_art = any(v.es_artificial for v in vars_base)
            if not hay_art:
                fm = [0.0] * (total_col + 1)

            pasos.append(self._snapshot(
                it,
                f"Iteración {it} — resultado",
                filas, fz, fm,
                vars_base, hay_art, cols_elim,
                -1, -1
            ))

        # Verificar infactibilidad
        for i, var in enumerate(vars_base):
            if var.es_artificial and filas[i][total_col] > self.TOL * 10:
                return ResultadoSimplex(
                    pasos=pasos, valores_variables=[], valor_z=0,
                    cant_variables=problema.cant_variables,
                    total_columnas=total_col,
                    variables_en_base_final=[], filas_final=[],
                    error="Problema infactible (variable artificial positiva)."
                )

        # Leer valores de variables originales
        nv      = problema.cant_variables
        valores = [0.0] * nv
        for j in range(nv):
            for i, var in enumerate(vars_base):
                if var.indice == j:
                    valores[j] = redondear(filas[i][total_col])
                    break

        # Calcular Z directamente desde la solución
        valor_z_final = redondear(
            sum(problema.objetivo[j] * valores[j] for j in range(nv))
        )

        return ResultadoSimplex(
            pasos=pasos,
            valores_variables=valores,
            valor_z=valor_z_final,
            cant_variables=nv,
            total_columnas=total_col,
            variables_en_base_final=[VariableBase(**v.__dict__) for v in vars_base],
            filas_final=[list(f) for f in filas]
        )