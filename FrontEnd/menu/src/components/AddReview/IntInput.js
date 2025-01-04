import styles from "./AddReview.module.scss";
import React from "react";

const IntInput = ({ id, string, setParameter }) => {
  return (
    <>
      <label htmlFor={id} className={styles.formLabel}>
        {string}
      </label>
      <input
        id={id}
        type="number"
        min="1"
        className={styles.formInput}
        onChange={(event) => setParameter(event.target.value)}
      ></input>
    </>
  );
};
export default IntInput;
