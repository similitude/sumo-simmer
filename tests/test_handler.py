import os
from hamcrest.core import assert_that
from hamcrest.core.core.isequal import equal_to

from api.handler import SumoServiceHandler
from api.util import build_clargs


def test_build_clargs():
    args = {
        '--net-file': '/path/to/file',
        '--begin': 0,
        '-W': None,
    }
    arg_str = ' '.join(build_clargs(args))
    assert_that('-W' in arg_str)
    assert_that('--net-file /path/to/file' in arg_str)
    assert_that('--begin 0' in arg_str)


def test_call_sumo():
    """
    Invokes SUMO to test that it is available.

    Set environment variable CI=true in continuous integration to skip.
    """
    if os.environ.get('CI'):  # pragma: no cover
        return

    output = SumoServiceHandler().call({})
    assert output['cli'].startswith('SUMO sumo Version ')


def test_call_sumo_data():
    """
    Invokes SUMO with pre-calculated data for the Eichstaett network.

    Set environment variable CI=true in continuous integration to skip.
    """
    if os.environ.get('CI'):  # pragma: no cover
        return

    example_dir = os.path.join(os.path.dirname(__file__), '..', 'example')
    output = SumoServiceHandler().call({
        '--net-file': os.path.join(example_dir, 'eich.net.xml'),
        '--route-files': os.path.join(example_dir, 'eich.rou.xml'),
        '--begin': 0,
        '--end': 120,  # Two minutes
        '--time-to-teleport': -1,
        '-W': None,
    })
    # TODO: Return written output.
    assert_that(output['data'].count('<edge'), equal_to(2354))
