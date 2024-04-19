import PhoneCard from "./phonecard";

const Body = () => {
  return (
    <div className="grow flex justify-between flex-wrap px-10">
      <PhoneCard />
      <PhoneCard />
      <PhoneCard />
      <PhoneCard />
      <PhoneCard />
      <div className="grow"></div>
    </div>
  );
};

export default Body;
