import React, { useState, useEffect } from "react";

function DashboardStats() {
  const [stats, setStats] = useState({
    totalUsers: 0,
    totalTransactions: 0,
    totalRevenue: 0,
  });

  useEffect(() => {
    // Simule des données récupérées depuis une API ou une base de données
    setStats({
      totalUsers: 1500,
      totalTransactions: 2450,
      totalRevenue: 120000,
    });
  }, []);

  return (
    <div className="dashboard-stats">
      <div className="stat-item">
        <h3>Utilisateurs Totaux</h3>
        <p>{stats.totalUsers}</p>
      </div>
      <div className="stat-item">
        <h3>Transactions Totales</h3>
        <p>{stats.totalTransactions}</p>
      </div>
      <div className="stat-item">
        <h3>Revenu Total</h3>
        <p>{stats.totalRevenue} F</p>
      </div>
    </div>
  );
}

export default DashboardStats;
