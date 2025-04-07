export const initiateDeposit = async (amount, paymentMethod) => {
    const token = localStorage.getItem("token"); // Récupère le token JWT
    
    const response = await fetch("http://127.0.0.1:8000/deposit", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        "Authorization": `Bearer ${token}`
      },
      body: JSON.stringify({ amount, paymentMethod }),
    });
  
    if (!response.ok) {
      throw new Error("Échec du paiement");
    }
  
    const data = await response.json();
    return data.payment_url; // URL vers CinetPay
  };
  