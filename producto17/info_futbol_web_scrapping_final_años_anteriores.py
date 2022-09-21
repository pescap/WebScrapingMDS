# Librerías
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import time
import pandas as pd
from selenium.webdriver.common.action_chains import ActionChains


años = [2019, 2020, 2021]

consolidado = pd.DataFrame()

# Ciclo años de la lista
for elemento in años:

    # Opciones de navegación
    options =  webdriver.ChromeOptions()
    options.add_argument('--start-maximized')
    options.add_argument('--disable-extensions')

    driver_path = 'C:\\Users\\fjast\\Desktop\\Magister\\La Web como Fuente de Datos\\Web scrapping - Futbol\\driver\\chromedriver.exe'

    driver = webdriver.Chrome(driver_path, chrome_options=options)

    # Inicialia el navegador con cada año de la lista
    driver.get('https://www.flashscore.cl/futbol/chile/primera-division-' + str(elemento) + "/")

    #driver.get('https://www.flashscore.cl/futbol/chile/primera-division-2021/')

    ### Aceptar cookies
    WebDriverWait(driver, 20)\
        .until(EC.element_to_be_clickable((By.ID,
                                        'onetrust-accept-btn-handler')))\
        .click()

    # Click a Botón mostrar más tantas veces como aparece en la página (depende a cuantos partidos van en el año)

    try:
        for i in range(1, 10):
            target = driver.find_element_by_link_text('Mostrar más partidos')

            # Se mueve al botón "mostrar más"
            actions = ActionChains(driver)
            actions.move_to_element(target)
            actions.perform()

            time.sleep(5)

            ### Click a Boton mostrar mas
            WebDriverWait(driver, 10)\
                .until(EC.element_to_be_clickable((By.CSS_SELECTOR,
                                                'a.event__more.event__more--static')))\
                .click()
            
            time.sleep(5)

    except:
        # Copia tabla de datos de los partidos y se pasa a texto
        resultados = driver.find_element(By.CLASS_NAME, 'event.event--results')

        time.sleep(10)

        resultados = resultados.text

    driver.quit()

    # Separa el texto y luego se eliminan los elementos que no irán en el DataFrame final
    resultados = resultados.split('\n')


    # Se eliminan todos los elementos que tengan la palabra JORNADA y otros que no van en la tabla Final
    resultados_1 = pd.DataFrame({'datos' : resultados})

    resultados_1['eliminar'] = None

    for i in range(0, len(resultados_1)):
        if( (str(resultados_1['datos'][i]).find('JORNADA') >= 0 ) | (str(resultados_1['datos'][i]).find('CHILE') >= 0 ) | \
            (str(resultados_1['datos'][i]).find('Primera') >= 0 ) | (str(resultados_1['datos'][i]).find('División') >= 0 ) | \
            (str(resultados_1['datos'][i]).find('Tabla') >= 0 ) | (str(resultados_1['datos'][i]).find('posiciones') >= 0 ) | \
            (str(resultados_1['datos'][i]).find('Descenso') >= 0 ) | (str(resultados_1['datos'][i]).find('Playoffs') >= 0 ) | \
            (str(resultados_1['datos'][i]).find('Cuadro') >= 0 ) | (str(resultados_1['datos'][i]).find('FINAL') >= 0) ):
            resultados_1['eliminar'][i] = 'Si'
        else:
            resultados_1['eliminar'][i] = 'No'

    resultados_1 = resultados_1[resultados_1['eliminar'] != "Si"]

    resultados_1 = resultados_1.reset_index(drop=True)

    # Se arma el DataFrame con los equipos de local y visita con sus respectivos goles de 1T y 2T

    Fecha = list()
    Local = list()
    Visita = list()
    gol_local = list()
    gol_visita = list()
    gol_local_1t = list()
    gol_visita_1t = list()

    for i in range(0, len(resultados_1), 7):
        Fecha.append(resultados_1['datos'][i])
        Local.append(resultados_1['datos'][i+1])
        Visita.append(resultados_1['datos'][i+2])
        gol_local.append(resultados_1['datos'][i+3])
        gol_visita.append(resultados_1['datos'][i+4])
        gol_local_1t.append(resultados_1['datos'][i+5])
        gol_visita_1t.append(resultados_1['datos'][i+6])


    df = pd.DataFrame({'Fecha':Fecha, 'Local':Local, 'Visita':Visita, 'gol_local':gol_local, \
                    'gol_visita':gol_visita, 'gol_local_1t':gol_local_1t, 'gol_visita_1t':gol_visita_1t})

    df['año'] = elemento

    driver.quit()

    consolidado = pd.concat([consolidado, df], axis=0)


