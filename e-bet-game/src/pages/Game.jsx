import { useState } from "react";
import "../styles/Game.css";
// Suppression de l'import inutile qui provoquait le conflit
// import EBet from "../components/EBet";


const GamePage = () => {
  const [userBalance, setUserBalance] = useState(1000);
  const [selectedLots, setSelectedLots] = useState([]);
  const [chosenNumbers, setChosenNumbers] = useState("");
  const [lotBetAmount, setLotBetAmount] = useState("");
  const [gameResult, setGameResult] = useState("");
  const [generatedNumbers, setGeneratedNumbers] = useState({ top: [], bottom: [] });
  const [isDemoMode, setIsDemoMode] = useState(false);
  const [referralLink, setReferralLink] = useState("https://monsite.com/?ref=123456");
  const [showRules, setShowRules] = useState(false); // Etat pour afficher/masquer les règles

  const lotCost = 50;

  const checkBalance = () => alert(`Votre solde est : ${userBalance} F`);

  const rechargeAccount = async () => {
    let amount = prompt("Montant à recharger :");
    if (amount && !isNaN(amount) && amount > 0) {
        try {
            const response = await fetch("http://127.0.0.1:8000/deposit", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                    "Authorization": `Bearer ${localStorage.getItem("token")}`  // Assurez-vous que l'utilisateur est connecté
                },
                body: JSON.stringify({ amount: parseFloat(amount) })
            });

            if (response.ok) {
                const data = await response.json();
                window.location.href = data.payment_url;  // Redirige vers la page de paiement CinetPay
            } else {
                alert("Erreur lors du paiement. Réessayez.");
            }
        } catch (error) {
            console.error("Erreur:", error);
            alert("Une erreur est survenue.");
        }
    } else {
        alert("Montant invalide.");
    }
};

  const withdrawFunds = () => {
    let amount = prompt("Montant à retirer :");
    if (amount && !isNaN(amount) && amount > 0 && amount <= userBalance) {
      setUserBalance(prev => prev - parseFloat(amount));
      alert("Retrait réussi ! Nouveau solde : " + (userBalance - parseFloat(amount)) + " F");
    } else {
      alert("Montant invalide ou insuffisant.");
    }
  };

  const addLot = () => {
    if (selectedLots.length >= 5) {
      alert("Vous ne pouvez ajouter que 5 lots maximum.");
      return;
    }

    let numbers = chosenNumbers.split(",").map(num => num.trim());
    if (numbers.length !== 2 || numbers.some(num => isNaN(num) || num < 1 || num > 99)) {
      alert("Veuillez entrer 2 numéros valides entre 1 et 99.");
      return;
    }

    let betAmount = parseFloat(lotBetAmount);
    if (isNaN(betAmount) || betAmount < lotCost || betAmount > userBalance) {
      alert("La mise doit être d'au moins 50F et ne peut pas dépasser votre solde.");
      return;
    }

    setSelectedLots([...selectedLots, { numbers, bet: betAmount }]);
    setChosenNumbers("");
    setLotBetAmount("");
  };

  const removeLot = index => {
    setSelectedLots(selectedLots.filter((_, i) => i !== index));
  };

  const getUniqueRandomNumbers = (count, min, max) => {
    let numbers = [];
    while (numbers.length < count) {
      let num = Math.floor(Math.random() * (max - min + 1)) + min;
      if (!numbers.includes(num)) {
        numbers.push(num);
      }
    }
    return numbers;
  };

  const playGame = () => {
    if (selectedLots.length === 0) {
      alert("Ajoutez au moins un lot avant de jouer.");
      return;
    }

    let totalBetAmount = selectedLots.reduce((sum, lot) => sum + lot.bet, 0);
    if (totalBetAmount > userBalance && !isDemoMode) {
      alert("Votre solde est insuffisant pour couvrir votre mise totale.");
      return;
    }

    if (!isDemoMode) setUserBalance(prev => prev - totalBetAmount); // Si en mode réel, on déduit de l'argent

    let generated = getUniqueRandomNumbers(10, 1, 99);
    let firstGroup = generated.slice(0, 5);
    let secondGroup = generated.slice(5, 10);
    setGeneratedNumbers({ top: firstGroup, bottom: secondGroup });

    let totalGain = 0;
    selectedLots.forEach(lot => {
      let lotMatch = 0;
      let num1 = parseInt(lot.numbers[0]);
      let num2 = parseInt(lot.numbers[1]);

      // Multiplication x200 : premier du premier groupe et dernier du deuxième groupe
      if ((num1 === firstGroup[0] && num2 === secondGroup[4]) || (num2 === firstGroup[0] && num1 === secondGroup[4])) {
        lotMatch = 200;
      }
      // Multiplication x150 : dernier du premier groupe et premier du deuxième groupe
      else if ((num1 === firstGroup[4] && num2 === secondGroup[0]) || (num2 === firstGroup[4] && num1 === secondGroup[0])) {
        lotMatch = 150;
      }
      // Multiplication x1000 : les 2 premiers du premier groupe
      else if (firstGroup[0] === num1 && firstGroup[1] === num2) lotMatch = 1000;
      // Multiplication x100 : présent dans les 5 premiers numéros mais pas dans les 2 premiers
      else if (firstGroup.includes(num1) && firstGroup.includes(num2)) lotMatch = 100;
      // Multiplication x50 : présent dans les 5 derniers numéros
      else if (secondGroup.includes(num1) && secondGroup.includes(num2)) lotMatch = 50;
      // Multiplication x25 : si un numéro dans le 1er et l'autre dans le 2e groupe
      else if (firstGroup.includes(num1) && secondGroup.includes(num2)) lotMatch = 25;

      if (lotMatch > 0) totalGain += lotMatch * lot.bet;
    });

    if (totalGain > 0) {
      if (!isDemoMode) setUserBalance(prev => prev + totalGain); // En mode réel, ajout du gain
      setGameResult(`Félicitations ! Vous avez gagné ${totalGain} F.`);
    } else {
      setGameResult("Dommage, vous pouvez réessayer !");
    }
  };

  return (
    <div className="p-5 flex flex-col items-center bg-gray-100 min-h-screen">
      {/* Bouton pour afficher les règles */}
      <button
        className="bg-blue-500 text-white py-2 px-4 mt-4"
        onClick={() => setShowRules(!showRules)}
      >
        {showRules ? "Cacher les règles du jeu" : "Afficher les règles du jeu"}
      </button>

      {/* Affichage des règles du jeu */}
      {showRules && (
        <div className="bg-yellow-100 p-4 rounded-lg shadow-md w-80 mt-4 text-left">
          <h2 className="text-lg font-semibold">Règles du Jeu :</h2>
          <ul className="list-disc ml-4">
            <li>Choisissez 2 numéros entre 1 et 99 pour chaque lot.</li>
            <li>Chaque lot coûte au moins 50F.</li>
            <li>Les numéros gagnants sont tirés au hasard, divisés en 2 groupes :</li>
            <ul className="ml-4">
              <li>Groupe 1 (haut) : Si vos 2 numéros sont dans les 2 premiers numéros → Gain = Mise x 1000</li>
              <li>Groupe 2 (bas) : Si vos 2 numéros sont dans les 5 derniers numéros → Gain = Mise x 50</li>
              <li>Combinaison dans les deux groupes → Gain = Mise x 25</li>
              <li>**Multiplication x200** → Si un numéro est le premier du premier groupe et l'autre est le dernier du deuxième groupe.</li>
              <li>**Multiplication x150** → Si un numéro est le dernier du premier groupe et l'autre est le premier du deuxième groupe.</li>
            </ul>
          </ul>
        </div>
      )}

      {/* Mode démo */}
      <div className="mb-4">
        <label className="mr-2">Mode Démo :</label>
        <input
          type="checkbox"
          checked={isDemoMode}
          onChange={() => setIsDemoMode(!isDemoMode)}
        />
        <span className="ml-2">{isDemoMode ? "Actif" : "Désactivé"}</span>
      </div>

      <div className="bg-blue-200 p-5 rounded-lg shadow-md w-80 text-center">
        <h1 className="text-xl font-bold">E.Bet</h1>
        <button className="bg-orange-500 text-white py-2 px-4 mt-2" onClick={checkBalance}>Solde</button>
        <button className="bg-white text-black py-2 px-4 mt-2" onClick={rechargeAccount}>Recharge</button>
        <button className="bg-green-500 text-white py-2 px-4 mt-2" onClick={withdrawFunds}>Retrait</button>
        <div className="flex flex-wrap justify-center gap-2 mt-2">
          {selectedLots.map((lot, index) => (
            <div key={index} className="bg-gray-300 p-2 rounded relative">
              {lot.numbers.join(", ")} - {lot.bet} F
              <button className="absolute top-0 right-0 text-red-500" onClick={() => removeLot(index)}>X</button>
            </div>
          ))}
        </div>
        <input type="text" value={chosenNumbers} onChange={e => setChosenNumbers(e.target.value)} placeholder="Numéros (ex: 10,23)" className="w-full p-2 mt-2" />
        <input type="number" value={lotBetAmount} onChange={e => setLotBetAmount(e.target.value)} placeholder="Mise (50F min)" className="w-full p-2 mt-2" />
        
        {/* Séparation des boutons "Ajouter le lot" et "Jouer" */}
        <div className="flex flex-col gap-2 mt-4">
          <button className="bg-blue-500 text-white py-2 px-4" onClick={addLot}>Ajouter le lot</button>
          <button className="bg-blue-700 text-white py-2 px-4" onClick={playGame}>Jouer</button>
        </div>

        <h2 className="text-lg font-bold mt-2">{gameResult}</h2>
        <h3>Numéros Gagnants : {generatedNumbers.top.join(", ")}</h3>
        <h3>Seconde Chance : {generatedNumbers.bottom.join(", ")}</h3>

        {/* Parrainage */}
        <div className="mt-4">
          <h3 className="font-semibold">Parrainage</h3>
          <p>Partagez ce lien pour inviter vos amis :</p>
          <input
            type="text"
            value={referralLink}
            readOnly
            className="w-full p-2 mt-2"
          />
          <button
            onClick={() => navigator.clipboard.writeText(referralLink)}
            className="bg-green-500 text-white py-2 px-4 mt-2"
          >
            Copier le lien
          </button>
        </div>
      </div>
    </div>
  );
};

export default GamePage;
