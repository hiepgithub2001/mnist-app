import React, { useState, useRef, useEffect } from 'react';
import APIservice from '../../services/APIservice';

export const JobAction = (props) => {
    const { jobID, setDetectChanging } = props;

    const handleSelect = (option) => {
        switch (option) {
            case 'Retry':
                APIservice.RetryMnistJob(jobID).then((data) => {
                    setDetectChanging(true);
                    console.log(`Updating job id = ${jobID}`);
                })
                break;
            case 'Delete':
                APIservice.DeleteMnistJob(jobID).then((data) => {
                    setDetectChanging(true);
                    console.log(`Deleted job id = ${jobID}`);
                });
                break;
            default:
                console.log('Invalid option');
        }
    };

    const options = ['Retry', 'Delete'];

    return (
        <div>
            {options.map((option, index) => (
                <div key={index} style={{marginBottom: '10px'}}>
                    <button key={index} onClick={() => handleSelect(option)}>
                        {option}
                    </button>
                </div>
            ))}
        </div>
    );
};
