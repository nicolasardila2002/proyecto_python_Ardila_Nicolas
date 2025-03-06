import json
import os
from typing import List, Dict, Any

# Función para cargar datos desde un archivo JSON en una carpeta específica
def cargar_datos(ruta_carpeta: str, archivo: str) -> List[Dict[str, Any]]:
    ruta_completa = os.path.join(ruta_carpeta, archivo)  # Construye la ruta completa al archivo
    try:
        with open(ruta_completa, 'r', encoding='utf-8') as f:
            datos = json.load(f)
            print(f"Datos cargados desde {ruta_completa}:")  # Imprimir datos cargados
            print(datos)  # Imprimir datos cargados
            return datos
    except FileNotFoundError:
        print(f"El archivo {ruta_completa} no existe. Creando uno nuevo con datos de ejemplo...")
        datos_ejemplo = []
        if archivo == 'poblacion.json':
            datos_ejemplo = [
                {"ano": 2018, "pais": "India", "codigo_iso3": "IND", "indicador_id": "SP.POP.TOTL", "descripcion": "Total de población", "valor": 1250000000, "estado": "disponible", "unidad": "personas"},
                {"ano": 2019, "pais": "India", "codigo_iso3": "IND", "indicador_id": "SP.POP.TOTL", "descripcion": "Total de población", "valor": 1270000000, "estado": "disponible", "unidad": "personas"},
                {"ano": 2020, "pais": "India", "codigo_iso3": "IND", "indicador_id": "SP.POP.TOTL", "descripcion": "Total de población", "valor": 1300000000, "estado": "disponible", "unidad": "personas"},
                {"ano": 2021, "pais": "India", "codigo_iso3": "IND", "indicador_id": "SP.POP.TOTL", "descripcion": "Total de población", "valor": 1320000000, "estado": "disponible", "unidad": "personas"},
                {"ano": 2022, "pais": "India", "codigo_iso3": "IND", "indicador_id": "SP.POP.TOTL", "descripcion": "Total de población", "valor": 1350000000, "estado": "disponible", "unidad": "personas"},
                {"ano": 2023, "pais": "India", "codigo_iso3": "IND", "indicador_id": "SP.POP.TOTL", "descripcion": "Total de población", "valor": 1380000000, "estado": "disponible", "unidad": "personas"}
            ]
        elif archivo == 'paises.json':
            datos_ejemplo = [
                {"nombre": "India", "codigo_iso": "IN", "codigo_iso3": "IND"},
                {"nombre": "China", "codigo_iso": "CN", "codigo_iso3": "CHN"},
                {"nombre": "Estados Unidos", "codigo_iso": "US", "codigo_iso3": "USA"},
                {"nombre": "Brasil", "codigo_iso": "BR", "codigo_iso3": "BRA"},
                {"nombre": "Indonesia", "codigo_iso": "ID", "codigo_iso3": "IDN"}
            ]
        elif archivo == 'indicadores.json':
            datos_ejemplo = [
                {"id_indicador": "SP.POP.TOTL", "descripcion": "Total de población"},
                {"id_indicador": "SP.POP.GROW", "descripcion": "Crecimiento anual de la población (%)"},
                {"id_indicador": "SP.URB.TOTL", "descripcion": "Población urbana"},
                {"id_indicador": "SP.RUR.TOTL", "descripcion": "Población rural"}
            ]
        # Guardar los datos de ejemplo en el archivo JSON
        with open(ruta_completa, 'w', encoding='utf-8') as f:
            json.dump(datos_ejemplo, f, indent=4, ensure_ascii=False)
        return datos_ejemplo

