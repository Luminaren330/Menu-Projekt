import React, { useCallback, useEffect, useState } from "react";
import styles from "./Orders.module.scss";
import { useNavigate } from "react-router-dom";
import { useGlobalContext } from "../context/context";
import Navbar from "../Navbar/Navbar";
import Axios from "axios";

const Order = () => {
  const navigate = useNavigate();
  const { isAdmin, isWorker, user } = useGlobalContext();
  const [orderData, setOrderData] = useState([]);

  const getOrderForUser = useCallback(() => {
    Axios.get(`http://127.0.0.1:5000/orders?account_id=${user.user_id}`).then(
      (res) => {
        setOrderData(res.data.records || []);
      }
    );
  }, [user.user_id]);

  const getOrder = useCallback(() => {
    Axios.get("http://127.0.0.1:5000/orders").then((res) => {
      setOrderData(res.data.records || []);
    });
  }, []);

  useEffect(() => {
    if (!isAdmin && !isWorker) {
      getOrderForUser();
    } else {
      getOrder();
    }
  }, [getOrder, getOrderForUser, isAdmin, isWorker]);

  const deleteOrder = (id) => {
    Axios.delete(`http://127.0.01:5000/orders?id=${id}`)
      .then((res) => {
        alert("Usunięto zamówienie");
        if (!isAdmin && !isWorker) {
          getOrderForUser();
        } else {
          getOrder();
        }
      })
      .catch((err) => {
        navigate("/error");
      });
  };

  return (
    <>
      <Navbar />
      <div className={styles.container}>
        <div className={styles.menu}>
          {!isAdmin && !isWorker ? (
            <h1 className={styles.menuHeader}>Twoje Zamówienia</h1>
          ) : (
            <h1 className={styles.menuHeader}>Zamówienia</h1>
          )}
          <div className={styles.menuItems}>
            <table className={styles.orderTable}>
              <thead>
                <tr>
                  <th>Nr</th>
                  <th>Data zamówienia</th>
                  <th>Przedmioty</th>
                  <th>Rezerwacja</th>
                  <th>Na wynos</th>
                  <th>Cena Całkowita</th>
                  {isAdmin || isWorker ? <th>Akcja</th> : null}
                </tr>
              </thead>
              <tbody>
                {orderData.map((order) => (
                  <tr key={order.order_id}>
                    <td>{order.order_id}</td>
                    <td>{order.order_date}</td>
                    <td>
                      {order.order_items.map((item, index) => (
                        <div key={index} className={styles.orderItem}>
                          <p>
                            <strong>{item.dish_name}</strong> - {item.quantity}x
                          </p>
                          <p>{item.price_per_dish.toFixed(2)} zł</p>
                        </div>
                      ))}
                    </td>
                    <td>
                      {order.table_id ? (
                        <div>
                          <p>Stolik: {order.table_id}</p>
                          <p>
                            {order.table_reservation_start_time} -{" "}
                            {order.table_reservation_end_time}
                          </p>
                        </div>
                      ) : (
                        "Brak rezerwacji"
                      )}
                    </td>
                    <td>
                      {order.take_away_time ? (
                        <p>{order.take_away_time}</p>
                      ) : (
                        "Nie dotyczy"
                      )}
                    </td>
                    <td>{order.total_price.toFixed(2)} zł</td>
                    {isAdmin || isWorker ? (
                      <td>
                        <button
                          onClick={() => deleteOrder(order.order_id)}
                          className={styles.deleteButton}
                        >
                          Zaznacz jako wykonane
                        </button>
                      </td>
                    ) : null}
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      </div>
    </>
  );
};

export default Order;
