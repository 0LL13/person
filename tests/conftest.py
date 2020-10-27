# -*- coding: utf-8 -*-
# conftest.py
import logging
import time
from dataclasses import asdict

import pytest
from context import mop_role, mop_tinyDB

LOGGER = logging.getLogger(__name__)


@pytest.fixture(scope="function")
def toomanyfirstnames_fixture():
    LOGGER.info("Setting Up TooManyFirstNames Fixture ...")
    yield
    LOGGER.info("Tearing Down TooManyFirstNames Fixture ...")


@pytest.fixture(scope="function")
def name_fixture():
    LOGGER.info("Setting Up Names Fixture ...")
    yield
    LOGGER.info("Tearing Down Names Fixture ...")


@pytest.fixture(scope="function")
def academic_fixture():
    LOGGER.info("Setting Up Academic Fixture ...")
    yield
    LOGGER.info("Tearing Down Academic Fixture ...")


@pytest.fixture(scope="function")
def noble_fixture():
    LOGGER.info("Setting Up Noble Fixture ...")
    yield
    LOGGER.info("Tearing Down Noble Fixture ...")


@pytest.fixture(scope="function")
def person_fixture():
    LOGGER.info("Setting Up Person Fixture ...")
    yield
    LOGGER.info("Tearing Down Person Fixture ...")


@pytest.fixture(scope="function")
def politician_fixture():
    LOGGER.info("Setting Up Politician Fixture ...")
    yield
    LOGGER.info("Tearing Down Politician Fixture ...")


@pytest.fixture(scope="function")
def mop_fixture():
    LOGGER.info("Setting Up MoP Fixture ...")
    yield
    LOGGER.info("Tearing Down MoP Fixture ...")


@pytest.fixture(scope="function")
def notinrange_fixture():
    LOGGER.info("Setting Up NotInRange Fixture ...")
    yield
    LOGGER.info("Tearing Down NotInRange Fixture ...")


@pytest.fixture(scope="function")
def attrdisplay_fixture():
    LOGGER.info("Setting Up AttrDisplay Fixture ...")
    yield
    LOGGER.info("Tearing Down AttrDisplay Fixture ...")


@pytest.fixture(scope="function")
def first_names_fixture():
    LOGGER.info("Setting Up FirstNames Fixture ...")
    yield
    LOGGER.info("Tearing Down FirstNames Fixture ...")


@pytest.fixture(scope="function")
def standardize_name_fixture():
    LOGGER.info("Setting Up StandardizeName Fixture ...")
    yield
    LOGGER.info("Tearing Down StandardizeName Fixture ...")


@pytest.fixture(scope="function")
def mops_db_fixture(tmpdir):
    "Connect to DB before test, disconnect after."""
    db = mop_tinyDB.start_mops_db(str(tmpdir))
    db.delete_all()
    yield db
    mop_tinyDB.stop_mops_db(str(tmpdir))


@pytest.fixture(scope="session")
def mops_db_session(tmpdir_factory):
    "Connect to DB before session, disconnect after."""
    db = mop_tinyDB.start_mops_db(str(tmpdir_factory))
    db.delete_all()
    yield db
    mop_tinyDB.stop_mops_db(str(tmpdir_factory))


@pytest.fixture()
def three_mops_fixture():
    """Three members of parliament."""
    return[
        mop_role.MoP("14", "NRW", "SPD", "Hans", "Maier"),
        mop_role.MoP("15", "NRW", "Grüne", "Johanna", "Gsell"),
        mop_role.MoP("16", "NRW", "Piraten", "Klaus", "Störtebekker")]


@pytest.fixture(scope="function")
def db_with_3_mops(tmpdir, mops_db_fixture, three_mops_fixture):
    """Return DB with three mops."""
    db = mop_tinyDB.start_mops_db(str(tmpdir))
    for mop in three_mops_fixture:
        db.add_mop(asdict(mop))
    yield db
    mop_tinyDB.stop_mops_db(str(tmpdir))


@pytest.fixture(autouse=True)
def footer_function_scope():
    """Report test durations after each function."""
    start = time.time()
    yield
    stop = time.time()
    delta = stop - start
    print(f"\ntest duration: {delta:0.3}")
