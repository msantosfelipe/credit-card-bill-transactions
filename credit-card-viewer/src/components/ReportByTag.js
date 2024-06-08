// src/components/ReportByTag.js
import React from 'react';
import { Bar } from 'react-chartjs-2';

const ReportByTag = ({ data }) => {

  const generateChartData = (report) => {
    const labels = report.map(item => item.date);
    const data = report.map(item => item.amount);

    return {
      labels,
      datasets: [
        {
          label: 'Amount',
          data,
          backgroundColor: 'rgba(75, 192, 192, 0.6)',
          borderColor: 'rgba(75, 192, 192, 1)',
          borderWidth: 1,
        }
      ]
    };
  };

  return (
    <div className="container">
      {data?.length > 0 ? (
        data.map((item, index) => (
          <div key={index} className="my-4">
            <details>
              <summary>{item.tag}</summary>
              <div style={{ width: '1000px', margin: '0 auto' }}>
                <Bar data={generateChartData(item.report)} />
              </div>
            </details>
          </div>
        ))
      ) : (
        <p>Nenhum dado disponível</p>
      )}
    </div>
  );
};

export default ReportByTag;
