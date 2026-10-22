import csv
import json


class Duty:
    def __init__(self, staff, day, duty, start, end):
        self.staff = staff  # list of staff numbers
        self.day = day
        self.duty = duty
        self.start = start
        self.end = end

    def display(self):
        print(self.staff, self.day, self.start, self.end, self.duty)


class Staff:
    def __init__(self, number, name):
        self.number = number
        self.name = name


class Roster:
    def __init__(self):
        self.staff = {}  # staff number -> Staff
        self.duties = []

    def duties_for(self, number):
        return [d for d in self.duties if number in d.staff]

    def names(self, numbers):
        return [self.staff[n].name for n in numbers]


def load(r):
    with open("staff.csv") as csvfile:
        for row in csv.DictReader(csvfile):
            number = int(row["number"])
            r.staff[number] = Staff(number, row["name"])

    with open("duties.csv") as csvfile:
        for row in csv.DictReader(csvfile):
            # Skip blank (free time) slots
            if not row["duty"].strip():
                continue
            r.duties.append(
                Duty(
                    json.loads(row["staff"]),
                    row["day"],
                    row["duty"],
                    row["time"],
                    row["end"],
                )
            )


if __name__ == "__main__":
    r = Roster()
    load(r)
    for d in r.duties[:10]:
        d.display()
