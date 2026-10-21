import csv


class Duty:
    def __init__(self, name, day, duty, start, end):
        self.name = name
        self.day = day
        self.duty = duty
        self.start = start
        self.end = end
        self.otherstaff = []

    def display(self):
        print(self.name, self.day, self.start, self.end, self.duty)


class Staff:
    def __init__(self, name, index):
        self.name = name
        self.index = index


class Roster:
    def __init__(self):
        self.stafflist = []
        self.duties = []

    def display(self):
        for staff in self.stafflist[0:10]:
            for d in self.duties:
                if d.name == staff:
                    d.display()


def add_other_staff(r):
    for d in r.duties:
        for o in r.duties:
            if (
                d.day == o.day
                and d.start == o.start
                and d.end == o.end
                and not d.name == o.name
                and not o.name in d.otherstaff
            ):
                d.otherstaff.append(o.name)


def load(r):
    with open("duties.csv") as csvfile:
        reader = csv.DictReader(csvfile)
        headers = reader.fieldnames
        stafflist = []

        for row in reader:
            if not row["staff"] in stafflist:
                stafflist.append(row["staff"])

            r.duties.append(
                Duty(row["staff"], row["day"], row["duty"], row["time"], row["end"])
            )
    for i, s in enumerate(stafflist):
        r.stafflist.append(Staff(s, i))
        add_other_staff(r)


if __name__ == "__main__":
    r = Roster()
    load(r)
