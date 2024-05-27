import './App.css';
import React, { useState, useEffect } from 'react';
import BarChart from './components/BarChart';
import PieChart from './components/PieChart';

const endpoint = 'http://localhost:8080/credit-card-reader/'

function App() {
  const [monthlyData, setMonthlyData] = useState([]);
  const [categoryData, setCategoryData] = useState([]);

  useEffect(() => {
    const fetchData = async () => {
      const data = {
        "monthlyExpenses": [
          { "month": "Janeiro", "amount": 1200 },
          { "month": "Fevereiro", "amount": 950 },
          { "month": "Março", "amount": 1300 },
          { "month": "Abril", "amount": 1100 },
          { "month": "Maio", "amount": 1400 },
          { "month": "Junho", "amount": 900 },
          { "month": "Julho", "amount": 1500 },
          { "month": "Agosto", "amount": 1200 },
          { "month": "Setembro", "amount": 1000 },
          { "month": "Outubro", "amount": 1350 },
          { "month": "Novembro", "amount": 1250 },
          { "month": "Dezembro", "amount": 1600 }
        ],
        "categoryExpenses": [
          { "category": "Alimentação", "amount": 3000 },
          { "category": "Transporte", "amount": 1200 },
          { "category": "Lazer", "amount": 900 },
          { "category": "Saúde", "amount": 700 },
          { "category": "Educação", "amount": 1100 },
          { "category": "Outros", "amount": 1500 }
        ]
      };
      setMonthlyData(data.monthlyExpenses);
      setCategoryData(data.categoryExpenses);

      //const responseByTag = await fetch(endpoint+'report/tag');
      //const dataByTag = await responseByTag.json();

      //setCategoryData(dataByTag[1].report);
    };

    fetchData();
  }, []);

  return (
    <div className="App">
      <h1>Gastos no Cartão de Crédito</h1>
      <div style={{ width: '600px', margin: '0 auto' }}>
        <h2>Gastos Mensais</h2>
        <BarChart data={monthlyData} />
        <h2>Distribuição por Categoria</h2>
        <PieChart data={categoryData} />
      </div>
    </div>
  );
}

export default App;
