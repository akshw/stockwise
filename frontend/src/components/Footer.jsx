import { Newspaper, BarChart, Github } from "lucide-react";

const Footer = () => {
  return (
    <footer className="bg-background border-t">
      <div className="max-w-7xl mx-auto py-6 px-4 sm:px-6 lg:px-8">
        <div className="flex justify-center space-x-6">
          <a
            href="https://markets.businessinsider.com/news/"
            target="_blank"
            className="text-muted-foreground hover:text-primary"
          >
            <Newspaper className="h-6 w-6" />
          </a>
          <a
            href="https://huggingface.co/ProsusAI/finbert"
            target="_blank"
            className="text-muted-foreground hover:text-primary"
          >
            <BarChart className="h-6 w-6" />
          </a>
          <a
            href="https://github.com/akshw/stockwise"
            target="_blank"
            className="text-muted-foreground hover:text-primary"
          >
            <Github className="h-6 w-6" />
          </a>
        </div>
        <p className="text-center text-muted-foreground mt-4">
          © 2023 StockAI News. All rights reserved.
        </p>
      </div>
    </footer>
  );
};

export default Footer;
