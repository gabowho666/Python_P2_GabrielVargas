def menuPrincipal(campus):
    while True:
        print("\n--- CAMPUSLANDS ---")
        print("1. Entrar como Camper")
        print("2. Entrar como Trainer")
        print("3. Entrar como Coordinador")
        print("4. Salir")
        op = input("Opción: ")
        if op == "1":
            menuCamper(campus)
        elif op == "2":
            menuTrainer(campus)
        elif op == "3":
            menuCoordinador(campus)
        elif op == "4":
            break
        else:
            print("Opción inválida")


def menuCamper(campus):
    while True:
        print("\n--- CAMPER ---")
        print("1. Ver mis datos")
        print("2. Ver mis notas")
        print("3. Volver")
        op = input("Opción: ")
        if op == "1":
            id_camper = input("Ingrese su ID: ")
            camper = next((c for c in campus.datos.get("campers", []) if c["id"] == id_camper), None)
            if camper:
                print(f"\nID: {camper['id']}")
                print(f"Nombres: {camper['nombres']}")
                print(f"Apellidos: {camper['apellidos']}")
                print(f"Dirección: {camper['direccion']}")
                print(f"Acudiente: {camper['acudiente']}")
                print(f"Teléfonos: {', '.join(camper['telefonos'])}")
                print(f"Estado: {camper['estado']}")
                print(f"Riesgo: {camper['riesgo']}")
            else:
                print("❌ ID no encontrado")
        elif op == "2":
            id_camper = input("Ingrese su ID: ")
            camper = next((c for c in campus.datos.get("campers", []) if c["id"] == id_camper), None)
            if camper:
                modulos = camper.get("modulos", {})
                if modulos:
                    print(f"\n📋 Notas de {camper['nombres']} {camper['apellidos']}:")
                    print(f"{'Módulo':<25} {'Teórica':>8} {'Práctica':>10} {'Quiz':>6} {'Promedio':>10}")
                    print("-" * 65)
                    for nombre_mod, datos_mod in modulos.items():
                        print(f"{nombre_mod:<25} {datos_mod['teorica']:>8} {datos_mod['practica']:>10} {datos_mod['quiz']:>6} {datos_mod['promedio']:>10}")
                    print("-" * 65)
                    promedios = [m['promedio'] for m in modulos.values()]
                    promedio_general = round(sum(promedios) / len(promedios), 2)
                    print(f"{'Promedio general:':<51} {promedio_general:>14}")
                    print(f"Riesgo actual: {camper.get('riesgo', 'N/A')}")
                else:
                    print("⚠️  Este camper aún no tiene notas registradas.")
            else:
                print("❌ ID no encontrado")
        elif op == "3":
            break
        else:
            print("Opción inválida")


def menuTrainer(campus):
    while True:
        print("\n--- TRAINER ---")
        print("1. Ver campers en mis rutas")
        print("2. Evaluar módulo")
        print("3. Volver")
        op = input("Opción: ")
        if op == "1":
            id_trainer = input("Ingrese su ID: ")
            trainer = next((t for t in campus.datos.get("trainers", []) if t["identificacion"] == id_trainer), None)
            if trainer:
                rutas = trainer.get("rutas", [])
                print(f"Trainer: {trainer['nombres']} {trainer['apellidos']} - Rutas: {', '.join(rutas)}")
                for ruta in rutas:
                    print(f"\nCampers matriculados en ruta {ruta}:")
                    matriculas = [m for m in campus.datos.get("matriculas", []) if m.get("ruta") == ruta]
                    if matriculas:
                        for m in matriculas:
                            camper = next((c for c in campus.datos.get("campers", []) if c["id"] == m["camper_id"]), None)
                            if camper:
                                print(f"  - {camper['nombres']} {camper['apellidos']} (ID: {camper['id']})")
                    else:
                        print("  No hay campers matriculados en esta ruta.")
            else:
                print("❌ ID de trainer no encontrado")
        elif op == "2":
            campus.evaluar_modulo()
        elif op == "3":
            break
        else:
            print("Opción inválida")


def menuCoordinador(campus):
    while True:
        print("\n--- COORDINADOR ---")
        print("1. Registrar camper")
        print("2. Registrar nota examen inicial")
        print("3. Crear ruta")
        print("4. Matricular camper")
        print("5. Ver reportes")
        print("6. Volver")
        op = input("Opción: ")

        if op == "1":
            campus.registrarCamper()
        elif op == "2":
            campus.registrarNotaInicial()
        elif op == "3":
            campus.crearRuta()
        elif op == "4":
            campus.matricularCamperCompleto()
        elif op == "5":
            campus.reportes()
        elif op == "6":
            break
        else:
            print("Opción inválida")
