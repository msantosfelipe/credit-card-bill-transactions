import './App.css';
import Chart from "chart.js/auto";
import { CategoryScale } from "chart.js";
import { useState, useEffect } from "react";
import { Data } from "./utils/Data";
import PieChart from "./components/PieChart";

Chart.register(CategoryScale);

const endpoint = 'http://localhost:8080/credit-card-reader/'

export default function App() {
  

  const [chartData, setChartData] = useState({
    labels: Data.map((data) => data.year), 
    datasets: [
      {
        label: "Users Gained ",
        data: Data.map((data) => data.userGain),
        backgroundColor: [
          "rgba(75,192,192,1)",
          "#ecf0f1",
          "#50AF95",
          "#f3ba2f",
          "#2a71d0"
        ],
        borderColor: "black",
        borderWidth: 2
      }
    ]
  });

  useEffect(() => {
    const fetchData = async () => {
      const billsAmounts = await fetch(endpoint + 'bills');
      const billsAmountsData = await billsAmounts.json();
      console.log(billsAmountsData)
    };
    fetchData();
  }, []);
 
  return (
    <div className="App">
      <h1>Gastos no Cartão de Crédito</h1>
      <details>
      <summary>Gastos Mensais</summary>
      <div style={{ width: '600px', margin: '0 auto' }}>
        <h2>Gastos Mensais</h2>
        <PieChart chartData={chartData} />
      </div>
      </details>
    </div>
  );
}