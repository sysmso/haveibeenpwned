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

mail_user = {}
id = 0
l=list()

for data in datas:
    sys.stdout.write("Scan in progress...")
    if data["mail"]:
        try:
            mail = data["mail"]
            rep = check(mail)
            if rep == [200]:
                pwneds = breach(mail)
                l.append([mail, pwneds])
            if rep == [429]:
                sys.stdout.write("Too many requests\n")
                break
            time.sleep(2)
        except KeyError:
            mail = 1
l.sort()
sys.stdout.write(tabulate(l, headers=["Adresse", "Breach"], tablefmt="rst"))