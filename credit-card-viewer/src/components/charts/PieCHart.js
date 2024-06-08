// components/PieChart.js
import { Pie } from "react-chartjs-2";

function PieChart({ chartData }) {
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
      <Pie data={chartData} options={options} />
    </div>
  );
};

export default PieChart;