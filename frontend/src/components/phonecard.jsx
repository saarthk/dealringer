import { BookmarkIcon, BellIcon } from "@heroicons/react/24/outline";
import { useState } from "react";
import clsx from "clsx/lite";

const PhoneCard = () => {
  const [alert, setAlert] = useState(false);

  return (
    <div className="flex flex-col shadow-xl p-1">
      <div className="flex">
        {/* Phone image */}
        <div className="h-40 flex relative">
          <img
            src="https://m-cdn.phonearena.com/images/phones/82892-800/Apple-iPhone-13.jpg"
            alt="Apple iPhone 13"
            className="h-full object-cover"
          />
          <button
            className="bg-base-100 btn btn-ghost btn-circle btn-xs absolute top-4 right-4"
            onClick={() => {
              setAlert(!alert);
            }}
          >
            <BellIcon
              className={clsx(
                "w-5 stroke-base-content stroke-2",
                alert && "fill-yellow-400",
              )}
            />
          </button>
        </div>
      </div>

      {/* Body */}
      <div className="py-3 px-3 flex flex-col">
        <div className="text-neutral font-medium text-sm">
          <span className="text-neutral">Apple</span> iPhone 13
        </div>
        <div className="text-neutral text-2xl font-bold">
          <span className="text-sm font-thin">₹ </span>36,999
        </div>
        <div className="grow"></div>
        {/* <div className="w-1/2 btn btn-primary btn-xs">View</div> */}
      </div>
    </div>
  );
};

export default PhoneCard;
