import styles from "./Workers.module.scss";
import Navbar from "../Navbar/Navbar";
import React, { useState, useEffect, useCallback } from "react";
import Axios from "axios";
import { Link } from "react-router-dom";

const Workers = () => {
  const [workers, setWorkers] = useState([]);
  const [index, setIndex] = useState(0);
  const [isEditing, setIsEditing] = useState(false);
  const [editedWorker, setEditedWorker] = useState({});

  const getWorkers = useCallback(() => {
    Axios.get("http://127.0.0.1:5000/users").then((res) => {
      setWorkers(res.data.employee_records || []);
    });
  }, []);

  useEffect(() => {
    getWorkers();
  }, [getWorkers]);

  const worker = workers[index] || {};
  const { firstname, lastname, telephone, position, email, is_available } =
    worker;

  const handleEditClick = () => {
    setIsEditing(true);
    setEditedWorker({
      firstname,
      lastname,
      telephone,
      position,
      email,
      is_available,
    });
  };

  const cancelClick = () => {
    setIsEditing(false);
  };

  const handleChange = (e) => {
    const { name, value, type, checked } = e.target;
    setEditedWorker({
      ...editedWorker,
      [name]: type === "checkbox" ? checked : value,
    });
  };

  const handleSaveClick = () => {
    Axios.patch(
      `http://127.0.0.1:5000/users?id=${worker.account_id}`,
      editedWorker
    )
      .then((res) => {
        console.log("Updated worker:", res.data);
        setIsEditing(false);
        getWorkers();
      })
      .catch((err) => console.error("Error updating worker:", err));
  };

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
              {isEditing ? (
                <input
                  type="text"
                  name="firstname"
                  value={editedWorker.firstname}
                  onChange={handleChange}
                />
              ) : (
                `${firstname} ${lastname}`
              )}{" "}
              {isEditing ? (
                <input
                  type="text"
                  name="lastname"
                  value={editedWorker.lastname}
                  onChange={handleChange}
                />
              ) : null}
            </h3>
            <h4>
              {isEditing ? (
                <input
                  type="text"
                  name="position"
                  value={editedWorker.position}
                  onChange={handleChange}
                />
              ) : (
                position
              )}
            </h4>
            <div className={styles.phone}>
              <p>Nr telefonu: </p>
              {isEditing ? (
                <input
                  type="text"
                  name="telephone"
                  value={editedWorker.telephone}
                  onChange={handleChange}
                />
              ) : (
                <p>{telephone}</p>
              )}
            </div>
            <div className={styles.phone}>
              <p>Email: </p>
              {isEditing ? (
                <input
                  type="email"
                  name="email"
                  value={editedWorker.email}
                  onChange={handleChange}
                />
              ) : (
                <p>{email}</p>
              )}
            </div>
            <div className={styles.phone}>
              <p>Czy jest dostępny: </p>
              {isEditing ? (
                <input
                  type="checkbox"
                  name="is_available"
                  checked={editedWorker.is_available}
                  onChange={handleChange}
                />
              ) : (
                <input type="checkbox" checked={is_available} readOnly />
              )}
            </div>
            <div className={styles.add}>
              <Link to="/workers/addworker" className={styles.addWorker}>
                Dodaj pracownika
              </Link>
              {isEditing ? (
                <div className={styles.newBtns}>
                  <button onClick={cancelClick} className={styles.addWorker}>
                    Anuluj
                  </button>
                  <button
                    onClick={handleSaveClick}
                    className={styles.addWorker}
                  >
                    Zapisz
                  </button>
                </div>
              ) : (
                <div className={styles.newBtns}>
                  <button
                    onClick={handleEditClick}
                    className={styles.addWorker}
                  >
                    Edytuj
                  </button>
                </div>
              )}
            </div>
          </article>
        </div>
      </section>
    </>
  );
};

export default Workers;
