import { MagnifyingGlassIcon } from "@heroicons/react/24/outline";
import { Form } from "react-router-dom";

const SearchBar = () => {
  return (
    <Form
      className="input input-bordered rounded-full flex items-center gap-2"
      method="get"
      action="/search"
    >
      <input
        type="text"
        className="grow text-base-content"
        placeholder="Search"
        name="q"
        aria-label="search phones"
      />
      <button
        type="submit"
        className="btn btn-ghost bg-base-300 btn-sm btn-circle"
      >
        <MagnifyingGlassIcon className="w-5 stroke-base-content" />
      </button>
    </Form>
  );
};

export default SearchBar;
