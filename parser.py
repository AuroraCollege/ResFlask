import csv
from itertools import islice


class Duty:
    def __init__(self, day, time, duty, staff_num):
        self.staff = [staff_num]
        self.day = day
        self.time = time
        self.duty = duty
        self.end = None

    def display(self):
        print(self.staff, self.day, self.time, self.duty, self.end)


def get_times(f):
    times = []
    with open(f, mode="r") as file:
        reader = csv.DictReader(file)
        for row in reader:
            times.append(row["Time"])
    return times


def get_staff_names(file):
    junk_rows = [
        "﻿Day",
        "Time",
        "Y5 (145) Narrabeen",
        "Year 7 (107) Narrabeen",
        "Year 8 (128) Collaroy",
        "Year 9 (100) Collaroy",
        "Year 10 (62) Collaroy",
    ]
    with open(file) as csvfile:
        reader = csv.DictReader(csvfile)
        staff_names = []
        headers = next(reader, None)
        for head in headers:
            if not head.strip() in junk_rows:
                staff_names.append(head)
    return staff_names


def get_duties(file, staff, staffdict):
    junk_duties = [
        "Day",
        "Time",
        "Activity",
        "Narra- Stage 3",
        "Narra- English",
        "Narra- Maths",
        "Narra- Science",
        "Narra- Exec",
        "Coll- English",
        "Coll- Maths",
        "Coll- Science",
        "Coll- Wellbeing",
        "Coll- Exec",
    ]

    with open(file) as csvfile:
        reader = csv.DictReader(csvfile)
        headers = reader.fieldnames
        duties = []
        for row in reader:
            for s in staff:
                if row[s].strip() not in junk_duties:
                    duty = next(
                        (
                            d
                            for d in duties
                            if d.day == row[headers[0]]
                            and d.time == row[headers[1]]
                            and d.duty == row[s]
                        ),
                        None,
                    )
                    if duty:
                        duty.staff.append(staffdict[s])
                    else:
                        duties.append(
                            Duty(
                                row[headers[0]],
                                row[headers[1]],
                                row[s],
                                staffdict[s],
                            )
                        )
        return duties


"""
                    for existing_duty in duties:
                        if (
                            existing_duty.day == row[headers[0]]
                            and existing_duty.time == row[headers[1]]
                            and existing_duty.duty == row[s]
                        ):
                            existing_duty.staff.append(staff_dict[s])

                        duties.append(
                            Duty(
                                row[headers[0]],
                                row[headers[1]],
                                row[s],
                                staff_dict[s],
                            )
                        )
        return duties

        for row in reader:
            for s in staff:
                if row[s]:
                    if row[s].strip() not in junk_duties:
                        duties.append(Duty(s, row[headers[0]], row[headers[1]], row[s]))
        return duties
        """


def write_duties(duties):
    with open("duties.csv", mode="w") as outfile:
        writer = csv.writer(outfile)
        writer.writerow(["staff", "day", "time", "duty", "end"])
        for duty in duties:
            writer.writerow([duty.staff, duty.day, duty.time, duty.duty, duty.end])


def write_staff(staff_dict):
    with open("staff.csv", mode="w") as outfile:
        writer = csv.writer(outfile)
        writer.writerow(["number", "name"])
        for name, number in staff_dict.items():
            writer.writerow([number, name])


def get_headers(file):
    with open(file) as csvfile:
        reader = csv.DictReader(csvfile)
        print(next(reader, 1))


def combine_times(duties, times):
    for d in duties:
        d.end = times[times.index(d.time) + 1]
        for e in duties:
            if d.staff == e.staff and d.day == e.day and d.end == e.time:
                e.display()
                duties.remove(e)
                d.end = times[times.index(e.time) + 1]


def make_staff_dict(staff):
    staffdict = {}
    for index, name in enumerate(staff):
        staffdict[name] = index
    return staffdict


if __name__ == "__main__":
    f = "com.csv"

    staff = get_staff_names(f)

    staffdict = make_staff_dict(staff)

    duties = get_duties(f, staff, staffdict)

    print(len(duties), " duties")

    times = get_times(f)

    combine_times(duties, times)

    write_duties(duties)

    write_staff(staffdict)
