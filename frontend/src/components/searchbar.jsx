import { MagnifyingGlassIcon } from "@heroicons/react/24/outline";

const SearchBar = () => {
  return (
    <label className="input input-bordered rounded-full flex items-center gap-2">
      <input
        type="text"
        className="grow text-base-content"
        placeholder="Search"
      />
      <MagnifyingGlassIcon className="w-5 stroke-base-content" />
    </label>
  );
};

export default SearchBar;
