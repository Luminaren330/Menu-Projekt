import styles from "./AddNewProduct.module.scss";
import React, { useEffect, useState } from "react";
import Navbar from "../Navbar/Navbar";
import StringInput from "../AddReview/StringInput";
import FloatInput from "../AddReview/FloatInput";
import { useNavigate } from "react-router-dom";
import TextAreaInput from "../AddReview/TextAreaInput";
import MultiSelectInput from "../AddReview/MultiSelectInput";
import Dropdown from "../AddReview/Dropdown";
import Axios from "axios";

const AddNewProduct = () => {
  const [name, setName] = useState("");
  const [photo, setPhoto] = useState(null);
  const [preview, setPreview] = useState("");
  const [description, setDescription] = useState("");
  const [unitPrice, setUnitPrice] = useState(0);
  const [category, setCategory] = useState("");
  const [wrong, setWrong] = useState(false);
  const [badPrice, setBadPrice] = useState(false);
  const navigate = useNavigate();
  const [categoryOptions, setCategoryOptions] = useState([]);
  const [ingredientOptions, setIngredientOptions] = useState([]);
  const [selectedIngredients, setSelectedIngredients] = useState([]);

  useEffect(() => {
    Axios.get("http://127.0.01:5000/categories").then((res) => {
      const categoryNames = (res.data.records || []).map((item) => item.name);
      setCategoryOptions(categoryNames);
      setCategory(categoryNames[0]);
    });
    Axios.get("http://127.0.01:5000/ingredients").then((res) => {
      const ingredientNames = (res.data.records || []).map((item) => item.name);
      setIngredientOptions(ingredientNames);
    });
  }, []);

  const CategorySet = (event) => {
    setCategory(event.target.value);
  };

  const handleFileChange = (event) => {
    const file = event.target.files[0];
    if (file) {
      setPhoto(file);
      setPreview(URL.createObjectURL(file));
    }
  };

  const addNewProduct = () => {
    setBadPrice(false);
    setWrong(false);
    if (name.length < 5 || description.length < 5) {
      setWrong(true);
    } else if (unitPrice <= 0) {
      setBadPrice(true);
    } else {
      const formData = new FormData();
      formData.append("category", category);
      formData.append("ingredients", selectedIngredients);
      formData.append("name", name);
      formData.append("price", unitPrice);
      formData.append("description", description);
      formData.append("photo", photo);
      Axios.post("http://127.0.0.1:5000/dishes", formData, {
        headers: {
          "Content-Type": "multipart/form-data",
        },
      })
        .then(() => {
          alert("Pomyślnie dodano nowe danie");
          navigate("/menu");
        })
        .catch((e) => {
          alert("Brak autoryzacji");
        });
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
              <MultiSelectInput
                id="ingredients"
                options={ingredientOptions}
                string="Składniki:"
                selectedItems={selectedIngredients}
                setSelectedItems={setSelectedIngredients}
              />
              <TextAreaInput string="Opis: " setParameter={setDescription} />
              <label className={styles.formLabel}>Zdjęcie: </label>
              <input
                type="file"
                accept="image/*"
                onChange={handleFileChange}
                className={styles.fileInput}
              />
              {preview && (
                <div className={styles.preview}>
                  <img
                    src={preview}
                    alt="Podgląd"
                    className={styles.previewImg}
                  />
                </div>
              )}
              {wrong && (
                <div className={styles.wrong}>
                  <h4>
                    Pola nazwa, opis lub składniki są za krótkie. Min 5 znaków
                  </h4>
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
