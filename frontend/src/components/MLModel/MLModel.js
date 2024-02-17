import React from 'react'
import './MLModel.css'
import { useState } from 'react'
import APIservice from '../../services/APIservice'

function MLModel() {
    const [modelName, setModelName] = useState('');
    const [modelScript, setModelScript] = useState('');

    const addMLModel = () => {
        console.log(modelName);
        console.log(modelScript);
        APIservice.SumitMLModel({
            name: modelName,
            model_script: modelScript,
        }).then((data) => {
            console.log(`Ml Model id = ${data.id}`)
        });
    }

    return (
        <div>
            <h2>Enter ML Name</h2>
            <input
                type="text"
                id="model_name"
                name="model_name"
                placeholder='Enter Model Name'
                onChange={(e) => setModelName(e.target.value)}
                style={{ marginLeft: '30px' }}
            />

            <h2>Enter Code</h2>
            <textarea
                id="codeInput"
                rows="10"
                cols="100"
                onChange={(e) => setModelScript(e.target.value)}
                className='text-box'
            >
                console.log('Hello, world!');
            </textarea>
            <div>
                <button
                    onClick={addMLModel}
                    style={{ marginLeft: '30px' }}
                > <h3> Add ML Model </h3> </button>
            </div>

        </div>
    )
}

export default MLModel
