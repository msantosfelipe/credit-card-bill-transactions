// src/components/pages/CreditCards.js
import 'bootstrap/dist/css/bootstrap.min.css';
import { Link } from 'react-router-dom';
import BarChart from "../charts/BarChart";
import useBillsData from '../../hooks/useBillsData';
import useInstallmentsData from '../../hooks/useInstallmentsData';
import InstallmentsTable from '../InstallmentsTable';
import ReportByTag from '../ReportByTag';

const CreditCards = () => {
    const billsData = useBillsData();
    const installmentsData = useInstallmentsData();

    return (
        <div className="App">
            <div className="container">
                <h1 className="text-center my-4">Gastos no Cartão de Crédito</h1>
                <details open>
                    <summary style={{ textAlign: 'left'}}>Histórico de valores das faturas:</summary>
                    <div className="d-flex justify-content-center">
                        <div style={{ width: '1000px' }}>
                            <BarChart chartData={billsData} />
                        </div>
                    </div>
                </details>
                <details>
                    <summary style={{ textAlign: 'left'}} >Contas parceladas:</summary>
                    <InstallmentsTable data={installmentsData} />
                </details>
                <details>
                    <summary style={{ textAlign: 'left'}}>Relatório por categoria de compra:</summary>
                    <ReportByTag />
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
