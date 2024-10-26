import Navbar from "./components/Navbar";
import Inputbox from "./components/InputBox";
import Hero from "./components/Hero";
import Footer from "./components/Footer";
import Newsfeed from "./components/Newsfeed";
import { useState } from "react";

const App = () => {
  const sampleNewsData = [
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
  ];

  const [newsArticles, setNewsArticles] = useState(sampleNewsData);
  const [isLoading, SetIsloading] = useState(false);

  const handleSearch = async () => {
    isLoading(true);
    await new Promise((resolve) => setTimeout(resolve, 1000));
    //api call
    setNewsArticles(sampleNewsData);
    SetIsloading(false);
  };
  return (
    <>
      <Navbar />
      <Hero />
      <Inputbox onSearch={handleSearch} isLoading={isLoading} />
      <Newsfeed articles={newsArticles} />
      <Footer />
    </>
  );
};

export default App;
