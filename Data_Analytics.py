import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import json
import statsmodels.api as sm
class Data_Analytics:



    def __init__(self, file):
        """Inicializa un objeto de esta clase en función del archivo que se le pase

        Args:
            file(str): csv file
        """
        self.file = pd.read_csv(file)


    def numPartidasRegistradas(self):
        """Devuelve cuantas partidas tiene registradas el archivo que se ha pasado al objeto en el constructor


        Returns:
            Número de partidas guardadas
        """
        return len(self.file["gameId"])


    def seasonsRegistradas(self):
        """

        Returns:
             Cuáles seasons se han registrado
        """
        seasons = self.file["seasonId"].unique()

        return seasons

    def duracionMediaPorPartida(self):
        """Calcula cuál es la duración media por partida y la desviación típica. En minutos


        Returns:
            Duración media por partida
            Desviación típica
        """
        duracion_partida = self.file["gameDuration"]  # Valores en segundos
        duracion_partida_media = round(duracion_partida.mean() / 60, 2)
        duracion_partida_desviacion = round(duracion_partida.std() / 60, 2)

        return duracion_partida_media, duracion_partida_desviacion


    #Por mejorar
    def histograma(self, condicion):
        """Muestra por pantalla el histograma de las opciones que se le pasen

        Args:
            condicion(str): variable de la que se quiere ver el histograma
        """
        opciones = ['duracion_partida']
        assert condicion in opciones, 'No existe esa opcion, opciones disponibles: ' + opciones
        self.file.hist(column='gameDuration')

        plt.show()


    def qqPlot(self):
        sm.qqplot(duracion_partida,line='s')  # Si pongo '45' me muestra la línea de acuerdo a una muestra estandarizada
        plt.show()


    def spellsData(self, opciones):
        """
        Análisis sobre los spells usados

        Args:
            opciones: Qué información se quiere obtener de los spells
        :return:
        """
        if opciones == 'max':
            spells = pd.DataFrame()
            for i in range(2):
                for j in range(5):
                    # cad = cad+'\'t'+str(i+1)+'_champ'+str(j+1)+'_sum'+str(i+1)+'\''+','
                    spells = spells.append(self.file['t' + str(i + 1) + '_champ' + str(j + 1) + '_sum' + str(i + 1)])
            spells = spells.transpose()

            spell = []
            count = []

            for i in range(2):
                for j in range(5):
                    champ_sum = 't' + str(i + 1) + '_champ' + str(j + 1) + '_sum' + str(i + 1)
                    sums = spells.groupby(champ_sum).size().reset_index(name='cuenta')
                    sums = sums.to_numpy()
                    c = sums[np.argmax(np.max(sums, axis=1)), :]
                    spell.append(c[0])
                    count.append(c[1])
            max_sum_count = np.argmax(count)
            max_sum_id = spell[max_sum_count]
            max_sum_name = ''
            total_max_sum_count = 0
            for i in range(len(count)):
                if spell[i] == max_sum_id:
                    total_max_sum_count = total_max_sum_count + count[i]

            with open('./summoner_spell_info.json', 'r') as f:
                data = json.load(f)
                max_sum_name = data['data'][str(max_sum_id)]['name']

    def winnerProportion(self):
        """

        Returns:
             Proporción de victorias para el lado azul y rojo
        """
        total_partidas = self.numPartidasRegistradas()
        ganadores = self.file.groupby('winner').size().reset_index(name='cuenta')
        ganadores = ganadores.to_numpy()

        porcentaje_azul = round(ganadores[0][1] / total_partidas * 100, 2)
        porcentaje_rojo = 1 - porcentaje_azul

        return porcentaje_azul, porcentaje_rojo


