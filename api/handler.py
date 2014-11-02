import subprocess
import uuid

from api.util import SECONDS_IN_HOUR, build_clargs, build_data_filename, \
    generate_output_spec, generate_random_routes, write_file


# The command to execute SUMO from the command line.
COMMAND = 'sumo'


class SumoServiceHandler():
    """
    Implements the SumoService interface.
    """

    def call(self, args):
        """
        Invokes SUMO from the command line.

        Parameters:
         - args: A dictionary of the command line arguments.
        """
        job = uuid.uuid4()

        if '--additional-files' not in args:
            args['--additional-files'] = build_data_filename(job, 'additional')
        out_path = build_data_filename(job, 'output')
        write_file(args['--additional-files'], generate_output_spec(out_path))

        args = [COMMAND] + build_clargs(args)

        print('Calling SUMO with arguments:\n%s' % ' '.join(args))
        subprocess.call(args)

        # If there was any output to a file, include that too.
        with open(out_path) as f:
            return f.read()

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

        write_file(net_file_path, network)
        generate_random_routes(job)
        write_file(adtl_file_path, generate_output_spec(out_file_path))

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
