import React, { useState, useContext } from "react";

const GlobalContext = React.createContext();

const Context = ({ children }) => {
  const [isLogedIn, setIsLogedIn] = useState(false);
  const [isAdmin, setIsAdmin] = useState(false);
  const [isWorker, setIsWorker] = useState(false);
  const [user, setUser] = useState({});

  return (
    <GlobalContext.Provider
      value={{
        isLogedIn,
        isWorker,
        isAdmin,
        setIsAdmin,
        setIsWorker,
        setIsLogedIn,
        user,
        setUser,
      }}
    >
      {children}
    </GlobalContext.Provider>
  );
};

export const useGlobalContext = () => {
  return useContext(GlobalContext);
};

export { GlobalContext, Context };
