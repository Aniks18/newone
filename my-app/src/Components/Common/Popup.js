import React, { useState } from "react";
import axios from 'axios';
import { useNavigate } from "react-router-dom";
import "./Popup.css";

const Popup = ({ isVisible, onClose }) => {
  const [grievanceData, setGrievanceData] = useState({
    name: "",
    contactNumber: "",
    address: "",
    pincode: "",
    disasterType: "",
    assistanceRequired: "",
    description: "",
    peopleCount: "",
    urgencyLevel: "",
  });

  const navigate = useNavigate();

  const handleGrievanceSubmit = async (e) => {
    e.preventDefault();
    try {
      const response = await axios.post('http://localhost:4000/grievance', grievanceData);
      console.log('Grievance reported:', response.data);
      alert("Grievance reported");
      setTimeout(() => {
        navigate('/');
      }, 2000);
    } catch (error) {
      console.error("Grievance submission failed", error.response ? error.response.data.msg : error.message);
    }
  };

  return (
    <div className={`popup-modal ${isVisible ? "show" : ""}`}>
      <div className="popup-content">
        <button onClick={onClose} className="close-button">X</button>
        <h1>Report Grievance</h1>
        <form onSubmit={handleGrievanceSubmit}>
          <div className="input-box">
            <input
              type="text"
              placeholder="Your Name"
              value={grievanceData.name}
              onChange={(e) =>
                setGrievanceData({ ...grievanceData, name: e.target.value })
              }
              required
            />
          </div>
          <div className="input-box">
            <input
              type="tel"
              placeholder="Contact Number"
              pattern="\d{10}"
              title="Please enter exactly 10 digits"
              value={grievanceData.contactNumber}
              onChange={(e) =>
                setGrievanceData({ ...grievanceData, contactNumber: e.target.value })
              }
              required
            />
          </div>
          <div className="input-box">
            <input
              type="text"
              placeholder="Address"
              value={grievanceData.address}
              onChange={(e) =>
                setGrievanceData({ ...grievanceData, address: e.target.value })
              }
              required
            />
          </div>
          <div className="input-box">
            <input
              type="number"
              placeholder="Pincode"
              pattern="\d{6}"
              title="Please enter exactly 6 digits"
              value={grievanceData.pincode}
              onChange={(e) =>
                setGrievanceData({ ...grievanceData, pincode: e.target.value })
              }
              required
            />
          </div>
          <div className="input-box">
            <input
              type="text"
              placeholder="Disaster Type"
              value={grievanceData.disasterType}
              onChange={(e) =>
                setGrievanceData({ ...grievanceData, disasterType: e.target.value })
              }
              required
            />
          </div>
          <div className="input-box">
            <input
              type="text"
              placeholder="Assistance Required"
              value={grievanceData.assistanceRequired}
              onChange={(e) =>
                setGrievanceData({ ...grievanceData, assistanceRequired: e.target.value })
              }
              required
            />
          </div>
          <div className="input-box">
            <input
              type="text"
              placeholder="Description"
              value={grievanceData.description}
              onChange={(e) =>
                setGrievanceData({ ...grievanceData, description: e.target.value })
              }
              required
            />
          </div>
          <div className="input-box">
            <input
              type="number"
              placeholder="Number of People Requiring Assistance"
              value={grievanceData.peopleCount}
              onChange={(e) =>
                setGrievanceData({ ...grievanceData, peopleCount: e.target.value })
              }
              required
            />
          </div>
          <div className="input-box">
            <input
              type="text"
              placeholder="Urgency Level"
              value={grievanceData.urgencyLevel}
              onChange={(e) =>
                setGrievanceData({ ...grievanceData, urgencyLevel: e.target.value })
              }
              required
            />
          </div>
          <button type="submit" className="submitBtn">
            Submit
          </button>
        </form>
      </div>
    </div>
  );
};

export default Popup;
