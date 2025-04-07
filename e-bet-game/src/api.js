// src/api.js
import axios from 'axios';

const api = axios.create({
  baseURL: 'http://localhost:8000', // Remplace par ton domaine réel si nécessaire
});

api.interceptors.request.use((config) => {
  const token = localStorage.getItem('token');

  if (token) {
    console.log('🔐 Token envoyé avec la requête :', token); // 👈 Log du token
    config.headers.Authorization = `Bearer ${token}`;
  } else {
    console.warn('⚠️ Aucun token trouvé dans localStorage');
  }

  return config;
});

export default api;
