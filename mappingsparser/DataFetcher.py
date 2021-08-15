import os
from pathlib import Path

import requests as requests

SPIGOT_COMMIT_VERSIONS = {
    "1.17.1": "a4785704979a469daa2b7f6826c84e7fe886bb03",
    "1.17": "3cec511b16ffa31cb414997a14be313716882e12",
    "1.16.5": "656df5e622bba97efb4e858e8cd3ec428a0b2d71",
    "1.16.4": "501ea060743c7bba4436878207e4f1232298efce",
    "1.16.3": "b2025bdddde79aea004399ec5f3652a1bce56b7a",
    "1.16.2": "2589242ccafbffaeb0a36d16e9f59f97ab3411b7",
    "1.16.1": "be3371e67489b5a2293306e24420793106baadc1",
    # "1.16": "be3371e67489b5a2293306e24420793106baadc1",
    "1.15.2": "4a6af056693a191400cc4bc242823734c865c282",
    "1.15.1": "bcded15a2b4e78ea3c3e53843736ebac013471c2",
    "1.15": "f845c6ee8a6d41562c71dc218c7d5b7b9eeb03d6",
}

MINECRAFT_VERSIONS = {
    "1.17.1": "f6cae1c5c1255f68ba4834b16a0da6a09621fe13",
    "1.17": "84d80036e14bc5c7894a4fad9dd9f367d3000334",
    "1.16.5": "41285beda6d251d190f2bf33beadd4fee187df7a",
    "1.16.4": "d9ae0e8e28475254855430ff051daaa0dd041a08",
    "1.16.3": "e75ff1e729aec4a3ec6a94fe1ddd2f5a87a2fd00",
    "1.16.2": "40337a76c8486473e5990f7bb44b13bc08b69e7a",
    "1.16.1": "11120c39da4df293c4bd020896391fb9ddd6c2ba",
    # "1.16": "11120c39da4df293c4bd020896391fb9ddd6c2ba",
    "1.15.2": "8ccf85df7a3a1f1119352b21e9a2f6894f6c3f3a",
    "1.15.1": "3a818e8d2f85b4a1ca6a35bac57be84e81d907a7",
    "1.15": "25ff0e2b1104b8f06fe55b7675dd11b05c72f5f4",
}

SPIGOT_CLASSES = "https://hub.spigotmc.org/stash/projects/SPIGOT/repos/builddata/raw/mappings/bukkit-{}-cl.csrg?at={}"
SPIGOT_METHODS = "https://hub.spigotmc.org/stash/projects/SPIGOT/repos/builddata/raw/mappings/bukkit-{}-members.csrg?at={}"
MINECRAFT_MAPPINGS = "https://launcher.mojang.com/v1/objects/{}/server.txt"


def req(url):
    print("Fetching {} :)".format(url))
    return requests.get(url, allow_redirects=True)


def fetch(file, url):
    if Path(file).exists():
        print("Skipping {}".format(url))
        return
    open(file, 'wb').write(req(url).content)


def fetch_all():
    for x in SPIGOT_COMMIT_VERSIONS:
        fetch('sources/{}-class.s_'.format(x), SPIGOT_CLASSES.format(x, SPIGOT_COMMIT_VERSIONS[x]))
        fetch('sources/{}-method.s_'.format(x), SPIGOT_METHODS.format(x, SPIGOT_COMMIT_VERSIONS[x]))
    for x in MINECRAFT_VERSIONS:
        fetch('sources/{}-all.m_'.format(x), MINECRAFT_MAPPINGS.format(MINECRAFT_VERSIONS[x]))
