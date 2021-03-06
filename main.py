import json
import requests
import time
import sys
from tabulate import tabulate

api_url = "https://haveibeenpwned.com/api/v2/breachedaccount/%s%s"
unverified = "?includeUnverified=true"


def check(email):
    req = api_url % (email, unverified)
    r = requests.get(req)
    code = r.status_code
    return [code]


def breach(email):
    req = api_url % (email, unverified)
    r = requests.get(req)
    pwneds = r.json()
    result = str()
    l = list()
    for pwned in pwneds:
        l.append(pwned["Title"])
    s = ", ";
    result = s.join(l)
    return [result]


with open("liste.json", "r") as read_file:
    datas = json.load(read_file)

l = list()
nb = 0

sys.stdout.write("Scan in progress...")
sys.stdout.flush()

for data in datas:
    if data["mail"]:
        try:
            mail = data["mail"]
            rep = check(mail)
            if rep == [200]:
                nb += 1
                pwneds = breach(mail)
                sys.stdout.write("Found %s compromised mail adress..." % nb)
                sys.stdout.flush()
                l.append([mail, pwneds])
            if rep == [429]:
                sys.stdout.write("Too many requests\n")
                break
            time.sleep(2)
        except KeyError:
            mail = 1
l.sort()
sys.stdout.write("\n")
sys.stdout.write(tabulate(l, headers=["Adress", "Breach"], tablefmt="rst"))
sys.stdout.write("\n")
