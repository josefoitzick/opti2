import pulp as pl
import json
import os
import time
import matplotlib.pyplot as plt

def resolver_problema(instancia, output_file, instancia_id):
    tiempo_inicio = time.time()

    # Cargar datos desde la instancia
    areas = instancia["areas"]
    vehiculos = instancia["vehiculos"]
    fiscalizadores = instancia["fiscalizadores"]
    TMax = instancia["TMax"]
    Tij = instancia["Tij"]
    Cap = instancia["Cap"]
    a = instancia["a"]
    b = instancia["b"]
    Cost = instancia["Cost"]
    Comb = instancia["Comb"]  # Costo de combustible

    # Crear el modelo de optimización
    model = pl.LpProblem("Optimización_Mantenimiento_Áreas_Verdes", pl.LpMinimize)

    # Variables de decisión
    x = {
        (area, vehiculo): pl.LpVariable(f"x_{area}_{vehiculo}", cat=pl.LpBinary)
        for area in areas
        for vehiculo in vehiculos
    }

    # Función objetivo: minimizar costos totales
    model += pl.lpSum(
        x[area, vehiculo] * Comb[str(area)][str(vehiculo)] for area in areas for vehiculo in vehiculos
    ) + pl.lpSum(
        Cost[str(vehiculo)] for vehiculo in vehiculos
    )

    # Restricciones
    # 1. Tiempo máximo por vehículo
    for vehiculo in vehiculos:
        model += (
            pl.lpSum(x[area, vehiculo] * Tij[str(area)][str(vehiculo)] for area in areas)
            <= TMax,
            f"TiempoMaximo_Vehiculo_{vehiculo}"
        )

    # 2. Capacidad del vehículo
    for vehiculo in vehiculos:
        model += (
            pl.lpSum(x[area, vehiculo] for area in areas) <= Cap,
            f"Capacidad_Vehiculo_{vehiculo}"
        )

    # 3. Cada área debe ser visitada por un solo vehículo
    for area in areas:
        model += (
            pl.lpSum(x[area, vehiculo] for vehiculo in vehiculos) == 1,
            f"UnVehiculoPorArea_{area}"
        )

    # Resolver el problema
    solver = pl.CPLEX_CMD(msg=False) if pl.CPLEX().available() else pl.PULP_CBC_CMD(msg=False)
    status = model.solve(solver)

    tiempo_total = time.time() - tiempo_inicio
    valor_z = pl.value(model.objective) if model.status == pl.LpStatusOptimal else None

    # Guardar resultados
    with open(output_file, "a", encoding='utf-8') as f:
        f.write(f"\nInstancia: {instancia_id}\n")
        f.write(f"Estado: {pl.LpStatus[model.status]}\n")
        f.write(f"Tiempo de ejecución: {tiempo_total:.2f} segundos\n")
        if model.status == pl.LpStatusOptimal:
            f.write(f"Función objetivo (Z): {valor_z:.2f}\n")
            f.write("Asignación de áreas a vehículos:\n")
            for (area, vehiculo), var in x.items():
                if pl.value(var) > 0.5:
                    f.write(f"  Área={area}, Vehículo={vehiculo}\n")
        else:
            f.write("  No se encontró solución óptima.\n")

    return tiempo_total, valor_z

def procesar_instancias(json_folder, output_file):
    if os.path.exists(output_file):
        os.remove(output_file)

    tiempos = []
    valores_z = []

    for filename in sorted(os.listdir(json_folder)):
        if filename.endswith(".json"):
            try:
                with open(os.path.join(json_folder, filename), "r") as f:
                    instancia = json.load(f)
                print(f"Procesando {filename}...")
                tiempo, valor_z = resolver_problema(instancia, output_file, filename)
                tiempos.append(tiempo)
                valores_z.append(valor_z if valor_z is not None else 0)
            except Exception as e:
                print(f"Error en {filename}: {str(e)}")
                tiempos.append(0)
                valores_z.append(0)

    # Crear gráfico de resultados
    plt.figure(figsize=(10, 6))
    plt.plot(range(len(tiempos)), tiempos, label='Tiempo de ejecución')
    plt.plot(range(len(valores_z)), valores_z, label='Valor de la función objetivo (Z)')
    plt.xlabel('Instancia')
    plt.ylabel('Valor')
    plt.legend()
    plt.grid()
    plt.savefig('resultados.png')
    print("Gráfico generado: 'resultados.png'")

# Configuración y ejecución
json_folder = "instancias_json"
output_file = "resumen_resultados.txt"

if not os.path.exists(json_folder):
    os.makedirs(json_folder)
procesar_instancias(json_folder, output_file)
