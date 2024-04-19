import { BellIcon } from "@heroicons/react/24/outline";
import { useState } from "react";
import clsx from "clsx/lite";

const PhoneCardHorizontal = () => {
  const [isAlert, setAlert] = useState(false);

  return (
    <div className="h-48 w-full lg:w-1/4 px-8 py-6 flex shadow-xl">
      {/* Phone image */}
      <div className="h-full">
        <img
          src="https://m-cdn.phonearena.com/images/phones/82892-800/Apple-iPhone-13.jpg"
          alt="Apple iPhone 13"
          className="h-full object-cover"
        />
      </div>

      {/* Separator */}
      <div className="w-5"></div>

      {/* Card body */}
      <div className="grow flex flex-col">
        {/* Separator */}
        <div className="h-5"></div>
        <div className="badge badge-success badge-sm badge-outline font-medium">
          Price drop!
        </div>
        <div className="h-1"></div>
        <div className="text-base-content">Apple iPhone 13</div>
        <div className="text-base-content font-bold">₹36,999</div>
        {/* Separator */}
        <div className="h-5"></div>
        <div className="flex items-center">
          <button
            className="bg-base-300 btn btn-ghost btn-circle btn-xs"
            onClick={() => {
              setAlert(!isAlert);
            }}
          >
            <BellIcon
              className={clsx(
                "w-7 p-0.5 stroke-base-content stroke-2",
                isAlert && "fill-yellow-300",
              )}
            />
          </button>
          {/* <p className="text-base-content text-xs">Set alert</p> */}
          <div className="grow"></div>
          <button className="btn btn-primary btn-xs">View</button>
        </div>
      </div>
    </div>
  );
};

export default PhoneCardHorizontal;
