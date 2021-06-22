from collections import namedtuple

Version = namedtuple("Version", ["name", "thesaurus_file", "substance_file", "description"])
THESAURUS_VERSIONS = [
    Version("092019", "thesaurus_092019.json", "index_substances092019.json", "Version de septembre 2019")
]


def get_thesaurus_representation(version: THESAURUS_VERSIONS):
    return {
        "thesaurus_version": version.name,
        "description": version.description
    }
