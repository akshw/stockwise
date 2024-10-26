import { LinkIcon, ThumbsUp, ThumbsDown, Minus } from "lucide-react";

const Newsfeed = ({ articles }) => {
  return (
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
                  article.sentiment === "Positive"
                    ? "text-green-500"
                    : article.sentiment === "Negative"
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
  );
};
export default Newsfeed;
