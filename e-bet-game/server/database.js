import { Client } from 'pg';

// Créez une instance du client PostgreSQL
const client = new Client({
  host: 'localhost',       // Hôte de la base de données
  port: 5432,              // Port par défaut pour PostgreSQL
  user: 'emerson',         // Utilisateur de la base de données
  password: 'carso22karas', // Mot de passe de l'utilisateur
  database: 'E.Bet',  // Nom de la base de données
});

// Connectez-vous à la base de données
client.connect();

// Exemple de fonction pour insérer une mise
function insertBet(userId, lotNumbers, betAmount) {
  const query = 'INSERT INTO bets (user_id, lot_numbers, bet_amount) VALUES ($1, $2, $3)';
  client.query(query, [userId, lotNumbers, betAmount], (err, res) => {
    if (err) {
      console.error('Erreur lors de l\'insertion de la mise', err);
    } else {
      console.log('Mise insérée avec succès');
    }
  });
}

// Exemple de fonction pour obtenir les gains d'un utilisateur
function getUserBalance(userId) {
  const query = 'SELECT balance FROM users WHERE user_id = $1';
  client.query(query, [userId], (err, res) => {
    if (err) {
      console.error('Erreur lors de la récupération du solde', err);
    } else {
      console.log('Solde de l\'utilisateur:', res.rows[0].balance);
    }
  });
}
