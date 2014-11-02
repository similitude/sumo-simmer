/**
 * The API for the SUMO model.
 */
service SumoService {

  /**
   * Invokes SUMO from the command line. Returns a map containing a key 'cli'
   * for the data printed to stdout, and 'data' for the contents of the output
   * file, if any.
   *
   * @param network The command line arguments.
   */
  map<string, string> call(1:map<string, string> clargs)

  /**
   * Simulates traffic for an hour with random trips on the given network, with
   * minutely output.
   *
   * @param network The contents of the .net.xml file.
   */
  map<string, string> randomHourMinutes(1:string network)

}
