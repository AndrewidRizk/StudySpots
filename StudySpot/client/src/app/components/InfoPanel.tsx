import React, { useState } from "react";
import styles from "../styles/InfoPanel.module.css";

const InfoPanel: React.FC = () => {
  const [isHovered, setIsHovered] = useState(false);

  return (
    <div
      className={styles.infoPanel}
      onMouseEnter={() => setIsHovered(true)}
      onMouseLeave={() => setIsHovered(false)}
    >
      {/* Icon */}
      <div className={styles.icon}>i</div>

      {/* Dropdown */}
      {isHovered && (
        <div className={styles.dropdown}>
            <h3>Important Notes:</h3>
            <ul>
              <li>Click on map pins or drop down to view room schedules for that building</li>
              <li>Buildings are sorted according to distance from your current location</li>
              <li>Displayed availability only reflects official class schedules</li>
              <li>Rooms may be locked, or occupied by unofficial meetings or study groups</li>
            </ul>
        </div>
      )}
    </div>
  );
};

export default InfoPanel;