# Clase para gestionar los datos de población
class GestionPoblacion:
    def __init__(self, ruta_carpeta: str):
        self.ruta_carpeta = ruta_carpeta
        self.poblacion = cargar_datos(ruta_carpeta, 'poblacion.json')
        self.paises = cargar_datos(ruta_carpeta, 'paises.json')
        self.indicadores = cargar_datos(ruta_carpeta, 'indicadores.json')

    # Obtener todos los datos de población para un país específico en un período de tiempo
    def obtener_poblacion_por_pais_y_ano(self, pais: str, inicio: int, fin: int) -> List[Dict[str, Any]]:
        return [dato for dato in self.poblacion if dato['pais'] == pais and inicio <= dato['ano'] <= fin]

    # Listar los países con su información de código ISO y código ISO3
    def listar_paises(self) -> List[Dict[str, str]]:
        return self.paises

    # Obtener los datos de población para un indicador específico
    def obtener_poblacion_por_indicador(self, indicador_id: str) -> List[Dict[str, Any]]:
        return [dato for dato in self.poblacion if dato['indicador_id'] == indicador_id]

    # Obtener los datos de población de los últimos 10 años para todos los países
    def obtener_poblacion_ultimos_10_anos(self) -> List[Dict[str, Any]]:
        ultimo_ano = max(dato['ano'] for dato in self.poblacion)
        return [dato for dato in self.poblacion if ultimo_ano - 10 <= dato['ano'] <= ultimo_ano]

    # Obtener la población total para un país en un año específico
    def obtener_poblacion_total_por_pais_y_ano(self, pais: str, ano: int) -> int:
        datos = [dato for dato in self.poblacion if dato['pais'] == pais and dato['ano'] == ano]
        return sum(dato['valor'] for dato in datos)

    # Obtener la población total registrada antes de un año específico
    def obtener_poblacion_total_antes_de(self, ano: int) -> int:
        return sum(dato['valor'] for dato in self.poblacion if dato['ano'] < ano)

    # Obtener la población total registrada después de un año específico
    def obtener_poblacion_total_despues_de(self, ano: int) -> int:
        return sum(dato['valor'] for dato in self.poblacion if dato['ano'] > ano)

    # Calcular el porcentaje de crecimiento de la población entre dos años para un país
    def calcular_crecimiento_poblacional(self, pais: str, inicio: int, fin: int) -> float:
        poblacion_inicio = self.obtener_poblacion_total_por_pais_y_ano(pais, inicio)
        poblacion_fin = self.obtener_poblacion_total_por_pais_y_ano(pais, fin)
        if poblacion_inicio == 0:
            return 0
        return ((poblacion_fin - poblacion_inicio) / poblacion_inicio) * 100

    # Obtener el año con la población más baja para un país
    def obtener_ano_poblacion_mas_baja(self, pais: str) -> int:
        datos = [dato for dato in self.poblacion if dato['pais'] == pais]
        return min(datos, key=lambda x: x['valor'])['ano']

    # Obtener el número de registros de población por año
    def obtener_registros_por_ano(self) -> Dict[int, int]:
        registros = {}
        for dato in self.poblacion:
            if dato['ano'] in registros:
                registros[dato['ano']] += 1
            else:
                registros[dato['ano']] = 1
        return registros

    # Obtener los países con un crecimiento poblacional mayor al 2% anual en los últimos 5 años
    def obtener_paises_con_crecimiento_mayor_al_2_porciento(self) -> List[str]:
        ultimo_ano = max(dato['ano'] for dato in self.poblacion)
        paises_crecimiento = []
        for pais in self.paises:
            crecimiento = self.calcular_crecimiento_poblacional(pais['nombre'], ultimo_ano - 5, ultimo_ano)
            if crecimiento > 2:
                paises_crecimiento.append(pais['nombre'])
        return paises_crecimiento

    # Obtener los años en los que la población de un país superó un valor específico
    def obtener_anos_poblacion_superior_a(self, pais: str, valor: int) -> List[int]:
        return [dato['ano'] for dato in self.poblacion if dato['pais'] == pais and dato['valor'] > valor]

    # Obtener la población total registrada para todos los países en un año específico
    def obtener_poblacion_total_por_ano(self, ano: int) -> int:
        return sum(dato['valor'] for dato in self.poblacion if dato['ano'] == ano)

    # Obtener la población menos registrada para un país en los últimos 20 años
    def obtener_poblacion_menos_registrada(self, pais: str) -> int:
        ultimo_ano = max(dato['ano'] for dato in self.poblacion)
        datos = [dato for dato in self.poblacion if dato['pais'] == pais and ultimo_ano - 20 <= dato['ano'] <= ultimo_ano]
        return min(datos, key=lambda x: x['valor'])['valor']

    # Calcular el promedio de población registrada por año para un país en un rango de años
    def calcular_promedio_poblacion(self, pais: str, inicio: int, fin: int) -> float:
        datos = [dato for dato in self.poblacion if dato['pais'] == pais and inicio <= dato['ano'] <= fin]
        return sum(dato['valor'] for dato in datos) / len(datos) if datos else 0

    # Obtener la cantidad de años con datos de población disponibles para un país
    def obtener_cantidad_anos_con_datos(self, pais: str) -> int:
        return len(set(dato['ano'] for dato in self.poblacion if dato['pais'] == pais))

    # Obtener los países con datos de población disponibles para cada año en un rango
    def obtener_paises_con_datos_por_ano(self, inicio: int, fin: int) -> List[str]:
        paises_con_datos = set()
        for ano in range(inicio, fin + 1):
            paises_ano = set(dato['pais'] for dato in self.poblacion if dato['ano'] == ano)
            if not paises_con_datos:
                paises_con_datos = paises_ano
            else:
                paises_con_datos.intersection_update(paises_ano)
        return list(paises_con_datos)

