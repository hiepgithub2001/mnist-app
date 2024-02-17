import React, { useEffect } from 'react'
import { useState } from 'react'
import './MnistJob.css'
import APIservice from '../../services/APIservice'

function MnistJobModal() {
    const [config, setConfig] = useState('');
    const [listModel, setListModel] = useState([]);
    const [MLModel, setMLModel] = useState({ id: '', name: '' });

    const submitJob = () => {
        try {
            console.log(config);
            console.log(MLModel.name);

            const jsonConfig = JSON.parse(config);
            APIservice.AddMnistJob({
                ml_model_id: MLModel.id,
                config: jsonConfig
            }).then((data) => {
                console.log(`Job id = ${data.id}`)
            });
        } catch (e) {
            console.log('Error parsing JSON');
        }
    }

    useEffect(() => {
        APIservice.GetMLModel().then((data) => {
            setListModel(data.map((model) => ({ id: model.id, name: model.name })));
        })
    }, []);

    const handleSelect = (event) => {
        const selectedIndex = event.target.selectedIndex;
        const selectedId = event.target[selectedIndex].value;
        const selectedName = event.target[selectedIndex].text;
        setMLModel({ id: selectedId, name: selectedName });
    };

    return (
        <div>
            <h2>Select Model</h2>
            <select
                value={MLModel.id}
                onChange={handleSelect}
                style={{ marginLeft: '30px' }}
            >
                <option value="" disabled>Select an option</option>
                {listModel.map((item, index) => (
                    <option
                        key={index}
                        value={item.id}
                    >
                        {item.name}
                    </option>
                ))}
            </select>

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

            <div>
                <button
                    onClick={submitJob}
                    style={{ marginLeft: '30px' }}
                    disabled={MLModel.id === ''}
                > <h3> Submit Mnist Job </h3> </button>
            </div>
        </div>
    )
}

export default MnistJobModal
