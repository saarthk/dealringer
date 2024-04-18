import {
  HomeIcon,
  TagIcon,
  BellIcon,
  BookmarkIcon,
  EnvelopeIcon,
  PowerIcon,
} from "@heroicons/react/24/outline";

const Sidebar = () => {
  return (
    <div className="py-4 px-2 w-56 min-h-full bg-base-200 text-base-content flex flex-col">
      {/* Top section */}
      <ul className="menu">
        <li>
          <a>
            <HomeIcon className="w-5 stroke-2 stroke-orange-400" />
            <span className="font-bold">Home</span>
          </a>
        </li>

        <li>
          <details open>
            <summary>
              <TagIcon className="w-5 stroke-2 stroke-green-500" />
              <span className="font-bold">Brand</span>
            </summary>
            <ul>
              <li>
                <a>Apple</a>
              </li>
              <li>
                <a>Google</a>
              </li>
              <li>
                <a>Samsung</a>
              </li>
              <li>
                <a>OnePlus</a>
              </li>
              <li>
                <a>Xiaomi</a>
              </li>
            </ul>
          </details>
        </li>
      </ul>
      {/* Mid section */}
      <ul className="menu">
        <li></li>
        <li>
          <a>
            <BellIcon className="w-5 stroke-2" />
            <span className="font-bold">Notifications</span>
          </a>
        </li>
        <li>
          <a>
            <BookmarkIcon className="w-5 stroke-2" />
            <span className="font-bold">Saved</span>
          </a>
        </li>

        {/* Alert toggle */}
        <li>
          <div className="flex">
            <EnvelopeIcon className="w-5 stroke-2" />
            <span className="font-bold">Alerts</span>
            <div className="w-10"></div>
            {/* Refer: https://www.codemzy.com/blog/how-to-react-checkbox */}
            <input
              type="checkbox"
              className="toggle toggle-sm toggle-success justify-self-end"
              defaultChecked={true}
            />
          </div>
        </li>
      </ul>

      {/* End section */}
      <ul className="menu">
        <li></li>
        <li>
          <a>
            <PowerIcon className="w-5 stroke-2 stroke-red-500" />
            <span className="font-bold">Logout</span>
          </a>
        </li>
      </ul>
    </div>
  );
};

export default Sidebar;
