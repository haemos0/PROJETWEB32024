import React, { useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import api from '../api';

const Dashboard = () => {
    const navigate = useNavigate();

    useEffect(() => {
        const checkAuth = async () => {
            const token = localStorage.getItem('access_token');
            if (!token) {
                // Pas de token, rediriger vers la page de connexion
                navigate('/login');
                return;
            }

            try {
                // Vérifier la validité du token en envoyant une requête au backend
                await api.get('/protected', {
                    headers: {
                        Authorization: `Bearer ${token}`,
                    },
                });
            } catch (error) {
                // Token invalide ou expiré, rediriger vers la page de connexion
                console.error('Accès refusé, redirection vers login');
                localStorage.removeItem('access_token'); // Nettoyer le stockage
                navigate('/login');
            }
        };

        checkAuth();
    }, [navigate]);

    const handleLogout = async () => {
        try {
            const token = localStorage.getItem('access_token');
            await api.post('/logout', {}, {
                headers: {
                    Authorization: `Bearer ${token}`,
                },
            });
            localStorage.removeItem('access_token'); // Supprimer le token
            navigate('/login'); // Rediriger vers login
        } catch (error) {
            console.error('Erreur lors de la déconnexion', error);
        }
    };

    return (
        <div>
            <h1>Tableau de bord</h1>
            <button onClick={handleLogout}>Se déconnecter</button>
        </div>
    );
};

export default Dashboard;
