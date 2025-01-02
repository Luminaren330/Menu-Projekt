import styles from "./Workers.module.scss";
import Navbar from "../Navbar/Navbar";
import React, { useState, useEffect, useCallback } from "react";
import Axios from "axios";
import { Link } from "react-router-dom";

const Workers = () => {
  const [workers, setWorkers] = useState([]);
  const [index, setIndex] = useState(0);

  const getWorkers = useCallback(() => {
    Axios.get("http://127.0.01:5000/users").then((res) => {
      setWorkers(res.data.employee_records || []);
      console.log(workers);
    });
  }, []);

  useEffect(() => {
    getWorkers();
  }, [getWorkers]);

  const worker = workers[index] || {};
  const { firstname, lastname, telephone, position, email, is_available } =
    worker;
  return (
    <>
      <Navbar></Navbar>
      <section className={styles.section}>
        <div className={styles.title}>
          <h2 className={styles.header}>Pracownicy</h2>
          <div className={styles.underline}></div>
        </div>
        <div className={styles.workers}>
          <div className={styles.names}>
            {workers.map((worker, indx) => {
              return (
                <button
                  key={worker.account_id}
                  onClick={() => setIndex(indx)}
                  className={`${styles.nameBtn} ${
                    indx === index && styles.activeBtn
                  }`}
                >
                  {worker.firstname}
                </button>
              );
            })}
          </div>
          <article className={styles.worker}>
            <h3>
              {firstname} {lastname}
            </h3>
            <h4>{position}</h4>
            <div className={styles.phone}>
              <p>Nr telefonu: </p>
              <p>{telephone}</p>
            </div>
            <div className={styles.phone}>
              <p>Email: </p>
              <p>{email}</p>
            </div>
            <div className={styles.phone}>
              <p>Czy jest dostępny </p>
              <input type="checkbox" checked={is_available} readOnly />
            </div>
            <div className={styles.add}>
              <Link to="/workers/addworker" className={styles.addWorker}>
                Dodaj pracownika
              </Link>
            </div>
          </article>
        </div>
      </section>
    </>
  );
};

export default Workers;
