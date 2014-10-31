# Utility functions to assist the service handler.

import os
import subprocess
from distutils.dir_util import mkpath

SECONDS_IN_MINUTE = 60
SECONDS_IN_HOUR = 60 * 60

# Standard file extensions for different types of SUMO file.
EXTENSIONS = {
    'network': '.net.xml',
    'trips': '.trips.xml',
    'routes': '.rou.xml',
    'config': '.sumo.cfg',
    'additional': '.add.xml',
    'output': '.out.xml',
}


def convert_osm_to_sumo(osm_network):
    # TODO(orlade): Implement conversion via netconvert.
    network = ''
    return network


def generate_random_routes(job):
    """
    Generates a random trips file for the network of the given job.
    """
    trip_generator = '%s/tools/trip/randomTrips.py' % os.environ['SUMO_HOME']
    [net_path, out_path, routes_path] = [build_data_filename(job, t) for t in ('network', 'output', 'routes')]
    print 'Generating routes to %s...' % routes_path
    args = ['python', trip_generator, '-e', str(SECONDS_IN_HOUR), '-n', net_path, '-o', out_path, '-r', routes_path]
    output = subprocess.call(args)
    print 'Generated routes: %s' % output
    return output


def generate_output_spec(output_file_path):
    # Generates the XML for an additional file to request output.
    return '<edgeData id="traffic" file="%s" freq="%d"/>' % (output_file_path, SECONDS_IN_MINUTE)


def build_data_filename(job, filetype):
    path = '/data/%s%s' % (job, EXTENSIONS[filetype])
    return os.path.abspath(path)


def write_to_file(filename, content):
    """
    Writes the given content to the given file.
    """
    # Ensure the directory exists.
    mkpath(os.path.dirname(filename))
    with open(filename, 'w') as f:
        f.write(content)
    return filename


def read_file(filename):
    with open(filename, 'r') as f:
        return f.read()
