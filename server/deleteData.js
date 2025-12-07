import fs from "node:fs";

fs.writeFileSync("./data.json", JSON.stringify({ forms: [] }, null, 2));
console.log("Database wiped!");
