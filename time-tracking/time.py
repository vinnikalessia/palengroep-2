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
        9, 10, 11, 12, 13, 14, 15
]

# Senne
# in deze list noteer je je gewerkte uren van toggle voor elke dag vanaf 9 januari
# (uren, minuten) => wordt dan herberekend door code zelf. MINUTEN NIET ZELF HERBEREKENEN!
# momenteel dummy data
uren_S = [
    (5, 20),
    (3, 10),
    (1, 50),
    (4, 23),
    (4, 46),
    (2, 21),
    (7, 23)
]
S = [x[0] + round(x[1] / 60, 3) for x in uren_S]

# Milan
# in deze list noteer je je gewerkte uren van toggle voor elke dag vanaf 9 januari
# (uren, minuten) => wordt dan herberekend door code zelf. MINUTEN NIET ZELF HERBEREKENEN!
# momenteel dummy data
uren_M = [
    (5, 20),
    (3, 10),
    (1, 50),
    (4, 23),
    (4, 46),
    (2, 21),
    (7, 23)
]
M = [x[0] + round(x[1] / 60, 3) for x in uren_M]

# Jari
# in deze list noteer je je gewerkte uren van toggle voor elke dag vanaf 9 januari
# (uren, minuten) => wordt dan herberekend door code zelf. MINUTEN NIET ZELF HERBEREKENEN!
# momenteel dummy data
uren_J = [
    (5, 20),
    (3, 10),
    (1, 50),
    (4, 23),
    (4, 46),
    (2, 21),
    (7, 23)
]
J = [x[0] + round(x[1] / 60, 3) for x in uren_J]

# Aléssia
# in deze list noteer je je gewerkte uren van toggle voor elke dag vanaf 9 januari
# (uren, minuten) => wordt dan herberekend door code zelf. MINUTEN NIET ZELF HERBEREKENEN!
# momenteel dummy data
uren_A = [
    (5, 20),
    (3, 10),
    (1, 50),
    (4, 23),
    (4, 46),
    (2, 21),
    (7, 23)
]
A = [x[0] + round(x[1] / 60, 3) for x in uren_A]

plt.rcParams["figure.figsize"] = [7.00, 3.50]

def time_senne(ax, y, fontsize=12):
    ax.plot(x, y, color='lightcoral')

    ax.locator_params(nbins=3)
    ax.set_xlabel('datum', fontsize=fontsize)
    ax.set_ylabel('hours', fontsize=fontsize)
    ax.set_title('Senne', fontsize=fontsize)

def time_milan(ax, y, fontsize=12):
    ax.plot(x, y, color='silver')

    ax.locator_params(nbins=3)
    ax.set_xlabel('datum', fontsize=fontsize)
    ax.set_ylabel('hours', fontsize=fontsize)
    ax.set_title('Milan', fontsize=fontsize)

def time_jari(ax, y, fontsize=12):
    ax.plot(x, y, color='powderblue')

    ax.locator_params(nbins=3)
    ax.set_xlabel('datum', fontsize=fontsize)
    ax.set_ylabel('hours', fontsize=fontsize)
    ax.set_title('Jari', fontsize=fontsize)

def time_alessia(ax, y, fontsize=12):
    ax.plot(x, y, color='hotpink')

    ax.locator_params(nbins=3)
    ax.set_xlabel('datum', fontsize=fontsize)
    ax.set_ylabel('hours', fontsize=fontsize)
    ax.set_title('Aléssia', fontsize=fontsize)

def all_times(ax, S, M, J, A, fontsize=12):
        ax.plot(x, S, color='lightcoral')
        ax.plot(x, M, color='silver')
        ax.plot(x, J, color='powderblue')
        ax.plot(x, A, color='hotpink')
        
        ax.locator_params(nbins=3)
        ax.set_xlabel('datum', fontsize=fontsize)
        ax.set_ylabel('hours', fontsize=fontsize)
        ax.set_title('Alle leden', fontsize=fontsize)
        ax.legend()

def total_time(ax, S, M, J, A, fontsize=12):
        T = [i + j + k + l for i,j,k,l in zip(S, M, J, A)]
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
print(f"\n\tGemiddelde gewerkte uren van Senne: {avgS}\n\tGemiddelde gewerkte uren van Milan: {avgS}\n\tGemiddelde gewerkte uren van Jari: {avgS}\n\tGemiddelde gewerkte uren van Aléssia: {avgS}")

##### totaal per persoon
totS = sum(S)
totM = sum(M)
totJ = sum(J)
totA = sum(A)
print(f"\n\tTotaal gewerkte uren van Senne: {totS}\n\tTotaal gewerkte uren van Milan: {totM}\n\tTotaal gewerkte uren van Jari: {totJ}\n\tTotaal gewerkte uren van Aléssia: {totA}")

##### totaal van alle leden
totaal = totS + totM + totJ + totA
print(f"\n\tTotaal gewerkte uren van alle leden: {totaal}\n")

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

