import React from "react";
import ReactDOM from "react-dom/client";
import App from "./App.jsx";
import "./index.css";
import Dashboard from "./pages/DashboardPage.jsx";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";


ReactDOM.createRoot(document.getElementById("root")).render(
  <React.StrictMode>
    <App />
  </React.StrictMode>
);

// Enregistrement du Service Worker
if ("serviceWorker" in navigator) {
  window.addEventListener("load", () => {
    navigator.serviceWorker
      .register("/sw.js")
      .then(() => console.log("✅ Service Worker enregistré !"))
      .catch((err) => console.log("❌ Erreur Service Worker:", err));
  });
}

// ➡️ Gestion de la bannière d'installation PWA
window.addEventListener("beforeinstallprompt", (event) => {
  event.preventDefault(); // Empêche l'affichage automatique
  let deferredPrompt = event;

  console.log("📌 L'événement beforeinstallprompt a été déclenché");

  // Ajouter un bouton pour déclencher l'installation
  const installButton = document.createElement("button");
  installButton.innerText = "📲 Installer E.Bet";
  installButton.style.position = "fixed";
  installButton.style.bottom = "20px";
  installButton.style.right = "20px";
  installButton.style.padding = "10px 20px";
  installButton.style.backgroundColor = "#28a745";
  installButton.style.color = "white";
  installButton.style.border = "none";
  installButton.style.borderRadius = "5px";
  installButton.style.cursor = "pointer";
  installButton.style.fontSize = "16px";
  installButton.style.boxShadow = "0px 4px 6px rgba(0, 0, 0, 0.1)";

  document.body.appendChild(installButton);

  installButton.addEventListener("click", () => {
    deferredPrompt.prompt();
    deferredPrompt.userChoice.then((choiceResult) => {
      if (choiceResult.outcome === "accepted") {
        console.log("🎉 L'utilisateur a accepté l'installation !");
      } else {
        console.log("❌ L'utilisateur a refusé l'installation.");
      }
      deferredPrompt = null;
      installButton.remove(); // Supprime le bouton après l'action
    });
  });
});
