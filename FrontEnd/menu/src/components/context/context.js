import React, { useState, useContext } from "react";

const GlobalContext = React.createContext();

const Context = ({ children }) => {
  const [isLogedIn, setIsLogedIn] = useState(true);
  const [isAdmin, setIsAdmin] = useState(true);

  return (
    <GlobalContext.Provider
      value={{ isLogedIn, isAdmin, setIsAdmin, setIsLogedIn }}
    >
      {children}
    </GlobalContext.Provider>
  );
};

export const useGlobalContext = () => {
  return useContext(GlobalContext);
};

export { GlobalContext, Context };
