import React, { useEffect } from 'react'
import { useState } from 'react'
import './MnistJob.css'
import APIservice from '../../services/APIservice'

function MnistJobModal() {
    const [mnistJobs, setMnistJobs] = useState([]);
    const [isOpen, setIsOpen] = useState({});

    const addTab = () => {
        // APIservice.AddMnistJob({}).then((data) => {
        //     setMnistJobs([...mnistJobs, data]);
        // });
    }

    useEffect(() => {
        APIservice.GetMnistJob().then((data) => {
            console.log(data);
            setMnistJobs(data);
        });
    }, []);

    return (
        <div>
            {mnistJobs.map(job => (
                <div key={job.id}>
                    <div className="bar-tab">Job {job.id}</div>
                    <div className="bar-content">{job.config}</div>
                </div>
            ))}
            <button onClick={addTab} className='center'> Add Mnist Job </button>
        </div>
    )
}

export default MnistJobModal
