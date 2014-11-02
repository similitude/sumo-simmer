/**
 * The API for the SUMO model.
 */
service SumoService {

  /**
   * Invokes SUMO from the command line. Directs output into a temporary file
   * and returns the contents.
   *
   * @param network The command line arguments.
   */
  string call(1:map<string, string> clargs)

  /**
   * Simulates traffic for an hour with random trips on the given network, with
   * minutely output.
   *
   * @param network The contents of the .net.xml file.
   */
  string randomHourMinutes(1:string network)

}
