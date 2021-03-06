Overview
========

:deployment:
    .. image:: https://img.shields.io/pypi/v/personroles
        :target: https://pypi.org/project/personroles/

    .. image:: https://img.shields.io/pypi/pyversions/personroles.svg
        :target: https://www.python.org/

    .. image:: https://img.shields.io/pypi/implementation/personroles.svg
        :target: https://realpython.com/cpython-source-code-guide/ 

:test/coverage:
    .. image:: https://app.codacy.com/project/badge/Grade/5a29d30f3ec7470cb17085a29a4c6a8f
        :target: https://www.codacy.com/manual/0LL13/person?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=0LL13/person&amp;utm_campaign=Badge_Grade)  

    .. image:: https://codecov.io/gh/0LL13/person/branch/master/graph/badge.svg
        :target: https://codecov.io/gh/0LL13/person

    .. image:: https://api.codeclimate.com/v1/badges/714a256d1edf47898a22/maintainability
       :target: https://codeclimate.com/github/0LL13/person/maintainability

    .. image:: https://coveralls.io/repos/github/0LL13/person/badge.svg?branch=master
        :target: https://coveralls.io/github/0LL13/person?branch=master

    .. image:: https://scrutinizer-ci.com/g/0LL13/person/badges/quality-score.png?s=0242cf58f51463f90ec17ee3d1708c07beaddd6624a07e9d228a2e337aa56388
        :target: https://scrutinizer-ci.com/g/0LL13/person/

:build status:
    .. image:: https://travis-ci.org/0LL13/person.svg?branch=master
        :target: https://travis-ci.org/github/0LL13/person

    .. image:: https://pyup.io/repos/github/0LL13/person/shield.svg
        :target: https://pyup.io/repos/github/0LL13/person/
        :alt: Updates

    .. image:: https://img.shields.io/github/issues-pr/0LL13/person
        :target: https://github.com/0LL13/person/pulls

    .. image:: https://img.shields.io/badge/security-bandit-yellow.svg
        :target: https://github.com/PyCQA/bandit

:docs:
    .. image:: https://readthedocs.org/projects/personroles/badge/?version=latest
        :target: https://person.readthedocs.io/en/latest/?badge=latest

    .. image:: https://img.shields.io/github/license/0LL13/person
        :target: https://opensource.org/licenses/MIT

A set of dataclasses concerning roles (academic, politician, ...)  of persons and their particulars

Features
--------

Currently names of this structure are supported::

    Names:                       first_name middle_name_1 middle_name_2 last_name/s
    Names with academic title:   academic_title/s first_name ... last_name/s
    Names with peer title:       peer_title/s first_name ... last_name/s
    Names with peer preposition: first_name ... peer_preposition last_name/s
    Names with all titles:       academic/peer_title first_name ... peer_preposition last_name/s

These roles have been sketched::

    Academic - academic_title
    Person - gender, born, age, deceased
    Noble - peer_title, peer_preposition
    Politician - minister, offices, party, parties
    MoP - legislature, state, electoral_ward, ward_no, voter_count, parl_pres, parl_vicePres

Usage
-----
::

    from personroles import person

    tom = person.Academic("Thomas H.", "Smith", academic_title="MBA")
    print(tom)

    Academic:
    academic_title=MBA
    first_name=Thomas
    last_name=Smith
    middle_name_1=H.

::

    from personroles import mop_role

    bob = mop_role.MoP("14", "NRW", "SPD", "Bob R.", "Smith", academic_title="Dr.", electoral_ward="Köln I")
    print(bob)

    MoP:
    academic_title=Dr.
    electoral_ward=Köln I
    first_name=Bob
    gender=male
    last_name=Smith
    legislature=14
    membership={'14'}
    middle_name_1=R.
    parties=[Party(party_name='SPD', party_entry='unknown', party_exit='unknown')]
    party_name=SPD
    state=NRW
    voter_count=121721
    ward_no=13

Credits
-------

This package was started with Cookiecutter_ and the `audreyr/cookiecutter-pypackage`_ project template.
Also the `project setup`_ by Martin Heinz was very helpful.
I felt the changes were necessary to keep the files containing the roles small.

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`audreyr/cookiecutter-pypackage`: https://github.com/audreyr/cookiecutter-pypackage
.. _`project setup`: https://martinheinz.dev/blog/14

Installation
------------
::

    pip install personroles

or 

::

    pipenv install personroles

Contribute
----------

| **Please fork first and use for your own ends.**
| This package is structured like this:

::

    personroles
    ├── mop_role.py
    ├── person.py
    ├── politician_role.py
    ├── your-contribution_role.py
    ├── resources
    │   ├── constants.py
    │   └── helpers.py
    └── tests
        ├── test_mop.py
        ├── test_person.py
        ├── test_politician.py
        └── test_your-contribution.py

Because of its modular structure, all you need to do is add another role as
"your-contribution_role.py", and another test as "test_your-contribution.py".
Use current \*_role modules as blueprint and delete if not needed.

Support
-------

Fork and improve.

Planned
-------

Fork and repeat with different roles.

Warranty
--------

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE, TITLE AND NON-INFRINGEMENT. IN NO EVENT SHALL
THE COPYRIGHT HOLDERS OR ANYONE DISTRIBUTING THE SOFTWARE BE LIABLE FOR ANY
DAMAGES OR OTHER LIABILITY, WHETHER IN CONTRACT, TORT OR OTHERWISE, ARISING
FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS
IN THE SOFTWARE.

License
-------

MIT License

Copyright (c) 2020 Oliver Stapel
