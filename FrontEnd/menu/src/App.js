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

function App() {
  return (
    <>
      <Router>
        <Routes>
          <Route exact path="/" element={<Navigate to="/dashboard" />} />
          <Route path="/dashboard" element={<Dashboard />} />
          <Route path="/menu" element={<Menu />} />
          <Route path="/reviews/:id" element={<Reviews />} />
          <Route path="/yourorder" element={<OrderItems />} />
          <Route path="/addreview/:id" element={<AddReview />}></Route>
          <Route path="/chooseplace" element={<ChoosePlace />}></Route>
          <Route path="/clientform" element={<ClientForm />}></Route>
          <Route path="/orders" element={<Orders />}></Route>
          <Route
            path="/products/addnewproduct"
            element={<AddNewProduct />}
          ></Route>
        </Routes>
      </Router>
    </>
  );
}

export default App;
