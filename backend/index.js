const express = require("express");
const app = express();
const mongoose = require("mongoose");
const cors = require("cors");
const bodyparser = require("body-parser");
require("dotenv").config();
const axios = express();

app.use(cors());
app.use(express.json());
app.use(bodyparser.json());

const DATABASE_URL = process.env.DATABASE_URL;
mongoose.connect(DATABASE_URL);

const dataSchema = new mongoose.Schema({
  datetime: String,
  name: String,
  title: String,
  link: String,
  sentiment: String,
  score: Number,
});

const data = mongoose.model("news_feed1", dataSchema);

app.get("/ainews/:name", async (req, res) => {
  try {
    const name = req.params.name;
    const response = await data.find({ name: name });
    console.log("here");
    console.log(response);

    if (response && response.length > 0) {
      console.log("here1");
      return res.json(response);
    } else {
      console.log("here2");
      const scrape_res = await axios.get("http://localhost:5000/stock", {
        params: { ticker: name },
      });

      if (scrape_res) {
        const response = await data.find({ name: name });
        res.json(response);
      }
    }
  } catch (error) {
    res.status(500).send(error);
  }
});

app.get("/", (req, res) => {
  res.send("stockwise");
});

app.listen(3000, () => {
  console.log("server running at 3000");
});
