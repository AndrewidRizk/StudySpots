import React, { useState } from "react";
import styles from "../styles/InfoPanel.module.css";

interface InfoPanelProps {
  info: string; // The information to display in the dropdown
}

const InfoPanel: React.FC<InfoPanelProps> = ({ info }) => {
  const [isHovered, setIsHovered] = useState(false);

  return (
    <div
      className={styles.infoPanel}
      onMouseEnter={() => setIsHovered(true)}
      onMouseLeave={() => setIsHovered(false)}
    >
      {/* Icon */}
      <div className={styles.icon}>!</div>

      {/* Dropdown */}
      {isHovered && (
        <div className={styles.dropdown}>
          <p>{info}</p>
        </div>
      )}
    </div>
  );
};

export default InfoPanel;
