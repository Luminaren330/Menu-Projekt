import React, { useEffect, useState, useMemo } from "react";
import styles from "./OrderItems.module.scss";
import { useNavigate } from "react-router-dom";
import { useGlobalContext } from "../context/context";
import Navbar from "../Navbar/Navbar";
import orderItems from "./orderitems-tmpdata";
import { FaArrowRight } from "react-icons/fa";
import { Link } from "react-router-dom";
const OrderItems = () => {
  const navigate = useNavigate();
  const { isLogedIn, isAdmin } = useGlobalContext();

  const [orders] = useState(orderItems);
  const [totalPrice, setTotalPrice] = useState(0);
  useEffect(() => {
    //TODO kiedy będzie bazka to wyciągnąć koszyk
    let totalPrice = 0;
    orders.forEach((order) => {
      totalPrice += order.price * order.amount;
    });
    setTotalPrice(totalPrice);
  }, []);

  const deleteOrder = (id) => {
    //TODO kiedy będzie baza
  };

  return (
    <>
      <Navbar />
      <div className={styles.container}>
        <div className={styles.menu}>
          <h1 className={styles.menuHeader}>Twoje zamówienie</h1>
          <div className={styles.menuItems}>
            {orders.map((product) => (
              <div key={product.id} className={styles.menuItem}>
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
                  <p className={styles.menuPrice}>Cena: {product.price} zł</p>
                </div>
              </div>
            ))}
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
