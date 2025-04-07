import React, { useState, useEffect } from "react";

const PaymentsList = () => {
  const [payments, setPayments] = useState([]);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchPayments = async () => {
      try {
        const response = await fetch("http://127.0.0.1:8000/payment/payments", {
          method: "GET",
          headers: {
            "Content-Type": "application/json",
            "Authorization": `Bearer ${localStorage.getItem("token")}` // Utilisez le token JWT pour l'authentification
          },
        });

        if (response.ok) {
          const data = await response.json();
          setPayments(data); // Mettez à jour l'état avec la liste des paiements
        } else {
          setError("Erreur lors de la récupération des paiements.");
        }
      } catch (error) {
        setError("Une erreur est survenue.");
      }
    };

    fetchPayments();
  }, []); // Effectue l'appel une fois lors du chargement du composant

  return (
    <div>
      {error && <p>{error}</p>}
      <h3>Liste des paiements :</h3>
      {payments.length === 0 ? (
        <p>Aucun paiement trouvé.</p>
      ) : (
        <ul>
          {payments.map((payment, index) => (
            <li key={index}>
              Paiement ID: {payment.id} - Montant: {payment.amount} F
            </li>
          ))}
        </ul>
      )}
    </div>
  );
};

export default PaymentsList;
