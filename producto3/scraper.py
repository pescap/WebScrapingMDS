from bs4 import BeautifulSoup
import pandas as pd
import re
import requests

# número de issue
issue = 1

# url del issue
url_name = "https://github.com/pescap/WebScrapingMDS/issues/" + str(issue)

# definición del DataFrame
columns = ["issue", "author", "state", "assignees"]
df = pd.DataFrame(columns=columns)

# Recuperar el html
url = requests.get(url_name)
soup = BeautifulSoup(url.text, "html.parser")

# Imprimir el código html de la página
# print(soup.prettify())

state = "open"

# if encuentro un banner de estado cerrado
#   state = "closed"

if soup.find("span", attrs={"title": "Status: Closed"}):
    state = "closed"


author = soup.find("a", attrs={"class": "author text-bold Link--secondary"}).get_text()
assignees = (
    soup.find("span", attrs={"class": "css-truncate js-issue-assignees"})
    .get_text()
    .replace("\n", "")
    .split()
)

if assignees == ["No", "one", "assigned"]:
    assignees = ["No one assigned"]


print(issue, author, state, assignees)

for l in range(len(assignees)):
    df = df.append(
        {"issue": issue, "author": author, "state": state, "assignees": assignees[l]},
        ignore_index=True,
    )
