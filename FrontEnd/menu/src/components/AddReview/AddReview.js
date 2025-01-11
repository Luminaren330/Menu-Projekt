import styles from "./AddReview.module.scss";
import React, { useState, useEffect } from "react";
import Navbar from "../Navbar/Navbar";
import TextAreaInput from "./TextAreaInput";
import { useNavigate, useParams } from "react-router-dom";
import ReactStars from "react-stars";
import Popup from "../Popup/Popup";
import Axios from "axios";
import { useGlobalContext } from "../context/context";

const AddReview = () => {
  const { id } = useParams();
  const [comment, setComment] = useState("");
  const [stars, setStars] = useState(0);
  const [isPopupVisible, setIsPopupVisible] = useState(false);
  const [dish, setDish] = useState({});
  const [wrong, setWrong] = useState(false);
  const navigate = useNavigate();
  const { user } = useGlobalContext();

  useEffect(() => {
    Axios.get("http://127.0.01:5000/dishes").then((res) => {
      let oneDish = res.data.records.filter(
        (element) => element.dish_id === Number(id)
      );

      setDish(oneDish[0]);
    });
  }, [id]);

  const ratingChange = (rating) => {
    setStars(rating);
  };

  const togglePopup = (value) => {
    setIsPopupVisible(value);
  };

  const addNewReview = () => {
    if (comment.length < 5) {
      setWrong(true);
      return;
    }

    Axios.post("http://127.0.01:5000/reviews", {
      dish_id: id,
      stars: stars,
      comment: comment,
      user_id: user.user_id,
    }).then(() => {
      setWrong(false);
      togglePopup(true);
      navigate("/menu");
      setTimeout(() => {
        togglePopup(false);
      }, 5000);
    });
  };

  return (
    <>
      <Navbar></Navbar>
      {isPopupVisible && (
        <Popup
          message="Dodano nową recenzję!"
          onClose={() => togglePopup(false)}
        />
      )}
      <div className={styles.container}>
        <div className={styles.menu}>
          <div className={styles.form}>
            <h2 className={styles.header}>Dodaj nową recenzję</h2>
            <div className={styles.menuImage}>
              <img
                src={`/${dish.photo_url?.split("\\").slice(-2).join("/")}`}
                alt={dish.name}
              />
              <h2>{dish.name}</h2>
            </div>
            <TextAreaInput string="Recenzja: " setParameter={setComment} />
            <div>
              <p className={styles.formLabel}>Gwiazdki</p>
              <ReactStars
                count={5}
                onChange={ratingChange}
                value={stars}
                size={40}
                className={styles.stars}
              />
            </div>
          </div>
          {wrong && (
            <div className={styles.wrong}>
              <h4>Za krótka recenzja. Min 5 znaków</h4>
            </div>
          )}
          <div className={styles.center}>
            <button
              className={styles.addProduct}
              onClick={() => {
                addNewReview();
              }}
            >
              Dodaj
            </button>
          </div>
        </div>
      </div>
    </>
  );
};

export default AddReview;
