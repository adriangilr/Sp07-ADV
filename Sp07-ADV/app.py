# Importamos librerias y paquetes
import pandas as pd
import plotly.express as px
import streamlit as st
from pathlib import Path

# Ttitulo de pagina
st.set_page_config(page_title="Analizador de Depreciacion Vehicular (ADV)", layout="wide")

# -------------------------
# Encabezado 
# -------------------------
st.title("Analizador de Depreciacion Vehicular (ADV)")
st.write("Explora cómo cambia el precio de vehículos usados según antiguedad, kilometraje y OEM.")

# Importamos path para obtener la ruta relativa al proyecto Sp07-ADV
BASE_DIR = Path(__file__).resolve().parent
car_data = pd.read_csv(BASE_DIR / "ds/vehicles_us.csv")

# -------------------------
# Limpieza de datos
# -------------------------
df = car_data.copy()

# convertimos valores invalidos a NaN
for col in ["price", "model_year", "odometer"]:
    df[col] = pd.to_numeric(df[col], errors="coerce")

# buscamos NAs
df = df.dropna(subset=["price", "model_year", "odometer", "model"])

# creamos manufacturer desde "model" con el criterio: ("bmw x5" -> "bmw")
df["manufacturer"] = df["model"].astype(str).str.split().str[0].str.lower()

# basado en el dataset
CURRENT_YEAR = 2024
df["vehicle_age"] = CURRENT_YEAR - df["model_year"]
# rango entre 0 y 50 reduciendo valores raros
df = df[df["vehicle_age"].between(0, 50)]

# -------------------------
# Filtros
# -------------------------
st.subheader("Filtros")

# definimos 4 columnas para los filtros
colf1, colf2, colf3, colf4 = st.columns(4)

# seleccionamos fabricante
manufacturers = sorted(df["manufacturer"].dropna().unique())
sel_manufacturer = colf1.selectbox("OEM (manufacturer)", ["(Todos)"] + manufacturers)

# filtro de tipo
types = sorted(df["type"].dropna().unique()) if "type" in df.columns else []
sel_type = colf2.selectbox("Tipo", ["(Todos)"] + types) if types else "(Todos)"
if not types:
    colf2.info("No existe columna 'type' o no tiene valores.")

# filtro por condición
conditions = sorted(df["condition"].dropna().unique()) if "condition" in df.columns else []
sel_condition = colf3.selectbox("Condición", ["(Todos)"] + conditions) if conditions else "(Todos)"
if not conditions:
    colf3.info("No existe columna 'condition' o no tiene valores.")

# slider de antiguedad
age_min, age_max = int(df["vehicle_age"].min()), int(df["vehicle_age"].max())
age_range = colf4.slider("Rango de antiguedad (años)", age_min, age_max, (0, min(20, age_max)))

# mostrar precios extremos
show_outliers = st.checkbox("Mostrar precios extremos", value=False)

# -------------------------
# Aplica filtros
# -------------------------
fdf = df[df["vehicle_age"].between(age_range[0], age_range[1])].copy()

if sel_manufacturer != "(Todos)":
    fdf = fdf[fdf["manufacturer"] == sel_manufacturer]

if sel_type != "(Todos)" and "type" in fdf.columns:
    fdf = fdf[fdf["type"] == sel_type]

if sel_condition != "(Todos)" and "condition" in fdf.columns:
    fdf = fdf[fdf["condition"] == sel_condition]

# aplicamos quantiles para evitar que algunos pocos precios extremos deformen la grafica
if not show_outliers and len(fdf) > 0:
    lo, hi = fdf["price"].quantile(0.01), fdf["price"].quantile(0.99)
    fdf = fdf[fdf["price"].between(lo, hi)]

# -------------------------
# Comienza el analisis (ya seleccionados los filtros)
# -------------------------
build_button = st.button("Construir análisis")

if build_button:
    if len(fdf) == 0:
        st.warning("No hay datos con esos filtros. Revisa OEM/tipo/condición/antiguedad.")
        st.stop()

    st.subheader("Métricas")
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Ocurrencias", f"{len(fdf):,}")
    c2.metric("Precio promedio", f"${fdf['price'].mean():,.0f}")
    c3.metric("Precio mediano", f"${fdf['price'].median():,.0f}")
    c4.metric("Antiguedad promedio", f"{fdf['vehicle_age'].mean():.1f} años")

    st.divider()

    # -------------------------
    # Histograma
    # -------------------------
    st.subheader("Histograma de distribución de precios")
    fig_hist = px.histogram(
        fdf,
        x="price",
        nbins=50,
        title="Distribución de precio (USD)"
    )
    fig_hist.update_xaxes(tickprefix="$")
    st.plotly_chart(fig_hist, use_container_width=True)

    # -------------------------
    # Dispersion
    # -------------------------
    st.subheader("Grafico de dispersión: precio vs kilometraje")
    hover_cols = ["model_year", "vehicle_age", "manufacturer", "model"]

    if "condition" in fdf.columns:
        hover_cols.append("condition")
    if "type" in fdf.columns:
        hover_cols.append("type")
    if "fuel" in fdf.columns:
        hover_cols.append("fuel")
    if "transmission" in fdf.columns:
        hover_cols.append("transmission")
    if "is_4wd" in fdf.columns:
        hover_cols.append("is_4wd")
    if "days_listed" in fdf.columns:
        hover_cols.append("days_listed")

    fig_scatter = px.scatter(
        fdf,
        x="odometer",
        y="price",
        color="vehicle_age",
        opacity=0.6,
        title="Relacion precio–kilometraje con antiguedad",
        hover_data=hover_cols
    )
    fig_scatter.update_yaxes(tickprefix="$")
    st.plotly_chart(fig_scatter, use_container_width=True)

    # curva de depreciación (mediana vs antiguedad)
    st.subheader("Depreciacion: Precio mediano vs antiguedad")
    dep = (
        fdf.groupby("vehicle_age", as_index=False)
           .agg(median_price=("price", "median"), n=("price", "size"))
           .sort_values("vehicle_age")
    )

    fig_line = px.line(
        dep,
        x="vehicle_age",
        y="median_price",
        markers=True,
        title="Precio mediano vs antiguedad del vehículo"
    )
    fig_line.update_yaxes(tickprefix="$")
    st.plotly_chart(fig_line, use_container_width=True)

    with st.expander("Ver muestra de datos filtrados"):
        st.dataframe(fdf.head(50))