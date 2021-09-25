var fs = require('fs')

fs.readFile("./players.json", function(error, content) {
  const obj = JSON.parse(content);
  console.log(obj["0"].Name);
})