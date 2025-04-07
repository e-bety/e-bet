import React from "react";
import { Link } from "react-router-dom";
import { FaHome, FaChartBar, FaListAlt, FaCog } from "react-icons/fa";

function Sidebar() {
  return (
    <div className="sidebar">
      <div className="logo">
        <h2>Admin Panel</h2>
      </div>
      <ul className="menu">
        <li>
          <Link to="/" className="menu-item">
            <FaHome /> Accueil
          </Link>
        </li>
        <li>
          <Link to="/stats" className="menu-item">
            <FaChartBar /> Statistiques
          </Link>
        </li>
        <li>
          <Link to="/transactions" className="menu-item">
            <FaListAlt /> Transactions
          </Link>
        </li>
        <li>
          <Link to="/settings" className="menu-item">
            <FaCog /> Paramètres
          </Link>
        </li>
      </ul>
    </div>
  );
}

export default Sidebar;
