import React, { useEffect, useState } from "react";
import { useParams } from "react-router-dom";
import reviews from "./reviews-tmpdata";
import Navbar from "../Navbar/Navbar";
import styles from "./Reviews.module.scss";
import { FaRegUserCircle } from "react-icons/fa";
import ReactStars from "react-stars";
import { Link } from "react-router-dom";

const Reviews = () => {
  const { id } = useParams();
  const [reviewData, setReviewData] = useState([]);

  useEffect(() => {
    const filteredReviews = reviews.filter(
      (review) => review.dish_id === Number(id)
    );
    setReviewData(filteredReviews);
  }, [id]);

  return (
    <>
      <Navbar />
      <div className={styles.container}>
        <div className={styles.menu}>
          <h1 className={styles.menuHeader}>Reviews</h1>
          <div className={styles.categories}>
            {reviewData.map((review) => (
              <div key={review.id} className={styles.user}>
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
            <Link className={styles.yourOrderBtn} to={`/addreview/${id}`}>
              Dodaj recenzję
            </Link>
          </div>
        </div>
      </div>
    </>
  );
};

export default Reviews;