consolidado = consolidado.reset_index()

consolidado.to_csv('partidos_años_2019_2021.csv', index=False)



años = [2020, 2021]

consolidado_est = pd.DataFrame()

# Ciclo años de la lista
for elemento in años:

    # Opciones de navegación
    options =  webdriver.ChromeOptions()
    options.add_argument('--start-maximized')
    options.add_argument('--disable-extensions')

    driver_path = 'C:\\Users\\fjast\\Desktop\\Magister\\La Web como Fuente de Datos\\Web scrapping - Futbol\\driver\\chromedriver.exe'

    driver = webdriver.Chrome(driver_path, chrome_options=options)

    # Inicialia el navegador con cada año de la lista
    driver.get('https://www.flashscore.cl/futbol/chile/primera-division-' + str(elemento) + "/")

    #driver.get('https://www.flashscore.cl/futbol/chile/primera-division-2021/')

    ### Aceptar cookies
    WebDriverWait(driver, 20)\
        .until(EC.element_to_be_clickable((By.ID,
                                        'onetrust-accept-btn-handler')))\
        .click()

    # Click a Botón mostrar más tantas veces como aparece en la página (depende a cuantos partidos van en el año)

    try:
        for i in range(1, 10):
            target = driver.find_element_by_link_text('Mostrar más partidos')

            # Se mueve al botón "mostrar más"
            actions = ActionChains(driver)
            actions.move_to_element(target)
            actions.perform()

            time.sleep(5)

            ### Click a Boton mostrar mas
            WebDriverWait(driver, 10)\
                .until(EC.element_to_be_clickable((By.CSS_SELECTOR,
                                                'a.event__more.event__more--static')))\
                .click()
            
            time.sleep(5)

    except:
        # Copia tabla de datos de los partidos y se pasa a texto
        resultados = driver.find_element(By.CLASS_NAME, 'event.event--results')

        time.sleep(10)

    # Toma la Lista de partidos
    content = driver.find_elements(By.CLASS_NAME, 'event__match.event__match--static.event__match--twoLine')


    # Comienza ciclo

    for i in range(0, len(content)):

        partido_busca = content[i]
        actions = ActionChains(driver)
        actions.move_to_element(partido_busca)
        actions.perform()
        content[i].click()

        time.sleep(2)

        # Listas de ventanas abiertas y selecciona la segunda, que siempre es la emergente de las estidisticas
        window = driver.window_handles
        ventana_est = window[1]
        driver.switch_to.window(ventana_est)

        # En caso de que la ventana emergente no esté por defecto en botón partido
        try:
            driver.find_element_by_link_text('PARTIDO').click()

        except:
            driver.find_element_by_link_text('ESTADÍSTICAS').click()

        time.sleep(5)


        # Item partido (se refiere al partido completo, primer y segundo tiempo)

        partido = driver.find_element(By.CLASS_NAME, 'section')

        # Paso de tabla a texto y separación por saltos
        partido = partido.text
        partido = partido.split('\n')

        # Enunciados estadisticas partido
        columnas_L = list()
        for i in range(0, len(partido), 3):
            columnas_L.append(partido[i+1] + '_local_final')

        columnas_V = list()
        for i in range(0, len(partido), 3):
            columnas_V.append(partido[i+1] + '_visita_final')

        # Estadisticas Local
        est_part_L = list()
        for i in range(0, len(partido), 3):
            est_part_L.append(partido[i])

        # Estadisticas Visita
        est_part_V = list()
        for i in range(2, len(partido), 3):
            est_part_V.append(partido[i])

        # Consolidado de listas
        columnas_L_V = columnas_L + columnas_V
        est_L_V = est_part_L + est_part_V

        # Creación DataFrame con nombres de columnas de estadisticas
        df_P = pd.DataFrame(columns=columnas_L_V)

        # Agregar Fila al df consolidado
        df_P.loc[len(df_P)] = est_L_V


        # Item Primer Tiempo

        # Click a Item Primer Tiempo
        driver.find_element_by_link_text('1ER TIEMPO').click()

        partido_1T = driver.find_element(By.CLASS_NAME, 'section')

        # Paso de tabla a texto y separación por saltos
        partido_1T = partido_1T.text
        partido_1T = partido_1T.split('\n')

        # Enunciados estadisticas partido
        columnas_L = list()
        for i in range(0, len(partido_1T), 3):
            columnas_L.append(partido_1T[i+1] + '_local_1T')

        columnas_V = list()
        for i in range(0, len(partido_1T), 3):
            columnas_V.append(partido_1T[i+1] + '_visita_1T')

        # Estadisticas Local
        est_part_L = list()
        for i in range(0, len(partido_1T), 3):
            est_part_L.append(partido_1T[i])

        # Estadisticas Visita
        est_part_V = list()
        for i in range(2, len(partido_1T), 3):
            est_part_V.append(partido_1T[i])

        # Consolidado de listas
        columnas_L_V = columnas_L + columnas_V
        est_L_V = est_part_L + est_part_V

        # Creación DataFrame con nombres de columnas de estadisticas
        df_1T = pd.DataFrame(columns=columnas_L_V)

        # Agregar Fila al df consolidado
        df_1T.loc[len(df_1T)] = est_L_V

        # Item Segundo Tiempo

        # Click a Item Segundo Tiempo
        driver.find_element_by_link_text('2º TIEMPO').click()

        partido_2T = driver.find_element(By.CLASS_NAME, 'section')

        # Paso de tabla a texto y separación por saltos
        partido_2T = partido_2T.text
        partido_2T = partido_2T.split('\n')

        # Enunciados estadisticas partido
        columnas_L = list()
        for i in range(0, len(partido_2T), 3):
            columnas_L.append(partido_2T[i+1] + '_local_2T')

        columnas_V = list()
        for i in range(0, len(partido_2T), 3):
            columnas_V.append(partido_2T[i+1] + '_visita_2T')

        # Estadisticas Local
        est_part_L = list()
        for i in range(0, len(partido_2T), 3):
            est_part_L.append(partido_2T[i])

        # Estadisticas Visita
        est_part_V = list()
        for i in range(2, len(partido_2T), 3):
            est_part_V.append(partido_2T[i])

        # Consolidado de listas
        columnas_L_V = columnas_L + columnas_V
        est_L_V = est_part_L + est_part_V

        # Creación DataFrame con nombres de columnas de estadisticas
        df_2T = pd.DataFrame(columns=columnas_L_V)

        # Agregar Fila al df consolidado
        df_2T.loc[len(df_2T)] = est_L_V

        estadisticas = pd.concat([df_P, df_1T, df_2T], axis=1)

        consolidado_est = pd.concat([consolidado_est, estadisticas], axis=0)

        consolidado_est['año'] = elemento

        driver.close()

        driver.switch_to.window(driver.window_handles[0])

consolidado_est = consolidado_est.reset_index()

consolidado_est.to_csv('est_2019_2021.csv', index=False)

