# This project was more like 6 small projects and
# everytime you had to do something else, that's why
# a lot of the code is commented out and not well-structured.
# I recommend to just ignore this mess!

import json
import re
import itertools


BUS_DATA_FIELDS = ["bus_id",
                   "stop_id",
                   "stop_name",
                   "next_stop",
                   "stop_type",
                   "a_time"]


STREET_NAME_SUFFIXES = ["Road",
                        "Avenue",
                        "Boulevard",
                        "Street"]

VALID_STREET_NAMES = re.compile(r"""^
                                ([A-Z][a-z]+[ ])+
                                (Road|Avenue|Boulevard|Street)
                                $""", flags=re.VERBOSE)


def check_field(bus_data: dict, field: str) -> bool:
    if field == BUS_DATA_FIELDS[0]:
        if not bus_data["bus_id"] in [128, 256, 512, 1024]:
            return False

    if field == BUS_DATA_FIELDS[1]:
        if not isinstance(bus_data["stop_id"], int):
            return False

    if field == BUS_DATA_FIELDS[2]:
        if not isinstance(bus_data["stop_name"], str):
            return False
        if bus_data["stop_name"] == "":
            return False
        name = bus_data["stop_name"]
        if not re.match(VALID_STREET_NAMES, name):
            return False

    if field == BUS_DATA_FIELDS[3]:
        if not isinstance(bus_data["next_stop"], int):
            return False

    if field == BUS_DATA_FIELDS[4]:
        if not isinstance(bus_data["stop_type"], str):
            return False
        if len(bus_data["stop_type"]) > 1:
            return False
        if len(bus_data["stop_type"]) != 0:
            if bus_data["stop_type"] not in ["S", "O", "F"]:
                return False

    if field == BUS_DATA_FIELDS[5]:
        if not isinstance(bus_data["a_time"], str):
            return False
        if not check_time_format(bus_data["a_time"]):
            return False
    
    return True


def check_time_format(time: str):
    if not re.match(r"^[0-9]{2}:[0-9]{2}$", time):
        return False
    hours, minutes = time.split(":")
    if not 0 <= int(hours) <= 23:
        return False
    if not 0 <= int(minutes) <= 59:
        return False
    return True


def check_line_stops(data: dict) -> None:
    stops = {}
    line_stops = {}
    starts = set()
    finishes = set()
    transfers = set()
    for bus_data in data:

        stops.setdefault(bus_data["stop_name"], None)
        if not stops[bus_data["stop_name"]]:
            stops[bus_data["stop_name"]] = bus_data["stop_id"]
        else:
            transfers.add(bus_data["stop_name"])

        line_stops.setdefault(bus_data["bus_id"], {"start": None, "end": None, "others": []})
        if bus_data["stop_type"] == "S" and not line_stops[bus_data["bus_id"]]["start"]:
            line_stops[bus_data["bus_id"]]["start"] = bus_data["stop_name"]
        elif bus_data["stop_type"] == "S" and line_stops[bus_data["bus_id"]]["start"]:
            print(f"There is no start or end stop for the line: {bus_data['bus_id']}.")
            break
        if bus_data["stop_type"] == "F" and not line_stops[bus_data["bus_id"]]["end"]:
            line_stops[bus_data["bus_id"]]["end"] = bus_data["stop_name"]
        elif bus_data["stop_type"] == "F" and line_stops[bus_data["bus_id"]]["end"]:
            print(f"There is no start or end stop for the line: {bus_data['bus_id']}.")
            break
        if bus_data["stop_type"] in ["", "O"]:
            line_stops[bus_data["bus_id"]]["others"].append(bus_data['stop_name'])
    else:
        for line in list(line_stops.keys()):
            if not line_stops[line]["start"] or not line_stops[line]["end"]:
                print(f"There is no start or end stop for the line: {line}.")
                break
            else:
                starts.add(line_stops[line]["start"])
                finishes.add(line_stops[line]["end"])

        else:
            print(f"Start stops: {len(starts)} {sorted(list(starts))}")
            print(f"Transfer stops: {len(transfers)} {sorted(list(transfers))}")
            print(f"Finish stops: {len(finishes)} {sorted(list(finishes))}")


