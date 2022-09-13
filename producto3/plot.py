from datetime import date
from matplotlib import pyplot as plt
import numpy as np
import pandas as pd
from matplotlib import collections  as mc


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
try:
  assignee_count = assignee_count.drop("pescap")
except:
  print('pescap not assigned')
try:
  assignee_count = assignee_count.drop("Davives")
except:
  print('Davives not assigned')

assignee_count = assignee_count.drop("No one assigned")

# Concatenar ambas listas
concat = pd.concat([issue_count, assignee_count])

test = pd.DataFrame(columns=["user", "nota"])
test["user"] = concat.index
test["nota"] = concat.values

# Definir la nota final
nota = test.groupby(["user"])["nota"].sum().sort_values() + 1
nota = nota.clip(upper=7)

alumnos = nota.shape

# Plot
#plt.figure(figsize=(16, 8))

fig, ax = plt.subplots(figsize = (16,8))

nota.plot(kind="barh")
plt.xlabel("Nota")
c = np.array([(1, 0, 0, 1), (0, 1, 0, 1), (0, 0, 1, 1)])

lines = [[(0, 0), (0, 9)], [(0, 9), (0, 19)], [(0, 19), (0, 29)]]

#lines = [[(0, 0), (0, 5)], [(7.2, 7.2), (5, 10)]]
lc = mc.LineCollection(lines, linewidths=2, colors=c)
ax.add_collection(lc)
plt.text(5.5,1,'Número de alumnos: %s'%alumnos)


plt.show(block=False)

# Guardar la imagen final con las notas de los usuarios
plt.savefig("output/issues.png")
