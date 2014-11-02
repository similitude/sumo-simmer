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


def build_clargs(arg_dict):
    """
    Converts a map of command-line flags and values into a string of
    command-line inputs.
    """
    items = reduce(lambda xs, (k, v): xs + [k, v], arg_dict.items(), [])
    return map(str, filter(lambda x: x not in (None, ''), items))


def generate_random_routes(job):
    """
    Generates a random trips file for the network of the given job.
    """
    trip_generator = '%s/tools/trip/randomTrips.py' % os.environ['SUMO_HOME']
    args = {
        '-e': SECONDS_IN_HOUR,
        '-n': build_data_filename(job, 'network'),
        '-o': build_data_filename(job, 'output'),
        '-r': build_data_filename(job, 'routes'),
    }
    print 'Generating routes to %s...' % args['-r']
    return subprocess.call(['python', trip_generator] + build_clargs(args))


def generate_output_spec(output_file_path):
    """
    Generates the XML for an additional file to request output every minute
    """
    return '<edgeData id="traffic" file="%s" freq="60"/>' % output_file_path


def build_data_filename(job, filetype):
    """
    Generates an absolute path to a file for the job and type.
    """
    path = '/tmp/%s/data%s' % (job, EXTENSIONS[filetype])
    return os.path.abspath(path)


def write_to_file(filename, content):
    """
    Writes the given content to the given file.
    """
    # Ensure the directory exists.
    mkpath(os.path.dirname(filename))
    with open(filename, 'w') as f:
        f.write(content)


def read_file(filename):
    """
    Returns the content of the given filename as a string.
    """
    with open(filename, 'r') as f:
        return f.read()
