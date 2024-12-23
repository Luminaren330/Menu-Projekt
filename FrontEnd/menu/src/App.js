import "./App.scss";
import Dashboard from "./components/Dashboard/Dashboard";
import Menu from "./components/Menu/Menu";
import Reviews from "./components/Reviews/Reviews";
import OrderItems from "./components/OrderItems/OrderItems";
import AddReview from "./components/AddReview/AddReview";
import ChoosePlace from "./components/ChoosePlace/ChoosePlace";
import ClientForm from "./components/ClientForm/ClientForm";
import Orders from "./components/Orders/Orders";
import AddNewProduct from "./components/AddNewProduct/AddNewProduct";
import {
  BrowserRouter as Router,
  Route,
  Routes,
  Navigate,
} from "react-router-dom";
import AddWorker from "./components/AddWorker/AddWorker";
import Workers from "./components/Workers/Workers";
import Login from "./components/Login/Login";
import { useGlobalContext } from "./components/context/context";

function App() {
  const { isLogedIn, isAdmin } = useGlobalContext();
  return (
    <>
      <Router>
        <Routes>
          <Route path="/login" element={<Login />}></Route>
          <Route
            exact
            path="/"
            element={isLogedIn ? <Dashboard /> : <Navigate to="/login" />}
          />
          <Route
            path="/dashboard"
            element={isLogedIn ? <Dashboard /> : <Navigate to="/login" />}
          />
          <Route
            path="/menu"
            element={isLogedIn ? <Menu /> : <Navigate to="/login" />}
          />
          <Route
            path="/reviews/:id"
            element={isLogedIn ? <Reviews /> : <Navigate to="/login" />}
          />
          <Route
            path="/yourorder"
            element={isLogedIn ? <OrderItems /> : <Navigate to="/login" />}
          />
          <Route
            path="/addreview/:id"
            element={isLogedIn ? <AddReview /> : <Navigate to="/login" />}
          ></Route>
          <Route
            path="/chooseplace"
            element={isLogedIn ? <ChoosePlace /> : <Navigate to="/login" />}
          ></Route>
          <Route
            path="/clientform"
            element={isLogedIn ? <ClientForm /> : <Navigate to="/login" />}
          ></Route>
          <Route
            path="/orders"
            element={isAdmin ? <Orders /> : <Navigate to="/login" />}
          ></Route>
          <Route
            path="/workers"
            element={isAdmin ? <Workers /> : <Navigate to="/login" />}
          ></Route>
          <Route
            path="/workers/addworker"
            element={isAdmin ? <AddWorker /> : <Navigate to="/login" />}
          ></Route>
          <Route
            path="/menu/addnewproduct"
            element={isLogedIn ? <AddNewProduct /> : <Navigate to="/login" />}
          ></Route>
        </Routes>
      </Router>
    </>
  );
}

export default App;
