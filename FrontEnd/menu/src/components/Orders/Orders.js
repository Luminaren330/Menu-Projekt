import React, { useEffect, useState } from "react";
import styles from "./Orders.module.scss";
import { useNavigate } from "react-router-dom";
import { useGlobalContext } from "../context/context";
import Navbar from "../Navbar/Navbar";
import orderItems from "../OrderItems/orderitems-tmpdata";
import orders from "./orders-tmpdata";
import { FaArrowRight } from "react-icons/fa";

const Order = () => {
  const navigate = useNavigate();
  const { isLogedIn, isAdmin } = useGlobalContext();
  const [orderData, setOrderData] = useState([]);

  useEffect(() => {
    // Łączenie orders i orderItems, obliczanie totalPrice dla każdego zamówienia
    const mergedOrders = orders.map((order) => {
      const items = orderItems.filter((item) => item.order_id === order.id);
      const totalPrice = items.reduce(
        (sum, item) => sum + item.price * item.amount,
        0
      );

      return {
        ...order,
        items,
        totalPrice,
      };
    });
    setOrderData(mergedOrders);
  }, []);

  const deleteOrder = (id) => {};

  return (
    <>
      <Navbar />
      <div className={styles.container}>
        <div className={styles.menu}>
          <h1 className={styles.menuHeader}>Zamówienia</h1>
          <div className={styles.menuItems}>
            <table className={styles.orderTable}>
              <thead>
                <tr>
                  <th>Nr</th>
                  <th>Imię i Nazwisko Klienta</th>
                  <th>Pracownik przypisany</th>
                  <th>Przedmioty</th>
                  <th>Cena Całkowita</th>
                  <th></th>
                </tr>
              </thead>
              <tbody>
                {orderData.map((order) => (
                  <tr key={order.id}>
                    <td>{order.id}</td>
                    <td>
                      {order.first_name} {order.last_name}
                    </td>
                    <td>{order.worker}</td>
                    <td>
                      {order.items.map((item) => (
                        <div key={item.id} className={styles.orderItem}>
                          <p>
                            <strong>{item.name}</strong> - {item.amount}x
                          </p>
                          <p>{item.price} zł</p>
                        </div>
                      ))}
                    </td>
                    <td>{order.totalPrice.toFixed(2)} zł</td>
                    <td>
                      <button
                        onClick={() => deleteOrder(order.id)}
                        className={styles.deleteButton}
                      >
                        Zaznacz jako wykonane
                      </button>
                    </td>
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
