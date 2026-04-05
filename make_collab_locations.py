import json
import time
import requests

API_KEY = "XXX"

institutes = [
  "The Johns Hopkins University",
  "University of Toronto",
  "Universidad de Cantabria",
  "Stockholm University",
  "University of Illinois Urbana - Champaign",
  "University of Texas at Austin",
  "Ben Gurion University",
  "Universidad de La Serena, La Serena, Chile",
  "Institut d'Astrophysique de Paris",
  "Pontificia Universidad Católica de Chile",
  "University of Pittsburgh",
  "European Space Astronomy Centre",
  "University of Texas at Austin",
  "University of Ljubljana",
  "Space Telescope Science Institute, Baltimore, MD, USA",
  "University of Copenhagen",
  "University of Nova Gorica",
  "University of Manchester",
  "University of California - Berkeley",
  "Canadian Institute for Theoretical Astrophysics",
  "University of Arizona",
  "Kapteyn Astronomical Institute, Groningen, Netherlands",
  "Instituto de Física de Cantabria",
  "NOIRLab, Tucson, AZ, USA",
  "University of Arizona",
  "Harvard University",
  "California Institute of Technology",
  "Chiba University",
  "Instituto de Astrofísica de Canarias",
  "Shawnee State University",
  "University of Tokyo",
  "University of Tsukuba",
  "National Astronomical Observatory of Japan",
  "Pekin University",
  "Instituto de Astrofísica de Andalucía",
  "Institut d'Astrophysique de Paris",
  "Rochester Institute of Technology",
  "University of Washington",
  "Chalmers University",
  "Universidad de Chile",
  "Swinburne University of Technology",
  "Massachusetts Institute of Technology",
  "Federal University of Rio de Janeiro",
  "Technical University of Denmark",
  "Tufts University",
  "Institute of Science and Technology Austria",
  "Saint Mary's University",
  "INAF - Bologna",
  "York University",
  "Massachusetts Institute of Technology",
  "Arizona State University",
  "Texas A&M University",
  "University of Pittsburgh",
  "Centre de Recherche Astrophysique de Lyon",
  "University of Maryland",
  "NASA Goddard Space Flight Center",
  "Tufts University",
  "University of Geneva",
  "Università di Roma La Sapienza",
  "University of California – Los Angeles",
  "Harvard University",
  "INAF - Bologna",
  "Massachusetts Institute of Technology",
  "University of Massachusetts Amherst",
  "NRC Herzberg Institute of Astrophysics, Victoria, BC, Canada",
  "Uppsala Astronomical Observatory",
  "INAF - Roma"
]

def geocode(address):
    url = "https://maps.googleapis.com/maps/api/geocode/json"
    params = {
        "address": address,
        "key": API_KEY
    }
    r = requests.get(url, params=params, timeout=30)
    r.raise_for_status()
    data = r.json()

    if data["status"] != "OK" or not data["results"]:
        print(f"Failed: {address} -> {data['status']}")
        return None

    loc = data["results"][0]["geometry"]["location"]
    return {
        "name": address,
        "lat": loc["lat"],
        "lng": loc["lng"]
    }

results = []
seen = set()

for inst in institutes:
    if inst in seen:
        continue
    seen.add(inst)

    item = geocode(inst)
    if item is not None:
        results.append(item)

    time.sleep(0.1)

with open("collaborator_locations.json", "w", encoding="utf-8") as f:
    json.dump(results, f, ensure_ascii=False, indent=2)

print(f"Saved {len(results)} locations.")