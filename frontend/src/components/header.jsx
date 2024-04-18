import Navbar from "./navbar";
import SearchBar from "./searchbar";

const Header = () => {
  return (
    <div className="flex flex-col px-2">
      <Navbar />
      <div className="px-4 py-2">
        <SearchBar />
      </div>
    </div>
  );
};

export default Header;
