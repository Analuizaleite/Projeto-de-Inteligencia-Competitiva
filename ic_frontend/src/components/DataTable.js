import React from 'react';

const DataTable = ({ data, columns }) => {
  const getSentimentColor = (value) => {
    if (value === 'Positivo') return { backgroundColor: '#E8F5E9', color: 'green', fontWeight: 'bold' };
    if (value === 'Negativo') return { backgroundColor: '#FFEBEE', color: 'red', fontWeight: 'bold' };
    if (value === 'Neutro') return { backgroundColor: '#FFFDE7', color: 'orange' };
    return {};
  };

  return (
    <table className="table">
      <thead>
        <tr>
          {columns.map(column => (
            <th key={column.key}>{column.label}</th>
          ))}
        </tr>
      </thead>
      <tbody>
        {data.map((row, index) => (
          <tr key={index}>
            {columns.map(column => (
              <td 
                key={column.key}
                style={column.key === 'sentimento_categoria' ? getSentimentColor(row[column.key]) : {}}
              >
                {typeof row[column.key] === 'number' 
                  ? row[column.key].toFixed(1) 
                  : row[column.key]
                }
              </td>
            ))}
          </tr>
        ))}
      </tbody>
    </table>
  );
};

export default DataTable;