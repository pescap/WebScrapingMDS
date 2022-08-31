from datetime import date
from matplotlib import pyplot as plt
import numpy as np
import pandas as pd

# Importar los resultados

fecha = date.today().strftime("%d-%m-%y")
name = "output/" + fecha + ".csv"

df = pd.read_csv(name)

# Creadores de issues
issue_count = df.author.value_counts()
issue_count = issue_count.drop("pescap")
issue_count = issue_count.drop("Davives")

# Usuarios asignados para issues cerrados
assignee_count = df[df.state == "closed"].assignees.value_counts()
assignee_count = assignee_count.drop("pescap")
assignee_count = assignee_count.drop("No one assigned")

# Concatenar ambas listas
concat = pd.concat([issue_count, assignee_count])

test = pd.DataFrame(columns=["user", "nota"])
test["user"] = concat.index
test["nota"] = concat.values

# Definir la nota final
nota = test.groupby(["user"])["nota"].sum().sort_values() + 1
nota = nota.clip(upper=7)

# Plot
plt.figure(figsize=(16, 8))
nota.plot(kind="barh")
plt.xlabel("Nota")


plt.show(block=False)

# Guardar la imagen final con las notas de los usuarios
plt.savefig("output/issues.png")
