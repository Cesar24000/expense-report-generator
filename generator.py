import csv
from pathlib import Path


def leer_gastos(ruta_csv: str) -> list[dict]:
    """Lee un archivo CSV y devuelve una lista de diccionarios con los montos convertidos a float."""
    archivo = Path(ruta_csv)
    if not archivo.exists():
        raise FileNotFoundError(f"No se encontró el archivo: {ruta_csv}")

    registros = []
    with open(archivo, mode="r", encoding="utf-8") as f:
        lector = csv.DictReader(f)
        for fila in lector:
            registros.append({
                "fecha": fila["Fecha"].strip(),
                "categoria": fila["Categoria"].strip(),
                "concepto": fila["Concepto"].strip(),
                "monto": float(fila["Monto"]),
            })
    return registros


def analizar_datos(registros: list[dict]) -> dict:
    """Calcula el gasto total, el gasto mayor y el desglose porcentual por categoría."""
    total_general = sum(r["monto"] for r in registros)
    gasto_mayor = max(registros, key=lambda r: r["monto"])

    por_categoria = {}
    for r in registros:
        cat = r["categoria"]
        por_categoria[cat] = por_categoria.get(cat, 0.0) + r["monto"]

    # Ordenar categorías de mayor a menor gasto
    categorias_ordenadas = []
    for cat, subtotal in sorted(por_categoria.items(), key=lambda item: item[1], reverse=True):
        porcentaje = (subtotal / total_general * 100) if total_general > 0 else 0
        categorias_ordenadas.append({
            "nombre": cat,
            "subtotal": subtotal,
            "porcentaje": porcentaje,
        })

    return {
        "total": total_general,
        "cantidad": len(registros),
        "mayor": gasto_mayor,
        "categorias": categorias_ordenadas,
    }


def generar_archivos_web(registros: list[dict], resumen: dict) -> None:
    """Genera los archivos styles.css y reporte.html con los resultados."""
    css_contenido = """* {
    box-sizing: border-box;
    margin: 0;
    padding: 0;
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
}
body {
    background-color: #f4f6f9;
    color: #1e293b;
    padding: 2rem;
}
.container {
    max-width: 900px;
    margin: 0 auto;
}
header {
    margin-bottom: 2rem;
}
header h1 {
    font-size: 1.8rem;
    color: #0f172a;
}
header p {
    color: #64748b;
    margin-top: 0.3rem;
}
.cards {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
    gap: 1rem;
    margin-bottom: 2rem;
}
.card {
    background: #ffffff;
    padding: 1.25rem;
    border-radius: 10px;
    box-shadow: 0 2px 6px rgba(0, 0, 0, 0.05);
}
.card span {
    font-size: 0.85rem;
    color: #64748b;
    text-transform: uppercase;
    letter-spacing: 0.04em;
}
.card h2 {
    font-size: 1.6rem;
    margin-top: 0.4rem;
    color: #2563eb;
}
.card small {
    color: #475569;
    display: block;
    margin-top: 0.3rem;
}
.section {
    background: #ffffff;
    padding: 1.5rem;
    border-radius: 10px;
    box-shadow: 0 2px 6px rgba(0, 0, 0, 0.05);
    margin-bottom: 2rem;
}
.section h3 {
    margin-bottom: 1rem;
    font-size: 1.2rem;
}
.bar-item {
    margin-bottom: 1rem;
}
.bar-label {
    display: flex;
    justify-content: space-between;
    font-size: 0.95rem;
    margin-bottom: 0.3rem;
}
.bar-bg {
    background: #e2e8f0;
    height: 10px;
    border-radius: 999px;
    overflow: hidden;
}
.bar-fill {
    background: #2563eb;
    height: 100%;
    border-radius: 999px;
}
table {
    width: 100%;
    border-collapse: collapse;
    text-align: left;
}
th, td {
    padding: 0.75rem;
    border-bottom: 1px solid #e2e8f0;
}
th {
    color: #475569;
    font-size: 0.85rem;
    text-transform: uppercase;
}
.monto {
    font-weight: 600;
    text-align: right;
}
"""

    barras_html = ""
    for cat in resumen["categorias"]:
        barras_html += f"""
        <div class="bar-item">
            <div class="bar-label">
                <strong>{cat['nombre']}</strong>
                <span>${cat['subtotal']:,.2f} ({cat['porcentaje']:.1f}%)</span>
            </div>
            <div class="bar-bg">
                <div class="bar-fill" style="width: {cat['porcentaje']:.1f}%;"></div>
            </div>
        </div>
        """

    filas_tabla = ""
    for r in registros:
        filas_tabla += f"""
        <tr>
            <td>{r['fecha']}</td>
            <td>{r['categoria']}</td>
            <td>{r['concepto']}</td>
            <td class="monto">${r['monto']:,.2f}</td>
        </tr>
        """

    html_contenido = f"""<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Reporte Financiero Mensual</title>
    <link rel="stylesheet" href="styles.css">
</head>
<body>
    <div class="container">
        <header>
            <h1>Reporte de Gastos Personales</h1>
            <p>Generado automáticamente desde datos CSV con Python</p>
        </header>

        <div class="cards">
            <div class="card">
                <span>Gasto Total</span>
                <h2>${resumen['total']:,.2f}</h2>
                <small>{resumen['cantidad']} movimientos registrados</small>
            </div>
            <div class="card">
                <span>Mayor Gasto Individual</span>
                <h2>${resumen['mayor']['monto']:,.2f}</h2>
                <small>{resumen['mayor']['concepto']} ({resumen['mayor']['categoria']})</small>
            </div>
        </div>

        <div class="section">
            <h3>Distribución por Categoría</h3>
            {barras_html}
        </div>

        <div class="section">
            <h3>Detalle de Movimientos</h3>
            <table>
                <thead>
                    <tr>
                        <th>Fecha</th>
                        <th>Categoría</th>
                        <th>Concepto</th>
                        <th style="text-align: right;">Monto</th>
                    </tr>
                </thead>
                <tbody>
                    {filas_tabla}
                </tbody>
            </table>
        </div>
    </div>
</body>
</html>
"""

    Path("styles.css").write_text(css_contenido, encoding="utf-8")
    Path("reporte.html").write_text(html_contenido, encoding="utf-8")
    print("Reporte generado con éxito: abre 'reporte.html' en tu navegador.")


if __name__ == "__main__":
    datos = leer_gastos("gastos.csv")
    analisis = analizar_datos(datos)
    generar_archivos_web(datos, analisis)