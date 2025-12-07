// server/routes/formRoutes.js
import express from "express";
import db from "../db.js";
import { nanoid } from "nanoid";
import createFormEntry from "../models/FormEntry.js";
import { customAlphabet } from "nanoid";

const router = express.Router();

// --- Simple sanitizer ---
function sanitize(str) {
  if (typeof str !== "string") return str;
  return str
    .replaceAll("&", "&amp;")
    .replaceAll("<", "&lt;")
    .replaceAll(">", "&gt;")
    .replaceAll("\"", "&quot;")
    .replaceAll("'", "&#39;");
}

const nanoidNumbers = customAlphabet("0123456789", 4);

// --- Sanitize all fields recursively ---
function sanitizeData(obj) {
  const result = {};
  for (const key in obj) {
    if (typeof obj[key] === "object" && obj[key] !== null) {
      result[key] = sanitizeData(obj[key]);
    } else {
      result[key] = sanitize(obj[key]);
    }
  }
  return result;
}

router.post("/submit", async (req, res) => {
  try {
    const rawData = req.body;
    const safeData = sanitizeData(rawData);

    const code = nanoidNumbers();
    const entry = createFormEntry(safeData, code);

    // Ensure db structure exists
    db.data ||= {};
    db.data.forms ||= [];
    db.data.forms.push(entry);
    await db.write();

    res.json({ success: true, code });
  } catch (err) {
    console.error("Error submitting form:", err);
    res.status(500).json({ success: false, error: "Server error" });
  }
});


router.get("/lookup/:code", async (req, res) => {
  try {
    db.data ||= {};
    db.data.forms ||= [];

    const code = sanitize(req.params.code.toUpperCase());
    const entry = db.data.forms.find(f => f.id === code);

    if (!entry) return res.status(404).json({ error: "Not found" });

    res.json(entry);
  } catch (err) {
    console.error("Lookup error:", err);
    res.status(500).json({ error: "Server error" });
  }
});

export default router;
