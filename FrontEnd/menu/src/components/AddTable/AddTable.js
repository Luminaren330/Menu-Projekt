import styles from "./AddTable.module.scss";
import React, { useState } from "react";
import Navbar from "../Navbar/Navbar";
import TextAreaInput from "../AddReview/TextAreaInput";
import Popup from "../Popup/Popup";
import Axios from "axios";

const AddTable = () => {
  const [capacity, setCapacity] = useState(4); // Domyślnie wybrane 4
  const [desc, setDesc] = useState("");
  const [wrong, setWrong] = useState(false);
  const [isPopupVisible, setIsPopupVisible] = useState(false);

  const togglePopup = (value) => {
    setIsPopupVisible(value);
  };

  const addNewtable = () => {
    setWrong(false);
    if (desc.length < 5) {
      setWrong(true);
    } else {
      Axios.post("http://127.0.0.1:5000/tables", {
        capacity: capacity,
        description: desc,
      })
        .then(() => {
          togglePopup(true);
          setTimeout(() => {
            togglePopup(false);
          }, 5000);
        })
        .catch(() => {
          alert("Brak autoryzacji");
        });
    }
  };

  return (
    <>
      <Navbar />
      {isPopupVisible && (
        <Popup
          message="Dodano nowy stolik!"
          onClose={() => togglePopup(false)}
        />
      )}
      <div>
        <div className={styles.container}>
          <div className={styles.menu}>
            <h1 className={styles.menuHeader}>Dodaj nowy stół</h1>
            <div className={styles.form}>
              <div className={styles.capacityGroup}>
                <label className={styles.formLabel}>Pojemność stolika</label>
                <div className={styles.buttons}>
                  <button
                    type="button"
                    className={`${styles.capacityButton} ${
                      capacity === 2 ? styles.selected : ""
                    }`}
                    onClick={() => setCapacity(2)}
                  >
                    2
                  </button>
                  <button
                    type="button"
                    className={`${styles.capacityButton} ${
                      capacity === 4 ? styles.selected : ""
                    }`}
                    onClick={() => setCapacity(4)}
                  >
                    4
                  </button>
                  <button
                    type="button"
                    className={`${styles.capacityButton} ${
                      capacity === 6 ? styles.selected : ""
                    }`}
                    onClick={() => setCapacity(6)}
                  >
                    6
                  </button>
                </div>
              </div>
              <TextAreaInput string="Opis: " setParameter={setDesc} />
              {wrong && (
                <div className={styles.wrong}>
                  <h4>Pole opis jest za krótkie. Min 5 znaków</h4>
                </div>
              )}
            </div>
            <div className={styles.center}>
              <button
                className={styles.addProduct}
                onClick={() => {
                  addNewtable();
                }}
              >
                Dodaj
              </button>
            </div>
          </div>
        </div>
      </div>
    </>
  );
};

export default AddTable;
