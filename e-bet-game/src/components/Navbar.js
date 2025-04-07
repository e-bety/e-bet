import React from "react";

function Navbar() {
  return (
    <div className="navbar">
      <div className="navbar-left">
        <h1>Tableau de bord</h1>
      </div>
      <div className="navbar-right">
        <button className="logout-btn">Déconnexion</button>
      </div>
    </div>
  );
}

export default Navbar;
