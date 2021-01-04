# import matplotlib.pyplot as plt

# with open('points.txt') as f:
#     lines = f.readlines()
#     x = [int(line.split()[1]) for line in lines]
#     y = [int(line.split()[0]) for line in lines]

# plt.plot(x ,y,'r--')
# plt.show()

for i in range(1,101):
  files = open("points.txt","a")
  str1 = [str(i),"\n"]
  files.writelines(str1)