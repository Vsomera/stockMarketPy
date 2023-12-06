import { useState, useEffect } from 'react';

const Health = () => {
    const [serviceStatuses, setServiceStatuses] = useState(null);

    useEffect(() => {
        const fetchHealthStatus = async () => {
            try {
                const response = await fetch('http://ec2-3-143-231-139.us-east-2.compute.amazonaws.com:8120/health');
                if (response.ok) {
                    const data = await response.json();
                    setServiceStatuses(data);
                    console.log(serviceStatuses)
                } else {
                    throw new Error('Network response was not ok.');
                }
            } catch (error) {
                console.error('Fetch error:', error);
            }
        };

        // Initial fetch
        fetchHealthStatus();

        // Set interval for repeated fetches
        const intervalId = setInterval(fetchHealthStatus, 20000);

        // Cleanup on component unmount
        return () => clearInterval(intervalId);
    }, []);

    // Render service statuses or a loading message
    return (
        <>
            {serviceStatuses ? (
                <div>
                    <h2>Service Statuses</h2>
                    <ul>
                        {Object.entries(serviceStatuses).map(([key, value]) => (
                            <li key={key}>{`${key}: ${value}`}</li>
                        ))}
                    </ul>
                </div>
            ) : (
                <p>Loading service statuses...</p>
            )}
        </>
    );
};

export default Health;