# Función para mostrar el menú
def mostrar_menu():
    print("\n--- Menú de Gestión de Población ---")
    print("1. Obtener todos los datos de población para India desde 2000 hasta 2023")
    print("2. Listar los países con su información de código ISO y código ISO3")
    print("3. Datos de población para el indicador 'SP.POP.TOTL'")
    print("4. Obtener los datos de población de los últimos 10 años para todos los países")
    print("5. Total de población para India en el año 2022")
    print("6. Población total registrada antes del año 2000")
    print("7. Población total registrada después del año 2010")
    print("8. Porcentaje de crecimiento de la población de India entre 2010 y 2020")
    print("9. Población de India en el año 2023 (si está disponible)")
    print("10. Obtener el año con la población más baja para India")
    print("11. Número de registros de población por año")
    print("12. Países con un crecimiento poblacional mayor al 2% anual en los últimos 5 años")
    print("13. Listar los años en los que la población de India superó los 1,000 millones")
    print("14. Obtener la población total registrada para todos los países en el año 2000")
    print("15. Obtener la población menos registrada para India en los últimos 20 años")
    print("16. Promedio de población registrada por año para India desde 1980 hasta 2020")
    print("17. Cantidad de años con datos de población disponibles para India")
    print("18. Listar los países con datos de población disponibles para cada año entre 2000 y 2023")
    print("19. Población total de India en 2019")
    print("20. Años en los que la población de India creció más de 1 millón en comparación con el año anterior")
    print("21. Población registrada de India en cada década desde 1960")
    print("22. Población total registrada para todos los países en 2023")
    print("23. Años en los que no hay datos de población disponibles para India")
    print("24. Año con la población más alta registrada para India")
    print("25. Años con datos de población disponibles para más de 50 países")
    print("26. Salir")

