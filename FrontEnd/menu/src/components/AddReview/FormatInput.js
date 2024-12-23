import styles from "./AddReview.module.scss";
import React from "react";

const FormatInput = ({ id, string, setParameter, format, pattern }) => {
  return (
    <>
      <div className={styles.format}>
        <label htmlFor={id} className={styles.formLabel}>
          {string}
        </label>
        <small className={styles.smallForm}> {format}</small>
      </div>
      <input
        id={id}
        type="tel"
        pattern={pattern}
        required
        className={styles.formInput}
        onChange={(event) => setParameter(event.target.value)}
      ></input>
    </>
  );
};
export default FormatInput;
