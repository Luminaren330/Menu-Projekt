import React, { useEffect, useState, useMemo } from "react";
import styles from "./ChoosePlace.module.scss";
import { useNavigate } from "react-router-dom";
import { useGlobalContext } from "../context/context";
import Navbar from "../Navbar/Navbar";
import { MdOutlineTableRestaurant } from "react-icons/md";
import { GiPaperBagFolded } from "react-icons/gi";

const ChoosePlace = () => {
  const navigate = useNavigate();

  const navigateToClientForm = (value) => {
    navigate("/clientform", { state: { orderType: value } });
  };

  return (
    <>
      <Navbar />
      <div className={styles.container}>
        <div className={styles.menu}>
          <div className={styles.cardsContainer}>
            <div
              className={styles.card}
              onClick={() => navigateToClientForm("in")}
            >
              <div className={styles.iconContainer}>
                <MdOutlineTableRestaurant className={styles.icon} />
              </div>
              <h1>Na miejcu</h1>
            </div>
            <div
              className={styles.card}
              onClick={() => navigateToClientForm("out")}
            >
              <div className={styles.iconContainer}>
                <GiPaperBagFolded className={styles.icon} />
              </div>
              <h1>Na wynos</h1>
            </div>
          </div>
        </div>
      </div>
    </>
  );
};

export default ChoosePlace;
