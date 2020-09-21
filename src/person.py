#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
A set of dataclasses concerning roles of persons and their particulars.
"""
import datetime
import os
import sys
from dataclasses import dataclass, field
from typing import List, Optional, Tuple

from gender_guesser import detector as sex  # type: ignore

PACKAGE_PARENT = ".."
SCRIPT_DIR = os.path.dirname(
    os.path.realpath(os.path.join(os.getcwd(), os.path.expanduser(__file__)))
)  # isort:skip # noqa # pylint: disable=wrong-import-position
sys.path.append(
    os.path.normpath(os.path.join(SCRIPT_DIR, PACKAGE_PARENT))
)  # isort: skip # noqa # pylint: disable=wrong-import-position

from src.resources.constants import GERMAN_PARTIES  # type: ignore  # noqa
from src.resources.constants import PEER_PREPOSITIONS  # type: ignore # noqa
from src.resources.constants import PEERTITLES  # type: ignore # noqa
from src.resources.helpers import (  # type: ignore # noqa; type: ignore # noqa; type: ignore  # noqa; type: ignore # noqa
    AttrDisplay,
    NotInRange,
    Party,
    TooManyFirstNames,
)


@dataclass
class _Name_default:
    middle_name_1: Optional[str] = field(default=None)
    middle_name_2: Optional[str] = field(default=None)
    maiden_name: Optional[str] = field(default=None)
    divorcée: Optional[str] = field(default=None)


@dataclass
class _Name_base:
    first_name: str
    last_name: str


@dataclass
class Name(_Name_default, _Name_base, AttrDisplay):

    """
    The most basic part to describe a person.
    To add more middle names, dataclass _Name_default has to be given further
    middle_name attributes. Since this project currently focusses on German
    politicians, the limit of three given names is preserved.
    """

    def __post_init__(self):
        """
        In case a Name instance is initialized with all first names in one
        string, __post_init__ will take care of this and assign each first
        name its attribute. Also it will raise TooManyFirstNames if more than
        three first names are given.
        """
        first_names = self.first_name.split(" ")
        self.first_name = first_names[0]
        if len(first_names) == 2:
            self.middle_name_1 = first_names[1]
        elif len(first_names) == 3:
            self.middle_name_1 = first_names[1]
            self.middle_name_2 = first_names[-1]
        elif len(first_names) > 3:
            print(first_names)
            raise TooManyFirstNames("There are more than three first names!")


@dataclass
class _Peertitle_default:
    peer_title: Optional[str] = field(default=None)
    peer_preposition: Optional[str] = field(default=None)

    def nobility_title(self) -> None:
        if self.peer_title is not None:
            title = self.peer_title
            self.peer_title, self.peer_preposition = self.title_fix(title)

    def title_fix(self, title) -> Tuple[str, str]:
        titles = title.split(" ")
        title_tmp = ""
        preposition_tmp = ""
        for prep in titles:
            if prep.lower() in PEER_PREPOSITIONS:
                preposition_tmp = preposition_tmp + prep.lower() + " "
            elif prep in PEERTITLES:
                title_tmp = title_tmp + prep + " "
        peer_preposition = preposition_tmp.strip()
        peer_title = title_tmp.strip()

        return peer_title, peer_preposition


@dataclass
class Noble(_Peertitle_default, Name, AttrDisplay):
    def __post_init__(self):
        """Initialize names and titles."""
        Name.__post_init__(self)
        self.nobility_title()


@dataclass
class _Academic_title_default:
    academic_title: Optional[str] = field(default=None)

    def degree_title(self) -> None:
        if self.academic_title is not None:
            title = self.academic_title
            self.academic_title = self.title_repair(title)

    def title_repair(self, title) -> str:
        if ".D" in title:
            title = ". ".join(c for c in title.split("."))
        if ".A" in title:
            title = ". ".join(c for c in title.split("."))
        if title.endswith("Dr"):
            title = title[:-2] + "Dr."
        while "  " in title:
            title = title.replace("  ", " ")
        title = title.strip()

        return title


@dataclass
class Academic(_Academic_title_default, Name, AttrDisplay):
    def __post_init__(self):
        Name.__post_init__(self)
        self.degree_title()


@dataclass
class _Person_default:
    gender: str = field(default="unknown")
    born: str = field(default="unknown")
    date_of_birth: str = field(default="unknown")
    age: str = field(default="unknown")
    deceased: str = field(default="unknown")
    profession: str = field(default="unknown")


@dataclass
class Person(
    _Peertitle_default,
    _Academic_title_default,
    _Person_default,
    Name,
    AttrDisplay,  # noqa
):
    def __post_init__(self):
        Name.__post_init__(self)
        Academic.__post_init__(self)
        self.get_sex()
        self.get_year_of_birth()
        self.get_age()

    def get_sex(self) -> None:
        if "-" in self.first_name:
            first_name = self.first_name.split("-")[0]
        else:
            first_name = self.first_name
        d = sex.Detector()
        gender = d.get_gender(f"{first_name}")
        if "female" in gender:
            self.gender = "female"
        elif "male" in gender:
            self.gender = "male"

    def get_year_of_birth(self) -> None:
        if self.date_of_birth != "unknown":
            self.born = self.date_of_birth.split(".")[-1]

    def get_age(self) -> None:
        if self.born != "unknown":
            born = str(self.born)
            if len(born) > 4:
                self.deceased = born.strip()[5:]
                self.born = born[:4]
            else:
                today = datetime.date.today()
                self.age = str(int(today.year) - int(born.strip()))


@dataclass
class _Politician_default:
    electoral_ward: str = field(default="ew")
    ward_no: Optional[int] = field(default=None)
    voter_count: Optional[int] = field(default=None)
    minister: Optional[str] = field(default=None)
    offices: List[str] = field(default_factory=lambda: [])
    parties: List[str] = field(default_factory=lambda: [])

    def renamed_wards(self):
        wards = {
            "Kreis Aachen I": "Aachen III",
            "Hochsauerlandkreis II – Soest III": "Hochsauerlandkreis II",
            "Kreis Aachen II": "Aachen IV"
            if self.last_name in ["Wirtz", "Weidenhaupt"]
            else "Kreis Aachen I",
        }
        if self.electoral_ward in wards.keys():
            self.electoral_ward = wards[self.electoral_ward]

    def scrape_wiki_for_ward(self) -> None:
        import requests
        from bs4 import BeautifulSoup  # type: ignore

        URL_base = "https://de.wikipedia.org/wiki/Landtagswahlkreis_{}"
        URL = URL_base.format(self.electoral_ward)
        req = requests.get(URL)
        bsObj = BeautifulSoup(req.text, "lxml")
        table = bsObj.find(class_="infobox float-right toptextcells")
        self.scrape_wiki_table_for_ward(table)

    def scrape_wiki_table_for_ward(self, table) -> None:
        for td in table.find_all("td"):
            if "Wahlkreisnummer" in td.text:
                ward_no = td.find_next().text.strip()
                ward_no = ward_no.split(" ")[0]
                self.ward_no = int(ward_no)
            elif "Wahlberechtigte" in td.text:
                voter_count = td.find_next().text.strip()
                voter_count = self.fix_voter_count(voter_count)
                self.voter_count = int(voter_count)

    def fix_voter_count(self, voter_count):
        if voter_count[-1] == "]":
            voter_count = voter_count[:-3]
        if " " in voter_count:
            voter_count = "".join(voter_count.split(" "))
        else:
            voter_count = "".join(voter_count.split("."))
        return voter_count


@dataclass
class Politician(
    _Peertitle_default,
    _Academic_title_default,
    _Person_default,
    _Politician_default,
    _Name_default,
    Party,
    _Name_base,
    AttrDisplay,
):
    def __post_init__(self):
        Name.__post_init__(self)
        Academic.__post_init__(self)
        Noble.__post_init__(self)
        Party.__post_init__(self)
        Person.get_sex(self)
        Person.get_age(self)
        self.change_ward()
        if self.party_name in GERMAN_PARTIES:
            self.parties.append(
                Party(self.party_name, self.party_entry, self.party_exit)
            )
        if self.minister and self.minister not in self.offices:
            self.offices.append(self.minister)

    def add_Party(
        self, party_name, party_entry="unknown", party_exit="unknown"
    ):  # noqa
        if party_name in GERMAN_PARTIES:
            if self.party_is_in_parties(party_name, party_entry, party_exit):
                pass
            else:
                self.parties.append(Party(party_name, party_entry, party_exit))
                self.party_name = party_name
                self.party_entry = party_entry
                self.party_exit = party_exit

    def align_party_entries(
        self, party, party_name, party_entry, party_exit
    ) -> Party:  # noqa
        if party_entry != "unknown" and party.party_entry == "unknown":
            party.party_entry = party_entry
        if party_exit != "unknown" and party.party_exit == "unknown":
            party.party_exit = party_exit
        return party

    def party_is_in_parties(self, party_name, party_entry, party_exit):
        parties_tmp = self.parties[:]
        for party in parties_tmp:
            if party_name == party.party_name:
                party_updated = self.align_party_entries(
                    party, party_name, party_entry, party_exit
                )
                self.parties.remove(party)
                self.parties.append(party_updated)
                self.party_entry = party_updated.party_entry
                self.party_exit = party_updated.party_exit
                return True
        return False

    def change_ward(self, ward=None):
        if ward:
            self.electoral_ward = ward
        if self.electoral_ward not in ["ew", "Landesliste"]:
            self.renamed_wards()
            self.scrape_wiki_for_ward()
        else:
            self.electoral_ward = "ew"


if __name__ == "__main__":

    name = Name("Hans Hermann", "Werner")
    print(name)

    noble = Noble("Dagmara", "Bodelschwingh", peer_title="Gräfin von")
    print(noble)

    academic = Academic("Horst Heiner", "Wiekeiner", academic_title="Dr.")  # noqa
    print(academic)

    person_1 = Person("Sven", "Rübennase", academic_title="MBA", born="1990")  # noqa
    print(person_1)

    politician = Politician(
        "Bärbel",
        "Gutherz",
        "SPD",
        academic_title="Dr.",
        born="1980",
        electoral_ward="Köln I",
    )
    print(politician)
