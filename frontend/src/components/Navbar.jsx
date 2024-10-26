import { Github, TrendingUp } from "lucide-react";

const Navbar = () => {
  return (
    <>
      <nav className="bg-background shadow-sm">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between h-16">
            <div className="flex items-center">
              <TrendingUp className="h-8 w-8 text-primary" />
              <span className="ml-2 text-xl font-bold text-primary">
                StockWise
              </span>
            </div>
            <div className="flex items-center">
              <a
                href="https://github.com/akshw/stockwise"
                target="_blank"
                rel="noopener noreferrer"
                className="text-muted-foreground hover:text-primary"
              >
                <Github className="h-6 w-6" />
              </a>
            </div>
          </div>
        </div>
      </nav>
    </>
  );
};

export default Navbar;
