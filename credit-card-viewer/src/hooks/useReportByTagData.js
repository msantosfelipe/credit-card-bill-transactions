// src/hooks/useReportByTagData.js
import { useState, useEffect } from 'react';

const endpoint = 'http://localhost:8080/credit-card-reader/';

const useReportByTagData = () => {
  const [reportData, setReportData] = useState([]);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const response = await fetch(endpoint + 'report/tag');
        const data = await response.json();
        setReportData(data);
      } catch (error) {
        console.error('Error fetching data:', error);
      }
    };
    fetchData();
  }, []);

  return reportData;
};

export default useReportByTagData;
