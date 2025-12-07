import crypto from "node:crypto";
import fs from "node:fs";
import path from "node:path";
import dotenv from "dotenv";

dotenv.config();

const algorithm = "aes-256-gcm";
const password = process.env.DB_SECRET || "supersecretkey";
const key = crypto.scryptSync(password, "salt", 32);

function encryptData(data) {
  const iv = crypto.randomBytes(16);
  const cipher = crypto.createCipheriv(algorithm, key, iv);
  const encrypted = Buffer.concat([cipher.update(JSON.stringify(data), "utf8"), cipher.final()]);
  const tag = cipher.getAuthTag();
  return { iv: iv.toString("hex"), data: encrypted.toString("hex"), tag: tag.toString("hex") };
}

// Absolute path to your server data.json
const dbPath = path.resolve("C:/Users/PC/Desktop/consular-system/server/data.json");

const emptyEncrypted = encryptData({ forms: [] });
fs.writeFileSync(dbPath, JSON.stringify(emptyEncrypted, null, 2));

console.log(`✔ Encrypted DB wiped and reset at ${dbPath}!`);
