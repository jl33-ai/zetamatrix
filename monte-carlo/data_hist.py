import matplotlib.pyplot as plt
import statistics

with open("export.txt", 'r') as fp:
    data = fp.read()

data = [int(num) for num in data.split(',')]
plt.hist(data, bins=250)
plt.title(f"mean: {statistics.mean(data)}, sd: {statistics.stdev(data)}")
plt.show()
