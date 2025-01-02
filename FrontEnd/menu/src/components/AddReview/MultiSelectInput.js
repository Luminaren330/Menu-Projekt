import React, { useState } from "react";
import styles from "./MultiSelectInput.module.scss";

const MultiSelectInput = ({
  id,
  options,
  string,
  selectedItems,
  setSelectedItems,
}) => {
  const [isDropdownOpen, setIsDropdownOpen] = useState(false);

  const toggleDropdown = () => {
    setIsDropdownOpen((prev) => !prev);
  };

  const handleItemClick = (item) => {
    if (selectedItems.includes(item)) {
      setSelectedItems(selectedItems.filter((selected) => selected !== item));
    } else {
      setSelectedItems([...selectedItems, item]);
    }
  };

  return (
    <div className={styles.multiSelectContainer}>
      <label htmlFor={id} className={styles.formLabel}>
        {string}
      </label>
      <div className={styles.multiSelect}>
        <div className={styles.selectedItems} onClick={toggleDropdown}>
          {selectedItems.length > 0 ? (
            selectedItems.join(", ")
          ) : (
            <span className={styles.placeholder}>Wybierz składniki</span>
          )}
          <span className={styles.arrow}>{isDropdownOpen ? "▲" : "▼"}</span>
        </div>
        {isDropdownOpen && (
          <ul className={styles.dropdownList}>
            {options.map((option) => (
              <li
                key={option}
                className={`${styles.dropdownItem} ${
                  selectedItems.includes(option) ? styles.selected : ""
                }`}
                onClick={() => handleItemClick(option)}
              >
                {option}
              </li>
            ))}
          </ul>
        )}
      </div>
    </div>
  );
};

export default MultiSelectInput;
