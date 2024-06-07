// components/BarChart.js
import { Bar } from "react-chartjs-2";

function BarChart({ chartData }) {
  const options = {
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
      <Bar data={chartData} options={options} />
    </div>
  );
};

export default BarChart;