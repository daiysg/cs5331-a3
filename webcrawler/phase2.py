#!/usr/bin/env python
import json
import copy


from urls import URLs


class phase2():
    arr = []
    changes = []

    urls_items = copy.deepcopy(URLs).items()

    for url, data in urls_items:
        name = data["name"]
        phase1_data = "output/" + name + "_phase1.json"

        # read phase 1 json
        phase_data = {}
        with open(phase1_data) as json_data:
            phase_data = json.load(json_data)

        for websites in phase_data:
            for params in websites:
                for get_post in params:
                    for items in get_post:
                        for value in arr:
                            if items not in value:
                                changes.append(phase_data[websites][params][get_post][items]["value"])
                            changes.append("CS5331" + phase_data[websites][params][get_post][items]["value"])
                            arr.append(changes)

        with open("output/" + name + '_phase2.json', 'w') as fp:
            json.dump(arr, fp, sort_keys=True, indent=4)
