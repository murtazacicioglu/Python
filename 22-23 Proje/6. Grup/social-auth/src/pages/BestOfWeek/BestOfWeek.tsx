import React, { useContext, useEffect, useState } from "react";
import AuthContext from "../../context/context";
import Post from "../../components/Post/Post";
import "./BestOfWeek.css";

function BestOfWeek() {
  const [post, setPost] = useState({});
  const { MostLikedPost }: any = useContext(AuthContext);
  useEffect((): any => {
    fetch("http://127.0.0.1:8000/api/post/most-liked", {
      method: "GET",
      headers: {
        Authorization: "Token " + localStorage.getItem("key"),
      },
    }).then(async (resp: Response) => {
      let data = await resp.json();
      setPost(data.data[0]);
    });
  }, []);
  return (
    <div className="lg:px-16 px-8">
      <div>
        <h3 className="font-semibold text-lg mb-1 mt-5">
          <span className="en">En</span>
          <span className="en-rest ml-[0.3rem]">çok beğenilen gönderi</span>
        </h3>
        <Post post={post} />
      </div>
      <div className="flex justify-end flex-1">
        <div className="max-w-[300x]">
          <h3 className="font-semibold text-lg mb-1 mt-5">
            <span className="en">En</span>
            <span className="en-rest ml-[0.3rem]">çok yorum alan gönderi</span>
          </h3>
          <Post post={post} />
        </div>
      </div>
    </div>
  );
}

export default BestOfWeek;
