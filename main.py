import matplotlib.pyplot as plt
import numpy as np
import random
import string

#labri.fr/perso/bourqui/downloads/cours

def randomString(stringLength=10):
    """Generate a random string of fixed length """
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(stringLength))

SIZE = 10
N = 8
x = np.linspace(1, SIZE-1, SIZE)
y = np.random.rand(SIZE, 1)
height = np.random.uniform(0, 100, SIZE)
names = [randomString(5) for i in range(SIZE)]
data = np.random.rand(N, SIZE)


###  Exo 1  ###

def plot(x, y):
    plt.plot(x, y, color='green', marker='o', linestyle='dashed', linewidth=2, markersize=12)

# plot(x, y)


###  Exo 2  ###

def plot_sin():
    X = np.linspace(-2 * np.pi, 2 * np.pi, 100)
    Y = [np.sin(x) for x in X]
    plt.plot(X, Y)

def plot_cos():
    X = np.linspace(-2 * np.pi, 2 * np.pi, 100)
    Y = [np.cos(x) for x in X]
    plt.plot(X, Y)

# plot_sin()
# plot_cos()


###  Exo 3  ###

def scatter(x, y):
    plt.scatter(x, y)

# scatter(x, y)


###  Exo 4  ###

def bar(x, height):
    plt.bar(x, height)

# bar(x, height)


###  Exo 5  ###

# bar(names, height)


###  Exo 6  ###

def exo6(names, data):
    mean = np.mean(data, axis=0)
    std = np.std(data, axis=0)
    plt.bar(names, mean, yerr=std)

# exo6(names, data)


###  Exo 7  ###

def hist(a, n):
    plt.hist(a, bins=n, color='red', rwidth=0.75)

# hist(y, 5)


###  Exo 8  ###

def moustache(data):
    plt.boxplot(data, widths=0.5)

def violon(data):
    plt.violinplot(data)

# moustache(data)
# violon(data)


###  Exo 10  ###

def bubble(a1, a2, a3, a4=None):
    plt.scatter(a1, a2, s=a3, c=a4)

# bubble(x, y, np.random.rand(SIZE, 1)*100, np.random.rand(SIZE, 1))


###  Exo 11  ###

def exo11(data):
    _, m = np.shape(data)
    # print(n, m)
    for i in range(m):
        for j in range(m):
            plt.subplot(m, m, i * m + j + 1)
            plt.scatter(data[:,i], data[:,j])

# exo11(np.random.rand(10, 5) * 100)


###  Exo 12  ###

def exo12(data):
    exo11(data)
    _, m = np.shape(data)
    for i in range(m):
        axes = plt.subplot(m, m, i * (m + 1) + 1)
        axes.clear()
        plt.hist(data[:,i], rwidth=0.75, color='green')

# exo12(np.random.rand(10, 5) * 100)


###  Exo 13  ###

def exo13(file):
    import os
    import sys
    import pandas as pd
    from dateutil import parser
    import matplotlib.dates as mdates
    
    # mute pandas warning when plotting
    pd.plotting.register_matplotlib_converters()

    def parse_date(df):
        def valid_datetime(date):
            try:
                return parser.parse(date)
            except ValueError:
                print("Invalid date:", date)
                return None
        df['Timestamp'] = df['Timestamp'].apply(valid_datetime)
        return df

    print("loading data...")
    data = pd.read_csv(file, sep=';', compression="gzip")
    print("data loaded")
    parse_date(data)
    # resample data on 1 hour
    data = data.set_index('Timestamp').resample('1h', label='right', closed='right').last().dropna().reset_index()

    days = mdates.DayLocator()   # every year
    hours = mdates.HourLocator()  # every month
    date_fmt = mdates.DateFormatter('%d-%b-%Y')

    fig, axes = plt.subplots(2, 3)
    for i in range(len(axes)):
        for j in range(len(axes[i])):
            axes[i, j].xaxis.set_major_locator(days)
            axes[i, j].xaxis.set_major_formatter(date_fmt)
            axes[i, j].xaxis.set_minor_locator(hours)

    axes[0, 0].set_title('Availability')
    axes[0, 0].bar(data['Timestamp'], data['Bikes'], linewidth=0, width=1/24, label='bikes')
    axes[0, 0].bar(data['Timestamp'], data['Slots'], bottom=data['Bikes'], linewidth=0, width=1/24, label='slots')
    axes[0, 0].set_ylabel('Quantity')
    axes[0, 0].legend()

    axes[0, 1].set_title('Humidity')
    axes[0, 1].plot(data['Timestamp'], data['Humidity'])
    axes[0, 1].set_ylabel('%')

    axes[1, 1].set_title('Pressure')
    axes[1, 1].plot(data['Timestamp'], data['Pressure'])
    axes[1, 1].set_ylabel('hPa')

    axes[1, 0].set_title('Temperature')
    axes[1, 0].plot(data['Timestamp'], data['TemperatureTemp'])
    axes[1, 0].set_ylabel('Celsius Degree (°C)')

    axes[0, 2].set_title('Wind degree')
    axes[0, 2].plot(data['Timestamp'], data['WindDeg'], marker='.', linestyle=' ')
    axes[0, 2].set_yticks(np.arange(0, 361, 45))
    axes[0, 2].set_yticklabels(('N', 'NE', 'E', 'SE', 'S', 'SW', 'W', 'NW', 'N'))

    axes[1, 2].set_title('Wind speed')
    axes[1, 2].plot(data['Timestamp'], data['WindSpeed'])
    axes[1, 2].set_ylabel('m.s-1')

    fig.autofmt_xdate()


exo13("./data/01. Duc/2014-11-14 09:40:00.csv.gz")

plt.show()