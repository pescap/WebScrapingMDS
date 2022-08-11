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

