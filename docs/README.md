## Introducción a GitHub

## Instalar GitHub

En esta sección, vamos a detallar cómo instalar y correr el comando git desde nuestros computadores

[Curso de GitHub](https://www.youtube.com/watch?v=ANF1X42_ae4&list=PLU8oAlHdN5BlyaPFiNQcV0xDqy0eR35aU)

[Guías de GitHub](https://www.youtube.com/githubguides)

[Tutorial de GitHub](https://towardsdatascience.com/github-actions-everything-you-need-to-know-to-get-started-537f1dffa0ed)


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

Notas:
Para limpiar un repositorio GitHub local, ir al repositorio y correr:
```
git clean -fd
```

## Uso GitHub Desktop en Windows

La aplicación GitHub Desktop se puede descargar desde cualquier parte de GitHub. Solo se debe ubicar el botón Code y hacer click en Open with GitHub Desktop. También puede ser descargado desde el siguiente link: [GitHub Desktop](https://desktop.github.com/).

![imagen1](https://github.com/gavalenz/proyectos/blob/main/docs/imagenes/imagen1.png?raw=true)

En caso de usar macOS, debe descargarlo desde [aquí](https://central.github.com/deployments/desktop/desktop/latest/darwin/)

Al iniciar el programa, deberá realizar las siguientes configuraciones:

1. Ir a **Sign in to GitHub.com**. En caso de estar logeado en la página lo dejará avanzar al paso siguiente, caso contrario deberá ingresar sus datos. En caso que no tenga su cuenta creada, ir a Create your free account y siga los pasos señalados.

![imagen2](https://github.com/gavalenz/proyectos/blob/main/docs/imagenes/imagen2.png?raw=true)

2. En la siguiente pantalla, deberá configurar su Git. En Email puede usar su correo personal o el correo que le asigna GitHub. Luego, hacer click en **Finish**.

![imagen3](https://github.com/gavalenz/proyectos/blob/main/docs/imagenes/imagen3.png?raw=true)

3. En la siguiente pantalla, en caso de haber hecho Fork al Git del profesor, le aparecerá su repositorio a la derecha, como se muestra en la imagen. Seleccionelo y haga click en **Clone [nombre usuario]/WebScrapingMDS**

![imagen4](https://github.com/gavalenz/proyectos/blob/main/docs/imagenes/imagen4.png?raw=true)

4. En la siguiente ventana, deberá aparecer el repositorio, por lo que solo deberá seleccionar la carpeta donde quiera alojar la copia local de los documentos. ***Cuide que la carpeta esté vacía***. Luego presione **Clone**.

![imagen5](https://github.com/gavalenz/proyectos/blob/main/docs/imagenes/imagen5.png?raw=true)

5. Luego, para trabajar en el Git del curso deberá seleccionar la opción **To contribute to the parent Project**, y con ello tendrá configurado GitHub Desktop para Windows.


Finalmente, cuando haga alguna modificación en la carpeta local, aparecerá en la pantalla principal de GitHub Desktop un mensaje para realizar push.

![imagen6](https://github.com/gavalenz/proyectos/blob/main/docs/imagenes/imagen6.png?raw=true)

## Jupyter Lab + GitHub

- Requiere tener instalado GitHub Desktop en el equipo y descargados los repositorios
- Descargar Jupyter Lab desde el siguiente link:  [Descarga Aquí](https://jupyter.org/)
- Instalar en el equipo
- Abrir Jupyter Lab
    - Ir a File / Open from Path
    - Seleccionar la carpeta que aloja el repositorio de GitHub
    - Dar aceptar


Ahora tenemos disponible para modificar todos los archivos de nuestro repositorio de GitHub. Para hacer los commit y push, se sigue usando GitHub Desktop :)

## Introducción a BeautifulSoup

Algunas referencias:

[Beautiful Soup Documentation](https://www.crummy.com/software/BeautifulSoup/bs4/doc/)


## Introducción a Selenium

[XPath Helper](https://chrome.google.com/webstore/detail/xpath-helper/hgimnogjllphhhkhlmebbmlgjoejdpjl?hl=en

)


## Introducción a GitHub Actions

[Video introductorio GitHub Actions](https://www.youtube.com/watch?v=PaGp7Vi5gfM)

Generador de cron: https://crontab.guru/
