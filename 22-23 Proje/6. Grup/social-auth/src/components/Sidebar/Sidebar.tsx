import { useContext } from "react";
import { HiBars3BottomRight } from "react-icons/hi2";
import { Link } from "react-router-dom";
import AuthContext from "../../context/context";

function Sidebar() {
  function toggleSidebar() {
    const sidebar = document.querySelector(".sidebar");
    sidebar?.classList.toggle("-right-full");
    sidebar?.classList.toggle("right-0");
  }
  let { profile, logout }: any = useContext(AuthContext);
  console.log(profile);

  return (
    <div className="h-full sidebar py-5 px-6 fixed md:hidden block -right-full top-0 bg-[#F6F6F6] w-5/6 sm:w-3/4 z-50 shadow-md duration-300">
      <div className="flex justify-end ">
        <HiBars3BottomRight
          size={22}
          className="cursor-pointer text-[#3A902F]"
          onClick={toggleSidebar}
        />
      </div>
      <div className="flex flex-col items-end text-lg font-semibold text-[#37902F] gap-6 mt-5">
        <Link to={"/"} className="w-fit">
          Anasayfa
        </Link>
        <Link to={"/"} className="w-fit">
          En Popülerler
        </Link>
        <Link to={"/"} className="w-fit">
          Haberler
        </Link>
        <Link to={"/best-of-the-week"} className="w-fit">
          Haftanın Enleri
        </Link>
        {profile ? (
          <div onClick={logout}>Çıkış Yap</div>
        ) : (
          <Link to={"/login"}>Giriş Yap</Link>
        )}
      </div>
    </div>
  );
}

export default Sidebar;
