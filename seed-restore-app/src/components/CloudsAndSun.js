// src/components/CloudsAndSun.js
import React from 'react';
import { Box } from '@mui/material';
import './CloudsAndSun.css';

const CloudsAndSun = () => {
  return (
    <Box className="sky">
      <div className="cloud cloud-1"></div>
      <div className="cloud cloud-2"></div>
      <div className="sun"></div>
    </Box>
  );
};

export default CloudsAndSun;