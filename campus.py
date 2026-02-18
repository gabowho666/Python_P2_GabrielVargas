import json

def cargarDatos():
    try:
        with open("data.json", "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        return {
            "campers": [],
            "trainers": [],
            "rutas": [],
            "areas": [],
            "matriculas": []
        }

def guardarDatos(datos):
    with open("data.json", "w", encoding="utf-8") as f:
        json.dump(datos, f, indent=4, ensure_ascii=False)

class Campus:
    def __init__(self):
        self.datos = cargarDatos()

    # ---------- CAMPERS ----------
    def registrarCamper(self):
        print("\n--- REGISTRAR CAMPER ---")
        camper = {}
        camper["id"] = input("ID: ")
        camper["nombres"] = input("Nombres: ")
        camper["apellidos"] = input("Apellidos: ")
        camper["direccion"] = input("Dirección: ")
        camper["acudiente"] = input("Acudiente: ")
        camper["telefonos"] = input("Teléfonos (#celular,#fijo): ").split(",")
        camper["estado"] = "En proceso de ingreso"
        camper["riesgo"] = "Bajo"
        self.datos.setdefault("campers", []).append(camper)
        guardarDatos(self.datos)
        print("✅ Camper registrado.")

    def registrarNotaInicial(self):
        print("\n--- REGISTRAR NOTA INICIAL ---")
        camper_id = input("ID del camper: ")
        for c in self.datos.get("campers", []):
            if c.get("id") == camper_id:
                try:
                    nota_teo = float(input("Nota teórica (0-100): "))
                    nota_prac = float(input("Nota práctica (0-100): "))
                    nota_quiz = float(input("Nota quiz (0-100): "))
                except ValueError:
                    print("❌ Entrada inválida para notas.")
                    return
                promedio = (nota_teo * 0.3) + (nota_prac * 0.6) + (nota_quiz * 0.1)
                c["estado"] = "Aprobado" if promedio >= 60 else "Inscrito"
                c["riesgo"] = "Alto" if promedio < 60 else "Bajo"
                guardarDatos(self.datos)
                print(f"✅ Promedio: {round(promedio, 2)} - Estado actualizado a: {c['estado']}")
                return
        print("❌ Camper no encontrado")

    # ---------- RUTAS ----------
    def crearRuta(self):
        print("\n--- CREAR RUTA ---")
        nombre = input("Nombre de la ruta: ")
        fundamentos = input("Fundamentos (separar con coma): ").split(",")
        web = input("Programación Web (separar con coma): ").split(",")
        formal = input("Programación Formal (separar con coma): ").split(",")
        bd_principal = input("BD principal: ")
        bd_alt = input("BD alternativo: ")
        backend = input("Backend (separar con coma): ").split(",")

        modulos = {
            "Fundamentos": [f.strip() for f in fundamentos],
            "Web": [w.strip() for w in web],
            "Formal": [f.strip() for f in formal],
            "Bases de Datos": {"principal": bd_principal.strip(), "alternativo": bd_alt.strip()},
            "Backend": [b.strip() for b in backend]
        }
        self.datos.setdefault("rutas", []).append({
            "nombre": nombre,
            "modulos": modulos,
            "capacidad": 33
        })
        guardarDatos(self.datos)
        print(f"✅ Ruta '{nombre}' creada con éxito.")

    # ---------- MATRICULAS ----------
    def matricularCamperCompleto(self):
        print("\n--- MATRICULAR CAMPER ---")
        camper_id = input("ID del camper aprobado: ")

        camper = next((c for c in self.datos.get("campers", []) if c.get("id") == camper_id), None)
        if not camper:
            print("❌ Camper no encontrado.")
            return
        if camper.get("estado") != "Aprobado":
            print("❌ Solo campers aprobados pueden ser matriculados.")
            return
        if not self.datos.get("rutas"):
            print("❌ No hay rutas disponibles.")
            return

        print("Rutas disponibles:")
        for i, r in enumerate(self.datos.get("rutas", [])):
            inscritos = sum(1 for m in self.datos.get("matriculas", []) if m.get("ruta") == r["nombre"])
            print(f"{i+1}. {r['nombre']} ({inscritos}/{r['capacidad']})")

        try:
            ruta_idx = int(input("Seleccione ruta: ")) - 1
        except ValueError:
            print("❌ Entrada inválida.")
            return
        if ruta_idx < 0 or ruta_idx >= len(self.datos.get("rutas", [])):
            print("❌ Ruta inválida.")
            return

        ruta = self.datos["rutas"][ruta_idx]
        inscritos_actual = sum(1 for m in self.datos.get("matriculas", []) if m.get("ruta") == ruta["nombre"])
        if inscritos_actual >= ruta["capacidad"]:
            print("❌ Capacidad máxima alcanzada para esta ruta.")
            return

        trainers = self.datos.get("trainers", [])
        if not trainers:
            print("❌ No hay trainers disponibles.")
            return

        print("Trainers disponibles:")
        for i, t in enumerate(trainers):
            rutas_t = ', '.join(t.get('rutas', []))
            print(f"{i+1}. {t['nombres']} {t['apellidos']} ({t['jornada']}) - Rutas: {rutas_t}")

        try:
            trainer_idx = int(input("Seleccione trainer: ")) - 1
        except ValueError:
            print("❌ Entrada inválida.")
            return
        if trainer_idx < 0 or trainer_idx >= len(trainers):
            print("❌ Trainer inválido.")
            return

        trainer = trainers[trainer_idx]
        fecha_inicio = input("Fecha inicio (YYYY-MM-DD): ")
        fecha_fin = input("Fecha finalización (YYYY-MM-DD): ")
        salon = input("Salón: ")

        matricula = {
            "camper_id": camper_id,
            "trainer_id": trainer["identificacion"],
            "ruta": ruta["nombre"],
            "fecha_inicio": fecha_inicio,
            "fecha_fin": fecha_fin,
            "salon": salon
        }
        self.datos.setdefault("matriculas", []).append(matricula)
        guardarDatos(self.datos)
        print(f"✅ Camper {camper['nombres']} matriculado en ruta '{ruta['nombre']}' con trainer {trainer['nombres']}.")

    # ---------- EVALUAR MÓDULO ----------
    def evaluar_modulo(self):
        print("\n--- EVALUAR MÓDULO ---")
        camper_id = input("ID del camper: ")
        camper = next((c for c in self.datos.get("campers", []) if c.get("id") == camper_id), None)
        if not camper:
            print("❌ Camper no encontrado.")
            return

        modulo = input("Nombre del módulo: ")
        try:
            nota_teo = float(input("Nota teórica (30%): "))
            nota_prac = float(input("Nota práctica (60%): "))
            nota_quiz = float(input("Nota quiz (10%): "))
        except ValueError:
            print("❌ Entrada inválida para notas.")
            return

        promedio = (nota_teo * 0.3) + (nota_prac * 0.6) + (nota_quiz * 0.1)

        if "modulos" not in camper:
            camper["modulos"] = {}
        camper["modulos"][modulo] = {
            "teorica": nota_teo,
            "practica": nota_prac,
            "quiz": nota_quiz,
            "promedio": round(promedio, 2)
        }
        camper["riesgo"] = "Alto" if promedio < 60 else "Bajo"
        guardarDatos(self.datos)
        print(f"✅ Módulo '{modulo}' evaluado. Promedio: {round(promedio, 2)} - Riesgo: {camper['riesgo']}")

    # ---------- LISTAR TRAINERS ----------
    def listarTrainers(self):
        print("\nTrainers disponibles:")
        for t in self.datos.get("trainers", []):
            print(f" - {t['identificacion']}: {t['nombres']} {t['apellidos']} | Jornada: {t['jornada']}")

    # ---------- REPORTES ----------
    def reportes(self):
        while True:
            print("\n--- REPORTES ---")
            print("1. Campers inscritos")
            print("2. Campers aprobados")
            print("3. Trainers")
            print("4. Campers con riesgo alto")
            print("5. Campers y trainers por matrícula")
            print("6. Volver")
            op = input("Opción: ")

            if op == "1":
                encontrados = [c for c in self.datos.get("campers", []) if c.get("estado") == "Inscrito"]
                if encontrados:
                    for c in encontrados:
                        print(f"  {c.get('id')} - {c.get('nombres')} {c.get('apellidos')}")
                else:
                    print("No hay campers inscritos.")
            elif op == "2":
                encontrados = [c for c in self.datos.get("campers", []) if c.get("estado") == "Aprobado"]
                if encontrados:
                    for c in encontrados:
                        print(f"  {c.get('id')} - {c.get('nombres')} {c.get('apellidos')}")
                else:
                    print("No hay campers aprobados.")
            elif op == "3":
                self.listarTrainers()
            elif op == "4":
                encontrados = [c for c in self.datos.get("campers", []) if c.get("riesgo") == "Alto"]
                if encontrados:
                    for c in encontrados:
                        print(f"  {c.get('id')} - {c.get('nombres')} {c.get('apellidos')}")
                else:
                    print("No hay campers con riesgo alto.")
            elif op == "5":
                for m in self.datos.get("matriculas", []):
                    print(f"  Camper: {m.get('camper_id')} | Trainer: {m.get('trainer_id')} | Ruta: {m.get('ruta')}")
            elif op == "6":
                break
            else:
                print("Opción inválida")
