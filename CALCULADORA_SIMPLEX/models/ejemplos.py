from models.estructuras import Problema, Restriccion

EJEMPLOS = {
    1: Problema(
        tipo="min",
        objetivo=[2.39, 4.16, 2.06, 0.8, 1.8],
        restricciones=[
            Restriccion(coeficientes=[0.085, 0.48, 0.08, 0.00, 0.15], signo=">=", limite=200),
            Restriccion(coeficientes=[0.72, 0.3, 0.7, 0.00, 0.55], signo=">=", limite=550), 
            Restriccion(coeficientes=[0.0002, 0.003, 0.0003, 0.38, 0.0013], signo=">=", limite=10.5),
            Restriccion(coeficientes=[0.0028, 0.0065, 0.003, 0.00, 0.009], signo=">=", limite=5.0),
            Restriccion(coeficientes=[1.0, 1.0, 1.0, 1.0, 1.0], signo="<=", limite=1000),
        ]
    )
}