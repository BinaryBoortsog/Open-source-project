// =========================
// 1) IMPORT + RUN WIPE FIRST
// =========================
import './wipeDB.js';


// =========================
// 2) THEN LOAD OTHER MODULES
// =========================
import express from "express";
import formRoutes from "./routes/formRoutes.js";
import adminRoutes from "./routes/adminRoutes.js";
import path from "node:path";
import fs from "node:fs";
import https from "node:https";
import http from "node:http";
import { fileURLToPath } from "node:url";

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

const app = express();

app.use(express.json());
app.use(express.static(path.join(__dirname, "../client")));

// Restrict lookup middleware
function restrictLookup(req, res, next) {
  const ip = (req.socket.remoteAddress || "").replace(/^::ffff:/, "");
  if (ip !== "127.0.0.1" && ip !== "::1") {
    return res.status(403).send("Forbidden: lookup only from server PC");
  }
  next();
}

// Lookup routes (local only)
app.use("/form/lookup", restrictLookup);
app.get("/lookup", restrictLookup, (req, res) => {
  res.sendFile(path.join(__dirname, "../client/lookup.html"));
});

// Form routes (LAN ok)
app.use("/form", formRoutes);

// Admin routes (restricted)
app.use("/admin", restrictLookup, (req, res, next) => {
  const auth = req.headers.authorization;
  if (auth !== "Bearer mysecretpassword") {
    return res.status(401).json({ error: "Unauthorized" });
  }
  next();
});
app.use("/admin", adminRoutes);

// Certificates ONLY for HTTPS
const certOptions = {
  key: fs.readFileSync(path.join(__dirname, "cert", "key.pem")),
  cert: fs.readFileSync(path.join(__dirname, "cert", "cert.pem")),
};

// Local-only HTTPS server
https.createServer(certOptions, app).listen(3443, "127.0.0.1", () => {
  console.log(`Local-only HTTPS server running at https://localhost:3443`);
});

// LAN-accessible HTTP server
http.createServer(app).listen(3000, "0.0.0.0", () => {
  console.log(`LAN HTTP server running at http://<your-local-ip>:3000`);
});
