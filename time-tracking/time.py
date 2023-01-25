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
    date2num(dt.datetime(2023, 1, 9)),
    date2num(dt.datetime(2023, 1, 10)),
    date2num(dt.datetime(2023, 1, 11)),
    date2num(dt.datetime(2023, 1, 12)),
    date2num(dt.datetime(2023, 1, 13)),
    date2num(dt.datetime(2023, 1, 14)),
    date2num(dt.datetime(2023, 1, 15)),

    date2num(dt.datetime(2023, 1, 16)),
    date2num(dt.datetime(2023, 1, 17)),
    date2num(dt.datetime(2023, 1, 18)),
    date2num(dt.datetime(2023, 1, 19)),
    date2num(dt.datetime(2023, 1, 20)),
    date2num(dt.datetime(2023, 1, 21)),
    date2num(dt.datetime(2023, 1, 22)),

    date2num(dt.datetime(2023, 1, 23)),
    date2num(dt.datetime(2023, 1, 24)),
]

x_week1 = [
    date2num(dt.datetime(2023, 1, 9)),
    date2num(dt.datetime(2023, 1, 10)),
    date2num(dt.datetime(2023, 1, 11)),
    date2num(dt.datetime(2023, 1, 12)),
    date2num(dt.datetime(2023, 1, 13)),
    date2num(dt.datetime(2023, 1, 14)),
    date2num(dt.datetime(2023, 1, 15))
]

x_week2 = [
    date2num(dt.datetime(2023, 1, 16)),
    date2num(dt.datetime(2023, 1, 17)),
    date2num(dt.datetime(2023, 1, 18)),
    date2num(dt.datetime(2023, 1, 19)),
    date2num(dt.datetime(2023, 1, 20)),
    date2num(dt.datetime(2023, 1, 21)),
    date2num(dt.datetime(2023, 1, 22)),
]

x_week3 = [
    date2num(dt.datetime(2023, 1, 23)),
    date2num(dt.datetime(2023, 1, 24)),
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

    (6, 51),
    (6, 33),
    (6, 40),
    (6, 8),
    (3, 19),
    (0, 0),
    (0, 0),

    (7, 17),
    (6, 5)
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

    (6, 38),
    (6, 30),
    (10, 29),
    (7, 23),
    (3, 26),
    (4, 2),
    (3, 2),

    (8, 53),
    (7, 55)
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

    (7, 38),
    (6, 3),
    (6, 13),
    (3, 40),
    (5, 22),
    (0, 44),
    (1, 15),

    (5, 37),
    (7, 0)
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

    (6, 00),
    (4, 42),
    (10, 44),
    (2, 53),
    (2, 17),
    (2, 40),
    (0, 0),

    (5, 9),
    (4, 54)
]
A = [x[0] + round(x[1] / 60, 3) for x in uren_A]

plt.rcParams["figure.figsize"] = [7.00, 3.50]

def worked_hours(ax, y, name, color, fontsize=12):
    ax.plot_date(x, y, "o-", color=color, label=name)

    ax.set_xlabel('datum', fontsize=fontsize)
    ax.set_ylabel('gewerkte uren per dag', fontsize=fontsize)
    ax.set_title(name, fontsize=fontsize)
    ax.xaxis.set_major_formatter(DateFormatter('%d/%m/%Y'))
    ax.tick_params(rotation=45)

def all_times(ax, S, M, J, A, fontsize=12):
    ax.plot_date(x, S, "o-", color='orangered', label='Senne')
    ax.plot_date(x, M, "o-", color='blueviolet', label='Milan')
    ax.plot_date(x, J, "o-", color='dodgerblue', label='Jari')
    ax.plot_date(x, A, "o-", color='hotpink', label='Aléssia')

    ax.xaxis.set_major_formatter(DateFormatter('%d/%m/%Y'))
    ax.tick_params(rotation=45)

    ax.set_xlabel('Datum', fontsize=fontsize)
    ax.set_ylabel('Hours', fontsize=fontsize)
    ax.set_title('Gewerkte uren per persoon', fontsize=fontsize)
    ax.legend(loc="upper left")

def total_time(ax, S, M, J, A, fontsize=12):
    T = [i + j + k + l for i, j, k, l in zip(S, M, J, A)]
    ax.plot(x, T, color='black')
    ax.set_xlabel('datum', fontsize=fontsize)
    ax.set_ylabel('hours', fontsize=fontsize)
    ax.set_title('Totaal gewerkte uren aan project', fontsize=fontsize)

plt.close('all')

