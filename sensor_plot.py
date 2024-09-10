import matplotlib.pyplot as plt
import pandas as pd

df = pd.read_csv("sensor_readings.csv", sep=',')
df.columns = ['direction', 'key', 'value','colour']

for d in ['left','right','up','down']:
    for c in ['grey', 'black']:
        temp = df[(df.direction==d) & (df.colour==c)]
        plt.plot(temp.direction, temp.value, 'o', c=c)
plt.title('NXT light sensor readings')
plt.xlabel('robot orientation')
plt.ylabel('sensor reading')
plt.savefig('sensor_plot.png', transparent=True)
plt.show()
