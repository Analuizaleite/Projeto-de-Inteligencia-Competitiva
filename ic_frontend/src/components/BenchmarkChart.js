import React from 'react';
import { ComposedChart, Bar, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';

const BenchmarkChart = ({ data }) => {
  const CustomTooltip = ({ active, payload, label }) => {
    if (active && payload && payload.length) {
      return (
        <div className="custom-tooltip" style={{
          backgroundColor: 'white',
          padding: '10px',
          border: '1px solid #ccc',
          borderRadius: '4px'
        }}>
          <p><strong>{label}</strong></p>
          <p style={{ color: '#4CAF50' }}>
            Nota Média: {payload[0]?.value?.toFixed(1)}
          </p>
          <p style={{ color: '#F44336' }}>
            Risco Negatividade: {payload[1]?.value?.toFixed(1)}%
          </p>
          <p>Total Menções: {payload[0]?.payload?.total_mencoes}</p>
        </div>
      );
    }
    return null;
  };

  return (
    <div className="chart-container">
      <ResponsiveContainer width="100%" height="100%">
        <ComposedChart data={data} margin={{ top: 20, right: 30, left: 20, bottom: 80 }}>
          <CartesianGrid strokeDasharray="3 3" />
          <XAxis 
            dataKey="empresa" 
            angle={-45}
            textAnchor="end"
            height={80}
            fontSize={11}
          />
          <YAxis yAxisId="left" domain={[0, 5]} label={{ value: 'Nota Média', angle: -90, position: 'insideLeft' }} />
          <YAxis yAxisId="right" orientation="right" domain={[0, 100]} label={{ value: 'Risco (%)', angle: 90, position: 'insideRight' }} />
          <Tooltip content={<CustomTooltip />} />
          <Legend 
            verticalAlign="bottom"
            height={50}
            wrapperStyle={{ paddingTop: '40px' }}
          />
          <Bar yAxisId="left" dataKey="nota_media" fill="#4CAF50" name="Nota Média (Reputação)" />
          <Line yAxisId="right" type="monotone" dataKey="risco_negatividade" stroke="#F44336" strokeWidth={3} name="Risco Negatividade (%)" />
        </ComposedChart>
      </ResponsiveContainer>
    </div>
  );
};

export default BenchmarkChart;