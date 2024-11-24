import React, { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import api from '../api';



const Login = () => {
    const [username, setUsername] = useState('');
    const [password, setPassword] = useState('');
    const [message, setMessage] = useState('');
    const navigate = useNavigate();

    const handleLogin = async (e) => {
        e.preventDefault();
        try {
            const response = await api.post('/login', { username, password });
            const token = response.data.access_token;
    
            // Stocker le token dans le stockage local
            localStorage.setItem('access_token', token);
    
            setMessage('Connexion réussie');
            navigate('/dashboard'); // Rediriger vers le tableau de bord
        } catch (error) {
            setMessage(error.response?.data?.message || 'Erreur');
        }
    };
    

    return (
        <div>
            <h1>Connexion</h1>
            <form onSubmit={handleLogin}>
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
                <button type="submit">Se connecter</button>
            </form>
            <p>{message}</p>
            <p>
                Pas encore de compte ? <Link to="/signup">Inscrivez-vous ici</Link>
            </p>
        </div>
    );
};

export default Login;
