import matplotlib.pyplot as plt

#Minimax
with open('Graph/pointsMM.txt') as f:
    lines = f.readlines()
    x = [int(line.split()[0]) for line in lines]
    y = [int(line.split()[1]) for line in lines]

plt.ylim(0, 101)
plt.plot(x ,y)

plt.xlabel('Number of Games')
plt.ylabel('Number of Points')
plt.title('Minimax Algorithm')

plt.show()


