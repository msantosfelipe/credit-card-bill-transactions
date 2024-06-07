// src/components/pages/CreditCards.js
import 'bootstrap/dist/css/bootstrap.min.css';
import { Link } from 'react-router-dom';
import Chart from "chart.js/auto";
import { CategoryScale } from "chart.js";
import { useState, useEffect } from "react";
import BarChart from "../charts/BarChart";

Chart.register(CategoryScale);

const endpoint = 'http://localhost:8080/credit-card-reader/'

const CreditCards = () => {
    const [billsData, setBillsData] = useState({
        labels: [],
        datasets: []
    });

    useEffect(() => {
        const fetchData = async () => {
            try {
                const billsAmounts = await fetch(endpoint + 'bills');
                const billsAmountsData = await billsAmounts.json();

                const transformedData = transformData(billsAmountsData);
                setBillsData(transformedData);
            } catch (error) {
                console.error("Error fetching data:", error);
            }
        };
        fetchData();
    }, []);

    const transformData = (data) => {
        const months = [];
        const amounts = [];

        data.forEach(item => {
            item.bills.forEach(bill => {
                months.push(bill.month);
                amounts.push(bill.total_amount);
            });
        });

        return {
            labels: months,
            datasets: [
                {
                    label: 'Total',
                    data: amounts,
                    backgroundColor: 'rgba(75, 192, 192, 0.6)',
                    borderColor: 'rgba(75, 192, 192, 1)',
                    borderWidth: 1,
                }
            ]
        };
    };

    return (
        <div className="App">
            <div className="container">
                <h1 className="text-center my-4">Gastos no Cartão de Crédito</h1>
                <details>
                    <summary>Valores das faturas</summary>
                    <div className="d-flex justify-content-center">
                        <div style={{ width: '1000px' }}>
                            <BarChart chartData={billsData} />
                        </div>
                    </div>
                </details>
            </div>
            <div className="container text-center my-5">
                <Link to="/">
                    <button className="btn btn-primary mt-3">Voltar</button>
                </Link>
            </div>
        </div>
    );
}

export default CreditCards;
