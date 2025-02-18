import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import plotly.graph_objects as go

# Cargar datos desde Google Sheets sin caché
def cargar_datos():
    url = "https://docs.google.com/spreadsheets/d/e/2PACX-1vRdoYbngv7jBofQIEtnuoeylBn0o0TEY8NiPOZ43VmLvz7AGfmNFdveUB_DVLIRC2bJVZnO4XI0vqdb/pub?output=csv"
    return pd.read_csv(url)

# Llamar a la función que carga los datos
df = cargar_datos()

# Definir la meta de recaudación
meta = 42108664

# Calcular total recaudado
total_recaudado = df["monto recaudado"].sum()

# Calcular el porcentaje de avance
porcentaje_avance = (total_recaudado / meta) * 100

# Mostrar datos en la app
st.title("Avance de la Colecta")
st.metric(
    label="Monto Recaudado",
    value=f"${total_recaudado:,.2f}",
    delta=f"${meta - total_recaudado:,.2f} faltan",
)

# Crear gráfico de barras
fig, ax = plt.subplots(figsize=(6, 2))
ax.barh(["Progreso"], [total_recaudado], color="green", label="Recaudado")
ax.barh(["Progreso"], [meta - total_recaudado], left=[total_recaudado], color="red", label="Faltante")

# Configurar el eje X en porcentaje
ax.set_xticks([0, meta * 0.25, meta * 0.50, meta * 0.75, meta])
ax.set_xticklabels(["0%", "25%", "50%", "75%", "100%"])

# Mejoras visuales
ax.set_xlabel("Porcentaje de la meta alcanzado")
ax.set_title(f"Avance de la Colecta: ${total_recaudado:,.2f} / ${meta:,.2f}")
ax.legend()
ax.grid(axis="x", linestyle="--", alpha=0.5)

# Mostrar gráfico en Streamlit
st.pyplot(fig)

# Crear un medidor circular con el porcentaje de avance
gauge = go.Figure(go.Indicator(
    mode="gauge+number",
    value=porcentaje_avance,
    title={"text": "Porcentaje Recaudado", "font": {"size": 20}},
    gauge={
        "axis": {"range": [0, 100]},
        "bar": {"color": "green"},
        "steps": [
            {"range": [0, 25], "color": "red"},
            {"range": [25, 50], "color": "yellow"},
            {"range": [50, 75], "color": "orange"},
            {"range": [75, 100], "color": "green"},
        ],
    }
))

# Mostrar medidor circular
st.plotly_chart(gauge, use_container_width=True)

