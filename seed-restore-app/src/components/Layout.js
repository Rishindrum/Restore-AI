// src/components/Layout.js
import React from 'react';
import './Layout.css'; // Add styles for clouds, plants, etc.

const Layout = ({ children }) => {
  return (
    <div className="layout-container">
      <div className="clouds">
        {/* Add cloud images or divs with CSS animations */}
      </div>
      <div className="content">
        {children}
      </div>
      <div className="plants">
        {/* Add plant images or divs with CSS animations */}
      </div>
    </div>
  );
};

export default Layout;