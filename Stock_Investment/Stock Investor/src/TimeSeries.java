
public class TimeSeries
{
	private final ApiConnector apiConnector;

	/**
	 * Constructs a Time Series Data api endpoint with the help of an {@link ApiConnector} and a {@link JsonParser}
	 *
	 * @param apiConnector the connection to the api
	 */
	public TimeSeries(ApiConnector apiConnector)
	{
		this.apiConnector = apiConnector;
	}

	/**
	 * This API returns intraday time series (timestamp, open, high, low, close, volume) of the equity specified, updated realtime.
	 *
	 * @param symbol the stock symbol to lookup
	 * @param interval the interval between two consecutive data points in the time series {@link Interval}
	 * @param outputSize the specification of the amount of returned data points {@link OutputSize}
	 * @return {@link IntraDay} time series data
	 */
	public IntraDay intraDay(String symbol, Interval interval, OutputSize outputSize)
	{
		//Symbol,Function,Interval, and OutputSize all implement the ApiParameter interface
		String json = apiConnector.getRequest(new Symbol(symbol), Function.TIME_SERIES_INTRADAY, interval, outputSize);
		return IntraDay.from(interval, json);
	}

	/**
	 * This API returns intraday time series (timestamp, open, high, low, close, volume) of the equity specified, updated realtime.
	 *
	 * @param symbol the stock symbol to lookup
	 * @param interval the interval between two consecutive data points in the time series {@link Interval}
	 * @return {@link IntraDay} time series data
	 */
	public IntraDay intraDay(String symbol, Interval interval)
	{
		String json = apiConnector.getRequest(new Symbol(symbol), Function.TIME_SERIES_INTRADAY, interval);
		return IntraDay.from(interval, json);
	}

	/**
	 * This API returns daily time series (date, daily open, daily high, daily low, daily close, daily volume) of the equity specified.
	 *
	 * @param symbol the stock symbol to lookup
	 * @param outputSize the specification of the amount of returned data points {@link OutputSize}
	 * @return {@link Daily} time series data
	 */
	public Daily daily(String symbol, OutputSize outputSize)
	{
		String json = apiConnector.getRequest(new Symbol(symbol), Function.TIME_SERIES_DAILY, outputSize);
		return Daily.from(json);
	}

	/**
	 * This API returns daily time series (date, daily open, daily high, daily low, daily close, daily volume) of the equity specified.
	 *
	 * @param symbol the stock symbol to lookup
	 * @return {@link Daily} time series data
	 */
	public Daily daily(String symbol)
	{
		String json = apiConnector.getRequest(new Symbol(symbol), Function.TIME_SERIES_DAILY);
		return Daily.from(json);
	}

	/**
	 * This API returns weekly time series (last trading day of each week, weekly open, weekly high, weekly low, weekly close, weekly volume).
	 *
	 * @param symbol the stock symbol to lookup
	 * @return {@link Weekly} time series data
	 */
	public Weekly weekly(String symbol)
	{
		String json = apiConnector.getRequest(new Symbol(symbol), Function.TIME_SERIES_WEEKLY);
		return Weekly.from(json);
	}

	/**
	 * This API returns monthly time series (last trading day of each month, monthly open, monthly high, monthly low, monthly close, monthly volume).
	 *
	 * @param symbol the stock symbol to lookup
	 * @return {@link Monthly} time series data
	 */
	public Monthly monthly(String symbol)
	{
		String json = apiConnector.getRequest(new Symbol(symbol), Function.TIME_SERIES_MONTHLY);
		return Monthly.from(json);
	}
}
