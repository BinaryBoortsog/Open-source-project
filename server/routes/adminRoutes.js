import express from "express";
import db from "../db.js";

const router = express.Router();

// Admin: view all forms
router.get("/forms", async (req, res) => {
  db.data ||= {};
  db.data.forms ||= [];
  res.json(db.data.forms);
});

// Admin: delete all forms
router.delete("/forms", async (req, res) => {
  try {
    db.data ||= {};
    db.data.forms = [];
    await db.write();
    res.json({ success: true });
  } catch (err) {
    console.error("Admin delete error:", err);
    res.status(500).json({ error: "Failed to delete forms" });
  }
});



export default router;
