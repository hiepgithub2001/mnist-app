import React, { useEffect, useMemo, useState } from 'react'
import APIservice from '../../services/APIservice'
import TableDisplay from '../../services/TableDisplay';
import ReactJson from 'react-json-view';
import { StatusView } from '../../services/UIhelper';
import { JOBSTATUS } from '../constant';


function ScoreBoardModal() {
    const [data, setData] = useState([]);

    const columns = [
        {
            name: "Job id",
            selector: row => row.id,
        },
        {
            name: "Status",
            selector: row => <StatusView status={row.status} />
        },
        {
            name: "Config",
            selector: (row) => {
                return <ReactJson src={row.config}  name={false}/>
            },
        },
        {
            name: "X",
            selector: row => row.result.numX,
            sortable: true,
        },
        {
            name: "Y",
            selector: row => row.result.numY,
            sortable: true,
        }
    ]

    useEffect(() => {
        APIservice.GetMnistJob({ list_status: [JOBSTATUS.DONE]}).then((data) => {
            setData(data);
        });
    }, []);

    return (
        <TableDisplay columns={columns} data={data} />
    )
}

export default ScoreBoardModal
