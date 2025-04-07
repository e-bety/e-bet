// src/admin/AdminDashboard.jsx
import React, { useState, useEffect } from 'react';
import axios from 'axios';

const AdminDashboard = () => {
  const [transactions, setTransactions] = useState([]);

  // Charger les transactions
  useEffect(() => {
    axios.get('/admin/transactions')
      .then(response => {
        setTransactions(response.data);
      })
      .catch(error => {
        console.error('Error fetching transactions:', error);
      });
  }, []);

  const validateTransaction = (transactionId) => {
    axios.put(`/admin/validate-transaction/${transactionId}`)
      .then(response => {
        alert('Transaction validée');
        setTransactions(transactions.map(transaction => 
          transaction.id === transactionId ? { ...transaction, status: 'validated' } : transaction
        ));
      })
      .catch(error => {
        console.error('Error validating transaction:', error);
      });
  };

  const cancelTransaction = (transactionId) => {
    axios.put(`/admin/cancel-transaction/${transactionId}`)
      .then(response => {
        alert('Transaction annulée');
        setTransactions(transactions.map(transaction => 
          transaction.id === transactionId ? { ...transaction, status: 'cancelled' } : transaction
        ));
      })
      .catch(error => {
        console.error('Error cancelling transaction:', error);
      });
  };

  return (
    <div>
      <h2>Tableau de bord Administrateur</h2>
      <table>
        <thead>
          <tr>
            <th>ID</th>
            <th>Utilisateur</th>
            <th>Montant</th>
            <th>Statut</th>
            <th>Actions</th>
          </tr>
        </thead>
        <tbody>
          {transactions.map((transaction) => (
            <tr key={transaction.id}>
              <td>{transaction.id}</td>
              <td>{transaction.user_id}</td>
              <td>{transaction.amount}</td>
              <td>{transaction.status}</td>
              <td>
                {transaction.status === 'pending' && (
                  <>
                    <button onClick={() => validateTransaction(transaction.id)}>Valider</button>
                    <button onClick={() => cancelTransaction(transaction.id)}>Annuler</button>
                  </>
                )}
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
};

export default AdminDashboard;
