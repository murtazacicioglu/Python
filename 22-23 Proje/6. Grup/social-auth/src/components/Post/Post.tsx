import { BsThreeDots } from "react-icons/bs";
import { AiFillHeart } from "react-icons/ai";
import { TfiCommentAlt } from "react-icons/tfi";
import "./Post.css";
function Post(post: any) {
  let Post = post.post;
  return (
    <>
      {post.post.profile_id != undefined ? (
        <div className="shadow-lg bg-[#F6F6F6] rounded-md max-w-md p-3">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-2">
              {Post?.profile?.profilePhotoUrl ? (
                <img
                  src={Post?.profile?.profilePhotoUrl}
                  alt="PP"
                  className="rounded-full w-8 h-8 border border-[#C5C5C5]"
                />
              ) : (
                <div className="rounded-full select-none w-8 h-8 border font-semibold text-sm bg-slate-300 border-[#C5C5C5] grid place-content-center">
                  {Post?.profile?.user?.username.slice(0, 2).toUpperCase()}
                </div>
              )}
              <p>{Post?.profile?.user?.username}</p>
              <p className="font-bold scale-110">•</p>
              <p>4g</p>
            </div>
            <BsThreeDots />
          </div>
          <p className="my-2">{Post?.text}</p>
          <div className="flex items-center justify-around">
            <div className="flex items-center gap-1">
              <TfiCommentAlt className="cursor-pointer" />
              <p>1</p>
            </div>
            <div className="flex items-center gap-1">
              <AiFillHeart className="cursor-pointer" color="red" size={19} />
              <p>{Post?.like_count}</p>
            </div>
          </div>
        </div>
      ) : (
        <div className="shadow-lg bg-[#F6F6F6] rounded-md max-w-md p-3">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-2">
              <div className="rounded-full w-8 h-8 border font-semibold text-sm bg-stone-300 grid place-content-center fade-bg"></div>
              <div className="w-28 h-3 rounded-lg bg-stone-300 fade-bg"></div>
            </div>
            <BsThreeDots />
          </div>
          <p className="my-2 w-5/6 h-2 bg-stone-300 rounded-lg fade-bg"></p>
          <p className="my-2 w-5/6 h-2 bg-stone-300 rounded-lg fade-bg"></p>
          <p className="my-2 w-5/6 h-2 bg-stone-300 rounded-lg fade-bg"></p>
          <div className="flex items-center justify-around">
            <div className="flex items-center gap-1">
              <TfiCommentAlt className="cursor-pointer" color="gray" />
              <p className="w-3 h-2 rounded-lg bg-stone-300 fade-bg"></p>
            </div>
            <div className="flex items-center gap-1">
              <AiFillHeart className="cursor-pointer" color="gray" size={19} />
              <p className="w-3 h-2 rounded-lg bg-stone-300 fade-bg"></p>
            </div>
          </div>
        </div>
      )}
    </>
  );
}

export default Post;
