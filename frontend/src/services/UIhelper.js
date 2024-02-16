import React from 'react';
import './service.css'

export function StatusView({ status }) {
    switch (status) {
        case 'DONE':
            return <div className="status-done"> {status} </div>;
        case 'ERROR':
            return <div className="status-error"> {status} </div>;
        case 'RUNNING':
            return <div className="status-running"> {status} </div>;
        case 'PENDING':
            return <div className="status-pending"> {status} </div>;
        default:
            return <div className="status-unknown"> {status}</div>;
    }
}