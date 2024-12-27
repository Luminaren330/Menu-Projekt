import React, { useEffect, useState, useMemo, useCallback } from "react";
import styles from "./Menu.module.scss";
import { useNavigate } from "react-router-dom";
import { useGlobalContext } from "../context/context";
import Navbar from "../Navbar/Navbar";
import menu from "./menu-tmpdata";
import { FaArrowRight, FaPlus, FaMinus } from "react-icons/fa";
import { Link } from "react-router-dom";
import Popup from "../Popup/Popup";
import Axios from "axios";

const Menu = () => {
  const navigate = useNavigate();
  const { isLogedIn, isAdmin } = useGlobalContext();

  const [products, setProducts] = useState([]);
  const [category, setCategory] = useState([]);
  const [selectedCategory, setSelectedCategory] = useState("All");
  const [quantities, setQuantities] = useState({});

  const categories = ["All", ...new Set(category.map((item) => item.name))];

  const getDishes = useCallback(() => {
    Axios.get("http://127.0.01:5000/dishes")
      .then((res) => {
        setProducts(res.data.records || []);
      })
      .catch(() => navigate("/error"));
  }, [navigate]);

  const getCategories = useCallback(() => {
    Axios.get("http://127.0.01:5000/categories")
      .then((res) => {
        setCategory(res.data.records || []);
      })
      .catch(() => navigate("/error"));
  }, [navigate]);

  useEffect(() => {
    getDishes();
    getCategories();
  }, [getDishes, getCategories]);

  const [isPopupVisible, setIsPopupVisible] = useState(false);

  const togglePopup = (value) => {
    setIsPopupVisible(value);
  };

  const addToOrderDetail = (dish_id) => {
    togglePopup(true);
    console.log(quantities);

    setTimeout(() => {
      togglePopup(false);
    }, 5000);

    setQuantities((prevQuantities) => ({ ...prevQuantities, [dish_id]: 1 }));
  };

  const filteredProducts = useMemo(() => {
    if (Array.isArray(products)) {
      if (selectedCategory === "All") {
        return products;
      }
      return products.filter((item) => item.category === selectedCategory);
    }
    return [];
  }, [products, selectedCategory]);

  const filterByCategory = (category) => {
    setSelectedCategory(category);
  };

  const increaseQuantity = (dish_id) => {
    setQuantities((prevQuantities) => ({
      ...prevQuantities,
      [dish_id]: (prevQuantities[dish_id] || 1) + 1,
    }));
  };

  const decreaseQuantity = (dish_id) => {
    setQuantities((prevQuantities) => ({
      ...prevQuantities,
      [dish_id]: Math.max((prevQuantities[dish_id] || 1) - 1, 1),
    }));
  };

  return (
    <>
      <Navbar />
      {isPopupVisible && (
        <Popup
          message="Dodano do zamówienia!"
          onClose={() => togglePopup(false)}
        />
      )}
      <div className={styles.container}>
        <div className={styles.menu}>
          <h1 className={styles.menuHeader}>Menu</h1>
          <div className={styles.categories}>
            {categories.map((category) => (
              <button
                key={category}
                className={`${styles.categoryButton} ${
                  selectedCategory === category ? styles.active : ""
                }`}
                onClick={() => filterByCategory(category)}
              >
                {category}
              </button>
            ))}
          </div>

          <div className={styles.menuItems}>
            {filteredProducts.map((product) => (
              <div key={product.dish_id} className={styles.menuItem}>
                <div className={styles.menuImage}>
                  <img src={product.photo_url} alt={product.name} />
                </div>
                <div className={styles.menuDesc}>
                  <div className={styles.headerAndAdd}>
                    <h2>{product.name}</h2>
                    <div className={styles.InputAndBtn}>
                      <div className={styles.quantityControl}>
                        <button
                          className={styles.quantityButton}
                          onClick={() => decreaseQuantity(product.dish_id)}
                        >
                          <FaMinus />
                        </button>
                        <input
                          type="number"
                          value={quantities[product.dish_id] || 1}
                          readOnly
                          className={styles.quantityInput}
                        />
                        <button
                          className={styles.quantityButton}
                          onClick={() => increaseQuantity(product.dish_id)}
                        >
                          <FaPlus />
                        </button>
                      </div>
                      <button
                        className={styles.orderButton}
                        onClick={() => addToOrderDetail(product.dish_id)}
                      >
                        Dodaj do Zamówienia <FaArrowRight />
                      </button>
                    </div>
                  </div>
                  <p>{product.description}</p>
                  <p>Składniki: {product.ingredients}</p>
                  <div className={styles.priceAndReview}>
                    <p className={styles.menuPrice}>Cena: {product.price} zł</p>
                    <Link
                      className={styles.reviews}
                      to={`/reviews/${product.dish_id}`}
                    >
                      Zobacz recenzje <FaArrowRight />
                    </Link>
                  </div>
                </div>
              </div>
            ))}
          </div>
          <div className={styles.btnBottom}>
            {!isAdmin ? (
              <Link className={styles.yourOrderBtn} to={"/menu/addnewproduct"}>
                Dodaj nowy produkt
              </Link>
            ) : (
              <Link className={styles.yourOrderBtn} to={"/yourorder"}>
                Przejdź do zamówienia
              </Link>
            )}
          </div>
        </div>
      </div>
    </>
  );
};

export default Menu;
