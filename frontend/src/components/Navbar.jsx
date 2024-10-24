const Navbar = () => {
  return (
    <>
      <div className=" flex justify-between shadow-md">
        <div className="text-2xl font-bold px-8 py-6">StockWise</div>
        <a
          href="https://github.com/akshw/stockwise"
          className=" text-lg px-8 py-6"
        >
          Github
        </a>
      </div>
    </>
  );
};

export default Navbar;
