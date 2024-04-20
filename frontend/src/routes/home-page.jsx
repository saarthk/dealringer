import { useLoaderData } from "react-router-dom";
import PhoneCardHorizontal from "../components/phonecardhorizontal";
import PaginationGroup from "../components/pagination-btn-group";

export async function loader({ request }) {
  const pageNum = new URL(request.url).searchParams.get("page") ?? "1";
  // const res = await fetch("http://localhost:8000/v1/phones/?page=2");
  const res = await fetch(`http://localhost:8000/v1/phones/?page=${pageNum}`);
  const phones = await res.json();
  return { pageNum: pageNum, phones: phones };
}

const HomePage = () => {
  const { pageNum, phones } = useLoaderData();
  let maxPageNum = phones.next
    ? Math.floor(phones.count / phones.results.length)
    : pageNum;

  return (
    <div className="grow p-10 flex flex-col lg:flex-row items-center gap-2">
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
