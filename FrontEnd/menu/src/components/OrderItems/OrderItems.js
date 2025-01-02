import React, { useEffect, useState, useMemo, useCallback } from "react";
import styles from "./OrderItems.module.scss";
import { useNavigate } from "react-router-dom";
import { useGlobalContext } from "../context/context";
import Navbar from "../Navbar/Navbar";
import { FaArrowRight } from "react-icons/fa";
import { Link } from "react-router-dom";
import Axios from "axios";

const OrderItems = () => {
  const navigate = useNavigate();
  const { isLogedIn, isAdmin } = useGlobalContext();

  const [orders, setOrders] = useState([]);
  const [totalPrice, setTotalPrice] = useState(0);

  const getOrderItems = useCallback(() => {
    Axios.get("http://127.0.01:5000/carts")
      .then((res) => {
        console.log(res);
        setOrders(res.data.records || []);
        console.log(orders);
      })
      .catch((err) => {
        console.error("Błąd podczas pobierania zamówień:", err);
        navigate("/error");
      });
  }, [navigate]);

  useEffect(() => {
    getOrderItems();
  }, [getOrderItems]);

  useEffect(() => {
    let totalPrice = 0;
    orders.forEach((order) => {
      totalPrice += order.price * order.amount;
    });
    setTotalPrice(totalPrice);
  }, [orders]);

  const deleteOrder = (id) => {
    Axios.delete(`http://127.0.01:5000/carts?id=${id}`)
      .then(() => {
        setOrders((prevOrders) =>
          prevOrders.filter((order) => order.id !== id)
        );
        alert("Zamówienie zostało usunięte.");
      })
      .catch((err) => {
        console.error("Błąd podczas usuwania zamówienia:", err);
      });
  };

  return (
    <>
      <Navbar />
      <div className={styles.container}>
        <div className={styles.menu}>
          <h1 className={styles.menuHeader}>Twoje zamówienie</h1>
          <div className={styles.menuItems}>
            {orders.length > 0
              ? orders.map((product) => (
                  <div key={product.item_id} className={styles.menuItem}>
                    <div className={styles.menuImage}>
                      <img src={product.photo_url} alt={product.name} />
                    </div>
                    <div className={styles.menuDesc}>
                      <div className={styles.nameAndAmount}>
                        <h2>{product.name}</h2>
                        <h3>X {product.amount}</h3>
                      </div>
                      <p>{product.description}</p>
                      <p>Składniki: {product.ingredients}</p>
                      <p className={styles.menuPrice}>
                        Cena: {product.price} zł
                      </p>
                    </div>
                  </div>
                ))
              : null}
            <h2>Suma: {totalPrice} zł</h2>
          </div>
          <div className={styles.btnBottom}>
            <Link className={styles.yourOrderBtn} to={"/menu"}>
              Wróć
            </Link>
            <Link className={styles.yourOrderBtn} to={"/chooseplace"}>
              Złóż zamówienie
            </Link>
          </div>
        </div>
      </div>
    </>
  );
};

export default OrderItems;
