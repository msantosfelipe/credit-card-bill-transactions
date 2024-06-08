// src/hooks/useBillsData.js
import { useState, useEffect } from 'react';
import Chart from "chart.js/auto";
import { CategoryScale } from "chart.js";

Chart.register(CategoryScale);

const endpoint = 'http://localhost:8080/credit-card-reader/';

const useBillsData = () => {
    const [chartData, setBillsData] = useState({
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

    return chartData;
};

export default useBillsData;
