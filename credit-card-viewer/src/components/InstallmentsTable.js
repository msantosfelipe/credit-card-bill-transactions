// src/components/InstallmentsTable.js
import React from 'react';

const InstallmentsTable = ({ data }) => {
    return (
        <div className="mt-4">
            <h5>Mês {data.month}</h5>
            <h5>Total pago nesse mês: {data.amount}</h5>
            {data?.data?.length > 0 ? (
                <table className="table table-striped">
                    <thead>
                        <tr>
                            <th>Data da compra</th>
                            <th>Cartão</th>
                            <th>Descrição</th>
                            <th>Parcela</th>
                            <th>Valor</th>
                        </tr>
                    </thead>
                    <tbody>
                        {data.data.map((item, index) => (
                            <tr key={index}>
                                <td>{item.purchase_date}</td>
                                <td>{item.card_digits}</td>
                                <td>{item.description}</td>
                                <td>{item.installment}</td>
                                <td>{item.amount_brl.toFixed(2)}</td>
                            </tr>
                        ))}
                    </tbody>
                </table>
            ) : (
                <p>Nenhum dado disponível</p>
            )}
        </div>
    );
};

export default InstallmentsTable;
