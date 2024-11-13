import React, { useEffect, useState, useMemo } from "react";
import styles from "./Menu.module.scss";
import { useNavigate } from "react-router-dom";
import { useGlobalContext } from "../context/context";
import Navbar from "../Navbar/Navbar";
import menu from "./menu-tmpdata";
import { FaArrowRight, FaPlus, FaMinus } from "react-icons/fa";
import { Link } from "react-router-dom";
import Popup from "../Popup/Popup";

const Menu = () => {
  const navigate = useNavigate();
  const { isLogedIn, isAdmin } = useGlobalContext();

  const [products] = useState(menu);
  const [selectedCategory, setSelectedCategory] = useState("All");
  const [quantities, setQuantities] = useState({});

  const categories = ["All", ...new Set(menu.map((item) => item.category))];

  useEffect(() => {
    setSelectedCategory("All");
  }, []);

  const [isPopupVisible, setIsPopupVisible] = useState(false);

  const togglePopup = (value) => {
    setIsPopupVisible(value);
  };

  const addToOrderDetail = (id) => {
    togglePopup(true);
    console.log(quantities);

    setTimeout(() => {
      togglePopup(false);
    }, 5000);

    setQuantities((prevQuantities) => ({ ...prevQuantities, [id]: 1 }));
  };

  const filteredProducts = useMemo(() => {
    if (selectedCategory === "All") {
      return products;
    }
    return products.filter((item) => item.category === selectedCategory);
  }, [products, selectedCategory]);

  const filterByCategory = (category) => {
    setSelectedCategory(category);
  };

  const increaseQuantity = (id) => {
    setQuantities((prevQuantities) => ({
      ...prevQuantities,
      [id]: (prevQuantities[id] || 1) + 1,
    }));
  };

  const decreaseQuantity = (id) => {
    setQuantities((prevQuantities) => ({
      ...prevQuantities,
      [id]: Math.max((prevQuantities[id] || 1) - 1, 1),
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
              <div key={product.id} className={styles.menuItem}>
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
                          onClick={() => decreaseQuantity(product.id)}
                        >
                          <FaMinus />
                        </button>
                        <input
                          type="number"
                          value={quantities[product.id] || 1}
                          readOnly
                          className={styles.quantityInput}
                        />
                        <button
                          className={styles.quantityButton}
                          onClick={() => increaseQuantity(product.id)}
                        >
                          <FaPlus />
                        </button>
                      </div>
                      <button
                        className={styles.orderButton}
                        onClick={() => addToOrderDetail(product.id)}
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
                      to={`/reviews/${product.id}`}
                    >
                      Zobacz recenzje <FaArrowRight />
                    </Link>
                  </div>
                </div>
              </div>
            ))}
          </div>
          <div className={styles.btnBottom}>
            <Link className={styles.yourOrderBtn} to={"/yourorder"}>
              Przejdź do zamówienia
            </Link>
          </div>
        </div>
      </div>
    </>
  );
};

export default Menu;
