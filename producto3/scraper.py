from bs4 import BeautifulSoup
import pandas as pd
import requests
from datetime import date

# fecha y nombre del archivo

fecha = date.today().strftime("%d-%m-%y")
name = "output/" + fecha + ".csv"

# número de issue

run = True
issue = 1
columns = ["issue", "author", "state", "assignees"]
df = pd.DataFrame(columns=columns)

while run:
    url_name = "https://github.com/pescap/WebScrapingMDS/issues/" + str(issue)

    # Recuperar el html
    url = requests.get(url_name)
    soup = BeautifulSoup(url.text, "html.parser")

    if str(soup) == "Not Found":
        run = False

    state = None

    isOpen = soup.find("span", attrs={"title": "Status: Open"})
    if isOpen:
        ### ver si está el octicon octicon octicon-issue-opened
        if isOpen.findChildren("svg", attrs={"class": "octicon octicon-issue-opened"}):
            state = "open"

    if soup.find(
        "span", attrs={"title": "Status: Closed", "class": "State State--merged"}
    ):
        state = "closed"

    if state is not None:
        author = soup.find(
            "a", attrs={"class": "author text-bold Link--secondary"}
        ).get_text()

        assignees = (
            soup.find("span", attrs={"class": "css-truncate js-issue-assignees"})
            .get_text()
            .replace("\n", "")
            .split()
        )

        if assignees == ["No", "one", "assigned"]:
            assignees = ["No one assigned"]

        for l in range(len(assignees)):
            new_row = {
                    "issue": issue,
                    "author": author,
                    "state": state,
                    "assignees": assignees[l],
                }
            df = pd.concat([df, pd.DataFrame([new_row])], axis=0, ignore_index=True)
    issue += 1

df.to_csv(name, index=False)
