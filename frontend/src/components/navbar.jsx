import { Bars3Icon, BellIcon, BookmarkIcon } from "@heroicons/react/24/outline";
import Logo from "./logo";

const Navbar = () => {
  return (
    <div className="navbar bg-base-100 pr-3 lg:pr-8">
      {/* Hamburger Icon */}
      <div className="flex-none">
        <label htmlFor="my-drawer" className="btn btn-square btn-ghost">
          <Bars3Icon className="w-6 stroke-base-content" />
        </label>
      </div>
      {/* Name and logo */}
      <div className="flex-1 pl-3 flex gap-2">
        <Logo />
        <div className="text-xl font-black text-base-content">dealringer</div>
      </div>
      {/* Action buttons */}
      {/* Notifications */}
      <div className="flex-none">
        <div className="btn btn-ghost">
          <div className="indicator">
            <BellIcon className="w-6 stroke-base-content stroke-2" />
            <span className="badge badge-xs badge-primary indicator-item"></span>
          </div>
        </div>

        {/* Separator */}
        <div className="w-1"></div>

        {/* User Avatar */}
        <div className="flex">
          <div className="avatar">
            <div className="w-8 rounded-full">
              <img src="https://daisyui.com/images/stock/photo-1534528741775-53994a69daeb.jpg" />
            </div>
          </div>
          <div className="text-base-content hidden md:flex items-center">
            Saarthak
          </div>
        </div>
      </div>
    </div>
  );
};

export default Navbar;
