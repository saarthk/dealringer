import { useLoaderData } from "react-router-dom";
import PhoneCardHorizontal from "../components/phonecardhorizontal";
import PaginationGroup from "../components/pagination-btn-group";

export async function loader({ request }) {
  const url = new URL(request.url);
  // Extract the search query and page number from the URL
  const searchQuery = url.searchParams.get("q");
  const pageNum = url.searchParams.get("page") ?? "1";

  const params = new URLSearchParams({ q: searchQuery, page: pageNum });
  const res = await fetch(
    `http://localhost:8000/v1/search?${params.toString()}`,
  );
  const phones = await res.json();

  return {
    pageNum: pageNum,
    searchQuery: searchQuery,
    phones: phones,
  };
}

const SearchPage = () => {
  const { pageNum, searchQuery, phones } = useLoaderData();

  const maxPageNum = phones.next
    ? Math.ceil(phones.count / phones.results.length)
    : pageNum;

  let infoMsg = `Showing results for ${searchQuery}`;
  if (searchQuery == "") {
    infoMsg = "Showing all results";
  } else if (phones.results.length == 0) {
    infoMsg = `No results for ${searchQuery}`;
  }

  return (
    <div className="grow p-10 flex flex-col items-center gap-2">
      <div className="text-base-content">{infoMsg}</div>
      {/* Phone Cards */}
      {phones.results.map((phone) => {
        return <PhoneCardHorizontal phone={phone} key={phone.device_id} />;
      })}
      {/* Separator */}
      <div className="h-10"></div>
      {/* Pagination buttons */}
      <PaginationGroup pageNum={pageNum} maxPageNum={maxPageNum} />j
    </div>
  );
};

export default SearchPage;
