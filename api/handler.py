import os
import subprocess
import uuid

from api.util import SECONDS_IN_HOUR, build_clargs, build_data_filename, \
    generate_output_spec, generate_random_routes, read_file, write_to_file


COMMAND = 'sumo'


class SumoServiceHandler():
    """
    Implements the SumoService interface.
    """

    def call(self, clargs):
        """
        Invokes SUMO from the command line.

        Parameters:
         - clargs: The command line arguments.
        """
        job = uuid.uuid4()

        if '--net-file' in clargs and '--additional-files' not in clargs:
            out_file_path = build_data_filename(job, 'output')
            adtl_file_path = build_data_filename(job, 'additional')
            write_to_file(adtl_file_path, generate_output_spec(out_file_path))
            clargs['--additional-files'] = adtl_file_path
        else:
            # TODO(orlade): Handle cases where output file is specified.
            out_file_path = None

        args = [COMMAND] + build_clargs(clargs)

        print('Calling SUMO with arguments:\n%s' % ' '.join(args))
        proc = subprocess.Popen(args, stdout=subprocess.PIPE)

        # Save the command-line output.
        output = {'cli': proc.stdout.read()}

        # If there was any output to a file, include that too.
        if out_file_path and os.path.isfile(out_file_path):
            with open(out_file_path) as f:
                output['data'] = f.read()

        return output

    def randomHourMinutes(self, network):
        """
        Simulates traffic for an hour with random trips on the given network,
        with minutely output.

        Parameters:
         - network: The contents of the .net.xml file.
        """
        job = uuid.uuid4()

        types = ('network', 'routes', 'additional', 'output')
        (net_file_path, route_file_path, adtl_file_path, out_file_path) = \
            [build_data_filename(job, t) for t in types]

        write_to_file(net_file_path, network)
        generate_random_routes(job)
        write_to_file(adtl_file_path, generate_output_spec(out_file_path))

        args = {
            '--net-file': net_file_path,  # Network input file.
            '--route-files': route_file_path,  # Route input file.
            '--additional-files': adtl_file_path,  # Output format spec.
            '--begin': 0,  # Time to begin the simulation.
            '--end': SECONDS_IN_HOUR,  # Time to end the simulation.
            '--time-to-teleport': -1,  # Disable teleporting for stuck vehicles.
            '-W': None,  # Disable warning messages.
        }
        return self.call(args)
