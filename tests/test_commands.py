# coding: utf8
from __future__ import unicode_literals, print_function, division
from collections import namedtuple

import pytest
from clldutils.path import copy, Path
from clldutils.misc import nfilter
from clldutils.clilib import ParserError

from pyconcepticon.util import read_all
from pyconcepticon import __main__


def test_link(mocker, fixturedir, tmpdir, capsys):
    from pyconcepticon.commands import link

    with pytest.raises(ParserError):
        link(mocker.Mock(args=['.'], data=None))

    def nattr(p, attr):
        return len(nfilter([getattr(i, attr, None) for i in read_all(str(p))]))

    test = tmpdir.join('test.tsv')
    copy(fixturedir.joinpath('conceptlist.tsv'), str(test))
    assert nattr(test, 'CONCEPTICON_GLOSS') == 0
    link(mocker.Mock(args=[str(test)], data=None))
    assert nattr(test, 'CONCEPTICON_GLOSS') == 1

    copy(fixturedir.joinpath('conceptlist2.tsv'), str(test))
    link(mocker.Mock(args=[str(test)], data=None))
    out, err = capsys.readouterr()
    assert 'unknown CONCEPTICON_GLOSS' in out
    assert 'mismatch' in out


def test_readme(tmpdir):
    from pyconcepticon.commands import readme

    readme(Path(str(tmpdir)), ['a', 'b'])
    assert tmpdir.join('README.md').ensure()


def test_stats(mocker):
    from pyconcepticon.commands import stats

    readme = mocker.Mock()
    mocker.patch('pyconcepticon.commands.readme', readme)
    stats(mocker.MagicMock(data=None))
    assert readme.call_count == 3


def test_attributes(mocker, capsys):
    from pyconcepticon.commands import attributes

    attributes(mocker.MagicMock(data=None))
    out, err = capsys.readouterr()
    assert 'Occurrences' in out


def test_union(capsys):
    from pyconcepticon.commands import union
    Args = namedtuple('Args', ['data', 'args'])

    union(Args(data='', args=['Swadesh-1955-100', 'Swadesh-1952-200']))
    out, err = capsys.readouterr()
    assert 208 == len(out.split('\n'))

    union(Args(data='', args=['Swadesh-1952-200', 'Matisoff-1978-200']))
    out, err = capsys.readouterr()
    assert 301 == len(out.split('\n'))


def test_intersection(capsys):
    from pyconcepticon.commands import intersection
    Args = namedtuple('Args', ['data', 'args'])

    intersection(Args(data='', args=['Swadesh-1955-100', 'Swadesh-1952-200']))
    out, err = capsys.readouterr()
    assert 94 == len(out.split('\n'))


def test_lookup(capsys, mocker):
    from pyconcepticon.commands import lookup

    lookup(mocker.MagicMock(full_search=True, args=['sky'], language='en'))
    out, err = capsys.readouterr()
    assert '1732' in out

    lookup(mocker.MagicMock(args=['sky'], language='en'))
    out, err = capsys.readouterr()
    assert '1732' in out
