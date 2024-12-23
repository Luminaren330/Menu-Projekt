import styles from "./Workers.module.scss";
import Navbar from "../Navbar/Navbar";
import React, { useState, useEffect } from "react";
import Axios from "axios";
import { Link } from "react-router-dom";

const Workers = () => {
  const [workers, setWorkers] = useState([]);
  const [index, setIndex] = useState(0);

  const getWorkers = async () => {
    // await Axios.get("http://localhost:3001/workers").then((response) => {
    //   setWorkers(response.data);
    // });
  };

  useEffect(() => {
    getWorkers();
  }, []);

  const worker = workers[index] || {};
  const { Name, Surname, PhoneNumber, Position } = worker;
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
                  key={worker.WorkerId}
                  onClick={() => setIndex(indx)}
                  className={`${styles.nameBtn} ${
                    indx === index && styles.activeBtn
                  }`}
                >
                  {worker.Name}
                </button>
              );
            })}
          </div>
          <article className={styles.worker}>
            <h3>
              {Name} {Surname}
            </h3>
            <h4>{Position}</h4>
            <div className={styles.phone}>
              <p>Nr telefonu: </p>
              <p>{PhoneNumber}</p>
            </div>
          </article>
        </div>
        <div className={styles.add}>
          <Link to="/workers/addworker" className={styles.addWorker}>
            Dodaj pracownika
          </Link>
        </div>
      </section>
    </>
  );
};

export default Workers;
