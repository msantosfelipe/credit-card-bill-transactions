// src/hooks/useInstallmentsData.js
import { useState, useEffect } from 'react';

const endpoint = 'http://localhost:8080/credit-card-reader/';

const useInstallmentsData = () => {
  const [installmentsData, setInstallmentsData] = useState([]);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const response = await fetch(endpoint + 'installments');
        const data = await response.json();
        setInstallmentsData(data);
      } catch (error) {
        console.error('Error fetching data:', error);
      }
    };
    fetchData();
  }, []);

  return installmentsData;
};

export default useInstallmentsData;
