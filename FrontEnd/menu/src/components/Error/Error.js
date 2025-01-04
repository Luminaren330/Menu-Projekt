import styles from "./Error.module.scss";
import React from "react";
import { useNavigate } from "react-router-dom";
const Error = () => {
  const navigate = useNavigate();
  return (
    <div className={styles.info}>
      <h1 className={styles.header}>Error</h1>
      <p>Nie można było połączyć się z serwerem. Spróbuj ponownie</p>
      <button
        className={styles.navigate}
        onClick={() => navigate("/dashboard")}
      >
        Wróć do strony głównej
      </button>
    </div>
  );
};
export default Error;
