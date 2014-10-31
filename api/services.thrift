/**
 * The API for the SUMO model.
 */

/** The contents of an XML file as a string. */
typedef string xml

service SumoService {

  /**
   * Invokes SUMO from the command line.
   */
  xml call(
    /** The command line arguments. */
    1:map<string, string> clargs
  )

  /**
   * Simulates traffic for an hour with random trips on the given network, with minutely output.
   */
  xml randomHourMinutes(
    /** The contents of the .net.xml file. */
    1:xml network
  )

}
