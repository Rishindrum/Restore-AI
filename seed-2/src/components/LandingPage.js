// src/components/LandingPage.js
import React from 'react';
import { Link } from 'react-router-dom';
import './LandingPage.css';

const LandingPage = () => {
    return (
        <div className="landing-page">
            <div className="overlay"></div>
            <h1>Germinance</h1>
            <p className="description">Reviving the Blackland Prairie, one seed at a time.</p>
            <Link to="/chat" className="start-button">
                Let's get started!
                <span className="arrow">→</span>
            </Link>
        </div>
    );
};

export default LandingPage;