import { Link } from "react-router-dom";
import { GoogleLogin } from "@react-oauth/google";
import jwt_decode from "jwt-decode";
import { useContext, useState } from "react";
import AuthContext from "src/context/context";
function Login() {
  let { responseGoogle, login }: any = useContext(AuthContext);

  const [username, setUsername]: any = useState("");
  const [password, setPassword]: any = useState("");

  return (
    <>
      <Link to={"/"}>Home</Link>
      <div>
        <input
          type="text"
          placeholder="username"
          onChange={(e) => {
            setUsername(e.target.value);
          }}
          className="border"
        />
      </div>
      <div>
        <input
          type="password"
          placeholder="password"
          onChange={(e) => {
            setPassword(e.target.value);
          }}
          className="border"
        />
      </div>
      <button
        className="bg-blue-500"
        onClick={() => {
          login(username, password);
        }}
      >
        Login
      </button>
      <GoogleLogin
        onSuccess={responseGoogle}
        onError={() => {
          console.log("Login Failed");
        }}
      />
    </>
  );
}

export default Login;
