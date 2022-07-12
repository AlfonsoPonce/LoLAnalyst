import pandas as pd
import numpy as np
from pandasgui import show
import matplotlib.pyplot as plt
import statsmodels.api as sm
from scipy.stats import kstest
import json
import Data_Analytics as da


#show(file)

da_object = da.Data_Analytics('./games.csv')


'''¿Cuantas partidas se han registrado?'''
print("Se han registrado un total de "+ str(da_object.numPartidasRegistradas()) +" partidas")

'''¿Cuantas seasons se han registrado?'''
seasons = da_object.seasonsRegistradas()
print("Se han registrado un total de: "+ str(len(seasons))+" seasons")
print("--------------")
for i in seasons:
    print("Temporada: "+ str(i))

'''¿Cuál ha sido la duración media por partida?'''
mean, std = da_object.duracionMediaPorPartida()

print("De media, cada partida ha durado "+str(mean)+" minutos")
print("Con una desviación de +- "+ str(std)+ " minutos")


#¿Proviene la duración de las partidas de una distribución normal?
da_object.qqPlot()


'''¿El lado azul(1) tiene mayor ventaja que el lado rojo(2)?'''
porcentaje_azul, porcentaje_rojo = da_object.winnerProportion()

print("El lado azul ha ganado un "+str(porcentaje_azul)+" % de las partidas")
print("El lado rojo ha ganado un "+str(porcentaje_rojo)+" % de las partidas")


'''¿Cuál ha sido el spell más usado?¿Y el que menos?'''
spells = pd.DataFrame()
for i in range(2):
    for j in range(5):
        #cad = cad+'\'t'+str(i+1)+'_champ'+str(j+1)+'_sum'+str(i+1)+'\''+','
        spells = spells.append(file['t'+str(i+1)+'_champ'+str(j+1)+'_sum'+str(i+1)])
spells = spells.transpose()

spell = []
count = []

for i in range(2):
    for j in range(5):
        champ_sum = 't'+str(i+1)+'_champ'+str(j+1)+'_sum'+str(i+1)
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
print("El spell más usado ha sido el "+ max_sum_name+" usado en un "+ str(round(total_max_sum_count / total_partidas * 100,2)) +"%")


'''(1)¿Qué relación hay entre el número de Baron Nashor y victoria?'''
'''(2)¿Qué relación hay entre el número de Dragones y victoria?'''
'''(3)¿Y de monstruos en total?'''

baron_nashor = file.groupby(['t1_baronKills', 't2_baronKills', 'winner']).size().reset_index(name='cuenta')
'''
baron_nashor_t1 = file[['t1_baronKills', 'winner']]
numpy_bn = baron_nashor_t1.to_numpy()
print(baron_nashor)
my_rho = np.corrcoef(numpy_bn[:,0], numpy_bn[:,1])
print(my_rho)
#baron_nashor.hist()
#plt.show()
'''


'''(3)'''
monstruos = file[['t1_baronKills', 't1_dragonKills', 't1_riftHeraldKills', 't2_baronKills', 't2_dragonKills', 't2_riftHeraldKills']]
monstruos_t1 = monstruos['t1_baronKills'] + monstruos['t1_dragonKills'] + monstruos['t1_riftHeraldKills']
monstruos_t2 = monstruos['t2_baronKills'] + monstruos['t2_dragonKills'] + monstruos['t2_riftHeraldKills']
stats_t1 = pd.concat([monstruos_t1, file['winner']])
print(stats_t1)
print(monstruos_t1)

fig = plt.figure()
#ax = fig.add_subplot(111, label="1")
#ax2 = fig.add_subplot(111, label="2")
'''
ax.plot(gameId, )
ax.set_xlabel("x label 1", color="C0")
ax.set_ylabel("y label 1", color="C0")
ax.tick_params(axis='x', colors="C0")
ax.tick_params(axis='y', colors="C0")
'''
'''
ax2.plot(monstruos_t2, gameId)
ax2.xaxis.tick_top()
ax2.yaxis.tick_right()
ax2.set_xlabel('x label 2', color="C1")
ax2.set_ylabel('y label 2', color="C1")
ax2.xaxis.set_label_position('top')
ax2.yaxis.set_label_position('right')
ax2.tick_params(axis='x', colors="C1")
ax2.tick_params(axis='y', colors="C1")
'''


monstruos_t1 = monstruos_t1.to_numpy()
labels, counts = np.unique(monstruos_t1, return_counts=True)
plt.subplot(1,2,1)
plt.title("Lado Azul", color='blue')
plt.bar(labels, counts, align='center')
plt.gca().set_xticks(labels)



monstruos_t2 = monstruos_t2.to_numpy()
labels, counts = np.unique(monstruos_t2, return_counts=True)
plt.subplot(1,2,2)
plt.title("Lado Rojo", color='red')
bar_list = plt.bar(labels, counts, align='center', color='red')
plt.gca().set_xticks(labels)

plt.show()

labels = 'Azul', 'Rojo'
total_monstruos_azul = round(monstruos_t1.sum() / len(gameId) * 100, 2)
total_monstruos_rojo = round(monstruos_t2.sum() / len(gameId) * 100, 2)
plt.pie([total_monstruos_azul, total_monstruos_rojo], labels=labels, autopct='%1.1f%%')

plt.show()



'''Para el siguiente día, Mirar las composiciones por partida'''
#show(file[[cad[:-1]]])