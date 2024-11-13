import styles from "./AddNewProduct.module.scss";
import React, { useState } from "react";
import Navbar from "../Navbar/Navbar";
import StringInput from "../AddReview/StringInput";
import FloatInput from "../AddReview/FloatInput";
import { useNavigate } from "react-router-dom";
import TextAreaInput from "../AddReview/TextAreaInput";
import Dropdown from "../AddReview/Dropdown";

const AddNewProduct = () => {
  const [name, setName] = useState("");
  const [photo, setPhoto] = useState("");
  const [ingredients, setIngredients] = useState("A");
  const [unitPrice, setUnitPrice] = useState(0);
  const [category, setCategory] = useState("Filtr");
  const [wrong, setWrong] = useState(false);
  const [badPrice, setBadPrice] = useState(false);
  const navigate = useNavigate();

  const categoryOptions = ["Przystawka", "Wino", "Główne danie", "Deser"];

  const CategorySet = (event) => {
    setCategory(event.target.value);
  };

  const addNewProduct = () => {
    setBadPrice(false);
    setWrong(false);
    if (name.length < 5 || ingredients.length < 5) {
      setWrong(true);
    } else if (unitPrice <= 0) {
      setBadPrice(true);
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
            <h1 className={styles.menuHeader}>Dodaj nowe danie</h1>
            <div className={styles.form}>
              <StringInput string="Nazwa: " setParameter={setName} />
              <FloatInput string="Cena: " setParameter={setUnitPrice} />
              <Dropdown
                options={categoryOptions}
                value={category}
                string="Kategoria"
                setFunction={CategorySet}
              />
              <TextAreaInput
                string="Składniki: "
                setParameter={setIngredients}
              />
              <StringInput string="Link do zdjęcia: " setParameter={setPhoto} />
              {wrong && (
                <div className={styles.wrong}>
                  <h4>Pola nazwa lub składniki są za krótkie. Min 5 znaków</h4>
                </div>
              )}
              {badPrice && (
                <div className={styles.wrong}>
                  <h4>Cena jest mniejsza od 0</h4>
                </div>
              )}
            </div>
            <div className={styles.center}>
              <button
                className={styles.addProduct}
                onClick={() => {
                  addNewProduct();
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

export default AddNewProduct;
