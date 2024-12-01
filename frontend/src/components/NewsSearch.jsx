import { LinkIcon, ThumbsUp, ThumbsDown, Minus, Search } from "lucide-react";

import { useState } from "react";
import axios from "axios";

const NewsSearch = () => {
  const [stockName, setStockName] = useState("");
  const [isLoading, setIsloading] = useState(false);
  const [articles, setArticles] = useState([
    {
      description:
        "Meta Platforms (META) provided strong guidance buoyed by its extensive thrust on generative artificial intelligence.",
      link: "https://finance.yahoo.com/news/buy-meta-platforms-long-term-123200995.html?.tsrc=rss",
      name: "meta",
      score: 0.9496831297874451,
      sentiment: "positive",
      title:
        "Buy Meta Platforms With a Long-Term Perspective After Q3 Earnings Beat",
    },
    {
      description:
        "Which of these niche social media companies has a brighter future?",
      link: "https://www.fool.com/investing/2024/11/05/better-social-media-stock-trump-media-vs-rumble/?source=eptyholnk0000202&utm_source=yahoo-host-full&utm_medium=feed&utm_campaign=article&referring_guid=0b22043b-e087-4ffa-b6a4-7e111925566b&.tsrc=rss",
      name: "meta",
      score: 0.6972834467887878,
      sentiment: "neutral",
      title: "Better Social Media Stock: Trump Media vs. Rumble",
    },
    {
      description:
        "The volume and methods for disinformation campaigns have grown since 2020, with a rise in bot accounts and deepfakes on social media.",
      link: "https://finance.yahoo.com/news/election-misinformation-thrived-online-during-100700252.html?.tsrc=rss",
      name: "meta",
      score: 0.4951629042625427,
      sentiment: "neutral",
      title:
        "How election misinformation thrived online during the 2024 presidential race—and will likely continue in the days to come",
    },
    {
      description:
        "Meta Platforms and Alphabet could surpass Nvidia's $3.3 trillion market value within four years.",
      link: "https://www.fool.com/investing/2024/11/05/2-ai-stock-worth-more-than-nvidia-stock-by-2028/?source=eptyholnk0000202&utm_source=yahoo-host-full&utm_medium=feed&utm_campaign=article&referring_guid=1d2db716-34e3-422e-a339-a67aae54550a&.tsrc=rss",
      name: "meta",
      score: 0.8659570217132568,
      sentiment: "positive",
      title:
        "Prediction: 2 Unstoppable AI Stocks Will Be Worth More Than Nvidia Stock by 2028 (or Sooner)",
    },
    {
      description:
        "Meta’s (META) plan to join the tech race for nuclear power has reportedly been foiled by bees.",
      link: "https://www.yahoo.com/tech/metas-nuclear-power-plans-were-194801911.html?.tsrc=rss",
      name: "meta",
      score: 0.5565478801727295,
      sentiment: "neutral",
      title: "Meta's nuclear power plans were foiled by bees — yes, bees",
    },
    {
      description:
        "Instagram's adding EU users, as Facebook sees a slight decline.",
      link: "https://www.socialmediatoday.com/news/instagram-now-more-users-than-facebook-eu/731951/?.tsrc=rss",
      name: "meta",
      score: 0.8936432600021362,
      sentiment: "negative",
      title: "Instagram Has More Users Than Facebook in the EU",
    },
    {
      description:
        "Meta Platforms (META) is well positioned to outperform the market, as it exhibits above-average growth in financials.",
      link: "https://finance.yahoo.com/news/meta-platforms-meta-incredible-growth-174510027.html?.tsrc=rss",
      name: "meta",
      score: 0.9308555722236633,
      sentiment: "positive",
      title:
        "Meta Platforms (META) is an Incredible Growth Stock: 3 Reasons Why",
    },
    {
      description:
        "We recently compiled a list of the Jim Cramer is Talking About These 7 Stocks. In this article, we are going to take a look at where Meta Platforms, Inc. (NASDAQ:META) stands against the other stocks Jim Cramer is currently talking about. Jim Cramer, the host of Mad Money, recently delved into the complexities of disappointing […]",
      link: "https://finance.yahoo.com/news/jim-cramer-meta-platforms-inc-171538211.html?.tsrc=rss",
      name: "meta",
      score: 0.9394007325172424,
      sentiment: "neutral",
      title:
        "Jim Cramer on Meta Platforms, Inc. (META): ‘There Was No Beat And Raise Lingo’",
    },
  ]);
  const handleSubmit = async (e) => {
    e.preventDefault();
    setIsloading(true);
    console.log(stockName);
    try {
      const response = await axios.get(
        "http://localhost:3001/ainews/" + stockName.toLowerCase()
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
      <div className="mt-8">
        <form
          onSubmit={handleSubmit}
          className="flex justify-center items-center space-x-4 mb-8"
        >
          <input
            type="text"
            placeholder="Search ticker symbols (e.g AAPL)"
            value={stockName}
            onChange={(e) => setStockName(e.target.value)}
            className="max-w-xl  border border-black px-4 py-2 rounded-lg"
          />
          <button type="submit" disabled={isLoading}>
            {isLoading ? "Searching..." : <Search className="h-6 w-10" />}
          </button>
        </form>
      </div>

      {/* News */}

      <div>
        <div className="space-y-6 lg:w-1/2 mx-auto">
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
              <div className="pb-4 px-2">
                <p>{article.description}</p>
              </div>
              <div className="flex items-center gap-2 text-sm">
                <span
                  className={`font-medium text-lg flex items-center ${
                    article.sentiment === "positive"
                      ? "text-green-500"
                      : article.sentiment === "negative"
                      ? "text-red-500"
                      : "text-yellow-500"
                  }`}
                >
                  {article.sentiment === "positive" ? (
                    <ThumbsUp className="h-4 w-4 mr-1" />
                  ) : article.sentiment === "negative" ? (
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

export default NewsSearch;
