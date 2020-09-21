#!/usr/bin/env python
# test_person.py
"""Tests for `person` package."""
from dataclasses import dataclass

import pytest
from context import constants  # noqa
from context import helpers  # noqa
from context import person

# pylint: disable=redefined-outer-name


names = [
    ["Alfons-Reimund Horst Emil", "Boeselager"],
    ["Horatio R.", "Pimpernell"],
    ["Sven Jakob", "Große Brömer"],
]


def equivalent_names(n1, n2):
    fn = n2[0].split()[0]
    ln = n2[-1]
    try:
        mn_2 = n2[0].split()[2]
    except IndexError:
        mn_2 = None
    try:
        mn_1 = n2[0].split()[1]
    except IndexError:
        mn_1 = None

    return (
        (n1.first_name == fn)
        and (n1.middle_name_1 == mn_1)
        and (n1.middle_name_2 == mn_2)
        and (n1.last_name == ln)
    )


@pytest.mark.parametrize("n", names)
def test_person_Name_para(n):
    name = person.Name(*n)
    assert equivalent_names(name, n)


def test_person_Name(name_fixture):
    # pylint: disable=W0612, W0613

    name = person.Name("Alfons-Reimund Horst Emil", "Boeselager")
    assert name.first_name == "Alfons-Reimund"
    assert name.middle_name_1 == "Horst"
    assert name.middle_name_2 == "Emil"
    assert name.last_name == "Boeselager"


def test_person_Academic(academic_fixture):
    # pylint: disable=W0612, W0613

    academic = person.Academic(
        "Horatio",
        "Pimpernell",
        middle_name_1="R.",
        academic_title="Prof.Dr.   Dr",  # noqa
    )
    assert academic.first_name == "Horatio"
    assert academic.middle_name_1 == "R."
    assert academic.last_name == "Pimpernell"
    assert academic.academic_title == "Prof. Dr. Dr."

    academic = person.Academic(
        "Horatio Rübennase D.", "Pimpernell", academic_title="Prof.Dr.Dr"
    )
    assert academic.first_name == "Horatio"
    assert academic.middle_name_1 == "Rübennase"
    assert academic.middle_name_2 == "D."
    assert academic.last_name == "Pimpernell"
    assert academic.academic_title == "Prof. Dr. Dr."

    academic = person.Academic("Horatio", "Pimpernell", academic_title="B.A.")
    assert academic.academic_title == "B. A."


def test_person_Noble(noble_fixture):
    # pylint: disable=W0612, W0613

    noble = person.Noble("Sepp Theo", "Müller", peer_title="von und zu")

    assert noble.first_name == "Sepp"
    assert noble.middle_name_1 == "Theo"
    assert noble.last_name == "Müller"
    assert noble.peer_preposition == "von und zu"

    noble = person.Noble("Seppl", "Müller", peer_title="Junker van")

    assert noble.first_name == "Seppl"
    assert noble.last_name == "Müller"
    assert noble.peer_title == "Junker"
    assert noble.peer_preposition == "van"

    noble = person.Noble("Sven Oskar", "Müller", peer_title="Graf Eumel von")

    assert noble.first_name == "Sven"
    assert noble.middle_name_1 == "Oskar"
    assert noble.last_name == "Müller"
    assert noble.peer_title == "Graf"
    assert noble.peer_preposition == "von"


def test_person_Person(person_fixture):
    # pylint: disable=W0612, W0613

    pers = person.Person("Hugo", "Berserker", academic_title="MBA", born="2000")  # noqa

    assert pers.gender == "male"
    assert pers.academic_title == "MBA"
    assert pers.age == "20"

    pers = person.Person("Siggi Mathilde", "Berserker", born="1980-2010")

    assert pers.gender == "unknown"
    assert pers.middle_name_1 == "Mathilde"
    assert pers.born == "1980"
    assert pers.deceased == "2010"

    pers = person.Person("Sigrid", "Berserker", date_of_birth="10.1.1979")  # noqa

    assert pers.gender == "female"
    assert pers.born == "1979"


