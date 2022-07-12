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


    def monsterImpact(self, opciones):
        if opciones == 'split':
            self.splitImpact('riftHerald')
        elif opciones == 'all':
            self.allImpact()



    def splitImpact(self, opcion):
        assert opcion in ['baron', 'dragon', 'riftHerald']

        stats = self.file[['t1_'+opcion+'Kills', 't2_'+opcion+'Kills', 'winner']]

        difference = stats['t1_'+opcion+'Kills'] - stats['t2_'+opcion+'Kills']

        new_stats = pd.DataFrame()
        new_stats['difference'] = difference
        new_stats['winner'] = stats['winner']
        #Si difference[i] > 0 entonces se ha hecho más barons el equipo azul

        blue_team_n = new_stats[new_stats['difference'] > 0]
        red_team_n = new_stats[new_stats['difference'] < 0]
        neutral_n = new_stats[new_stats['difference'] == 0]

        porcentajes = [len(blue_team_n) / self.numPartidasRegistradas()*100, len(red_team_n) / self.numPartidasRegistradas()*100,
                       len(neutral_n) / self.numPartidasRegistradas()*100]

        print("En " + str(len(blue_team_n)) + " el equipo azul se ha hecho más "+opcion+"s.")
        print("En " + str(len(red_team_n))  + " el equipo rojo se ha hecho más "+opcion+"s.")
        print("En " + str(len(neutral_n))   + " ambos equipos hicieron los mismos "+opcion+"s.")

        labels = ['blue', 'red', 'neutral']

        fig1, ax1 = plt.subplots()
        ax1.pie(porcentajes, labels=labels, autopct='%1.1f%%',
                shadow=True, startangle=90)
        ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.

        plt.show()

        labels2 = [opcion+'_blue_Win_blue', opcion+'_blue_Win_red', opcion+'_red_Win_blue', opcion+'_red_Win_red',
                   opcion+'_neutral_Win_blue', opcion+'_neutral_Win_red']

        blue_team_n_wb = blue_team_n[blue_team_n['winner'] == 1]
        blue_team_n_wr = blue_team_n[blue_team_n['winner'] == 2]

        red_team_n_wb = red_team_n[red_team_n['winner'] == 1]
        red_team_n_wr = red_team_n[red_team_n['winner'] == 2]

        neutral_team_n_wb = neutral_n[neutral_n['winner'] == 1]
        neutral_team_n_wr = neutral_n[neutral_n['winner'] == 2]

        porcentajes2 = [len(blue_team_n_wb) / self.numPartidasRegistradas() * 100, len(blue_team_n_wr) / self.numPartidasRegistradas() * 100,
                        len(red_team_n_wb) / self.numPartidasRegistradas() * 100, len(red_team_n_wr) / self.numPartidasRegistradas() * 100,
                        len(neutral_team_n_wb) / self.numPartidasRegistradas() * 100, len(neutral_team_n_wr) / self.numPartidasRegistradas() * 100]

        fig2, ax2 = plt.subplots()
        ax2.pie(porcentajes2, labels=labels2, autopct='%1.1f%%',
                shadow=True, startangle=90)
        ax2.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.

        plt.show()

    def allImpact(self):
        stats = pd.DataFrame()
        stats['t1_monsterKills'] = self.file['t1_baronKills']+ self.file['t1_dragonKills']+self.file['t1_riftHeraldKills']
        stats['t2_monsterKills'] = self.file['t2_baronKills'] +self.file['t2_dragonKills']+self.file['t2_riftHeraldKills']

        stats['winner'] = self.file['winner']

        difference = stats['t1_monsterKills'] - stats['t2_monsterKills']

        new_stats = pd.DataFrame()
        new_stats['difference'] = difference
        new_stats['winner'] = stats['winner']
        # Si difference[i] > 0 entonces se ha hecho más barons el equipo azul

        blue_team_n = new_stats[new_stats['difference'] > 0]
        red_team_n = new_stats[new_stats['difference'] < 0]
        neutral_n = new_stats[new_stats['difference'] == 0]

        porcentajes = [len(blue_team_n) / self.numPartidasRegistradas() * 100,
                       len(red_team_n) / self.numPartidasRegistradas() * 100,
                       len(neutral_n) / self.numPartidasRegistradas() * 100]

        print("En " + str(len(blue_team_n)) + " el equipo azul se ha hecho más monstruos.")
        print("En " + str(len(red_team_n)) + " el equipo rojo se ha hecho más monstruos.")
        print("En " + str(len(neutral_n)) + " ambos equipos hicieron los mismos monstruos.")

        labels = ['blue', 'red', 'neutral']

        fig1, ax1 = plt.subplots()
        ax1.pie(porcentajes, labels=labels, autopct='%1.1f%%',
                shadow=True, startangle=90)
        ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.

        plt.show()

        labels2 = ['Monster_blue_Win_blue', 'Monster_blue_Win_red', 'Monster_red_Win_blue',
                   'Monster_red_Win_red',
                   'Monster_neutral_Win_blue', 'Monster_neutral_Win_red']

        blue_team_n_wb = blue_team_n[blue_team_n['winner'] == 1]
        blue_team_n_wr = blue_team_n[blue_team_n['winner'] == 2]

        red_team_n_wb = red_team_n[red_team_n['winner'] == 1]
        red_team_n_wr = red_team_n[red_team_n['winner'] == 2]

        neutral_team_n_wb = neutral_n[neutral_n['winner'] == 1]
        neutral_team_n_wr = neutral_n[neutral_n['winner'] == 2]

        porcentajes2 = [len(blue_team_n_wb) / self.numPartidasRegistradas() * 100,
                        len(blue_team_n_wr) / self.numPartidasRegistradas() * 100,
                        len(red_team_n_wb) / self.numPartidasRegistradas() * 100,
                        len(red_team_n_wr) / self.numPartidasRegistradas() * 100,
                        len(neutral_team_n_wb) / self.numPartidasRegistradas() * 100,
                        len(neutral_team_n_wr) / self.numPartidasRegistradas() * 100]

        fig2, ax2 = plt.subplots()
        ax2.pie(porcentajes2, labels=labels2, autopct='%1.1f%%',
                shadow=True, startangle=90)
        ax2.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.

        plt.show()

        print(stats)


    def champStats(self, opcion):
        if opcion == 'histogramPlayed':
            self.histrogramPlayedChamps()


    def histrogramPlayedChamps(self):
        champs = self.file[['t1_champ1id', 't1_champ2id', 't1_champ3id', 't1_champ4id', 't1_champ5id',
                            't2_champ1id', 't2_champ2id', 't2_champ3id', 't2_champ4id', 't2_champ5id',]]



        champ_dict = {}

        with open('champion_info.json', 'r') as f:
            data = json.load(f)
            for id in data['data']:
                champ_dict[data['data'][str(id)]['name']] = id

        Z = champs['t1_champ1id']
        key_list = list(champ_dict.keys())
        val_list = list(champ_dict.values())
        x = []
        for champ in Z:
            position = val_list.index(str(champ))
            name = key_list[position]
            x.append(name)
        values, counts = np.unique(x, return_counts=True)
        plt.vlines(values, 0, counts, color='C0', lw=4)
        plt.xticks(rotation='vertical')
        plt.ylim(0, max(counts) * 1.06)
        plt.show()







