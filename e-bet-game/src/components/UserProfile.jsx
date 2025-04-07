import React, { useState, useEffect } from "react";

const UserProfile = () => {
  const [userData, setUserData] = useState(null);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchUserData = async () => {
      try {
        const response = await fetch("http://127.0.0.1:8000/auth/me", {
          method: "GET",
          headers: {
            "Content-Type": "application/json",
            "Authorization": `Bearer ${localStorage.getItem("token")}` // Assurez-vous que l'utilisateur est connecté
          },
        });

        if (response.ok) {
          const data = await response.json();
          setUserData(data);  // Mettez à jour l'état avec les données de l'utilisateur
        } else {
          setError("Erreur lors de la récupération des informations de l'utilisateur.");
        }
      } catch (error) {
        setError("Une erreur est survenue.");
      }
    };

    fetchUserData();
  }, []); // Effectue l'appel une fois lors du chargement du composant

  return (
    <div>
      {error && <p>{error}</p>}
      {userData ? (
        <div>
          <h3>Bienvenue, {userData.username}!</h3>
          {/* Affichez d'autres informations utilisateur ici */}
        </div>
      ) : (
        <p>Chargement des données...</p>
      )}
    </div>
  );
};

export default UserProfile;
