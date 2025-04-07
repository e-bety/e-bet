import React, { useState, useEffect } from "react";

function TransactionsTable() {
  const [transactions, setTransactions] = useState([]);

  useEffect(() => {
    // Simule la récupération des données des transactions
    setTransactions([
      { id: 1, user: "User1", amount: 100, type: "Deposit", date: "2025-04-01" },
      { id: 2, user: "User2", amount: 50, type: "Withdraw", date: "2025-04-02" },
      { id: 3, user: "User3", amount: 200, type: "Deposit", date: "2025-04-03" },
    ]);
  }, []);

  return (
    <div className="transactions-table">
      <h2>Transactions</h2>
      <table>
        <thead>
          <tr>
            <th>ID</th>
            <th>Utilisateur</th>
            <th>Montant</th>
            <th>Type</th>
            <th>Date</th>
          </tr>
        </thead>
        <tbody>
          {transactions.map((transaction) => (
            <tr key={transaction.id}>
              <td>{transaction.id}</td>
              <td>{transaction.user}</td>
              <td>{transaction.amount} F</td>
              <td>{transaction.type}</td>
              <td>{transaction.date}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}

export default TransactionsTable;
