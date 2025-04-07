import React, { useState } from "react";

const EBet = () => {
  const [lots, setLots] = useState([{ num1: "", num2: "" }]);
  const [rulesVisible, setRulesVisible] = useState(false);

  const handleAddLot = () => {
    if (lots.length < 5) {
      setLots([...lots, { num1: "", num2: "" }]);
    }
  };

  const handleInputChange = (index, field, value) => {
    const newLots = [...lots];
    newLots[index][field] = value;
    setLots(newLots);
  };

  const handlePlay = () => {
    console.log("Jouer avec les lots :", lots);
    // Intégration de la logique du jeu ici
  };

  return (
    <div style={styles.container}>
      <h1 style={styles.title}>🎲 E.Bet - Le jeu où chaque mise peut tout changer !</h1>

      <button onClick={() => setRulesVisible(!rulesVisible)} style={styles.ruleToggle}>
        {rulesVisible ? "Masquer les règles" : "Afficher les règles"}
      </button>

      {rulesVisible && (
        <div style={styles.rulesBox}>
          <h3>📜 Règles du jeu</h3>
          <ul>
            <li>Tu peux ajouter jusqu’à 5 lots de 2 numéros.</li>
            <li>Chaque lot coûte au moins 50F.</li>
            <li>Les gains dépendent des numéros générés dans 2 groupes.</li>
            <li>Matching partiel ou total → différents multiplicateurs !</li>
          </ul>
        </div>
      )}

      {lots.map((lot, index) => (
        <div key={index} style={styles.inputRow}>
          <input
            type="number"
            placeholder="Numéro 1"
            value={lot.num1}
            onChange={(e) => handleInputChange(index, "num1", e.target.value)}
            style={styles.input}
          />
          <input
            type="number"
            placeholder="Numéro 2"
            value={lot.num2}
            onChange={(e) => handleInputChange(index, "num2", e.target.value)}
            style={styles.input}
          />
        </div>
      ))}

      <div style={styles.buttonGroup}>
        <button onClick={handleAddLot} style={styles.addButton}>
          ➕ Ajouter un lot
        </button>
        <button onClick={handlePlay} style={styles.playButton}>
          🎮 Jouer
        </button>
      </div>
    </div>
  );
};

const styles = {
  container: {
    padding: "20px",
    maxWidth: "600px",
    margin: "0 auto",
    fontFamily: "Arial, sans-serif",
  },
  title: {
    textAlign: "center",
    color: "#2c3e50",
  },
  ruleToggle: {
    margin: "15px 0",
    padding: "10px 18px",
    backgroundColor: "#3498db",
    color: "#fff",
    border: "none",
    borderRadius: "8px",
    cursor: "pointer",
  },
  rulesBox: {
    backgroundColor: "#f9f9f9",
    padding: "15px",
    borderRadius: "8px",
    boxShadow: "0 2px 6px rgba(0,0,0,0.1)",
    marginBottom: "20px",
  },
  inputRow: {
    marginBottom: "10px",
    display: "flex",
    gap: "10px",
  },
  input: {
    flex: 1,
    padding: "8px",
    borderRadius: "5px",
    border: "1px solid #ccc",
    fontSize: "16px",
  },
  buttonGroup: {
    display: "flex",
    justifyContent: "center",
    gap: "20px",
    marginTop: "25px",
  },
  addButton: {
    padding: "10px 20px",
    backgroundColor: "#2ecc71",
    color: "white",
    border: "none",
    borderRadius: "5px",
    cursor: "pointer",
  },
  playButton: {
    padding: "10px 20px",
    backgroundColor: "#e74c3c",
    color: "white",
    border: "none",
    borderRadius: "5px",
    cursor: "pointer",
  },
};

export default EBet;
