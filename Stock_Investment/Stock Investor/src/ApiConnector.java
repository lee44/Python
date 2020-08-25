
public interface ApiConnector
{
	/**
	   * Sends request to the api.
	   *
	   * @param apiParameters the api parameters (required/optional) to the api call.
	   * @return the json response for the given call.
	   */
	  String getRequest(ApiParameter... apiParameters);
}
