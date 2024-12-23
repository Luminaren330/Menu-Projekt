import styles from "../AddNewProduct/AddNewProduct.module.scss";
import React, { useState } from "react";
import Navbar from "../Navbar/Navbar";
import StringInput from "../AddReview/StringInput";
import FloatInput from "../AddReview/FloatInput";
import { useNavigate } from "react-router-dom";
import TextAreaInput from "../AddReview/TextAreaInput";
import Dropdown from "../AddReview/Dropdown";
import FormatInput from "../AddReview/FormatInput";

const AddWorker = () => {
  const [name, setName] = useState("");
  const [surname, setSurname] = useState("");
  const [phoneNumber, setPhoneNumber] = useState("");
  const [category, setCategory] = useState("Kelner");
  const [wrong, setWrong] = useState(false);
  const navigate = useNavigate();

  const categoryOptions = ["Kelner", "Kucharz"];

  const CategorySet = (event) => {
    setCategory(event.target.value);
  };

  const addWorker = () => {
    setWrong(false);
    if (name.length < 3 || surname.length < 3) {
      setWrong(true);
    } else {
      //TODO dodać jak baza
    }
  };

  return (
    <>
      <Navbar></Navbar>
      <div>
        <div className={styles.container}>
          <div className={styles.menu}>
            <h1 className={styles.menuHeader}>Dodaj nowego pracownika</h1>
            <div className={styles.form}>
              <StringInput string="Imię: " setParameter={setName} />
              <StringInput string="Nazwisko: " setParameter={setSurname} />
              {/* <Dropdown
                options={categoryOptions}
                value={category}
                string="Rola"
                setFunction={CategorySet}
              /> */}
              <FormatInput
                id="phoneNumber"
                string="Nr telefonu:"
                setParameter={setPhoneNumber}
                format="Format: 123456124"
                pattern="[0-9]{9}"
              />{" "}
              {wrong && (
                <div className={styles.wrong}>
                  <h4>Pola imię lub nazwisko są za krótkie. Min 3 znaki</h4>
                </div>
              )}
            </div>
            <div className={styles.center}>
              <button
                className={styles.addProduct}
                onClick={() => {
                  addWorker();
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

export default AddWorker;
