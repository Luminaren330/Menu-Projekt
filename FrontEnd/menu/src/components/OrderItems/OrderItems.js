import React, { useEffect, useState, useCallback } from "react";
import styles from "./OrderItems.module.scss";
import { useNavigate } from "react-router-dom";
import { useGlobalContext } from "../context/context";
import Navbar from "../Navbar/Navbar";
import { FaTrashAlt } from "react-icons/fa";
import { Link } from "react-router-dom";
import Axios from "axios";

const OrderItems = () => {
  const navigate = useNavigate();
  const { user } = useGlobalContext();

  const [orders, setOrders] = useState([]);
  const [tempQuantities, setTempQuantities] = useState({});
  const [totalPrice, setTotalPrice] = useState(0);
  const [isPressed, setIsPressed] = useState(false);

  const getOrderItems = useCallback(() => {
    Axios.get(`http://127.0.01:5000/carts?user_id=${user.user_id}`)
      .then((res) => {
        const records = res.data.records || [];
        setOrders(records);
        const initialQuantities = records.reduce(
          (acc, record) => ({
            ...acc,
            [record.item_id]: record.quantity,
          }),
          {}
        );
        setTempQuantities(initialQuantities);
      })
      .catch((err) => {
        console.error("Błąd podczas pobierania zamówień:", err);
        navigate("/error");
      });
  }, [navigate, user.user_id]);

  useEffect(() => {
    getOrderItems();
  }, [getOrderItems, isPressed]);

  useEffect(() => {
    let totalPrice = 0;
    orders.forEach((order) => {
      totalPrice += order.price_per_item * order.quantity;
    });
    setTotalPrice(totalPrice);
  }, [orders]);

  const deleteOrder = (id) => {
    setIsPressed(false);
    Axios.delete(`http://127.0.01:5000/carts?id=${id}`)
      .then(() => {
        setOrders((prevOrders) =>
          prevOrders.filter((order) => order.item_id !== id)
        );
        alert("Zamówienie zostało usunięte.");
        setIsPressed(true);
      })
      .catch((err) => {
        console.error("Błąd podczas usuwania zamówienia:", err);
      });
  };

  const updateOrderQuantity = (id, newQuantity, cartId) => {
    setIsPressed(false);
    Axios.patch(`http://127.0.01:5000/carts?id=${cartId}`, {
      dish_id: id,
      quantity: newQuantity,
    })
      .then(() => {
        setOrders((prevOrders) =>
          prevOrders.map((order) =>
            order.item_id === id ? { ...order, quantity: newQuantity } : order
          )
        );
        alert("Ilość zamówienia została zaktualizowana.");
        setIsPressed(true);
      })
      .catch((err) => {
        console.error("Błąd podczas aktualizacji ilości zamówienia:", err);
      });
  };

  const handleQuantityChange = (itemId, value) => {
    if (value >= 1) {
      setTempQuantities((prev) => ({ ...prev, [itemId]: value }));
    }
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
                      <img
                        src={`/${product.photo_url
                          .split("\\")
                          .slice(-2)
                          .join("/")}`}
                        alt={product.name}
                      />
                    </div>
                    <div className={styles.menuDesc}>
                      <div className={styles.nameAndAmount}>
                        <h2>{product.dish_name}</h2>
                        <div className={styles.quantityContainer}>
                          <input
                            type="number"
                            min="1"
                            value={tempQuantities[product.item_id] || ""}
                            className={styles.quantityInput}
                            onChange={(e) =>
                              handleQuantityChange(
                                product.item_id,
                                parseInt(e.target.value)
                              )
                            }
                          />
                          <button
                            className={styles.updateBtn}
                            onClick={() =>
                              updateOrderQuantity(
                                product.dish_id,
                                tempQuantities[product.item_id],
                                product.item_id
                              )
                            }
                          >
                            Aktualizuj
                          </button>
                        </div>
                      </div>
                      <p>{product.description}</p>
                      <p className={styles.menuPrice}>
                        Ilość: {product.quantity}
                      </p>
                      <p className={styles.menuPrice}>
                        Cena: {product.price_per_item} zł
                      </p>
                    </div>
                    <button
                      className={styles.deleteBtn}
                      onClick={() => deleteOrder(product.item_id)}
                    >
                      Usuń <FaTrashAlt />
                    </button>
                  </div>
                ))
              : null}
            <h2>Suma: {totalPrice} zł</h2>
          </div>
          <div className={styles.btnBottom}>
            <Link className={styles.yourOrderBtn} to={"/menu"}>
              Wróć
            </Link>
            {orders.length > 0 ? (
              <Link className={styles.yourOrderBtn} to={"/chooseplace"}>
                Złóż zamówienie
              </Link>
            ) : null}
          </div>
        </div>
      </div>
    </>
  );
};

export default OrderItems;
