import { useLoaderData } from "react-router-dom";
import PhoneCardHorizontal from "../components/phonecardhorizontal";
import PaginationGroup from "../components/pagination-btn-group";

export async function loader({ request }) {
  const url = new URL(request.url);
  const pageNum = url.searchParams.get("page") ?? "1";
  const res = await fetch(`http://localhost:8000/v1/phones?page=${pageNum}`);
  const phones = await res.json();
  return { pageNum: pageNum, phones: phones };
}

const HomePage = () => {
  const { pageNum, phones } = useLoaderData();
  // If phones.next is not null, it means there are more pages to load.
  // So, we calculate the maximum page number based on the total count of phones
  // Else, we use the current page number as the maximum page number.
  const maxPageNum = phones.next
    ? Math.ceil(phones.count / phones.results.length)
    : pageNum;

  return (
    <div className="grow p-10 flex flex-col items-center gap-2">
      {/* Phone Cards */}
      {phones.results.map((phone) => {
        return <PhoneCardHorizontal phone={phone} key={phone.device_id} />;
      })}

      {/* Separator */}
      <div className="h-10"></div>

      {/* Pagination buttons */}
      <PaginationGroup pageNum={pageNum} maxPageNum={maxPageNum} />
    </div>
  );
};

export default HomePage;
