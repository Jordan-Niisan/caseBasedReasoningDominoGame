import matplotlib.pyplot as plt

#Greedy
with open('Graph/pointGreedy.txt') as f:
    lines = f.readlines()
    x = [int(line.split()[0]) for line in lines]
    y = [int(line.split()[1]) for line in lines]

plt.ylim(0, 101)
plt.plot(x ,y)

plt.xlabel('Number of Games')
plt.ylabel('Number of Points')
plt.title('Greedy Algorithm')

plt.show()