##### gemiddelde per persoon
avgS = sum(S) / len(x)
avgM = sum(M) / len(x)
avgJ = sum(J) / len(x)
avgA = sum(A) / len(x)

##### totaal per persoon
totS = sum(S)
totM = sum(M)
totJ = sum(J)
totA = sum(A)

##### totaal van alle leden
totaal = totS + totM + totJ + totA

# chart van alle leden met gewerkte uren over per week
week1_S = [(0, 0), (5, 31), (7, 11), (6, 26), (5, 7), (0, 0), (1, 1)]
week2_S = [(6, 51), (6, 33), (6, 40), (6, 8), (3, 19), (0, 0), (0, 0)]
week3_S = [(7, 17), (6, 5)]
y_week1_S = [x[0] + round(x[1] / 60, 3) for x in week1_S]
y_week2_S = [x[0] + round(x[1] / 60, 3) for x in week2_S]
y_week3_S = [x[0] + round(x[1] / 60, 3) for x in week3_S]

week1_M = [(0, 0), (5, 16), (3, 8), (6, 30), (3, 50), (0, 20), (0, 0)]
week2_M = [(6, 38), (6, 30), (10, 29), (7, 23), (3, 26), (4, 2), (3, 2)]
week3_M = [(8, 53), (7, 55)]
y_week1_M = [x[0] + round(x[1] / 60, 3) for x in week1_M]
y_week2_M = [x[0] + round(x[1] / 60, 3) for x in week2_M]
y_week3_M = [x[0] + round(x[1] / 60, 3) for x in week3_M]

week1_J = [(3, 0), (6, 41), (8, 30), (5, 14), (3, 9), (0, 0), (0, 0)]
week2_J = [(7, 38), (6, 3), (6, 13), (3, 40), (5, 22), (0, 44), (1, 15)]
week3_J = [(5, 37), (7, 0)]
y_week1_J = [x[0] + round(x[1] / 60, 3) for x in week1_J]
y_week2_J = [x[0] + round(x[1] / 60, 3) for x in week2_J]
y_week3_J = [x[0] + round(x[1] / 60, 3) for x in week3_J]

week1_A = [(0, 0), (3, 20), (8, 00), (4, 49), (4, 10), (0, 0), (0, 0)]
week2_A = [(6, 00), (4, 42), (10, 44), (2, 53), (2, 17), (2, 40), (0, 0)]
week3_A = [(5, 9), (4, 54)]
y_week1_A = [x[0] + round(x[1] / 60, 3) for x in week1_A]
y_week2_A = [x[0] + round(x[1] / 60, 3) for x in week2_A]
y_week3_A = [x[0] + round(x[1] / 60, 3) for x in week3_A]



###########################################################################################
teller = 1

