import React from "react";
import DepositForm from "../components/DepositForm";
import { initiateDeposit } from "../api/cinetpay";

const DepositPage = () => {
  const handleDeposit = async (amount, paymentMethod) => {
    try {
      const paymentUrl = await initiateDeposit(amount, paymentMethod);
      window.location.href = paymentUrl; // Redirige vers CinetPay
    } catch (error) {
      alert("Erreur lors du paiement. Veuillez réessayer.");
    }
  };

  return (
    <div className="flex justify-center items-center min-h-screen bg-gray-100">
      <DepositForm onDeposit={handleDeposit} />
    </div>
  );
};

export default DepositPage;