def test_person_Politician(politician_fixture):
    # pylint: disable=W0612, W0613

    pol_1 = person.Politician(
        "Regina",
        "Dinther",
        "CDU",
        peer_title="van",
        electoral_ward="Rhein-Sieg-Kreis IV",
    )

    assert pol_1.first_name == "Regina"
    assert pol_1.last_name == "Dinther"
    assert pol_1.gender == "female"
    assert pol_1.peer_preposition == "van"
    assert pol_1.party_name == "CDU"
    assert pol_1.ward_no == 28
    assert pol_1.voter_count == 110389

    pol_1.party_name = "fraktionslos"
    assert pol_1.party_name == "fraktionslos"
    assert pol_1.parties == [
        helpers.Party(
            party_name="CDU", party_entry="unknown", party_exit="unknown"
        )  # noqa
    ]  # noqa

    pol_2 = person.Politician(
        "Regina",
        "Dinther",
        "CDU",
        electoral_ward="Landesliste",
    )  # noqa

    assert pol_2.electoral_ward == "ew"

    pol_3 = person.Politician(
        "Heiner", "Wiekeiner", "Piraten", electoral_ward="Kreis Aachen I"
    )  # noqa

    assert pol_3.voter_count == 116389

    with pytest.raises(helpers.NotGermanParty):
        pol_4 = person.Politician("Thomas", "Gschwindner", "not_a_German_party")  # noqa

    pol_4 = person.Politician("Thomas", "Gschwindner", "FDP")
    pol_4.add_Party("FDP")

    assert pol_4.party_name == "FDP"
    assert pol_4.parties == [
        helpers.Party(
            party_name="FDP", party_entry="unknown", party_exit="unknown"
        )  # noqa
    ]  # noqa

    pol_4.add_Party("not_a_German_party")

    assert pol_4.party_name == "FDP"
    assert pol_4.parties == [
        helpers.Party(
            party_name="FDP", party_entry="unknown", party_exit="unknown"
        )  # noqa
    ]  # noqa

    pol_4.add_Party("AfD")

    assert pol_4.parties == [
        helpers.Party(
            party_name="FDP", party_entry="unknown", party_exit="unknown"
        ),  # noqa
        helpers.Party(
            party_name="AfD", party_entry="unknown", party_exit="unknown"
        ),  # noqa
    ]

    pol_4.add_Party("AfD", party_entry="2019")

    assert pol_4.party_entry == "2019"
    assert pol_4.parties == [
        helpers.Party(
            party_name="FDP", party_entry="unknown", party_exit="unknown"
        ),  # noqa
        helpers.Party(
            party_name="AfD", party_entry="2019", party_exit="unknown"
        ),  # noqa
    ]

    pol_4.add_Party("AfD", party_entry="2019", party_exit="2020")

    assert pol_4.party_exit == "2020"
    assert pol_4.parties == [
        helpers.Party(
            party_name="FDP", party_entry="unknown", party_exit="unknown"
        ),  # noqa
        helpers.Party(party_name="AfD", party_entry="2019", party_exit="2020"),
    ]

    pol_5 = person.Politician(
        "Heiner", "Wiekeiner", "Linke", electoral_ward="Köln I"
    )  # noqa

    assert pol_5.ward_no == 13
    assert pol_5.voter_count == 121721

    pol_6 = person.Politician("Heiner", "Wiekeiner", "Grüne")

    assert pol_6.electoral_ward == "ew"
    assert pol_6.ward_no is None
    assert pol_6.voter_count is None

    pol_6.change_ward("Essen III")

    assert pol_6.electoral_ward == "Essen III"
    assert pol_6.ward_no == 67
    assert pol_6.voter_count == 104181


def test_person_TooManyFirstNames(toomanyfirstnames_fixture):
    # pylint: disable=W0612, W0613

    name = person.Name
    with pytest.raises(helpers.TooManyFirstNames):
        name("Alfons-Reimund Horst Emil Pupsi", "Schulze")


def test_person_AttrDisplay(capsys, attrdisplay_fixture):
    # pylint: disable=W0612, W0613

    @dataclass
    class MockClass(helpers.AttrDisplay):
        a: str
        b: str
        c: str

    var_1 = "späm"
    var_2 = "ham"
    var_3 = "ew"

    mock_instance = MockClass(var_1, var_2, var_3)
    print(mock_instance)
    captured = capsys.readouterr()

    expected = """MockClass:\na=späm\nb=ham\n\n"""

    assert expected == captured.out
