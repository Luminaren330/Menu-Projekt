import React from "react";
import { Link } from "react-router-dom";
import styles from "./Dashboard.module.scss";
import Navbar from "../Navbar/Navbar";

const Dashboard = () => {
  return (
    <>
      <Navbar></Navbar>
      <div className={styles.container}>
        <div className={styles.content}>
          <h3 className={styles.welcome}>Witamy</h3>
          <h1 className={styles.title}>Restauracja Felipino</h1>
          <p className={styles.subtitle}>Nowe smaki i dania</p>
          <Link to="/menu" className={styles.button}>
            Przejdź do menu
          </Link>
        </div>
      </div>
    </>
  );
};

export default Dashboard;
