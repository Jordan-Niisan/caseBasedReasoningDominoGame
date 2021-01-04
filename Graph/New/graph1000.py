import matplotlib.pyplot as plt

#Case Based
with open('Graph/casebased1000.txt') as f:
    lines = f.readlines()
    x = [int(line.split()[0]) for line in lines]
    y = [int(line.split()[1]) for line in lines]

plt.ylim(0, 101)
plt.plot(x ,y)

plt.xlabel('Number of Games')
plt.ylabel('Number of Points')
plt.title('Case-based reasoning Algorithm 1000+ data')

plt.show()