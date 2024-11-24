import React from 'react';
import { Navigate } from 'react-router-dom';

const ProtectedRoute = ({ children }) => {
    const token = localStorage.getItem('access_token');

    if (!token) {
        // Rediriger l'utilisateur non authentifié vers la page de connexion
        return <Navigate to="/login" />;
    }

    return children;
};

export default ProtectedRoute;
