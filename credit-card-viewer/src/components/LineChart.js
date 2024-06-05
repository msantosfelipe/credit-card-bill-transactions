// components/LineChart.js
import { Line } from "react-chartjs-2";

function LineChart({ chartData }) {
  const options = {
    responsive: true,
    plugins: {
      title: {
        display: false,
      },
      legend: {
        display: false
      }
    }
  };
  return (
    <div className="chart-container">
      <Line data={chartData} options={options} />
    </div>
  );
};

export default LineChart;