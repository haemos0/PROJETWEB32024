import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import api from '../api';

const Signup = () => {
    const [username, setUsername] = useState('');
    const [password, setPassword] = useState('');
    const [message, setMessage] = useState('');
    const navigate = useNavigate();

    const handleSignup = async (e) => {
        e.preventDefault();
        try {
            const response = await api.post('/register', { username, password });
            setMessage(response.data.message);

            // Si inscription réussie, connectez automatiquement l'utilisateur
            const loginResponse = await api.post('/login', { username, password });
            const token = loginResponse.data.access_token;

            // Stocker le token dans localStorage
            localStorage.setItem('access_token', token);

            // Rediriger vers le tableau de bord
            navigate('/dashboard');
        } catch (error) {
            setMessage(error.response?.data?.message || "Erreur lors de l'inscription");
        }
    };

    return (
        <div>
            <h1>Inscription</h1>
            <form onSubmit={handleSignup}>
                <input
                    type="text"
                    placeholder="Nom d'utilisateur"
                    value={username}
                    onChange={(e) => setUsername(e.target.value)}
                />
                <input
                    type="password"
                    placeholder="Mot de passe"
                    value={password}
                    onChange={(e) => setPassword(e.target.value)}
                />
                <button type="submit">S'inscrire</button>
            </form>
            <p>{message}</p>
        </div>
    );
};

export default Signup;
