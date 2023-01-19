import matplotlib.pyplot as plt
from matplotlib.dates import date2num, DateFormatter
import datetime as dt

plt.rcParams["figure.figsize"] = [7.00, 3.50]
plt.rcParams["figure.autolayout"] = True


# tijdslijn => vanaf 9 januari tot 3& januari
# 9, 10, 11, 12, 13, 14, 15,
# 16, 17, 18, 19, 20, 21, 22,
# 23, 24, 25, 26, 27, 28, 29,
# 30, 31
x = [
    date2num(dt.datetime(2022, 11, 9)),
    date2num(dt.datetime(2022, 11, 10)),
    date2num(dt.datetime(2022, 11, 11)),
    date2num(dt.datetime(2022, 11, 12)),
    date2num(dt.datetime(2022, 11, 13)),
    date2num(dt.datetime(2022, 11, 14)),
    date2num(dt.datetime(2022, 11, 15)),
    date2num(dt.datetime(2022, 11, 16))
]

# Senne
# in deze list noteer je je gewerkte uren van toggle voor elke dag vanaf 9 januari
# (uren, minuten) => wordt dan herberekend door code zelf. MINUTEN NIET ZELF HERBEREKENEN!
# momenteel dummy data
uren_S = [
    (0, 0),
    (5, 31),
    (7, 11),
    (6, 26),
    (5, 7),
    (0, 0),
    (1, 1),
    (6, 51)
]
S = [x[0] + round(x[1] / 60, 3) for x in uren_S]

# Milan
# in deze list noteer je je gewerkte uren van toggle voor elke dag vanaf 9 januari
# (uren, minuten) => wordt dan herberekend door code zelf. MINUTEN NIET ZELF HERBEREKENEN!
# momenteel dummy data
uren_M = [
    (0, 0),
    (5, 16),
    (3, 8),
    (6, 30),
    (3, 50),
    (0, 20),
    (0, 0),
    (6, 38)
]
M = [x[0] + round(x[1] / 60, 3) for x in uren_M]

# Jari
# in deze list noteer je je gewerkte uren van toggle voor elke dag vanaf 9 januari
# (uren, minuten) => wordt dan herberekend door code zelf. MINUTEN NIET ZELF HERBEREKENEN!
# momenteel dummy data
uren_J = [
    (3, 0),
    (6, 41),
    (8, 30),
    (5, 14),
    (3, 9),
    (0, 0),
    (0, 0),
    (7, 38)
]
J = [x[0] + round(x[1] / 60, 3) for x in uren_J]

# Aléssia
# in deze list noteer je je gewerkte uren van toggle voor elke dag vanaf 9 januari
# (uren, minuten) => wordt dan herberekend door code zelf. MINUTEN NIET ZELF HERBEREKENEN!
# momenteel dummy data
uren_A = [
    (0, 0),
    (3, 20),
    (8, 00),
    (4, 49),
    (4, 10),
    (0, 0),
    (0, 0),
    (6, 00)
]
A = [x[0] + round(x[1] / 60, 3) for x in uren_A]

plt.rcParams["figure.figsize"] = [7.00, 3.50]

def time_senne(ax, y, fontsize=8):
    ax.plot(x, y, color='orangered')

    ax.locator_params(nbins=3)
    ax.set_xlabel('datum', fontsize=fontsize)
    ax.set_ylabel('gewerkte uren per dag', fontsize=fontsize)
    ax.set_title('Senne', fontsize=fontsize)

def time_milan(ax, y, fontsize=8):
    ax.plot(x, y, color='blueviolet')

    ax.locator_params(nbins=3)
    ax.set_xlabel('datum', fontsize=fontsize)
    ax.set_ylabel('gewerkte uren per dag', fontsize=fontsize)
    ax.set_title('Milan', fontsize=fontsize)

def time_jari(ax, y, fontsize=8):
    ax.plot(x, y, color='dodgerblue')

    ax.locator_params(nbins=3)
    ax.set_xlabel('datum', fontsize=fontsize)
    ax.set_ylabel('gewerkte uren per dag', fontsize=fontsize)
    ax.set_title('Jari', fontsize=fontsize)

def time_alessia(ax, y, fontsize=8):
    ax.plot(x, y, color='hotpink')

    ax.locator_params(nbins=3)
    ax.set_xlabel('datum', fontsize=fontsize)
    ax.set_ylabel('gewerkte uren per dag', fontsize=fontsize)
    ax.set_title('Aléssia', fontsize=fontsize)

def all_times(ax, S, M, J, A, fontsize=12):
        ax.plot_date(x, S, "o-", color='orangered', label='Senne')
        ax.plot_date(x, M, "o-", color='blueviolet', label='Milan')
        ax.plot_date(x, J, "o-", color='dodgerblue', label='Jari')
        ax.plot_date(x, A, "o-", color='hotpink', label='Aléssia')

        ax.xaxis.set_major_formatter(DateFormatter('%d/%m/%Y'))
        ax.tick_params(rotation=45)
        
        ax.locator_params(nbins=3)
        ax.set_xlabel('Datum', fontsize=fontsize)
        ax.set_ylabel('Hours', fontsize=fontsize)
        ax.set_title('Gewerkte uren per persoon', fontsize=fontsize)
        ax.legend(loc="upper left")

def total_time(ax, S, M, J, A, fontsize=12):
        T = [i + j + k + l for i, j, k, l in zip(S, M, J, A)]
        ax.plot(x, T, color='black')
        ax.locator_params(nbins=3)
        ax.set_xlabel('datum', fontsize=fontsize)
        ax.set_ylabel('hours', fontsize=fontsize)
        ax.set_title('Totaal gewerkte uren aan project', fontsize=fontsize)

plt.close('all')

##### gemiddelde per persoon
avgS = sum(S) / len(x)
avgM = sum(M) / len(x)
avgJ = sum(J) / len(x)
avgA = sum(A) / len(x)
print(f"\nGEMIDDELDE UREN:")
print(f"\tGemiddelde gewerkte uren van Senne: {avgS}\n\tGemiddelde gewerkte uren van Milan: {avgS}\n\tGemiddelde gewerkte uren van Jari: {avgS}\n\tGemiddelde gewerkte uren van Aléssia: {avgS}")

##### totaal per persoon
totS = sum(S)
totM = sum(M)
totJ = sum(J)
totA = sum(A)
print(f"\nTOTAAL UREN:")
print(f"\tTotaal gewerkte uren van Senne: {totS}\n\tTotaal gewerkte uren van Milan: {totM}\n\tTotaal gewerkte uren van Jari: {totJ}\n\tTotaal gewerkte uren van Aléssia: {totA}")

##### totaal van alle leden
totaal = totS + totM + totJ + totA
print(f"\n\tTotaal gewerkte uren voor het project: {totaal}\n")

# gewerkte uren per dag van alle leden apart in 4 grafieken
fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(nrows=2, ncols=2)
time_senne(ax1, S)
time_milan(ax2, M)
time_jari(ax3, J)
time_alessia(ax4, A)
plt.tight_layout()
plt.show()

# gewerkte uren per dag van alle leden apart in 1 grafiek
fig, ax = plt.subplots()
all_times(ax, S, M, J, A)
plt.tight_layout()
plt.show()

# gewerkte uren van alle leden te samen in 1 grafiek
fig, ax = plt.subplots()
total_time(ax, S, M, J, A)
plt.tight_layout()
plt.show()

