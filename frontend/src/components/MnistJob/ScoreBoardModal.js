import React, { useMemo } from 'react'
import APIservice from '../../services/APIservice'
import TableDisplay from '../../services/TableDisplay';

function ScoreBoardModal() {
    const columns = [
        {
            name: "Job id",
            selector: row => row.id,
        },
        {
            name: "Status",
            selector: row => row.status,
        },
        {
            name: "Config",
            selector: row => row.config,
        },
        {
            name: "X",
            selector: row => row.result.numX,
        },
        {
            name: "Y",
            selector: row => row.result.numY,
        }
    ]

    const data = useMemo(async() => {
        await APIservice.GetMnistJob().then((data) => {
            console.log(data);
            return data;
        });
    })

    return (
        <TableDisplay columns={columns} data={data} />
    )
}

export default ScoreBoardModal
