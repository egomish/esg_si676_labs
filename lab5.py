import requests
import json


# 1. URL / URI Formation

url1 = "https://www.loc.gov/resource/cph.3f05183/"
url2 = "https://www.loc.gov/resource/fsa.8d24709/"
url3 = "https://www.loc.gov/resource/highsm.64003/"


# 2. LC Permalinks as URIs

perma1 = "https://lccn.loc.gov/98508155"
perma2 = "https://lccn.loc.gov/2017843202"
perma3 = "https://lccn.loc.gov/2020722343"


# 3. Retreive JSON data for items

params = {"fo": "json"}
respa = requests.get(url1, params=params)
respb = requests.get(url2, params=params)
respc = requests.get(url3, params=params)

with open("libposter.json", "w") as f:
    f.write(str(respa.content))

with open("readingroom.json", "w") as f:
    f.write(str(respb.content))

with open("bookmobile.json", "w") as f:
    f.write(str(respc.content))


# 4. Use a different parameter

query = "fourth estate"
url = "https://www.loc.gov/search"

params = {"q": query, "fo": "json"}
resp = requests.get(url, params=params)
js = json.loads(resp.content)
print(json.dumps(js, indent=2))
