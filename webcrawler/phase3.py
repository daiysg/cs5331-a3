#!/usr/bin/env python
import os
import json
import copy
import itertools


from urls import URLs


# exploiitable key/value
exploitable_values = ["del"]
exploitable_keys = ["pass1", "pass", "pass2", "password", "currency", "currency_code"]




def phase3(outputpath):

    #log
    print "########## PHASE 3 ##########"
    print "##  Generate all injection points. ##"

    urls = copy.deepcopy(URLs).items()

    for url, data in urls:
        name = data["name"]
        phase2_data = outputpath + name + "_phase2.json"

        # read result from phase2
        if os.path.isfile(phase2_data):
            with open(phase2_data) as json_data:
                original_data = json.load(json_data)

            # delete old phase 3 json
            phase3_json_file = outputpath + name + '_phase3.json'
            if os.path.isfile(phase3_json_file):
                os.remove(phase3_json_file)
            else:
                open(phase3_json_file, "w")

            print "Phase 3: generating " + name + "_phase.json."
            # collate phase data
            execudephase3(original_data, phase3_json_file)
            print "Phase 3 Finish: generating " + name + "_phase.json."

    print "##  Phase 3 Finished. ##"


def execudephase3(json_data, path):


    urls = json_data.keys()
    for url in urls:
        forms = json_data[url]
        print "Form Info: " + str(len(forms))

        # trim form with first 100:
        filter_forms = forms[:100] if len(forms) > 100 else forms

        for form in filter_forms:
            # find POST pairs
            post_param_names = sorted(form["params"]["POST"])
            post_pairs = {}
            for post_param_name in post_param_names:
                values = form["params"]["POST"][post_param_name]["value"]
                # print "Values for forms: " + values
                if len(values) > 100:
                    post_pairs[post_param_name] = post_pairs
                else:
                    post_pairs[post_param_name] = values
            post_combinations = [dict(zip(post_param_names, prod)) for prod in
                                 itertools.product(*(post_pairs[param_name] for param_name in post_param_names))]

            # find GET pairs
            get_param_names = sorted(form["params"]["GET"])
            get_pairs = {}
            for get_param_name in get_param_names:
                values = form["params"]["GET"][get_param_name]["value"]
                if len(values) > 100:
                    get_pairs[get_param_name] = values[:100]
                else:
                    get_pairs[get_param_name] = values
            get_combinations = [dict(zip(get_param_names, prod)) for prod in
                                itertools.product(*(get_pairs[param_name] for param_name in get_param_names))]

            original_url = url
            print "Generate result for phase3"
            for get_comb in get_combinations:
                for post_comb in post_combinations:
                    if any(key in get_comb for key in ["tokens"]):
                        continue
                    if any(key in post_comb for key in ["tokens"]):
                        continue

                    arr = []

                    # POST is empty
                    if not post_comb:
                        if not get_comb:
                            continue
                        else:
                            # check for GET exploit
                            if check_exploit(get_comb):
                                new_url = append_get(original_url, get_comb)
                                generate_exploit(new_url, arr, path)
                    # POST not empty
                    else:
                        # if GET is empty
                        if not get_comb:
                            if check_exploit(post_comb):
                                arr.append({"params": post_comb, "method": "POST"})
                                generate_exploit(url, arr, path)
                        else:
                            if check_exploit(post_comb) or check_exploit(get_comb):
                                new_url = append_get(original_url, get_comb)
                                arr.append({"params": post_comb, "method": "POST"})
                                generate_exploit(new_url, arr, path)


def append_get(url, value_comb):
    strquery = []
    sort = iter(sorted(value_comb.iteritems()))
    for k, v in sort:
        strquery.append(k + '=' + v)

    exploit_url = url + '?' + '&'.join(strquery)
    return exploit_url


def check_exploit(value_comb):
    if value_comb:
        if any(value in value_comb.values() for value in exploitable_values):
            return 1
        if any(key in value_comb for key in exploitable_keys):
            return 1
    return 0


def generate_exploit(url, data_array, path):
    json_data = {}
    # if the output file exists, read the content of this json file
    if os.path.isfile(path):
        with open(path, "r") as json_file:
            if os.stat(path).st_size > 0:
                json_data = json.load(json_file)

    if url in json_data:
        # if url already exists, append the method and parameters
        json_data[url].append(data_array)
    else:
        # if ulr doesn't exist, append the url, method and parameters
        json_data[str(url)] = [data_array]

    # create json file
    with open(path, "w") as outfile:
        json.dump(json_data, outfile, indent=4)


if __name__ == "__main__":
    phase3("output/")
