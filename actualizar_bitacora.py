def agregar_entrada():
    with open("bitacora.md", "a") as bitacora:
        fecha = input("Fecha (YYYY-MM-DD): ")
        descripcion = input("Descripción del avance: ")
        bitacora.write(f"### {fecha}\n- {descripcion}\n\n")
    print("Entrada agregada a la bitácora.")

agregar_entrada()