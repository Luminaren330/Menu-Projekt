import React, { useEffect, useState, useMemo } from "react";
import styles from "./ClientForm.module.scss";
import { useNavigate } from "react-router-dom";
import { useGlobalContext } from "../context/context";
import Navbar from "../Navbar/Navbar";
import { Link } from "react-router-dom";
import { useLocation } from "react-router-dom";
import tables from "./tables-tmpdata";
import DatePicker from "react-datepicker";
import "react-datepicker/dist/react-datepicker.css";
import Popup from "../Popup/Popup";
import StringInput from "../AddReview/StringInput";
import seatImages from "./seatImages";

const ClientForm = () => {
  const navigate = useNavigate();
  const location = useLocation();
  const orderType = location.state?.orderType;
  const [isAnything, setIsAnything] = useState(true);
  const [seats] = useState(tables);
  const [selectedSeatId, setSelectedSeatId] = useState(null);
  const [isPopupVisible, setIsPopupVisible] = useState(false);
  const [date, setDate] = useState(null);
  const [arrivalTime, setArrivalTime] = useState("");
  const [wrong, setWrong] = useState(false);

  const handleSeatClick = (seat) => {
    if (seat.is_available) {
      setSelectedSeatId(seat.id === selectedSeatId ? null : seat.id);
    }
  };

  const togglePopup = (value) => {
    setIsPopupVisible(value);
  };

  const validateTime = () => {
    const currentTime = new Date();
    const selectedTime = new Date();

    const [hours, minutes] = arrivalTime.split(":");
    selectedTime.setHours(hours, minutes, 0);

    return selectedTime.getTime() - currentTime.getTime() >= 3600000;
  };

  const addOrder = () => {
    if (!validateTime()) {
      setWrong(true);
      return;
    }
    setWrong(false);
    togglePopup(true);
    //TODO add review

    navigate("/menu");
    setTimeout(() => {
      togglePopup(false);
    }, 5000);
  };

  const addTableOrder = () => {
    togglePopup(true);
    //TODO add review

    navigate("/menu");
    setTimeout(() => {
      togglePopup(false);
    }, 5000);
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
          message="Dodano nową recenzję!"
          onClose={() => togglePopup(false)}
        />
      )}
      <div className={styles.container}>
        <div className={styles.menu}>
          {orderType === "in" ? (
            <div>
              <h2 className={styles.menuHeader}>
                Wybierz stolik i date rezerwacji
              </h2>
              <div className={styles.hourPick}>
                <h1>Najpierw Wybierz Dzień i Godzinę</h1>
                <DatePicker
                  selected={date}
                  onChange={(date) => setDate(date)}
                  timeInputLabel="Czas przyjścia"
                  dateFormat="MM/dd/yyyy h:mm aa"
                  showTimeInput
                  className={styles.datePicker}
                />
              </div>
              {isAnything ? (
                date && (
                  <>
                    <div className={styles.centerLay}>
                      <div className={styles.layout}>
                        {seats.map((seat) => {
                          const seatStatus =
                            seat.id === selectedSeatId
                              ? "wybrany"
                              : seat.is_available
                              ? "dostepny"
                              : "niedostepny";

                          const seatSize = seat.capacity;
                          const seatImageSrc = seatImages[seatStatus][seatSize];

                          return (
                            <div
                              key={seat.id}
                              className={styles.seatWrapper}
                              onClick={() => handleSeatClick(seat)}
                            >
                              {/* Tooltip element */}
                              <div className={styles.tooltip}>
                                Stolik nr {seat.id}
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
              <div className={styles.timeInputContainer}>
                <h2 className={styles.menuHeader}>Podaj Godzinę przyjścia</h2>
                <input
                  type="time"
                  className={styles.timeInput}
                  value={arrivalTime}
                  onChange={(e) => setArrivalTime(e.target.value)}
                />
                {wrong && (
                  <div className={styles.wrong}>
                    <p>
                      Godzina przyjścia jest wymagana, min 1 godzina od teraz
                    </p>
                  </div>
                )}
                <div className={styles.form}>
                  <button className={styles.yourOrderBtn} onClick={addOrder}>
                    Złóż zamówienie
                  </button>
                </div>
              </div>
            </>
          )}
        </div>
      </div>
    </>
  );
};

export default ClientForm;