def check_arrival_times(data: dict) -> None:
    times_dict = {}
    wrong_times = {}
    for bus_data in data:
        if bus_data["bus_id"] in list(wrong_times.keys()):
            continue
        times_dict.setdefault(bus_data["bus_id"], None)
        if not times_dict[bus_data["bus_id"]]:
            times_dict[bus_data["bus_id"]] = bus_data["a_time"]
        else:
            hours, minutes = bus_data["a_time"].split(":")
            prev_hours, prev_minutes = times_dict[bus_data["bus_id"]].split(":")
            if int(hours) > int(prev_hours):
                times_dict[bus_data["bus_id"]] = bus_data["a_time"]
            elif int(hours) == int(prev_hours):
                if int(minutes) > int(prev_minutes):
                    times_dict[bus_data["bus_id"]] = bus_data["a_time"]
                else:
                    wrong_times[bus_data["bus_id"]] = bus_data["stop_name"]
            else:
                wrong_times[bus_data["bus_id"]] = bus_data["stop_name"]
    print("Arrival time test:")
    if not len(wrong_times):
        print("OK")
    for key in list(wrong_times.keys()):
        print(f"bus_id line {key}: wrong time on station {wrong_times[key]}")


def check_on_demand(data: dict) -> None:
    stops = {}
    wrong_stops = []
    for bus_data in data:
        stops.setdefault(bus_data["stop_name"], None)
        if bus_data["stop_type"] == "O":
            if not stops[bus_data["stop_name"]]:
                stops[bus_data["stop_name"]] = "O"
            else:
                wrong_stops.append(bus_data["stop_name"])
        else:
            if not stops[bus_data["stop_name"]]:
                stops[bus_data["stop_name"]] = bus_data["stop_type"]
            elif stops[bus_data["stop_name"]] == "O":
                wrong_stops.append(bus_data["stop_name"])
    if not len(wrong_stops):
        print("OK")
    else:
        print(f"Wrong stop type: {sorted(wrong_stops)}")


def main():
    fields_to_check = [0]
    data = json.loads(input())
    errors_per_field = []
    # for field in BUS_DATA_FIELDS:
    #     errors_found = 0
    #     for bus_data in data:
    #         if not check_field(bus_data, field):
    #             errors_found += 1
    #     errors_per_field.append(errors_found)
    # print(f"Type and required field validation: {sum(errors_per_field)} errors")
    # for i, count in enumerate(errors_per_field):
    #     if i in fields_to_check:
    #         print(f"{BUS_DATA_FIELDS[i]}: {count}")

    # stops_per_route = {}
    # for bus_data in data:
    #     stops_per_route.setdefault(bus_data["bus_id"], []).append(bus_data["stop_id"])
    # for key in list(stops_per_route.keys()):
    #     print(f"\"bus_id\": {key}, stops: {len(set(stops_per_route[key]))}")

    # [{"bus_id" : 128, "stop_id" : 1, "stop_name" : "Prospekt Avenue", "next_stop" : 3, "stop_type" : "S", "a_time" : "08:12"}, {"bus_id" : 128, "stop_id" : 3, "stop_name" : "Elm Street", "next_stop" : 5, "stop_type" : "", "a_time" : "08:19"}, {"bus_id" : 128, "stop_id" : 5, "stop_name" : "Fifth Avenue", "next_stop" : 7, "stop_type" : "O", "a_time" : "08:25"}, {"bus_id" : 128, "stop_id" : 7, "stop_name" : "Sesame Street", "next_stop" : 0, "stop_type" : "F", "a_time" : "08:37"}, {"bus_id" : 512, "stop_id" : 4, "stop_name" : "Bourbon Street", "next_stop" : 6, "stop_type" : "", "a_time" : "08:13"}, {"bus_id" : 512, "stop_id" : 6, "stop_name" : "Sunset Boulevard", "next_stop" : 0, "stop_type" : "F", "a_time" : "08:16"}]
    # check_line_stops(data)
    # check_arrival_times(data)
    check_on_demand(data)


if __name__ == "__main__":
    main()
