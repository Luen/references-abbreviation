import requests
import json
import csv

# abbreviated data from https://images.webofknowledge.com/images/help/WOS/A_abrvjt.html

# set up your Google Sheet:
# https://www.freecodecamp.org/news/cjn-google-sheets-as-json-endpoint/

# example google sheet
# https://spreadsheets.google.com/feeds/cells/1pYqQt055e4Kq9ysxH-qnHbsuHkj9e6_4vU4sIyPk2N0/1/public/full?alt=json
google_sheet_url = "https://spreadsheets.google.com/feeds/cells/1pYqQt055e4Kq9ysxH-qnHbsuHkj9e6_4vU4sIyPk2N0/1/public/full?alt=json"
response = requests.get(google_sheet_url).text
google_sheet = json.loads(response)

with open("abb.json") as json_file:
    abb = json.load(json_file)

with open("output.csv", mode="w") as ref_out:  # , encoding="UTF-8"
    ref_writer = csv.writer(
        ref_out,
        delimiter=",",
        quotechar='"',
        quoting=csv.QUOTE_MINIMAL,
        lineterminator="\n",
    )
    ref_writer.writerow(["Original", "Abbreviated"])  # Headers

    for entry in google_sheet["feed"]["entry"]:
        name = entry["gs$cell"]["$t"]

        flag = 0
        for a in abb:
            if a in name:
                flag = 1

                name_orignal = name
                name = name.lower()
                abbreviated = name.replace(a.lower(), abb[a].lower())

                if name == abbreviated:
                    try:
                        # ref_writer.writerow([name, abbreviated])
                        ref_writer.writerow([name, abb[a]])

                    except:
                        print("Charmap error on row", entry["gs$cell"]["row"])
                        try:
                            name = name.replace("‐", "-")
                            name = name.replace("ı́", "i")
                            name = name.replace("α", "a")
                            # abbreviated = abbreviated.replace("‐", "-")
                            # abbreviated = abbreviated.replace("ı́", "i")
                            # abbreviated = abbreviated.replace("α", "a")
                            print("- or ı́ or α")
                            ref_writer.writerow([name, abb[a]])
                        except:
                            ref_writer.writerow(["ERROR", "ERROR"])
                            print(name)
                else:
                    ref_writer.writerow(["", ""])

                break

        if not flag:
            """
            try:
                ref_writer.writerow([name, name])
            except:
                print("Charmap error on row", entry["gs$cell"]["row"])
                try:
                    # fix charmap error
                    name = name.replace("‐", "-")
                    name = name.replace("ı́", "i")
                    name = name.replace("α", "a")

                    print("- or ı́ or α")
                    ref_writer.writerow([name, name])
                except:
                    ref_writer.writerow(["ERROR", "ERROR"])
                    print(name)
            """
            ref_writer.writerow(["", ""])
