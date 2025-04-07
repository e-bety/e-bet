import React, { useEffect, useState } from "react";

const Dashboard = () => {
    const [data, setData] = useState({
        total_transactions: 0,
        total_users: 0,
        users: [],
        transactions: [],
        recharges: [],
    });

    useEffect(() => {
        fetch("http://localhost:8000/dashboard-data")
            .then((response) => response.json())
            .then((data) => setData(data))
            .catch((error) => console.error("Erreur de chargement:", error));
    }, []);

    return (
        <div className="p-6 bg-gray-100 min-h-screen">
            <h1 className="text-3xl font-bold mb-4">Tableau de Bord</h1>

            <section className="mb-6">
                <h2 className="text-xl font-semibold">Résumé des Transactions</h2>
                <table className="w-full border-collapse border border-gray-300 mt-2">
                    <tbody>
                        <tr><th className="border p-2">Total Transactions</th><td className="border p-2">{data.total_transactions}</td></tr>
                        <tr><th className="border p-2">Nombre d'inscriptions</th><td className="border p-2">{data.total_users}</td></tr>
                    </tbody>
                </table>
            </section>

            <section className="mb-6">
                <h2 className="text-xl font-semibold">Utilisateurs</h2>
                <table className="w-full border-collapse border border-gray-300 mt-2">
                    <thead>
                        <tr>
                            <th className="border p-2">Nom</th>
                            <th className="border p-2">Solde</th>
                            <th className="border p-2">Statut</th>
                            <th className="border p-2">Parrainages</th>
                        </tr>
                    </thead>
                    <tbody>
                        {data.users.map((user, index) => (
                            <tr key={index}>
                                <td className="border p-2">{user.name}</td>
                                <td className="border p-2">{user.balance}</td>
                                <td className="border p-2">{user.status}</td>
                                <td className="border p-2">{user.referrals}</td>
                            </tr>
                        ))}
                    </tbody>
                </table>
            </section>

            <section className="mb-6">
                <h2 className="text-xl font-semibold">Transactions</h2>
                <table className="w-full border-collapse border border-gray-300 mt-2">
                    <thead>
                        <tr>
                            <th className="border p-2">Montant</th>
                            <th className="border p-2">Type</th>
                            <th className="border p-2">Statut</th>
                            <th className="border p-2">Date</th>
                        </tr>
                    </thead>
                    <tbody>
                        {data.transactions.map((tx, index) => (
                            <tr key={index}>
                                <td className="border p-2">{tx.amount}</td>
                                <td className="border p-2">{tx.type}</td>
                                <td className="border p-2">{tx.status}</td>
                                <td className="border p-2">{tx.date}</td>
                            </tr>
                        ))}
                    </tbody>
                </table>
            </section>

            <section>
                <h2 className="text-xl font-semibold">Demandes de Recharge</h2>
                <table className="w-full border-collapse border border-gray-300 mt-2">
                    <thead>
                        <tr>
                            <th className="border p-2">Utilisateur</th>
                            <th className="border p-2">Montant</th>
                            <th className="border p-2">Statut</th>
                        </tr>
                    </thead>
                    <tbody>
                        {data.recharges.map((rc, index) => (
                            <tr key={index}>
                                <td className="border p-2">{rc.user}</td>
                                <td className="border p-2">{rc.amount}</td>
                                <td className="border p-2">{rc.status}</td>
                            </tr>
                        ))}
                    </tbody>
                </table>
            </section>
        </div>
    );
};

export default Dashboard;
