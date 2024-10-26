import { LinkIcon, ThumbsUp, ThumbsDown, Minus, Search } from "lucide-react";

import { useState } from "react";
import axios from "axios";

const Inputbox = () => {
  const [stockName, setStockName] = useState("");
  const [isLoading, setIsloading] = useState(false);
  const [articles, setArticles] = useState([
    {
      title: "AAPL Reports Strong Q2 Earnings",
      link: "https://example.com/news1",
      sentiment: "Positive",
      score: 0.8,
    },
    {
      title: "TSLA Faces Supply Chain Challenges",
      link: "https://example.com/news2",
      sentiment: "Negative",
      score: 0.6,
    },
    {
      title: "MSFT Announces New Cloud Services",
      link: "https://example.com/news3",
      sentiment: "Positive",
      score: 0.75,
    },
    {
      title: "AMZN Stock Remains Neutral Amid Market Volatility",
      link: "https://example.com/news4",
      sentiment: "Neutral",
      score: 0.5,
    },
    {
      title: "GOOGL Invests in AI Research",
      link: "https://example.com/news5",
      sentiment: "Positive",
      score: 0.85,
    },
  ]);
  const handleSubmit = async (e) => {
    e.preventDefault();
    setIsloading(true);
    console.log(stockName);
    //api call
    try {
      const response = await axios.get(
        "http://localhost:3000/ainews/" + stockName.toLowerCase()
      );
      setArticles(response.data);
      console.log(response.data);
    } catch (err) {
      console.log(err);
    }

    setIsloading(false);
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
      <div>
        <div className="space-y-6">
          <h2 className="text-2xl font-bold text-primary">Latest Stock News</h2>
          {articles.map((article, index) => (
            <div key={index} className="bg-card rounded-lg shadow p-4">
              <div className="flex justify-between items-start">
                <h3 className="text-lg font-semibold mb-2">{article.title}</h3>
                <a
                  href={article.link}
                  target="_blank"
                  rel="noopener noreferrer"
                  className="text-primary hover:text-primary/80"
                >
                  <LinkIcon className="h-5 w-5" />
                </a>
              </div>
              <div className="flex items-center gap-2 text-sm">
                <span
                  className={`font-medium flex items-center ${
                    article.sentiment === "positive"
                      ? "text-green-500"
                      : article.sentiment === "negative"
                      ? "text-red-500"
                      : "text-yellow-500"
                  }`}
                >
                  {article.sentiment === "Positive" ? (
                    <ThumbsUp className="h-4 w-4 mr-1" />
                  ) : article.sentiment === "Negative" ? (
                    <ThumbsDown className="h-4 w-4 mr-1" />
                  ) : (
                    <Minus className="h-4 w-4 mr-1" />
                  )}
                  {article.sentiment}
                </span>
                <span className="text-muted-foreground">
                  Score: {article.score.toFixed(2)}
                </span>
              </div>
            </div>
          ))}
        </div>
      </div>
    </>
  );
};

export default Inputbox;
