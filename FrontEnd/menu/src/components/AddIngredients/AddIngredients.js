import styles from "./AddIngredients.module.scss";
import React, { useEffect, useState } from "react";
import Navbar from "../Navbar/Navbar";
import StringInput from "../AddReview/StringInput";
import { useNavigate } from "react-router-dom";
import Axios from "axios";
import Popup from "../Popup/Popup";

const AddIngredient = () => {
  const [name, setName] = useState("");
  const [wrong, setWrong] = useState(false);
  const navigate = useNavigate();
  const [isPopupVisible, setIsPopupVisible] = useState(false);

  const togglePopup = (value) => {
    setIsPopupVisible(value);
  };

  const addNewIngredient = () => {
    setWrong(false);
    if (name.length < 5) {
      setWrong(true);
    } else {
      Axios.post("http://127.0.0.1:5000/ingredients", {
        name: name,
      })
        .then(() => {
          togglePopup(true);
          setTimeout(() => {
            togglePopup(false);
          }, 5000);
        })
        .catch((e) => {
          alert("Brak autoryzacji");
        });
    }
  };

  return (
    <>
      <Navbar></Navbar>
      {isPopupVisible && (
        <Popup
          message="Dodano nowy składnik!"
          onClose={() => togglePopup(false)}
        />
      )}
      <div>
        <div className={styles.container}>
          <div className={styles.menu}>
            <h1 className={styles.menuHeader}>Dodaj nowy składnik</h1>
            <div className={styles.form}>
              <StringInput string="Nazwa: " setParameter={setName} />
              {wrong && (
                <div className={styles.wrong}>
                  <h4>Pola nazwa jest za krótkie. Min 5 znaków</h4>
                </div>
              )}
            </div>
            <div className={styles.center}>
              <button
                className={styles.addProduct}
                onClick={() => {
                  addNewIngredient();
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

export default AddIngredient;
