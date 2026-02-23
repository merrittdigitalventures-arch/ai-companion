import express from "express";
import cors from "cors";
import bodyParser from "body-parser";
import dotenv from "dotenv";
import OpenAI from "openai";

dotenv.config();

const app = express();
const PORT = process.env.PORT || 3000;

const openai = new OpenAI({
  apiKey: process.env.OPENAI_API_KEY
});

app.use(cors());
app.use(bodyParser.json());

// In-memory storage for logs
const logs = {};

// Simple token check (replace with real subscription logic)
const validTokens = new Set(["demo-token-123", "another-valid-token"]);

app.post("/ask", async (req, res) => {
  const { question, user_id, token } = req.body;

  if (!question || !user_id || !token) {
    return res.status(400).json({ error: "Missing question, user_id, or token" });
  }

  if (!validTokens.has(token)) {
    return res.status(403).json({ error: "Invalid subscription token" });
  }

  try {
    // Ask OpenAI (GPT-4)
    const response = await openai.chat.completions.create({
      model: "gpt-4o-mini",
      messages: [
        { role: "system", content: "You are JonGPT, a helpful assistant." },
        { role: "user", content: question }
      ],
      max_tokens: 500
    });

    const answer = response.choices[0].message.content;

    // Log in memory
    if (!logs[user_id]) logs[user_id] = [];
    logs[user_id].push({ q: question, a: answer });

    res.json({ answer });
  } catch (err) {
    console.error("Error calling OpenAI:", err);
    res.status(500).json({ error: "Failed to get answer from AI" });
  }
});

// Optional: get logs for a user
app.get("/logs/:user_id", (req, res) => {
  const { user_id } = req.params;
  res.json({ logs: logs[user_id] || [] });
});

app.listen(PORT, () => {
  console.log(`JonGPT backend running on port ${PORT}`);
});
