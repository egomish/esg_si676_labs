import requests
import json
import csv
import os
import time

def get_content(key, delay=0):
    url = "https://www.loc.gov" + key
    try:
        print("Fetching '", url, "'...", sep="", end="")
        time.sleep(delay)
        resp = requests.get(url, params={"fo": "json"})
        print(resp.status_code)
        resp.raise_for_status()
        resp = resp.content
    except requests.exceptions.HTTPError as err:
        print("HTTP Error")
        print(err.args[0])
        # This isn't very clean error handling, but it IS very quick
        resp = None
    return resp


# Get the collection list.

url = "https://www.loc.gov/free-to-use/libraries"
resp = requests.get(url, params={"fo": "json"})
js = json.loads(resp.content)


# Dump the collection list to a file.

with open("ftu-libraries-set-info.json", "w") as f:
    f.write(json.dumps(js, indent=2))


# Extract just the items.

items = js["content"]["set"]["items"]


# Scrape data from the web and dump to separate files.

headers = ["image", "link", "title"]
with open("ftu-libraries-set-list.csv", "w") as csvfile:
    cout = csv.DictWriter(csvfile, fieldnames=headers, dialect="unix")
    print("Writing csv headers...", end="")
    cout.writeheader()
    print("done.")

    i = 0  # Oh boy I do not want to spell out the numbers while looping
    err_count = 0  # Ignore items with errors, but do keep track of them
    for elem in items:
        print("Writing '", elem["title"][:59], "'...", sep="")
        cout.writerow(elem)
        i += 1

        metadata = get_content(elem["link"])
        if not metadata:
            err_count += 1
        else:
            metadata = json.loads(metadata)
            fjson = os.path.join("item-metadata/", "item" + str(i) + ".json")
            with open(fjson, "w") as f:
                f.write(json.dumps(metadata, indent=2))

            image = get_content(elem["image"])
            if image:
                fimg = os.path.join("item-files/", "item" + str(i) + "-image.jpg")
                with open(fimg, "wb") as f:
                    f.write(image)

print("Done writing items. Errors: ", err_count, sep="")
