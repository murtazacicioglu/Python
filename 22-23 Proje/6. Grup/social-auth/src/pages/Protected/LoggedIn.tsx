import React, { useContext } from "react";
import AuthContext from "src/context/context";
import { Navigate, Outlet } from "react-router-dom";

const LoggedIn = () => {
  let { profile }: any = useContext(AuthContext);
  return !profile ? <Navigate to="/" /> : <Outlet />;
};

export default LoggedIn;
