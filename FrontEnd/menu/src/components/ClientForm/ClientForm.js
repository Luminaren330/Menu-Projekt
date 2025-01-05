import React, { useEffect, useState, useCallback } from "react";
import styles from "./ClientForm.module.scss";
import { useNavigate } from "react-router-dom";
import { useGlobalContext } from "../context/context";
import Navbar from "../Navbar/Navbar";
import { useLocation } from "react-router-dom";
import tables from "./tables-tmpdata";
import Popup from "../Popup/Popup";
import seatImages from "./seatImages";
import Axios from "axios";
import Datetime from "react-datetime";
import "react-datetime/css/react-datetime.css";

const ClientForm = () => {
  const navigate = useNavigate();
  const location = useLocation();
  const { user } = useGlobalContext();
  const orderType = location.state?.orderType;
  const [isAnything, setIsAnything] = useState(true);
  const [seats, setSeats] = useState([]);
  const [selectedSeatId, setSelectedSeatId] = useState(null);
  const [isPopupVisible, setIsPopupVisible] = useState(false);
  const [dateTime, setDateTime] = useState(null);
  const [wrong, setWrong] = useState(false);

  const handleSeatClick = (seat) => {
    if (seat.is_available) {
      setSelectedSeatId(
        seat.table_id === selectedSeatId ? null : seat.table_id
      );
    }
  };

  const togglePopup = (value) => {
    setIsPopupVisible(value);
  };

  const formatDate = (dateInput) => {
    const dateObj = new Date(dateInput);
    if (isNaN(dateObj.getTime())) {
      throw new Error("Nieprawidłowy format daty");
    }
    const year = dateObj.getFullYear();
    const month = String(dateObj.getMonth() + 1).padStart(2, "0");
    const day = String(dateObj.getDate()).padStart(2, "0");
    const hours = String(dateObj.getHours()).padStart(2, "0");
    const minutes = String(dateObj.getMinutes()).padStart(2, "0");
    const seconds = String(dateObj.getSeconds()).padStart(2, "0");

    return `${year}-${month}-${day} ${hours}:${minutes}:${seconds}`;
  };

  const getTables = useCallback(() => {
    if (dateTime) {
      Axios.get(
        `http://127.0.01:5000/tables?start_time=${formatDate(dateTime)}`
      ).then((res) => {
        setSeats(res.data.records || []);
      });
    }
  }, [dateTime]);

  useEffect(() => {
    getTables();
  }, [dateTime, getTables]);

  const validateTime = () => {
    const currentTime = new Date();
    return new Date(dateTime).getTime() - currentTime.getTime() >= 3600000;
  };

  const addOrder = () => {
    if (!validateTime()) {
      setWrong(true);
      return;
    }
    Axios.post("http://127.0.01:5000/orders", {
      take_away_time: formatDate(dateTime),
      user_id: user.user_id,
    })
      .then(() => {
        navigate("/menu");
        alert("Zamowienie złożone");
      })
      .catch((err) => {
        console.log(err);
        navigate("/error");
      });
  };

  const goBack = () => {
    navigate("/chooseplace");
  };

  const addTableOrder = () => {
    if (!validateTime()) {
      setWrong(true);
      return;
    }
    Axios.post("http://127.0.01:5000/orders", {
      table_id: selectedSeatId,
      user_id: user.user_id,
      table_reservation_start_time: formatDate(dateTime),
    })
      .then(() => {
        navigate("/menu");
        alert("Stolik zarezerwowany");
      })
      .catch((err) => {
        console.log(err);
        navigate("/error");
      });
  };

  useEffect(() => {
    let tablesAvailable = tables.filter((table) => table.is_available === true);
    setIsAnything(tablesAvailable.length > 0);
  }, []);

  return (
    <>
      <Navbar />
      {isPopupVisible && (
        <Popup
          message="Dodano twoje zamówienie!"
          onClose={() => togglePopup(false)}
        />
      )}
      <div className={styles.timeInputContainer}>
        <div className={styles.menu}>
          {orderType === "in" ? (
            <div>
              <h2 className={styles.menuHeader}>
                Wybierz stolik i datę rezerwacji
              </h2>
              <div className={styles.centeredPicker}>
                <Datetime
                  value={dateTime}
                  onChange={(date) => setDateTime(date)}
                  dateFormat="YYYY-MM-DD"
                  timeFormat="HH:mm"
                  className={styles.datePicker}
                />
              </div>
              {wrong && (
                <div className={styles.wrong}>
                  <p>Data musi być późniejsza</p>
                </div>
              )}
              {isAnything ? (
                dateTime && (
                  <>
                    <div className={styles.centerLay}>
                      <div className={styles.layout}>
                        {seats.map((seat) => {
                          const seatStatus =
                            seat.table_id === selectedSeatId
                              ? "wybrany"
                              : seat.is_available
                              ? "dostepny"
                              : "niedostepny";

                          const seatSize = seat.capacity;
                          const seatImageSrc = seatImages[seatStatus][seatSize];

                          return (
                            <div
                              key={seat.table_id}
                              className={styles.seatWrapper}
                              onClick={() => handleSeatClick(seat)}
                            >
                              <div className={styles.tooltip}>
                                {seat.description}
                              </div>
                              <img
                                src={seatImageSrc}
                                alt={`Seat ${seat.capacity}`}
                                className={styles.seatImage}
                              />
                            </div>
                          );
                        })}
                      </div>
                    </div>
                    <div className={styles.legendText}>
                      <div className={styles.legendLeft}>
                        <h3>Legenda:</h3>
                        <div className={styles.boxes}>
                          <div className={styles.legend}>
                            <div
                              className={`${styles.box} ${styles.box1}`}
                            ></div>
                            <p>-Dostępne</p>
                          </div>
                          <div className={styles.legend}>
                            <div
                              className={`${styles.box} ${styles.box2}`}
                            ></div>
                            <p>-Niedostępne</p>
                          </div>
                          <div className={styles.legend}>
                            <div
                              className={`${styles.box} ${styles.box3}`}
                            ></div>
                            <p>-Wybrane</p>
                          </div>
                        </div>
                        {selectedSeatId && (
                          <div className={styles.tableAndButton}>
                            <div className={styles.selectedInfo}>
                              Wybrano Stolik {selectedSeatId}
                            </div>
                            <button
                              className={styles.yourOrderBtn}
                              onClick={() => {
                                addTableOrder();
                              }}
                            >
                              Złóż zamówienie
                            </button>
                          </div>
                        )}
                        <button
                          className={styles.yourOrderBtn}
                          onClick={goBack}
                        >
                          Wróć
                        </button>
                      </div>
                    </div>
                  </>
                )
              ) : (
                <h1 className={styles.menuHeader}>
                  Nie znaleziono stolika. Spróbuj w innych godzinach.
                </h1>
              )}
            </div>
          ) : (
            <>
              <h2 className={styles.menuHeader}>
                Podaj Datę i Godzinę przyjścia
              </h2>
              <div className={styles.centeredPicker}>
                <Datetime
                  value={dateTime}
                  onChange={(date) => setDateTime(date)}
                  dateFormat="YYYY-MM-DD"
                  timeFormat="HH:mm"
                  className={styles.datePicker}
                />
              </div>
              {wrong && (
                <div className={styles.wrong}>
                  <p>Godzina przyjścia jest wymagana, min 1 godzina od teraz</p>
                </div>
              )}

              <div className={styles.form}>
                {dateTime ? (
                  <button className={styles.yourOrderBtn} onClick={addOrder}>
                    Złóż zamówienie
                  </button>
                ) : null}
                <button className={styles.yourOrderBtn} onClick={goBack}>
                  Wróć
                </button>
              </div>
            </>
          )}
        </div>
      </div>
    </>
  );
};

export default ClientForm;