while teller == 1:
    keuze_1 = input(f"Wat wil je zien?\n1. Grafiek\n2. Cijfers\n3. Quit\n\t->")
    if(keuze_1 == "1"):
        keuze_2 = input(f"Welke grafieken wil je zien?\n1. Alle leden samen\n2. Per lid\n\t")
        if(keuze_2 == "1"):
            fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(nrows=2, ncols=2)
            worked_hours(ax1, S, "Senne", "orangered")
            worked_hours(ax2, M, "Milan", "blueviolet")
            worked_hours(ax3, J, "Jari", "dodgerblue")
            worked_hours(ax4, A, "Alésssia", "hotpink")
            plt.show()

            fig, ax = plt.subplots()
            all_times(ax, S, M, J, A)
            plt.show()

            fig, ax = plt.subplots()
            total_time(ax, S, M, J, A)
            plt.show()
        elif(keuze_2 == "2"):
            keuze_3 = input(f"Van welke lid wil je een grafiek zien?\n1. Senne\n2. Milan\n3. Jari\n4. Aléssia\n\t->")
            if(keuze_3 == "1"):
                keuze_4 = input(f"Van de voorbije maand of van een specifieke week?\n1. Maand\n2. Week 1\n3. Week 2\n4. Week 3\n\t->")
                if(keuze_4 == "1"):
                    fig, ax = plt.subplots()
                    worked_hours(ax, S, "Senne", "orangered")
                    plt.show()
                elif(keuze_4 == "2"):
                    fig, ax = plt.subplots()
                    ax.plot_date(x_week1, y_week1_S, 'o-', color='orangered')
                    plt.show()
                elif(keuze_4 == "3"):
                    fig, ax = plt.subplots()
                    ax.plot_date(x_week2, y_week2_S, 'o-', color='orangered')
                    plt.show()
                elif(keuze_4 == "4"):
                    fig, ax = plt.subplots()
                    ax.plot_date(x_week3, y_week3_S, 'o-', color='orangered')
                    plt.show()
            elif(keuze_3 == "2"):
                keuze_4 = input(f"Van de voorbije maand of van een specifieke week?\n1. Maand\n2. Week 1\n3. Week 2\n4. Week 3\n\t->")
                if(keuze_4 == "1"):
                    fig, ax = plt.subplots()
                    worked_hours(ax, M, "Milan", "violetblue")
                    plt.show()
                elif(keuze_4 == "2"):
                    fig, ax = plt.subplots()
                    ax.plot_date(x_week1, y_week1_M, 'o-', color='blueviolet')
                    plt.show()
                elif(keuze_4 == "3"):
                    fig, ax = plt.subplots()
                    ax.plot_date(x_week2, y_week2_M, 'o-', color='blueviolet')
                    plt.show()
                elif(keuze_4 == "4"):
                    fig, ax = plt.subplots()
                    ax.plot_date(x_week3, y_week3_M, 'o-', color='blueviolet')
                    plt.show()
            elif(keuze_3 == "3"):
                keuze_4 = input(f"Van de voorbije maand of van een specifieke week?\n1. Maand\n2. Week 1\n3. Week 2\n4. Week 3\n\t->")
                if(keuze_4 == "1"):
                    fig, ax = plt.subplots()
                    worked_hours(ax, J, "Jari", "dodgerblue")
                    plt.show()
                elif(keuze_4 == "2"):
                    fig, ax = plt.subplots()
                    ax.plot_date(x_week1, y_week1_J, 'o-', color='dodgerblue')
                    plt.show()
                elif(keuze_4 == "3"):
                    fig, ax = plt.subplots()
                    ax.plot_date(x_week2, y_week2_J, 'o-', color='dodgerblue')
                    plt.show()
                elif(keuze_4 == "4"):
                    fig, ax = plt.subplots()
                    ax.plot_date(x_week3, y_week3_J, 'o-', color='dodgerblue')
                    plt.show()
            elif(keuze_3 == "4"):
                keuze_4 = input(f"Van de voorbije maand of van een specifieke week?\n1. Maand\n2. Week 1\n3. Week 2\n4. Week 3\n\t->")
                if(keuze_4 == "1"):
                    fig, ax = plt.subplots()
                    worked_hours(ax, A, "Aléssia", "hotpink")
                    plt.show()
                elif(keuze_4 == "2"):
                    fig, ax = plt.subplots()
                    ax.plot_date(x_week1, y_week1_A, 'o-', color='hotpink')
                    plt.show()
                elif(keuze_4 == "3"):
                    fig, ax = plt.subplots()
                    ax.plot_date(x_week2, y_week2_A, 'o-', color='hotpink')
                    plt.show()
                elif(keuze_4 == "4"):
                    fig, ax = plt.subplots()
                    ax.plot_date(x_week3, y_week3_A, 'o-', color='hotpink')
                    plt.show()
            else:
                print("Ongeldige invoer, probeer opnieuw.")
        else:
            print("Ongeldige invoer, probeer opnieuw.")
    elif(keuze_1 == "2"):
        keuze_2 = input(f"Wat wil je van cijfers zien?\n1. Gemiddelde uren\n2. Totaal gewerkte uren\n3. Gewerkte uren voor het project\n\t->")
        if(keuze_2 == "1"):
            print(f"\nGemiddelde uren:")
            print(f"\tGemiddelde gewerkte uren van Senne: {avgS}\n\tGemiddelde gewerkte uren van Milan: {avgM}\n\tGemiddelde gewerkte uren van Jari: {avgJ}\n\tGemiddelde gewerkte uren van Aléssia: {avgA}")
        elif(keuze_2 == "2"):
            print(f"\nTotaal uren:")
            print(f"\tTotaal gewerkte uren van Senne: {totS}\n\tTotaal gewerkte uren van Milan: {totM}\n\tTotaal gewerkte uren van Jari: {totJ}\n\tTotaal gewerkte uren van Aléssia: {totA}")
        elif(keuze_2 == "3"):
            print(f"\nTotaal uren voor het project:")
            print(f"\n\tTotaal gewerkte uren voor het project: {totaal}\n")
        else:
            print(f"Ongeldige invoer, probeer opnieuw.")
    elif(keuze_1 == "3" or keuze_1.capitalize() == "Q"):
        teller = 0
    else:
        print(f"Ongeldige invoer, probeer opnieuw.")



