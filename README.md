# Static Web Expense Report Generator

Herramienta en Python que procesa registros financieros desde archivos CSV y genera automáticamente un dashboard web estático (`HTML5` + `CSS3`) con métricas clave, distribución porcentual y desglose tabular, sin dependencias externas.

## Características principales

* **Procesamiento de datos tabulares:** Lee archivos `.csv` mediante `csv.DictReader`, validando y estructurando registros financieros en memoria.
* **Análisis estadístico automático:** Calcula el gasto total, identifica el mayor gasto individual y agrupa subtotales por categoría ordenados de mayor a menor mediante funciones `lambda`.
* **Generación de frontend sin librerías externas:** Construye dinámicamente `reporte.html` y `styles.css` con diseño responsivo basado en CSS Grid y barras de progreso proporcionales en puro CSS.

## Tecnologías utilizadas

* **Python 3** (Librerías estándar: `csv`, `pathlib`)
* **HTML5 & CSS3** (CSS Grid, variables de diseño y maquetación responsiva)

## Estructura del proyecto

```text
expense-report-generator/
├── generator.py       # Procesamiento CSV y generación de HTML/CSS
├── gastos.csv         # Dataset de ejemplo con movimientos financieros
├── README.md          # Documentación del proyecto
└── .gitignore         # Exclusión de archivos generados y de sistema
```

## Cómo ejecutarlo

1. Clona este repositorio:
   ```bash
   git clone [https://github.com/Cesar24000/expense-report-generator.git](https://github.com/Cesar24000/expense-report-generator.git)
   ```
2. Entra al directorio y ejecuta el generador:
   ```bash
   cd expense-report-generator
   python3 generator.py
   ```
3. Abre `reporte.html` en tu navegador (en macOS puedes ejecutar `open reporte.html`).

---
Desarrollado por **César Alejandro Aguayo Gómez** — Estudiante de Ingeniería en Desarrollo de Software (ITESO)