import React, { useState, useRef, useEffect } from "react";
import { links } from "../../data/navbar-data";
import { FaBars } from "react-icons/fa";
import { Link, useNavigate } from "react-router-dom";
import styles from "./Navbar.module.scss";
import { FaHome } from "react-icons/fa";
import { useGlobalContext } from "../context/context";

const Navbar = () => {
  const [showLinks, setShowLinks] = useState(false);
  const linksContainerRef = useRef(null);
  const linksRef = useRef(null);
  const {
    isLogedIn,
    isAdmin,
    isWorker,
    setIsLogedIn,
    setIsAdmin,
    setIsWorker,
  } = useGlobalContext();
  const logedInText = isLogedIn ? "Wyloguj" : "Zaloguj";
  const navigate = useNavigate();

  useEffect(() => {
    const linksHeight = linksRef.current.getBoundingClientRect().height;
    if (showLinks) {
      linksContainerRef.current.style.height = `${linksHeight}px`;
    } else {
      linksContainerRef.current.style.height = "0px";
    }
  }, [showLinks]);

  const handleLogin = () => {
    if (!isLogedIn) {
      navigate("/login");
    } else {
      setIsAdmin(false);
      setIsWorker(false);
      setIsLogedIn(false);
      localStorage.removeItem("user");
      alert("Pomyślnie wylogowano");
      navigate("/login");
    }
  };

  return (
    <nav className={styles.navbar}>
      <div className={styles.nav_center}>
        <div className={styles.nav_header}>
          <div className={styles.links}>
            <Link to="/">
              <FaHome />
            </Link>
          </div>
          <button
            className={styles.nav_toggle}
            onClick={() => setShowLinks(!showLinks)}
          >
            <FaBars />
          </button>
        </div>
        <div className={styles.links_container} ref={linksContainerRef}>
          <ul className={styles.links} ref={linksRef}>
            {links.map((linkers) => {
              const { id, link, text } = linkers;
              if (
                (id !== 2 && (isAdmin || isWorker)) ||
                (!isAdmin && !isWorker && id < 4)
              ) {
                return (
                  <li key={id}>
                    <Link to={link}>{text}</Link>
                  </li>
                );
              } else {
                return null;
              }
            })}
            <>
              <li className={styles.links}>
                <button
                  type="button"
                  className={styles.logout_button}
                  onClick={() => handleLogin()}
                >
                  {logedInText}
                </button>
              </li>
            </>
          </ul>
        </div>
      </div>
    </nav>
  );
};

export default Navbar;
