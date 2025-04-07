import express from 'express';
import { insertBet, getUserBalance } from './database.js';

const app = express();
const PORT = 3000;

app.get('/bet', (req, res) => {
  const { userId, lotNumbers, betAmount } = req.query;
  insertBet(userId, lotNumbers, betAmount);
  res.send('Mise insérée');
});

app.get('/balance', (req, res) => {
  const { userId } = req.query;
  getUserBalance(userId);
  res.send('Solde de l\'utilisateur récupéré');
});

app.listen(PORT, () => {
  console.log(`Serveur en écoute sur le port ${PORT}`);
});
