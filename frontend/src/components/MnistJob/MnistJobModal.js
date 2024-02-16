import React, { useEffect } from 'react'
import { useState } from 'react'
import './MnistJob.css'
import APIservice from '../../services/APIservice'

function MnistJobModal() {
    const [config, setConfig] = useState('');
    const [model, setModel] = useState('');

    const submitJob = () => {
        try {
            console.log(config)
            const jsonConfig = JSON.parse(config);
            APIservice.AddMnistJob({ config: jsonConfig }).then((data) => {
                console.log(`Job id = ${data.id}`)
            });
        } catch (e) {
            console.log('Error parsing JSON');
        }
    }

    return (
        <div>
            <h2>Enter JSON input</h2>
            <textarea
                id="jsonInput" 
                rows="4"
                cols="50"
                onChange={(e) => setConfig(e.target.value)}
                className='text-box'
            >
                {JSON.stringify({
                    "epochs": 10,
                    "batch_size": 32,
                    "learning_rate": 0.01
                })}
            </textarea>

            <h2>Enter Code</h2>
            <textarea
                id="codeInput"
                rows="10"
                cols="100"
                onChange={(e) => setModel(e.target.value)}
                className='text-box'
            >
                console.log('Hello, world!');
            </textarea>
            <div>
                <button
                    onClick={submitJob}
                    style={{marginLeft: '30px'}}
                > <h3> Submit </h3> </button>
            </div>
            
        </div>
    )
}

export default MnistJobModal
