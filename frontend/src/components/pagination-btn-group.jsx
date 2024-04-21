import clsx from "clsx/lite";
import { useSearchParams } from "react-router-dom";

const PaginationGroup = ({ pageNum, maxPageNum }) => {
  let [searchParams, setSearchParams] = useSearchParams();

  const updatePageNum = (newPageNum) => {
    searchParams.set("page", newPageNum);
    setSearchParams(searchParams);
  };

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
      {/* Previous arrow */}
      {pageNum > 1 && (
        <>
          <button
            className="join-item btn"
            onClick={() => updatePageNum(pageNum - 1)}
          >
            ‹
          </button>
        </>
      )}

      {/* Page number buttons */}
      {deltas.map((d) => {
        return (
          <button
            onClick={() => updatePageNum(pageNum + d)}
            className={clsx("join-item btn", d == 0 && "btn-active")}
            key={d}
          >
            {pageNum + d}
          </button>
        );
      })}

      {/* Next arrow */}
      {pageNum < maxPageNum && (
        <>
          <button
            className="join-item btn"
            onClick={() => updatePageNum(pageNum + 1)}
          >
            ›
          </button>
        </>
      )}
    </div>
  );
};

export default PaginationGroup;
