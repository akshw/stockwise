import { Search } from "lucide-react";
import { useState } from "react";

const Inputbox = ({ onSearch, isLoading }) => {
  const [stockName, setStockName] = useState("");
  const handleSubmit = (e) => {
    e.preventDefault();
    onSearch(stockName);
  };
  return (
    <>
      <form
        onSubmit={handleSubmit}
        className="flex justify-center items-center space-x-2 mb-8"
      >
        <input
          type="text"
          placeholder="Enter a stock ticker Symbol (e.g., AAPL)"
          value={stockName}
          onChange={(e) => setStockName(e.target.value)}
          className="max-w-xs"
        />
        <button type="submit" disabled={isLoading}>
          {isLoading ? "Searching..." : <Search className="h-4 w-4" />}
        </button>
      </form>
    </>
  );
};

export default Inputbox;
