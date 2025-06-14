// src/components/pages/Home.js
import React from 'react';
import { Link } from 'react-router-dom';

const Home = () => {
  return (
    <div className="container text-center my-5">
      <h1>Bem-vindo à Análise de gastos no cartão de crédito</h1>
      <Link to="/credit-cards">
        <button className="btn btn-primary mt-3">Gastos gerais</button>
      </Link>
    </div>
  );
};

export default Home;
