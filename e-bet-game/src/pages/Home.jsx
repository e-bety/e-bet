// Home.jsx
import { Link } from "react-router-dom";

function Home() {
  return (
    <div className="p-10 flex flex-col items-center justify-center">
      <h1 className="text-3xl font-bold mb-4">Bienvenue sur E.Bet</h1>
      <Link to="/jeu">
        <button className="bg-green-500 text-white px-4 py-2 rounded-lg hover:bg-green-600 transition">
          Lancer le jeu
        </button>
      </Link>
    </div>
  );
}

export default Home;
