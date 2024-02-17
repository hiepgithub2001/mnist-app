import React from 'react'
import { StatusView } from '../../services/UIhelper.js'
import ReactJson from 'react-json-view'
import TableDisplay from '../../services/TableDisplay.js'
import { useEffect, useState } from 'react'
import APIservice from '../../services/APIservice.js'
import { JOBSTATUS } from '../constant'
import { JobAction } from './JobAction';


function JobDetailModal() {
    const [data, setData] = useState([]);
    const [detectChanging, setDetectChanging] = useState(true);

    const columns = [
        {
            name: "Job id",
            selector: row => row.id,
        },
        {
            name: "Status",
            selector: row => <StatusView status={row.related_status.status} />
        },
        {
            name: "Config",
            selector: (row) => {
                return <ReactJson src={row.config} name={false} />
            },
        },
        {
            name: "Action",
            selector: (row) => (
                <div>
                    <JobAction jobID={row.id} setDetectChanging={setDetectChanging} />
                </div>
            ),
        }
    ]

    useEffect(() => {
        if (detectChanging) {
            APIservice.GetMnistJob({ list_status: [JOBSTATUS.ERROR, JOBSTATUS.PENDING, JOBSTATUS.RUNNING, JOBSTATUS.DONE] })
                .then((data) => {
                    setData(data);
                });
            setDetectChanging(false);
        }
    }, [detectChanging]);


    return (
        <TableDisplay columns={columns} data={data} />
    )
}

export default JobDetailModal
