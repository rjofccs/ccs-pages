var fs = require("fs");

// fs.writeFile('input.txt', 'input', f=>{});
var jsonData = '{"persons":[{"name":"John","city":"New York"},{"name":"Phil","city":"Ohio"}]}'; 
var jsonParsed = JSON.parse(jsonData); 
jsonData = JSON.stringify(jsonParsed);
console.log(jsonData);