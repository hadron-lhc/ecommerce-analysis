# E-Commerce Sales Analysis

## Dashboard interactivo con la posibilidad de crear nuevos datos (clientes, productos, ordenes), que seran represeantados en tiempo real en los gráficos de análisis

## Tecnologías utilizadas

- **Python** — lenguaje principal
- **Pandas** — limpieza y transformación de datos
- **SQLite** — base de datos relacional
- **Streamlit** — dashboard interactivo
- **Plotly** — visualizaciones
- **Faker** — generación de datos sintéticos

---

## Estructura del proyecto

```
ecommerce-analysis/
├── app/
│   ├── main.py               # Página de inicio
│   └── pages/
│       ├── 01_dashboard.py   # KPIs y gráficos
│       ├── 02_clientes.py    # Gestión de clientes
│       ├── 03_productos.py   # Catálogo de productos
│       └── 04_ordenes.py     # Historial de órdenes
├── data/
│   ├── raw/                  # Datos crudos y sucios
│   └── processed/            # Datos limpios
├── database/
│   └── ecommerce.db          # Base de datos SQLite
├── src/
│   ├── generate_data.py      # Generación de datos sintéticos
│   ├── clean.py              # Limpieza de datos
│   ├── transform.py          # Transformaciones y merges
│   ├── analyze.py            # Análisis con Pandas
│   └── sql_queries.py        # Consultas SQL
└── requirements.txt
```

---

## Cómo correr el proyecto

**1. Clonar el repositorio**

```bash
git clone https://github.com/hadron/ecommerce-analysis.git
cd ecommerce-analysis
```

**2. Instalar dependencias**

```bash
pip install -r requirements.txt
```

**3. Generar y procesar los datos**

```bash
python src/generate_data.py
python src/clean.py
python src/transform.py
python src/sql_queries.py
```

**4. Correr la app**

```bash
streamlit run app/main.py
```

---

## Preguntas de negocio respondidas

1. ¿Cuál es el top 5 de productos más vendidos por categoría?
2. ¿Qué clientes generaron más revenue?
3. ¿Cuál es el ticket promedio por ciudad?
4. ¿Qué mes tuvo el pico de ventas?
5. ¿Qué porcentaje de clientes no realizó ninguna compra?
6. ¿Cuál es la tasa de recompra por categoría de producto?

---

## Notas

- Los datos son sintéticos generados con la librería `Faker`
- La base de datos SQLite es local — los cambios persisten durante la sesión
- Para deploy en producción se recomienda migrar a PostgreSQL o Supabase
