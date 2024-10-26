import { Newspaper, BarChart, DollarSign } from "lucide-react";

const Hero = () => {
  return (
    <>
      <div className="relative py-20 flex items-center justify-center bg-gradient-to-br from-primary/10 to-secondary/10 overflow-hidden">
        <div className="absolute inset-0 bg-grid-white/10 bg-grid-16 [mask-image:radial-gradient(ellipse_at_center,white,transparent_75%)]" />
        <div className="relative z-10 text-center px-4 sm:px-6 lg:px-8">
          <h1 className="text-4xl sm:text-5xl md:text-6xl font-extrabold text-primary mb-4 tracking-tight">
            Get AI-Generated Stock News
          </h1>
          <h2 className="text-2xl sm:text-3xl md:text-4xl font-bold text-secondary mb-6">
            For Stock You Wish
          </h2>
          <p className="text-lg sm:text-xl text-muted-foreground mb-8 max-w-2xl mx-auto">
            Stay ahead of the market with personalized AI insights on any
            stocknews youre interested in.
          </p>
          <div className="flex justify-center space-x-8">
            <div className="flex items-center">
              <Newspaper className="h-6 w-6 text-primary mr-2" />
              <span>Real-time News</span>
            </div>
            <div className="flex items-center">
              <BarChart className="h-6 w-6 text-primary mr-2" />
              <span>Sentiment Analysis</span>
            </div>
            <div className="flex items-center">
              <DollarSign className="h-6 w-6 text-primary mr-2" />
              <span>Market Insights</span>
            </div>
          </div>
        </div>
      </div>
    </>
  );
};
export default Hero;
