import clsx from "clsx/lite";
import { Link } from "react-router-dom";

const PaginationGroup = ({ pageNum, maxPageNum }) => {
  // To ensure that the page number is within the bounds
  pageNum = Math.min(pageNum, maxPageNum);

  // Generate an array of deltas
  // Delta is the difference between the current page number and the page number of a button
  // For example, if the current page number is 4, deltas of pages [2,3,4,5] are [-2,-1,0,1]
  const deltas = [-2, -1, 0, 1, 2].filter((d) => {
    const p = pageNum + d;
    // Filter out the deltas that are out of bounds
    return p > 0 && p <= maxPageNum;
  });

  return (
    <div className="join">
      {/* Next arrow */}
      {pageNum > 1 && (
        <>
          {/* <button className="join-item btn">«</button> */}
          <Link to={`?page=${pageNum - 1}`} className="join-item btn">
            ‹
          </Link>
        </>
      )}

      {/* Page number buttons */}
      {deltas.map((d) => {
        return (
          <Link
            to={`?page=${pageNum + d}`}
            // If delta is 0, i.e., it's the current page, show an active button
            className={clsx("join-item btn", d == 0 && "btn-active")}
            key={d}
          >
            {pageNum + d}
          </Link>
        );
      })}

      {/* Previous arrow */}
      {pageNum < maxPageNum && (
        <>
          <Link to={`?page=${pageNum + 1}`} className="join-item btn">
            ›
          </Link>
          {/* <button className="join-item btn">»</button> */}
        </>
      )}
    </div>
  );
};

export default PaginationGroup;
