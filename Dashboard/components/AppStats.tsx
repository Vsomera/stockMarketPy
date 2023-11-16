import { useEffect, useState } from 'react';

interface OrderStats  {
    highest_order_price: number
    last_updated: string
    lowest_order_price: number
    num_buy_orders: number
    num_orders_filled: number
    num_sell_orders: number
}

export default function AppStats() {
  const [isLoaded, setIsLoaded] = useState(false);
  const [stats, setStats] = useState<OrderStats | null >(null);
  const [error, setError] = useState(null);

  useEffect(() => {
    const getStats = () => {
      fetch(import.meta.env.VITE_PROCESSING_URI)
        .then((res) => res.json())
        .then(
          (result) => {
            console.log("Received Stats");
            setStats(result);
            setIsLoaded(true);
          },
          (error) => {
            setError(error);
            setIsLoaded(true);
          }
        );
    };

    const interval = setInterval(getStats, 2000); // Update every 2 seconds

    return () => clearInterval(interval);
  }, []); // Empty dependency array, indicating no external dependencies

  if (error) {
    return <div className={"error"}>Error found when fetching from API</div>;
  } else if (isLoaded === false) {
    return <div>Loading...</div>;
  } else if (isLoaded === true) {
    return (
      <div style={{ textAlign : "center" , display : 'flex', justifyContent : "center"}}>
         <table className={"StatsTable"}>
					<tbody>
						<tr>
							<th>Order Stats</th>
						</tr>
                        { stats &&
                            <>

                                <tr>
                                    <td># Last Updated: {stats['last_updated']}</td>
                                </tr>	                                
                                <tr>
                                    <td># Buy Orders: {stats['num_buy_orders']}</td>
                                </tr>						
                                <tr>
                                    <td># Sell Orders: {stats['num_sell_orders']}</td>
                                </tr>
                                <tr>
                                    <td>Highest Order Price: ${stats['highest_order_price']}</td>
                                </tr>
                                <tr>
                                    <td>Lowest Order Price: ${stats['lowest_order_price']}</td>
                                </tr>
                                <tr>
                                    <td>Total Orders Filled: {stats['num_buy_orders'] + stats['num_sell_orders']}</td>
                                </tr>
                            </>
                        }
					</tbody>
                </table>
      </div>
    );
  }
}
