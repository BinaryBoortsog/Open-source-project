// db.js
import { Low } from "lowdb";
import crypto from "node:crypto";
import fs from "node:fs/promises";
import dotenv from "dotenv";

dotenv.config();

const algorithm = "aes-256-gcm";
const password = process.env.DB_SECRET || "supersecretkey";
const key = crypto.scryptSync(password, "salt", 32);

const filePath = "./data.json";

// Encryption
function encryptData(data) {
  const iv = crypto.randomBytes(16);
  const cipher = crypto.createCipheriv(algorithm, key, iv);
  const encrypted = Buffer.concat([cipher.update(JSON.stringify(data), "utf8"), cipher.final()]);
  const tag = cipher.getAuthTag();
  return { iv: iv.toString("hex"), data: encrypted.toString("hex"), tag: tag.toString("hex") };
}

// Decryption
function decryptData(encryptedObj) {
  const { iv, data, tag } = encryptedObj;
  const decipher = crypto.createDecipheriv(algorithm, key, Buffer.from(iv, "hex"));
  decipher.setAuthTag(Buffer.from(tag, "hex"));
  const decrypted = Buffer.concat([decipher.update(Buffer.from(data, "hex")), decipher.final()]);
  return JSON.parse(decrypted.toString("utf8"));
}

// Custom adapter
class EncryptedJSONFile {
  constructor(filename) {
    this.filename = filename;
    this.data = { forms: [] }; // must exist synchronously
  }

  async read() {
    try {
      const raw = await fs.readFile(this.filename, "utf8");
      if (!raw) return;
      const encryptedObj = JSON.parse(raw);
      this.data = decryptData(encryptedObj);
    } catch {
      // file missing or corrupted, start fresh
      this.data = { forms: [] };
      try {
        await this.write();
      } catch (err) {
        console.error("Failed to create new DB file:", err);
      }
    }
  }

  async write() {
    const encrypted = encryptData(this.data);
    await fs.writeFile(this.filename, JSON.stringify(encrypted, null, 2), "utf8");
  }
}

// --- Setup LowDB ---
// --- Setup LowDB ---
const adapter = new EncryptedJSONFile(filePath);

// Ensure the file exists before LowDB uses it
await adapter.read(); 

// Pass default data explicitly
const db = new Low(adapter, { forms: [] });

// fallback in case read failed
db.data ||= { forms: [] };

export default db;

