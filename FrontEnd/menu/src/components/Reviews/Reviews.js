import React, { useEffect, useState } from "react";
import { useParams } from "react-router-dom";
import reviews from "./reviews-tmpdata";
import Navbar from "../Navbar/Navbar";
import styles from "./Reviews.module.scss";
import { FaRegUserCircle } from "react-icons/fa";
import { useGlobalContext } from "../context/context";
import ReactStars from "react-stars";
import { Link } from "react-router-dom";
import Axios from "axios";

const Reviews = () => {
  const { id } = useParams();
  const { isLogedIn, isAdmin, isWorker } = useGlobalContext();
  const [reviewData, setReviewData] = useState([]);

  useEffect(() => {
    Axios.get(`http://127.0.01:5000/reviews?dish_id=${id}`).then((res) => {
      setReviewData(res.data.records || []);
    });
  }, [id]);

  return (
    <>
      <Navbar />
      <div className={styles.container}>
        <div className={styles.menu}>
          <h1 className={styles.menuHeader}>Reviews</h1>
          <div className={styles.categories}>
            {reviewData.map((review) => (
              <div key={review.review_id} className={styles.user}>
                <div className={styles.icon}>
                  <FaRegUserCircle />
                </div>
                <div className={styles.message}>
                  <div className={styles.userStars}>
                    <h3>{review.user}</h3>
                    <ReactStars
                      count={5}
                      value={review.stars}
                      edit={false}
                      className={styles.stars}
                      size={20}
                    />
                  </div>
                  <p>{review.comment}</p>
                </div>
              </div>
            ))}
          </div>
          <div className={styles.btnBottom}>
            <Link className={styles.yourOrderBtn} to={"/menu"}>
              Wróć
            </Link>
            {!isAdmin && !isWorker ? (
              <Link className={styles.yourOrderBtn} to={`/addreview/${id}`}>
                Dodaj recenzję
              </Link>
            ) : null}
          </div>
        </div>
      </div>
    </>
  );
};

export default Reviews;
