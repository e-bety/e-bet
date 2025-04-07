   // src/components/EbetGame.jsx
import React, { useState } from 'react';
import api from '../api';

const MAX_LOTS = 5;

const EbetGame = () => {
  const [lots, setLots] = useState([{ num1: '', num2: '' }]);
  const [mise, setMise] = useState(50);
  const [resultat, setResultat] = useState(null);
  const [erreur, setErreur] = useState(null);
  const [loading, setLoading] = useState(false);

  const ajouterLot = () => {
    if (lots.length < MAX_LOTS) {
      setLots([...lots, { num1: '', num2: '' }]);
    }
  };

  const supprimerLot = (index) => {
    const newLots = lots.filter((_, i) => i !== index);
    setLots(newLots);
  };

  const modifierLot = (index, champ, valeur) => {
    const newLots = [...lots];
    newLots[index][champ] = parseInt(valeur) || '';
    setLots(newLots);
  };

  const lancerPartie = async () => {
    try {
      setLoading(true);
      setErreur(null);
      const res = await api.post('/jouer', {
        lots,
        mise: parseInt(mise),
      });
      setResultat(res.data);
    } catch (err) {
      setErreur(err.response?.data?.detail || 'Erreur pendant la partie');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="max-w-xl mx-auto bg-white shadow-md rounded-xl p-6 mt-6 dark:bg-zinc-900">
      <h1 className="text-2xl font-bold mb-4 text-center">🎮 Jouer à E.Bet</h1>

      {lots.map((lot, index) => (
        <div key={index} className="flex gap-2 items-center mb-2">
          <input
            type="number"
            min={1}
            max={99}
            placeholder="Num 1"
            value={lot.num1}
            onChange={(e) => modifierLot(index, 'num1', e.target.value)}
            className="w-20 p-2 border rounded"
          />
          <input
            type="number"
            min={1}
            max={99}
            placeholder="Num 2"
            value={lot.num2}
            onChange={(e) => modifierLot(index, 'num2', e.target.value)}
            className="w-20 p-2 border rounded"
          />
          {index > 0 && (
            <button
              onClick={() => supprimerLot(index)}
              className="text-red-500 text-sm"
            >
              Supprimer
            </button>
          )}
        </div>
      ))}

      {lots.length < MAX_LOTS && (
        <button
          onClick={ajouterLot}
          className="bg-gray-200 dark:bg-zinc-700 p-2 rounded mb-4"
        >
          ➕ Ajouter un lot
        </button>
      )}

      <div className="mb-4">
        <label className="block mb-1">💰 Mise par lot (min 50F)</label>
        <input
          type="number"
          min={50}
          value={mise}
          onChange={(e) => setMise(e.target.value)}
          className="w-full p-2 border rounded"
        />
      </div>

      <button
        onClick={lancerPartie}
        disabled={loading}
        className="bg-blue-600 hover:bg-blue-700 text-white p-2 w-full rounded"
      >
        {loading ? 'Chargement...' : '🎲 Lancer la partie'}
      </button>

      {erreur && <p className="text-red-500 mt-4">{erreur}</p>}

      {resultat && (
        <div className="mt-6 bg-green-100 p-4 rounded dark:bg-green-800 dark:text-white">
          <h2 className="text-lg font-bold mb-2">🎉 Résultat du tirage</h2>
          <p>Groupe haut : {resultat.haut?.join(', ')}</p>
          <p>Groupe bas : {resultat.bas?.join(', ')}</p>
          <p className="font-semibold mt-2">Gain total : {resultat.gain} F</p>
        </div>
      )}
    </div>
  );
};

export default EbetGame;                                          