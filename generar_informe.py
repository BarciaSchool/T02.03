"""Genera los informes de la Tarea T02.03 rellenando la PLANTILLA OFICIAL de la UPS
(portada, logo y Figura 1 incluidos). Produce un .docx por integrante; luego se
convierten a PDF.

Uso:
    pip install python-docx
    python generar_informe.py
"""
from docx import Document
from docx.oxml.ns import qn

# ---------------- CONFIG (datos del grupo) ----------------
PLANTILLA = r"T02_03_GrupoXX_Apellido1Nombre1 (1).docx"

CONFIG = {
    "grupo": "AKETOY",
    "docente": "Guillermo Pizarro",
    "fecha": "2026-06-24",
    "repositorio_url": "https://github.com/BarciaSchool/T02.03.git",
    "integrantes": [
        "Abatte Kelly",
        "Barcia Adrian",
        "Huambo Cesar",
        "Totoy Victor",
    ],
}

CONCLUSIONES = (
    "El desarrollo de la presente aplicación permitió aplicar de manera práctica los "
    "principios de la ingeniería de software estudiados en la asignatura, materializando "
    "un servicio REST funcional para la gestión de categorías. La implementación del "
    "backend bajo una arquitectura en capas —modelo, repositorio, servicio y controlador— "
    "evidenció las ventajas de la separación de responsabilidades: cada componente cumple "
    "una función específica, lo que facilita el mantenimiento, las pruebas y la "
    "escalabilidad del sistema. El uso de FastAPI como framework agilizó la construcción de "
    "los servicios y proporcionó documentación interactiva automática mediante "
    "Swagger/OpenAPI, cumpliendo con el requerimiento de publicar servicios documentados. "
    "La gestión del proyecto mediante un repositorio de código con control de versiones "
    "resultó fundamental para coordinar el trabajo del equipo; la definición y asignación de "
    "tareas, junto con los commits incrementales, permitió evidenciar la participación de "
    "todos los integrantes y mantener la trazabilidad del desarrollo. Asimismo, la "
    "contenerización con Docker garantizó un despliegue reproducible e independiente del "
    "entorno. En conjunto, la tarea consolidó competencias técnicas en el diseño e "
    "implementación de APIs y, sobre todo, en el trabajo colaborativo propio de un equipo de "
    "desarrollo de software, reforzando la importancia de las buenas prácticas de "
    "documentación y versionamiento en proyectos reales."
)


def replace_in_paragraph(p, old, new):
    """Reemplaza `old` por `new` en un párrafo, preservando el formato.
    Funciona aunque `old` esté repartido en varios runs."""
    if old in p.text:
        # Caso simple: algún run contiene el texto completo.
        for run in p.runs:
            if old in run.text:
                run.text = run.text.replace(old, new)
                return True
        # Caso difícil: el texto cruza varios runs -> consolidar en el primero.
        if p.runs:
            p.runs[0].text = p.text.replace(old, new)
            for run in p.runs[1:]:
                run.text = ""
            return True
    return False


def build(doc_template_path, archivo_estudiante):
    doc = Document(doc_template_path)

    for p in doc.paragraphs:
        # 1. Fecha
        if p.text.strip() == "Fecha:":
            p.add_run(f" {CONFIG['fecha']}")
        # 2. Grupo base
        replace_in_paragraph(p, "Grupo XX", f"Grupo {CONFIG['grupo']}")
        # 6.1 Nombre del archivo PDF
        replace_in_paragraph(p, "GrupoXX", f"Grupo{CONFIG['grupo']}")
        replace_in_paragraph(p, "Apellido1Nombre1", archivo_estudiante)
        # 8. Enlace del repositorio (sustituye la línea de EJEMPLO).
        # El texto de ejemplo incluye un hipervínculo (w:hyperlink), por eso se
        # eliminan tanto los runs como los hipervínculos antes de escribir el real.
        if p.text.strip().startswith("EJEMPLO:"):
            for child in list(p._p):
                if child.tag in (qn("w:r"), qn("w:hyperlink")):
                    p._p.remove(child)
            p.add_run(f"Repositorio: {CONFIG['repositorio_url']}")

    # 3. Integrantes (primera tabla, columna "Apellidos y Nombres")
    tabla = doc.tables[0]
    filas_datos = tabla.rows[1:]
    for i, integ in enumerate(CONFIG["integrantes"]):
        if i < len(filas_datos):
            filas_datos[i].cells[0].text = integ

    # 9. Conclusiones (insertar el texto justo después del encabezado)
    for p in doc.paragraphs:
        if p.text.strip().startswith("Conclusiones de la Tarea"):
            nuevo_p = doc.add_paragraph(CONCLUSIONES)
            p._p.addnext(nuevo_p._p)
            break

    nombre = f"T02_03_Grupo{CONFIG['grupo']}_{archivo_estudiante}.docx"
    doc.save(nombre)
    print(f"Generado: {nombre}")
    return nombre


def main():
    # Un informe por integrante (la carga al AVAC es individual).
    # archivo_estudiante = "ApellidoNombre" (sin espacios), a partir de "Apellido Nombre".
    for integ in CONFIG["integrantes"]:
        archivo_estudiante = integ.replace(" ", "")
        build(PLANTILLA, archivo_estudiante)


if __name__ == "__main__":
    main()
