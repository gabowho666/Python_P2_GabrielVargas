from campus import Campus
from menus import menuPrincipal

if __name__=="__main__":
    campus = Campus()
    menuPrincipal(campus)
import json

def cargarDatos():
    try:
        with open("data.json", "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        return {
            "campers": [],
            "rutas": [],
            "matriculas": [],
            "trainers": []
        }

def guardarDatos(datos):
    with open("data.json", "w", encoding="utf-8") as f:
        json.dump(datos, f, indent=4, ensure_ascii=False)

class Campus:
    def __init__(self):
        self.datos = cargarDatos()
        self.trainers = self.datos.get("trainers", [])

    # Función para aprobar camper (solo coordinador)
    def aprobarCamper(self):
        print("--- APROBAR CAMPER ---")
        camper_id = input("Ingrese ID del camper para registrar notas: ")

        camper = next((c for c in self.datos.get("campers", []) if c.get("id") == camper_id), None)
        if not camper:
            print("❌ Camper no encontrado.")
            return

        try:
            nota_teo = float(input("Nota teórica (0-100): "))
            nota_prac = float(input("Nota práctica (0-100): "))
        except ValueError:
            print("❌ Entrada inválida para notas.")
            return

        promedio = (nota_teo + nota_prac) / 2
        if promedio >= 60:
            camper["estado"] = "Aprobado"
            print(f"✅ Camper {camper['nombres']} aprobado con promedio {promedio}.")
        else:
            print(f"❌ Camper {camper['nombres']} no aprobó. Promedio {promedio}.")

        guardarDatos(self.datos)

    # Matricular camper aprobado
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

        if not self.trainers:
            print("❌ No hay trainers disponibles.")
            return
        print("Trainers disponibles:")
        for i, t in enumerate(self.trainers):
            print(f"{i+1}. {t['nombres']} {t['apellidos']} ({t['jornada']}) - Rutas: {', '.join(t['rutas'])}")
        try:
            trainer_idx = int(input("Seleccione trainer: ")) - 1
        except ValueError:
            print("❌ Entrada inválida.")
            return
        if trainer_idx < 0 or trainer_idx >= len(self.trainers):
            print("❌ Trainer inválido.")
            return
        trainer = self.trainers[trainer_idx]

        fecha_inicio = input("Fecha inicio (YYYY-MM-DD): ")
        fecha_fin = input("Fecha finalización (YYYY-MM-DD): ")
        salon = input("Salón de entrenamiento: ")

        matricula = {
            "camper_id": camper_id,
            "trainer_id": trainer["identificacion"],
            "ruta": ruta["nombre"],
            "fecha_inicio": fecha_inicio,
            "fecha_fin": fecha_fin,
            "salon": salon
        }
        self.datos.setdefault("matriculas", []).append(matricula)
        print(f"✅ Camper {camper['nombres']} matriculado en ruta {ruta['nombre']} con trainer {trainer['nombres']}.")
        guardarDatos(self.datos)

    # Reportes de ejemplo (puedes expandirlos)
    def listarCamperPorEstado(self, estado):
        print(f"\nCampers en estado '{estado}':")
        for c in self.datos.get("campers", []):
            if c.get("estado") == estado:
                print(f" - {c['id']}: {c['nombres']} {c['apellidos']}")

    def listarTrainers(self):
        print("\nTrainers disponibles:")
        for t in self.trainers:
            print(f" - {t['identificacion']}: {t['nombres']} {t['apellidos']} Jornada: {t['jornada']}")

    

# Menús simples para interactuar
def menuCoordinador(campus):
    while True:
        print("\n--- Menú Coordinador ---")
        print("1. Aprobar camper")
        print("2. Matricular camper")
        print("3. Listar campers inscritos")
        print("4. Listar trainers")
        print("0. Salir")
        op = input("Seleccione opción: ")
        if op == "1":
            campus.aprobarCamper()
        elif op == "2":
            campus.matricularCamperCompleto()
        elif op == "3":
            campus.listarCamperPorEstado("Inscrito")
        elif op == "4":
            campus.listarTrainers()
        elif op == "0":
            break
        else:
            print("Opción inválida.")

def main():
    campus = Campus()
    print("Bienvenido a CampusLands")
    while True:
        print("\n--- Seleccione rol ---")
        print("1. Camper")
        print("2. Trainer")
        print("3. Coordinador")
        print("0. Salir")
        rol = input("Ingrese rol: ")
        if rol == "3":
            menuCoordinador(campus)
        elif rol == "0":
            break
        else:
            print("Rol no implementado en este ejemplo.")

if __name__ == "__main__":
    main()