# Función principal
def main():
    print("Iniciando el programa...")  # Mensaje de depuración
    ruta_carpeta = input("Ingrese la ruta de la carpeta que contiene los archivos JSON: ")
    gestion = GestionPoblacion(ruta_carpeta)

    while True:
        print("Mostrando el menú...")  # Mensaje de depuración
        mostrar_menu()
        opcion = input("Seleccione una opción (1-26): ")

        if opcion == "1":
            resultado = gestion.obtener_poblacion_por_pais_y_ano("India", 2000, 2023)
            print(f"\nPoblación de India desde 2000 hasta 2023:")
            print(resultado)

        elif opcion == "2":
            resultado = gestion.listar_paises()
            print("\nListado de países:")
            print(resultado)

        elif opcion == "3":
            resultado = gestion.obtener_poblacion_por_indicador("SP.POP.TOTL")
            print(f"\nDatos de población para el indicador 'SP.POP.TOTL':")
            print(resultado)

        elif opcion == "4":
            resultado = gestion.obtener_poblacion_ultimos_10_anos()
            print("\nDatos de población de los últimos 10 años para todos los países:")
            print(resultado)

        elif opcion == "5":
            resultado = gestion.obtener_poblacion_total_por_pais_y_ano("India", 2022)
            print(f"\nPoblación total de India en 2022: {resultado}")

        elif opcion == "6":
            resultado = gestion.obtener_poblacion_total_antes_de(2000)
            print(f"\nPoblación total registrada antes del año 2000: {resultado}")

        elif opcion == "7":
            resultado = gestion.obtener_poblacion_total_despues_de(2010)
            print(f"\nPoblación total registrada después del año 2010: {resultado}")

        elif opcion == "8":
            resultado = gestion.calcular_crecimiento_poblacional("India", 2010, 2020)
            print(f"\nCrecimiento poblacional de India entre 2010 y 2020: {resultado:.2f}%")

        elif opcion == "9":
            resultado = gestion.obtener_poblacion_total_por_pais_y_ano("India", 2023)
            print(f"\nPoblación de India en 2023: {resultado}")

        elif opcion == "10":
            resultado = gestion.obtener_ano_poblacion_mas_baja("India")
            print(f"\nAño con la población más baja para India: {resultado}")

        elif opcion == "11":
            resultado = gestion.obtener_registros_por_ano()
            print("\nNúmero de registros de población por año:")
            print(resultado)

        elif opcion == "12":
            resultado = gestion.obtener_paises_con_crecimiento_mayor_al_2_porciento()
            print("\nPaíses con un crecimiento poblacional mayor al 2% anual en los últimos 5 años:")
            print(resultado)

        elif opcion == "13":
            resultado = gestion.obtener_anos_poblacion_superior_a("India", 1000000000)
            print("\nAños enAños en los que la población de India superó los 1,000 millones:")
            print(resultado)

        elif opcion == "14":
            resultado = gestion.obtener_poblacion_total_por_ano(2000)
            print(f"\nPoblación total registrada para todos los países en el año 2000: {resultado}")

        elif opcion == "15":
            resultado = gestion.obtener_poblacion_menos_registrada("India")
            print(f"\nPoblación menos registrada para India en los últimos 20 años: {resultado}")

        elif opcion == "16":
            resultado = gestion.calcular_promedio_poblacion("India", 1980, 2020)
            print(f"\nPromedio de población registrada por año para India desde 1980 hasta 2020: {resultado:.2f}")

        elif opcion == "17":
            resultado = gestion.obtener_cantidad_anos_con_datos("India")
            print(f"\nCantidad de años con datos de población disponibles para India: {resultado}")

        elif opcion == "18":
            resultado = gestion.obtener_paises_con_datos_por_ano(2000, 2023)
            print("\nPaíses con datos de población disponibles para cada año entre 2000 y 2023:")
            print(resultado)

        elif opcion == "19":
            resultado = gestion.obtener_poblacion_total_por_pais_y_ano("India", 2019)
            print(f"\nPoblación total de India en 2019: {resultado}")

        elif opcion == "20":
            # Implementar lógica para años en los que la población creció más de 1 millón
            print("\nOpción no implementada aún.")

        elif opcion == "21":
            # Implementar lógica para población registrada en cada década desde 1960
            print("\nOpción no implementada aún.")

        elif opcion == "22":
            resultado = gestion.obtener_poblacion_total_por_ano(2023)
            print(f"\nPoblación total registrada para todos los países en 2023: {resultado}")

        elif opcion == "23":
            # Implementar lógica para años sin datos de población para India
            print("\nOpción no implementada aún.")

        elif opcion == "24":
            # Implementar lógica para año con la población más alta para India
            print("\nOpción no implementada aún.")

        elif opcion == "25":
            # Implementar lógica para años con datos de población disponibles para más de 50 países
            print("\nOpción no implementada aún.")

        elif opcion == "26":
            print("Saliendo del programa...")
            break

        else:
            print("Opción no válida. Por favor, seleccione una opción del 1 al 26.")

# Ejecutar el programa
if __name__ == "__main__":
    main()