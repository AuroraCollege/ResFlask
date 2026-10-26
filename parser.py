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
            # Skip continuation rows (extra lines of a cell above)
            if row["Time"].strip():
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
        "Welcome to Res",
    ]

    with open(file) as csvfile:
        reader = csv.DictReader(csvfile)
        headers = reader.fieldnames
        duties = []
        for row in reader:
            # Skip continuation rows (extra lines of a cell above)
            if not row[headers[0]].strip():
                continue
            for s in staff:
                if row[s].strip() not in junk_duties:
                    duty = next(
                        (
                            d
                            for d in duties
                            if d.day == row[headers[0]]
                            and d.time == row[headers[1]]
                            and d.duty.lower() == row[s].lower()
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
            if (
                d.staff == e.staff
                and d.day == e.day
                and d.end == e.time
                and d.duty == e.duty
            ):
                # e.display()
                duties.remove(e)
                d.end = times[times.index(e.time) + 1]


# Year group column in yeargroups.csv -> column header in com.csv
GROUPS = {
    "Y5": "Y5 (145) Narrabeen",
    "Y7": "Year 7 (107) Narrabeen",
    "Y8": "Year 8 (128) Collaroy",
    "Y9": "Year 9 (100) Collaroy",
    "Y10": "Year 10 (62) Collaroy",
}


def get_groups(file):
    with open(file) as csvfile:
        reader = csv.DictReader(csvfile)
        headers = reader.fieldnames
        # Match headers ignoring stray whitespace/newlines
        columns = {h.strip(): h for h in headers}
        rows = []
        for row in reader:
            day = row[headers[0]]
            # Skip the "Activity" header row and continuation rows
            if not day.strip() or day == "Day":
                continue
            group_row = {"Day": day, "Time": row[headers[1]], "End": None}
            for group, column in GROUPS.items():
                group_row[group] = row[columns[column]].strip()
            rows.append(group_row)
        return rows


def combine_group_times(rows, times):
    combined = []
    for row in rows:
        row["End"] = times[times.index(row["Time"]) + 1]
        prev = combined[-1] if combined else None
        if (
            prev
            and prev["Day"] == row["Day"]
            and prev["End"] == row["Time"]
            and all(prev[g] == row[g] for g in GROUPS)
        ):
            prev["End"] = row["End"]
        else:
            combined.append(row)
    return combined


def write_groups(rows):
    with open("yeargroups.csv", mode="w") as outfile:
        writer = csv.DictWriter(outfile, ["Day", "Time", "End", *GROUPS])
        writer.writeheader()
        writer.writerows(rows)


def make_staff_dict(staff):
    staffdict = {}
    for index, name in enumerate(staff):
        staffdict[name] = index
    return staffdict


def parse(f="com.csv"):
    staff = get_staff_names(f)

    staffdict = make_staff_dict(staff)

    duties = get_duties(f, staff, staffdict)

    print(len(duties), " duties")

    times = get_times(f)

    combine_times(duties, times)

    write_duties(duties)

    write_staff(staffdict)

    groups = combine_group_times(get_groups(f), times)

    write_groups(groups)


if __name__ == "__main__":
    parse()
