import "./App.css";
import { BrowserRouter as Router, Route, Routes } from "react-router-dom";
import { AuthProvider } from "./context/context";
import Login from "./pages/Login/Login";
import { GoogleOAuthProvider } from "@react-oauth/google";
import Home from "./pages/Home/Home";
import Header from "./components/Header/Header";
import AuthProtect from "./pages/Protected/AuthProtect";
import Footer from "./components/Footer/Footer";
import HomeLoggedIn from "./pages/HomeLoggedIn/HomeLoggedIn";
import BestOfWeek from "./pages/BestOfWeek/BestOfWeek";
import Sidebar from "./components/Sidebar/Sidebar";
import LoggedIn from "./pages/Protected/LoggedIn";

function App() {
  return (
    <div className="font-sans">
      <GoogleOAuthProvider clientId="796799461942-os8v3rqcun15nbre1icr48qleieoklk2.apps.googleusercontent.com">
        <Router>
          <Sidebar />
          <AuthProvider>
            <Header />
            <Routes>
              <Route element={<LoggedIn />}>
                <Route path="/home" element={<HomeLoggedIn />} />
                <Route path="/best-of-the-week" element={<BestOfWeek />} />
              </Route>

              <Route element={<AuthProtect />}>
                <Route path="/" element={<Home />} />
                <Route path="/login" element={<Login />} />
              </Route>
            </Routes>
            <Footer />
          </AuthProvider>
        </Router>
      </GoogleOAuthProvider>
    </div>
  );
}

export default App;
