import React from "react";
import FooterDesign from "src/assets/footerDesign.svg";
import Rectangle from "src/assets/Rectangle.svg";
import icon from "src/assets/icon.png";
import { FaFacebookF } from "react-icons/fa/index";
import {
  AiFillLinkedin,
  AiOutlineTwitter,
  AiFillInstagram,
} from "react-icons/ai/index";

function Footer() {
  return (
    <div className="relative py-6 px-2 lg:px-10">
      <div className="flex justify-start px-4 items-center flex-wrap gap-6">
        <div>
          <div className="flex items-center gap-2">
            <img src={icon} alt="icon" className="w-12" />
            <p className="text-lg font-semibold">SportCom</p>
          </div>
          <p className="w-60">
            Nam posuere accumsan porta. Integer id orci sed ante tincidunt
            tincidunt sit amet sed libero.
          </p>
          <p className="mt-2">© SportCom 2023</p>
        </div>
        <div className="flex gap-6 flex-auto items-start flex-wrap">
          <div>
            <h4 className="text-[#37902F] font-semibold text-lg">COMPANY</h4>
            <p className="my-2">Donec dignissim</p>
            <p className="my-2">Curabitur egestas</p>
            <p className="my-2">Nam posuere</p>
            <p className="my-2">Aenean facilisis</p>
          </div>
          <div>
            <h4 className="text-[#37902F] font-semibold text-lg">SERVICES</h4>
            <p className="my-2">Donec dignissim</p>
            <p className="my-2">Curabitur egestas</p>
            <p className="my-2">Nam posuere</p>
            <p className="my-2">Aenean facilisis</p>
          </div>
          <div>
            <h4 className="text-[#37902F] font-semibold text-lg">RESOURCES</h4>
            <p className="my-2">Donec dignissim</p>
            <p className="my-2">Curabitur egestas</p>
            <p className="my-2">Nam posuere</p>
          </div>
        </div>
        <div>
          <div className="flex items-center gap-3">
            <div className="bg-[#D8EED6] w-auto h-auto rounded-full grid place-content-center p-1">
              <FaFacebookF />
            </div>
            <div className="bg-[#D8EED6] w-auto h-auto rounded-full grid place-content-center p-1">
              <AiFillLinkedin />
            </div>
            <div className="bg-[#D8EED6] w-auto h-auto rounded-full grid place-content-center p-1">
              <AiOutlineTwitter />
            </div>
            <div className="bg-[#D8EED6] w-auto h-auto rounded-full grid place-content-center p-1">
              <AiFillInstagram />
            </div>
          </div>
          <div className="grid place-content-center mt-3">
            <div className="w-10 rounded-lg bg-stone-200">
              <img
                src="https://upload.wikimedia.org/wikipedia/commons/thumb/b/b4/Flag_of_Turkey.svg/2000px-Flag_of_Turkey.svg.png"
                alt="Turkish Flag"
                className="w-5 h-5 rounded-full cursor-pointer"
              />
            </div>
          </div>
        </div>
      </div>
      <img
        src={Rectangle}
        alt="Footer"
        className="w-full absolute bottom-0 -z-20 left-0"
      />
      <img
        src={FooterDesign}
        alt="Footer"
        className="w-full absolute bottom-0 -z-10 left-0"
      />
    </div>
  );
}

export default Footer;
