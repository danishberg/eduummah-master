// Dashboard.js
import React from 'react';
import { Outlet } from 'react-router-dom';
import DashboardHeader from './DashboardHeader'; // Assuming this is the path

const Dashboard = () => {
  return (
    <>
      <DashboardHeader />
      <div className="dashboard-content">
        <Outlet />  {/* This will render the nested route's component */}
      </div>
    </>
  );
};

export default Dashboard;
