
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

#df = pd.DataFrame([{1: 0, 2: 3, 3: 2, 4: 0, 5: 1, 6: 2, 7: 5, 8: 3, 9: 2, 'datetime': '2020-12-23 15:24:17.008097', 'project_id': '01', 'team_id': '01'}, {1: 4, 2: 2, 3: 0, 4: 1, 5: 5, 6: 1, 7: 2, 8: 2, 9: 0, 'datetime': '2021-01-09 20:19:47.775812', 'project_id': '01', 'team_id': '01'}, {1: 5, 2: 5, 3: 5, 4: 5, 5: 0, 6: 0, 7: 5, 8: 5, 9: 5, 'datetime': '2021-01-09 20:23:14.744930', 'project_id': '01', 'team_id': '01'}, {1: 5, 2: 1, 3: 3, 4: 3, 5: 1, 6: 3, 7: 2, 8: 1, 9: 5, 'datetime': '2021-01-16 14:09:51.267759', 'project_id': '01', 'team_id': '01'}, {1: 4, 2: 0, 3: 3, 4: 4, 5: 0, 6: 5, 7: 5, 8: 5, 9: 5, 'datetime': '2021-01-16 15:31:34.703931', 'project_id': '01', 'team_id': '01'}])
df = pd.DataFrame([{'Precondiciones': '4.5', 'Seguridad sicológica': '2.75', 'Dependabilidad': '1.5', 'Estructura y claridad': '3.5', 'Significado': '3.25', 'Impacto': '1.75'}])
print(df)
labels=np.array(['Precondiciones', 'Seguridad sicológica', 'Dependabilidad', 'Estructura y claridad', 'Significado', 'Impacto'])
stats=df.loc[0,labels].values
print(stats)

angles=np.linspace(0, 2*np.pi, len(labels), endpoint=False) # quirto el +1
#new_angles = np.delete(angles, np.s_[:1])
print(angles)
#print(new_angles)
# angles = new_angles # Esto solo deja un espacio en blanco en el crículo.

# close the plot
stats=np.concatenate((stats,[stats[0]]))
angles=np.concatenate((angles,[angles[0]]))

"""
#fig=sns.plt.figure()
fig=plt.figure()
ax = fig.add_subplot(111, polar=True) # El número es la pos dónde se dibuja el grafo
#ax.set_xbound(lower=.0, upper=5.0)
#ax.set_ybound(lower=.0, upper=5.0)
ax.set_autoscalex_on(False)
ax.set_xticks([.0, .5, 1.0, 1.5, 2.0, 3.0, 4.0, 5.0])
ax.plot(angles, stats, 'o-', linewidth=2) #scale no hace nda
ax.fill(angles, stats, alpha=0.25) # Rellena la zona
ax.set_thetagrids(angles * 180/np.pi, labels)
ax.set_title("__Titulo__")
ax.grid(True)

#fig.savefig("output.png")
"""

N = 6
values = stats

# What will be the angle of each axis in the plot? (we divide the plot / number of variable)
angles = [n / float(N) * 2 * np.pi for n in range(N)]
angles += angles[:1]

# Initialise the spider plot
fig=plt.figure()
ax = fig.add_subplot(111, polar=True)

categories = labels
# Draw one axe per variable + add labels labels yet
plt.xticks(angles[:-1], categories, color='grey', size=8)

# Draw ylabels
ax.set_rlabel_position(0)
#plt.yticks([0, 1.0, 2.0, 3.0, 4.0, 5.0], ["0", "1.0", "2.0", "3.0", "4.0", "5.0"], color="grey", size=7)
plt.ylim(0, 5.0)

# Plot data
print("Values:", values)
ax.plot(angles, values, linewidth=1, linestyle='solid')

# Fill area
ax.fill(angles, values, 'b', alpha=0.1)

fig.savefig("output.png")


