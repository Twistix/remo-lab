import matplotlib.pyplot as plt

with open('waveform.txt') as f:
    lines = f.readlines()

waveform = [[],[]]
for i in range(len(lines)) :
    index1 = lines[i].index(',')
    index2 = lines[i].index('\n')
    waveform[0].append(float(lines[i][0:index1]))
    waveform[1].append(float(lines[i][index1+1:index2]))

plt.plot(waveform[1],waveform[0])
plt.ylabel('voltage (V)')
plt.ylabel('time (ms)')
plt.show()

