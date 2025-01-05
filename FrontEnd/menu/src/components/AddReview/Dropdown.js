import styles from "./AddReview.module.scss";
import React from "react";

const Dropdown = ({ id, options, value, string, setFunction }) => {
  return (
    <>
      <label htmlFor={id} className={styles.formLabel}>
        {string}:
      </label>
      <select
        id={id}
        className={styles.dropdown}
        value={value}
        onChange={setFunction}
      >
        {options.map((option, key) => {
          return (
            <option key={key} value={option}>
              {option}
            </option>
          );
        })}
      </select>
    </>
  );
};

export default Dropdown;
