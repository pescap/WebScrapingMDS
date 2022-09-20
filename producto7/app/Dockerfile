ARG pythonVersion=3.9-buster
ARG pythonSourceDir="/opt/app"

# build stage
FROM python:${pythonVersion} AS build-env
ARG pythonSourceDir

WORKDIR ${pythonSourceDir}

RUN apt-get update && apt-get install -y git

COPY . .
RUN pip install  --no-cache-dir -r ./requirements.txt

WORKDIR ${pythonSourceDir}

# final stage
FROM build-env

#Expose port 8080
EXPOSE 8080

#Non Root User Configuration
RUN addgroup --system --gid 10001 appgroup \
  && adduser --system --disabled-password --uid 10000 --shell /sbin/nologin --home /opt/app --ingroup appgroup appuser \
  && chown -R appuser:appgroup /opt/app

USER 10000

#Run the application on port 8080
CMD ["streamlit", "run", "app.py","--browser.serverAddress","0.0.0.0","--server.port","8080","--server.headless","true","--global.developmentMode","false"]