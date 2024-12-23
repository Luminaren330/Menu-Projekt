import React, { useState, useEffect } from "react";
import { useGlobalContext } from "../context/context";
import styles from "./Login.module.scss";
import Axios from "axios";
import { useNavigate } from "react-router-dom";

const Login = () => {
  const { setIsLogedIn, setIsAdmin, setUser } = useGlobalContext();
  const [login, setLogin] = useState("");
  const [firstName, setFirstName] = useState("");
  const [lastName, setLastName] = useState("");
  const [password, setPassword] = useState("");
  const [role, setRole] = useState("");
  const [phone, setPhone] = useState(0);
  const [credentials, setCredentials] = useState([]);
  const [isRegister, setIsRegister] = useState(false);
  const navigate = useNavigate();

  const handleLogin = () => {
    Axios.post("http://127.0.01:5000/login", {
      email: login,
      password: password,
    }).then((res) => {
      if (res.data.message === "Logged in successfully!") {
        setIsLogedIn(true);
        setUser({
          email: login,
          password: password,
        });
        alert("Pomyslnie zalogowano");
        navigate("/dashboard");
      } else {
        alert("Niepoprawne dane logowania");
      }
    });
  };

  const handleRegister = () => {
    Axios.post("http://127.0.01:5000/register", {
      email: login,
      password: password,
      role: "client",
      firstname: firstName,
      lastname: lastName,
      telephone: phone,
    }).then((res) => {
      console.log(res.data.message);
      if (res.data.message === "User registered successfully!") {
        setIsLogedIn(true);
        setUser({
          email: login,
          password: password,
          role: "client",
          firstname: firstName,
          lastname: lastName,
          telephone: phone,
        });
        alert("Pomyslnie założono konto");
        navigate("/dashboard");
      } else {
        alert("Niepoprawne dane rejestarcji");
      }
    });
  };

  return (
    <div className={styles.container}>
      <div className={styles.login}>
        <h3 className={styles.title}>
          {isRegister ? "Zarejestruj się" : "Zaloguj się"}
        </h3>

        <div className={styles.labels}>
          <label htmlFor="username">Nazwa użytkownika: </label>
          <input
            id="username"
            type="text"
            className={styles.input}
            onChange={(event) => setLogin(event.target.value)}
          ></input>
        </div>

        <div className={styles.labels}>
          <label htmlFor="password">Hasło: </label>
          <input
            id="password"
            type="password"
            className={styles.input}
            onChange={(event) => setPassword(event.target.value)}
          ></input>
        </div>

        {isRegister ? (
          <div>
            <div className={styles.labels}>
              <label htmlFor="firstName">Imię: </label>
              <input
                id="firstName"
                type="text"
                className={styles.input}
                onChange={(event) => setFirstName(event.target.value)}
              ></input>
            </div>

            <div className={styles.labels}>
              <label htmlFor="lastName">Nazwisko: </label>
              <input
                id="lastName"
                type="text"
                className={styles.input}
                onChange={(event) => setLastName(event.target.value)}
              ></input>
            </div>

            <div className={styles.labels}>
              <label htmlFor="phoneNumber">Nr telefonu: </label>
              <input
                id="phoneNumber"
                type="number"
                className={styles.input}
                onChange={(event) => setPhone(event.target.value)}
              ></input>
            </div>
          </div>
        ) : null}

        {isRegister ? (
          <button
            className={styles.button}
            onClick={() => {
              handleRegister();
            }}
          >
            Zarejestruj się
          </button>
        ) : (
          <button
            className={styles.button}
            onClick={() => {
              handleLogin();
            }}
          >
            Zaloguj się
          </button>
        )}

        <div className={styles.toggle}>
          {isRegister ? (
            <p>
              Masz już konto?
              <button
                className={styles.link}
                onClick={() => setIsRegister(false)}
              >
                Zaloguj się
              </button>
            </p>
          ) : (
            <p>
              Nie masz konta?
              <button
                className={styles.link}
                onClick={() => setIsRegister(true)}
              >
                Zarejestruj się
              </button>
            </p>
          )}
        </div>
      </div>
    </div>
  );
};

export default Login;
