import "./App.scss";
import Dashboard from "./components/Dashboard/Dashboard";

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
        </Routes>
      </Router>
    </>
  );
}

export default App;
