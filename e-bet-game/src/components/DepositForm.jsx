import React, { useState } from "react";

const DepositForm = ({ onDeposit }) => {
  const [amount, setAmount] = useState("");
  const [paymentMethod, setPaymentMethod] = useState("MTN");

  const handleSubmit = (e) => {
    e.preventDefault();
    if (amount < 1000) {
      alert("Le montant minimum est 1000F");
      return;
    }
    onDeposit(amount, paymentMethod);
  };

  return (
    <div className="p-6 bg-white shadow-lg rounded-xl">
      <h2 className="text-xl font-bold mb-4">Recharger mon compte</h2>
      <form onSubmit={handleSubmit}>
        <label className="block mb-2">Montant (F CFA) :</label>
        <input
          type="number"
          value={amount}
          onChange={(e) => setAmount(e.target.value)}
          className="w-full p-2 border rounded-lg mb-4"
          min="1000"
          required
        />

        <label className="block mb-2">Moyen de paiement :</label>
        <select
          value={paymentMethod}
          onChange={(e) => setPaymentMethod(e.target.value)}
          className="w-full p-2 border rounded-lg mb-4"
        >
          <option value="MTN">MTN</option>
          <option value="Orange">Orange</option>
          <option value="Moov">Moov</option>
          <option value="Wave">Wave</option>
        </select>

        <button
          type="submit"
          className="w-full bg-blue-500 text-white py-2 rounded-lg hover:bg-blue-600"
        >
          Payer
        </button>
      </form>
    </div>
  );
};

export default DepositForm;
