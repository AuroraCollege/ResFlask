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
        self.groups = {}  # year (5, 7, ...) -> list of Duty

    def duties_for(self, number):
        return [d for d in self.duties if number in d.staff]

    def names(self, numbers):
        return [self.staff[n].name for n in numbers]

    def by_day(self, duties=None):
        # Group duties by day, keeping the roster's day order
        days = {}
        for d in self.duties if duties is None else duties:
            days.setdefault(d.day, []).append(d)
        return days


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

    with open("yeargroups.csv") as csvfile:
        reader = csv.DictReader(csvfile)
        years = [h for h in reader.fieldnames if h.startswith("Y")]
        for year in years:
            r.groups[int(year[1:])] = []
        for row in reader:
            for year in years:
                activity = row[year]
                # Skip blank (free time) slots
                if not activity.strip():
                    continue
                duties = r.groups[int(year[1:])]
                prev = duties[-1] if duties else None
                # Rows are only combined when every group matches, so
                # join this group's back-to-back slots of the same activity
                if (
                    prev
                    and prev.day == row["Day"]
                    and prev.end == row["Time"]
                    and prev.duty == activity
                ):
                    prev.end = row["End"]
                else:
                    duties.append(
                        Duty([], row["Day"], activity, row["Time"], row["End"])
                    )


if __name__ == "__main__":
    r = Roster()
    load(r)
    for d in r.duties[:10]:
        d.display()
