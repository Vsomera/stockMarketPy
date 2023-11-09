import React, { useEffect, useState } from 'react';

export default function AppStats() {
  const [isLoaded, setIsLoaded] = useState(false);
  const [stats, setStats] = useState({});
  const [error, setError] = useState(null);

  useEffect(() => {
    const getStats = () => {
      fetch(import.meta.env.PROCESSING_URI)
        .then((res) => res.json())
        .then(
          (result) => {
            console.log("Received Stats");
            console.log(stats)
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
      <div>
         <table className={"StatsTable"}>
					<tbody>
						<tr>
							<th>Blood Pressure</th>
							<th>Heart Rate</th>
						</tr>
						{/* <tr>
							<td># num_buy_orders: {stats['num_bp_readings']}</td>
							<td># HR: {stats['num_hr_readings']}</td>
						</tr>
						<tr>
							<td>Highest Order Price: {stats['highest_order_price']}</td>
						</tr>
						<tr>
							<td>Lowest Order Price: {stats['lowest_order_price']}</td>
						</tr>
						<tr>
							<td>Max HR: {stats['max_bp_sys_reading']}</td>
						</tr> */}
					</tbody>
                </table>
      </div>
    );
  }
}
