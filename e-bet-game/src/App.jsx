import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import HomePage from "./pages/HomePage"; // Page d'accueil
import Game from "./pages/Game"; // Interface du jeu
import AdminDashboard from "./components/AdminDashboard"; // Si nécessaire

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<HomePage />} />  {/* Accueil */}
        <Route path="/jeu" element={<Game />} />  {/* Page du jeu */}
        {/* Ajoute d'autres routes si nécessaire */}
      </Routes>
    </Router>
  );
}

export default App;
