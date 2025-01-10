import pulp as pl
import json
import os
import time
import matplotlib.pyplot as plt


def resolver_problema(instancia, output_file, instancia_id):
    try:
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

        # Crear el modelo de optimización
        model = pl.LpProblem("Optimización_Mantenimiento_Areas_Verdes", pl.LpMinimize)

        # Variables de decisión
        X = {
            (i, k): pl.LpVariable(f"X_{i}_{k}", cat=pl.LpBinary)
            for i in areas for k in vehiculos
        }
        F = {
            (f, k): pl.LpVariable(f"F_{f}_{k}", cat=pl.LpBinary)
            for f in fiscalizadores for k in vehiculos
        }
        A = {
            (i, k): pl.LpVariable(f"A_{i}_{k}", cat=pl.LpBinary)
            for i in areas for k in vehiculos
        }

        # Función objetivo: Minimizar costos fijos y de desplazamiento
        model += (
            pl.lpSum(X[i, k] * Tij[str(i)][str(k)] for i in areas for k in vehiculos)
            + pl.lpSum(Cost[str(k)] * pl.lpSum(A[i, k] for i in areas) for k in vehiculos)
        )

        # Restricciones
        # 1. Tiempo máximo por vehículo
        for k in vehiculos:
            model += pl.lpSum(X[i, k] * Tij[str(i)][str(k)] for i in areas) <= TMax

        # 2. Capacidad máxima de los vehículos
        for k in vehiculos:
            model += pl.lpSum(F[f, k] for f in fiscalizadores) <= Cap

        # 3. Número mínimo y máximo de salidas por fiscalizador
        for f in fiscalizadores:
            model += pl.lpSum(F[f, k] for k in vehiculos) >= a
            model += pl.lpSum(F[f, k] for k in vehiculos) <= b

        # 4. Un fiscalizador en un día debe estar asignado a un solo vehículo
        for f in fiscalizadores:
            model += pl.lpSum(F[f, k] for k in vehiculos) <= 1

        # 5. Cada área debe ser visitada por un solo vehículo
        for i in areas:
            model += pl.lpSum(A[i, k] for k in vehiculos) == 1

        # 6. Balancear la asignación de áreas entre vehículos
        for k in vehiculos:
            model += pl.lpSum(A[i, k] for i in areas) <= len(areas) // len(vehiculos)
            model += pl.lpSum(A[i, k] for i in areas) >= 1

        # Resolver el problema
        solver = pl.CPLEX_CMD(msg=False) if pl.CPLEX().available() else pl.PULP_CBC_CMD(msg=False)
        status = model.solve(solver)

        tiempo_total = time.time() - tiempo_inicio
        valor_z = pl.value(model.objective) if model.status == pl.LpStatusOptimal else None

        # Guardar resultados
        with open(output_file, "a", encoding="utf-8") as f:
            f.write(f"\nInstancia: {instancia_id}\n")
            f.write(f"Estado: {pl.LpStatus[model.status]}\n")
            f.write(f"Tiempo de ejecución: {tiempo_total:.2f} segundos\n")

            if model.status == pl.LpStatusOptimal:
                f.write(f"Función objetivo (Z): {valor_z:.2f}\n")
                f.write("Asignación:\n")
                for i in areas:
                    for k in vehiculos:
                        if pl.value(A[i, k]) > 0:
                            f.write(f"  Área={i}, Vehículo={k}\n")
            else:
                f.write("  No se encontró solución óptima.\n")

        return tiempo_total, valor_z

    except KeyError as e:
        print(f"Error: Falta el campo {str(e)} en la instancia {instancia_id}")
        return 0, None
    except Exception as e:
        print(f"Error en instancia {instancia_id}: {str(e)}")
        return 0, None


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
    plt.plot(range(len(tiempos)), tiempos, label="Tiempo de ejecución")
    plt.plot(range(len(valores_z)), valores_z, label="Valor de la función objetivo (Z)")
    plt.xlabel("Instancia")
    plt.ylabel("Valor")
    plt.legend()
    plt.grid()
    plt.savefig("resultados.png")
    print("Gráfico generado: 'resultados.png'")


# Configuración y ejecución
json_folder = "instancias_json"
output_file = "resumen_resultados.txt"

if not os.path.exists(json_folder):
    os.makedirs(json_folder)
procesar_instancias(json_folder, output_file)
