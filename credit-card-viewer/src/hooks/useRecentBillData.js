// src/hooks/useRecentBillData.js
import { useState, useEffect } from 'react';

const endpoint = 'http://localhost:8080/credit-card-reader/';

const useRecentBillData = () => {
  const [recentBillData, setRecentBillData] = useState({
    labels: [],
    datasets: []
  });

  useEffect(() => {
    const fetchData = async () => {
      try {
        const response = await fetch(endpoint + 'bill');
        const data = await response.json();
        const transformedData = transformData(data);
        setRecentBillData(transformedData);
      } catch (error) {
        console.error('Error fetching data:', error);
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

  return recentBillData;
};

export default useRecentBillData;
