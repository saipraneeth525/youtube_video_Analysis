const express = require("express");
const app = express();

app.get("/", (req, res) => {
  res.send("Backend Running ✅");
});

app.listen(4000, () => {
  console.log("Backend running on port 4000");
});

