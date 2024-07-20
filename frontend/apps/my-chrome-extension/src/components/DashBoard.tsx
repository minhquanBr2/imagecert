// src/components/Dashboard.tsx

import React from 'react';

const Dashboard: React.FC = () => {
  return (
    <div>
      <h1>Welcome to the Dashboard</h1>
      <p>This is a protected route only accessible after login.</p>
    </div>
  );
};

export default Dashboard;
