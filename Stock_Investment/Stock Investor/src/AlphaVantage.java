import java.util.List;
import java.util.Map;

public class AlphaVantage
{
	private static final String API_KEY = "OB12RQ5U8B3JWQLY";
	private static final String BASE_URL = "https://www.alphavantage.co/query?";

	public static void main(String[] args)
	{
		int timeout = 3000;
		AlphaVantageConnector apiConnector = new AlphaVantageConnector(API_KEY,timeout);
		TimeSeries stockTimeSeries = new TimeSeries(apiConnector);

		try
		{
			IntraDay response = stockTimeSeries.intraDay("MSFT", Interval.ONE_MIN, OutputSize.COMPACT);
			Map<String, String> metaData = response.getMetaData();
			System.out.println("Information: " + metaData.get("1. Information"));
			System.out.println("Stock: " + metaData.get("2. Symbol"));

			List<StockData> stockData = response.getStockData();
			stockData.forEach(stock ->
			{
				System.out.println("date:   " + stock.getDateTime());
				System.out.println("open:   " + stock.getOpen());
				System.out.println("high:   " + stock.getHigh());
				System.out.println("low:    " + stock.getLow());
				System.out.println("close:  " + stock.getClose());
				System.out.println("volume: " + stock.getVolume());
			});
		}
		catch (AlphaVantageException e)
		{
			System.out.println("something went wrong");
		}
	}
}