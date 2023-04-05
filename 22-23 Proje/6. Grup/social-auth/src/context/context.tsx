import { createContext, useState, useEffect } from "react";
import jwt_decode from "jwt-decode";
const AuthContext = createContext({});
import { useNavigate } from "react-router-dom";

export default AuthContext;

export const AuthProvider = ({ children }: any) => {
  const [profile, setProfile] = useState();
  const [googleDataState, setGoogleDataState] = useState();
  const [key, setKey] = useState();
  const navigate = useNavigate();

  useEffect(() => {
    if (localStorage.getItem("key")) {
      getUserByKeyGoogle(localStorage.getItem("key")!, googleDataState);
    }
    if (localStorage.getItem("nkey")) {
      getUserByKey(localStorage.getItem("nkey")!);
    }
  }, [key]);

  const getProfile = async (id: number) => {
    let response = await fetch(`http://localhost:8000/api/profile/${id}`, {
      method: "GET",
      headers: {
        "Content-Type": "application/json",
      },
    }).then(async (resp: Response) => {
      let data = await resp.json();
      setProfile(data["data"]);
    });
  };

  const GoogleGetProfile = async (id: number, googleData: any) => {
    let postData: {} = {
      user: id,
      profilePhotoUrl: googleData?.picture,
    };
    let response = await fetch(
      `http://localhost:8000/api/profile/${id}/google`,
      {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(postData),
      }
    ).then(async (resp: Response) => {
      let data = await resp.json();
      setProfile(data["data"]);
    });
  };

  const getUserByKeyGoogle = async (key: string, googleData: any) => {
    let response = await fetch("http://127.0.0.1:8000/api/auth/user/", {
      method: "GET",
      headers: {
        Authorization: "Token " + key,
      },
    }).then(async (resp: Response) => {
      let data = await resp.json();
      GoogleGetProfile(data["pk"], googleData);
    });
  };

  const getUserByKey = async (key: string) => {
    let response = await fetch("http://127.0.0.1:8000/api/auth/user/", {
      method: "GET",
      headers: {
        Authorization: "Token " + key,
      },
    }).then(async (resp: Response) => {
      let data = await resp.json();
      getProfile(data["pk"]);
    });
  };

  const addProfile = async (data: any) => {
    let response = await fetch("http://localhost:8000/api/profile/add", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(data),
    }).then(async (resp: Response) => {
      let data = await resp.json();
      if (data["msg_en"] == "Profile already exists. 😥") {
        return;
      }
      setProfile(data["data"]);
    });
  };

  const responseGoogle = async (tokens: any) => {
    let resp: Promise<Response | void> = fetch(
      "http://localhost:8000/api/rest-auth/google/",
      {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          access_token: tokens.credential,
        }),
      }
    ).then(async (resp: Response) => {
      if (resp.status == 200) {
        let googleData: any = await jwt_decode(tokens.credential);
        setGoogleDataState(googleData);
        let data: any = await resp.json();
        setKey(data["key"]);
        localStorage.setItem("key", data["key"]);
      }
    });
  };

  const login = (username: string, password: string) => {
    let resp: Promise<Response | void> = fetch(
      "http://127.0.0.1:8000/api/auth/login/",
      {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          username: username,
          password: password,
        }),
      }
    ).then(async (resp: Response) => {
      if (resp.status == 200) {
        let data: any = await resp.json();
        setKey(data["key"]);
        localStorage.setItem("key", data["key"]);
      }
    });
  };

  const logout = async () => {
    let resp = await fetch("http://127.0.0.1:8000/api/auth/logout/", {
      method: "POST",
      headers: {
        Authorization: "Token " + localStorage.getItem("key"),
      },
    }).then(() => {
      setKey(undefined);
      setProfile(undefined);
      localStorage.removeItem("key");
      localStorage.removeItem("nkey");
      localStorage.removeItem("profile");
      navigate("/");
    });
  };

  const toggleSidebar = () => {
    const sidebar = document.querySelector(".sidebar");
    sidebar?.classList.toggle("-right-full");
    sidebar?.classList.toggle("right-0");
  };

  const MostLikedPost = async () => {
    await fetch("http://127.0.0.1:8000/api/post/most-liked", {
      method: "GET",
      headers: {
        Authorization: "Token " + localStorage.getItem("key"),
      },
    }).then(async (resp: Response) => {
      let data = await resp.json();
      return data.data[0];
    });
  };

  let contextData = {
    profile: profile,
    responseGoogle: responseGoogle,
    addProfile: addProfile,
    logout: logout,
    login: login,
    toggleSidebar: toggleSidebar,
    MostLikedPost: MostLikedPost,
  };
  return (
    <AuthContext.Provider value={contextData}>{children}</AuthContext.Provider>
  );
};
