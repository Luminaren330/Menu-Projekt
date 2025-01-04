import styles from "../AddNewProduct/AddNewProduct.module.scss";
import React, { useState } from "react";
import Navbar from "../Navbar/Navbar";
import StringInput from "../AddReview/StringInput";
import { useNavigate } from "react-router-dom";
import Dropdown from "../AddReview/Dropdown";
import FormatInput from "../AddReview/FormatInput";
import Axios from "axios";

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
    console.log(name);
    console.log(surname);
    setWrong(false);
    if (name.length < 3 || surname.length < 3) {
      setWrong(true);
    } else {
      Axios.post("http://127.0.01:5000/register", {
        email: name + surname + "@mail.com",
        password: name.substring(0, 3) + phoneNumber.substring(0, 3),
        role: "employee",
        firstname: name,
        lastname: surname,
        telephone: parseInt(phoneNumber),
        position: category,
      })
        .then(() => {
          alert("Dodano pracownika");
          navigate("/workers");
        })
        .catch((err) => {
          console.error(err);
          navigate("/error");
        });
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
              <Dropdown
                options={categoryOptions}
                value={category}
                string="Rola"
                setFunction={CategorySet}
              />
              <FormatInput
                id="phoneNumber"
                string="Nr telefonu:"
                setParameter={setPhoneNumber}
                format="Format: 123456124"
                pattern="[0-9]{9}"
              />{" "}
              {wrong && (
                <div className={styles.wrong}>
                  <h4>
                    Pola imię, pozycja lub nazwisko są za krótkie. Min 3 znaki
                  </h4>
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
