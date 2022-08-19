## Introducción a GitHub

## Instalar GitHub

En esta sección, vamos a detallar cómo instalar y correr el comando git desde nuestros computadores

### GitHub Desktop

### Linux

Abre la terminal y corre:

```
sudo apt-get update
sudo apt-get install git
```

Referencia: [Hostinger](https://www.hostinger.es/tutoriales/instalar-git-en-distintos-sistemas-operativos)


## Uso básico de GitHub desde un fork actualizado

Una vez que el fork está sincronizado, crear una nueva rama (por ejemplo con nombre `neo`:

```
git branch neo
```
Mover a la rama `neo``

```
git checkout neo
```

Estamos listos para trabajar y realizar cambios a nuestra rama. Una vez que queremos estabilizar el código, podemos sacar foto del estado actual de la rama. Para esto, correr:

```
git commit -a -m "mensaje explicando los cambios"
```
Y hacer push (subir a GitHub los cambios):

```
git push origin neo
```

Ahora, podemos ir a nuestro repositorio desde el navegador y proponer Pull Requests.


## Jupyter Lab + GitHub

- Requiere tener instalado GitHub Desktop en el equipo y descargados los repositorios
- Descargar Jupyter Lab desde el siguiente link:  [Descarga Aquí](https://jupyter.org/)
- Instalar en el equipo
- Abrir Jupyter Lab
    - Ir a File / Open from Path
    - Seleccionar la carpeta que aloja el repositorio de GitHub
    - Dar aceptar


Ahora tenemos disponible para modificar todos los archivos de nuestro repositorio de GitHub. Para hacer los commit y push, se sigue usando GitHub Desktop :)
