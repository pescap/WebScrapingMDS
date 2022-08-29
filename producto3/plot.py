import numpy as np
import pandas as pd
from matplotlib import pyplot as plt

df = pd.read_csv("issues.csv")

issue_count = df.author.value_counts()
issue_count = issue_count.drop("pescap")

assignee_count = df[df.state == "closed"].assignees.value_counts()
assignee_count = assignee_count.drop("pescap")
assignee_count = assignee_count.drop("No one assigned")


concat = pd.concat([issue_count, assignee_count])

test = pd.DataFrame(columns=["user", "nota"])
test["user"] = concat.index
test["nota"] = concat.values

plt.figure(figsize=(16, 8))
nota = test.groupby(["user"])["nota"].sum().sort_values() + 1
nota = nota.clip(upper=7)

nota.plot(kind="barh")
plt.xlabel("Nota")


plt.show(block=False)
plt.savefig("issues.png")
