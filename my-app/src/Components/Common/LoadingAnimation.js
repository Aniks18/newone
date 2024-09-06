import React from 'react';
import './LoadingAnimation.css';

const LoadingAnimation = ({ message, show }) => {
  return (
    show && (
      <div className="loading-overlay">
        <div className="loading-card">
          <div className="loading-spinner"></div>
          <div className="loading-message">{message}</div>
        </div>
      </div>
    )
  );
};

const LoadingAnimationWrapper = ({ show }) => {
  return <LoadingAnimation message="Processing your request..." show={show} />;
};

export default LoadingAnimationWrapper;