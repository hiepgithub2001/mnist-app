import React, { useEffect, useMemo, useState } from 'react'
import APIservice from '../../services/APIservice'
import TableDisplay from '../../services/TableDisplay';
import ReactJson from 'react-json-view';
import { StatusView } from '../../services/UIhelper';
import { JOBSTATUS } from '../constant';


function ScoreBoardModal() {
    const [data, setData] = useState([]);

    let columns = [
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
    ]


    let markedName = {};
    for(const item of data){
        for(const key in item.result){
            if (!markedName[key]){
                columns.push({
                    name: key,
                    selector: row => row.result[key] ? row.result[key] : "N/A",
                    sortable: true,
                })
                markedName[key] = true;
            }
        }
    }


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
