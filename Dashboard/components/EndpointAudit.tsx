import { useEffect, useState } from 'react'

interface Props {
    endpoint : string
}

export default function EndpointAudit(props : Props) {
    const [isLoaded, setIsLoaded] = useState(false);
    const [log, setLog] = useState(null);
    const [error, setError] = useState(null)
	const rand_val = Math.floor(Math.random() * 100);
    const [index, setIndex] = useState(null)

	useEffect(() => {

        const getAudit = () => {
            fetch(`http://ec2-3-143-231-139.us-east-2.compute.amazonaws.com:8110/api/${props.endpoint}?index=${rand_val}`)
                .then(res => res.json())
                .then((result)=>{
                    console.log("Received Audit Results for " + props.endpoint)
                    setLog(result);
                    setIndex(rand_val)
                    setIsLoaded(true);
                },(error) =>{
                    setError(error)
                    setIsLoaded(true);
                })
        }

		const interval = setInterval(() => getAudit(), 4000); // Update every 4 seconds
		return() => clearInterval(interval);
    }, [rand_val, props.endpoint]);

    if (error){
        return (<div className={"error"}>Error found when fetching from API</div>)
    } else if (isLoaded === false){
        return(<div>Loading...</div>)
    } else if (isLoaded === true){
        
        return (
            <div>
                <h3>{props.endpoint}-{index}</h3>
                {JSON.stringify(log)}
            </div>
        )
    }
}
