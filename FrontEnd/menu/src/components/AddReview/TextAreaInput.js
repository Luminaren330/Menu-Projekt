import styles from "./AddReview.module.scss";
import React from "react";

const TextAreaInput = ({ id, string, setParameter }) => {
  return (
    <>
      <label htmlFor={id} className={styles.formLabel}>
        {string}
      </label>
      <textarea
        id={id}
        type="text"
        className={styles.formTextInput}
        minLength={0}
        maxLength={200}
        onChange={(event) => setParameter(event.target.value)}
      ></textarea>
    </>
  );
};
export default TextAreaInput;
