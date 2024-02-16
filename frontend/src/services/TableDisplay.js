import React from 'react'
import DataTable from 'react-data-table-component'

function TableDisplay(props) {
    const { columns, data } = props;

    return (
        <div className='container mt-5'>
            <DataTable
                columns={columns}
                data={data}
            ></DataTable>
        </div>
    )
}

export default TableDisplay
