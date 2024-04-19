import PhoneCard from "./phonecard";
import PhoneCardHorizontal from "./phonecardhorizontal";

const Body = () => {
  return (
    <div className="grow p-10 flex flex-col lg:flex-row items-center gap-2">
      <PhoneCardHorizontal />
      <PhoneCardHorizontal />
      <PhoneCardHorizontal />
    </div>
  );
};

export default Body;
