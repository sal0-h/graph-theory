from graph import *

#Examples of different dependence tables and how they are converted to an acitivy network

dependence_table = {
    "A" : [[], 10],
    "B" : [[], 6],
    "C" : [["A"], 7],
    "D" : [["A"], 7],
    "E" : [["B"], 7],
    "F" : [["C", "E"], 7],
    "G" : [["D", "F"], 7]
    }

net1 = ActivityNetwork(dependence_table)
# net1.show("basic.html")

dependence_table = {
    "A" : [[], 10],
    "B" : [[], 6],
    "C" : [["A"], 7],
    "D" : [["A"], 7],
    "E" : [["B"], 7],
    "F" : [["B"], 7],
    "G" : [["D"], 7],
    "H" : [["D"], 7],
    "I" : [["C", "E"], 7],
    "J" : [["F"], 7],
    "K" : [["G", "I", "J"], 7],
    "L" : [["H", "K"], 19]
    }

net2 = ActivityNetwork(dependence_table)
# net2.show("basic.html")

dependence_table = {
    "A" : [[], 10],
    "B" : [["A"], 10],
    "C" : [["A"], 10],
    "D" : [["A"], 10],
    "E" : [["B"], 10],
    "F" : [["B"], 10],
    "G" : [["C", "E"], 10],
    "H" : [["D"], 10],
    "I" : [["G", "F"], 10],
    "J" : [["H", "I"], 9]
    }

net3 = ActivityNetwork(dependence_table)
# net3.show("basic.html")

# Example of a dependence table that requires dummy activities
dependence_table = {
    "A" : [[], 10],
    "B" : [["A"], 10],
    "C" : [["A"], 10],
    "D" : [["A"], 10],
    "E" : [["B"], 10],
    "F" : [["B", "C"], 10],
    "G" : [["F", "D"], 10],
    "H" : [["D"], 10],
    "I" : [["G", "H"], 10]
    }


net4 = ActivityNetwork(dependence_table)
net4.show("basic.html")

dependence_table = {
    "A" : [[], 10],
    "B" : [[], 10],
    "C" : [["A", "B"], 10],
    "D" : [["B"], 10],
    "E" : [["B"], 10],
    "F" : [["C"], 10],
    "G" : [["C", "D"], 10],
    "H" : [["E"], 10],
    }

net5 = ActivityNetwork(dependence_table)
# net5.show("basic.html")

depend = {
"A" : [[], 8],
"B" : [[], 6],
"C" : [["A"], 9],
"D" : [["A"], 7],
"E" : [["B"], 5],
"F" : [["C"], 4],
"G" : [["D"], 5],
"H" : [["E"], 8],
"I" : [["F", "D"], 5],
"J" : [["I", "G", "H"], 5],
"K" : [["E"], 5],
}

net = ActivityNetwork(depend)
# net.show('basic.html')

times = net.calculate_early_late_event_times()
for node in times:
    print(node, ': ', times[node][0], times[node][1])

depend = {
"A" : [[], 3],
"B" : [["A"], 6],
"C" : [["A"], 4],
"D" : [["B"], 2],
"E" : [["C"], 1],
"F" : [["C"], 4],
"G" : [["D"], 5],
"H" : [["E", "B"], 4],
}

net = ActivityNetwork(depend)
# net.show('basic.html')

times = net.calculate_early_late_event_times()
for node in times:
    print(node, ': ', times[node][0], times[node][1])

for activity in depend:
    print(activity, ": ", net.float_of_activity(activity))