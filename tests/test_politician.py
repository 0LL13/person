#!/usr/bin/env python
# -*- coding: utf-8 -*-
# test_politician.py
"""Tests for `politician_role` module."""
import pytest
from context import helpers  # noqa
from context import politician_role  # noqa

# pylint: disable=redefined-outer-name


def test_politician_role(politician_fixture):
    # pylint: disable=W0612, W0613

    pol_1 = politician_role.Politician(
        "CDU",
        "Regina",
        "Dinther",
        peer_title="van",
    )

    assert pol_1.first_name == "Regina"  # nosec
    assert pol_1.last_name == "Dinther"  # nosec
    assert pol_1.gender == "female"  # nosec
    assert pol_1.peer_preposition == "van"  # nosec
    assert pol_1.party_name == "CDU"  # nosec

    pol_1.party_name = "fraktionslos"
    assert pol_1.party_name == "fraktionslos"  # nosec
    assert pol_1.parties == [  # nosec
        helpers.Party(
            party_name="CDU", party_entry="unknown", party_exit="unknown"
        )  # noqa  # nosec
    ]  # noqa  # nosec

    with pytest.raises(helpers.NotGermanParty):
        pol_4 = politician_role.Politician(
            "Thomas", "Gschwindner", "not_a_German_party"
        )  # noqa

    pol_4 = politician_role.Politician("FDP", "Thomas", "Gschwindner")
    pol_4.add_Party("FDP")

    assert pol_4.party_name == "FDP"  # nosec
    assert pol_4.parties == [  # nosec
        helpers.Party(
            party_name="FDP", party_entry="unknown", party_exit="unknown"
        )  # noqa  # nosec
    ]  # noqa  # nosec

    pol_4.add_Party("not_a_German_party")

    assert pol_4.party_name == "FDP"  # nosec
    assert pol_4.parties == [  # nosec
        helpers.Party(
            party_name="FDP", party_entry="unknown", party_exit="unknown"
        )  # noqa  # nosec
    ]  # noqa  # nosec

    pol_4.add_Party("AfD")

    assert pol_4.parties == [  # nosec
        helpers.Party(
            party_name="FDP", party_entry="unknown", party_exit="unknown"
        ),  # noqa  # nosec
        helpers.Party(
            party_name="AfD", party_entry="unknown", party_exit="unknown"
        ),  # noqa  # nosec
    ]

    pol_4.add_Party("AfD", party_entry="2019")

    assert pol_4.party_entry == "2019"  # nosec
    assert pol_4.parties == [  # nosec
        helpers.Party(
            party_name="FDP", party_entry="unknown", party_exit="unknown"
        ),  # noqa  # nosec
        helpers.Party(
            party_name="AfD", party_entry="2019", party_exit="unknown"
        ),  # noqa  # nosec
    ]

    pol_4.add_Party("AfD", party_entry="2019", party_exit="2020")

    assert pol_4.party_exit == "2020"  # nosec
    assert pol_4.parties == [  # nosec
        helpers.Party(
            party_name="FDP", party_entry="unknown", party_exit="unknown"
        ),  # noqa  # nosec
        helpers.Party(party_name="AfD", party_entry="2019", party_exit="2020"),
    ]
