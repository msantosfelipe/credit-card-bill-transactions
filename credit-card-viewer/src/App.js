// src/App.js
import './App.css';
import 'bootstrap/dist/css/bootstrap.min.css';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import Home from './components/pages/Home';
import CreditCards from './components/pages/CreditCards';

export default function App() {
  return (
    <Router>
      <div className="App">
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/credit-cards" element={<CreditCards />} />
        </Routes>
      </div>
    </Router>
  );
}
