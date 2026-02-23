import express from "express";
import cors from "cors";
import bodyParser from "body-parser";
import dotenv from "dotenv";
import OpenAIPkg from "openai";  // default import for CommonJS module

dotenv.config();

const { OpenAI } = OpenAIPkg;  // destructure OpenAI class

const app = express();
const PORT = process.env.PORT || 3000;

app.use(cors());
app.use(bodyParser.json());

// Initialize OpenAI client
const openai = new OpenAI({
  apiKey: process.env.OPENAI_API_KEY
});

// In-memory logs
const logs = {};

// Demo valid tokens
const validTokens = new Set(["demo-token-123", "another-valid-token"]);

// Ask endpoint
app.post("/ask", async (req, res) => {
  const { question, user_id, token } = req.body;

  if (!question || !user_id || !token) {
    return res.status(400).json({ error: "Missing question, user_id, or token" });
  }

  if (!validTokens.has(token)) {
    return res.status(403).json({ error: "Invalid subscription token" });
  }

  try {
    const response = await openai.chat.completions.create({
      model: "gpt-4o-mini",
      messages: [
        { role: "system", content: "You are JonGPT, a helpful assistant." },
        { role: "user", content: question }
      ],
      max_tokens: 500
    });

    const answer = response.choices[0].message.content;

    if (!logs[user_id]) logs[user_id] = [];
    logs[user_id].push({ q: question, a: answer });

    res.json({ answer });
  } catch (err) {
    console.error("Error calling OpenAI:", err);
    res.status(500).json({ error: "Failed to get answer from AI" });
  }
});

// Logs endpoint
app.get("/logs/:user_id", (req, res) => {
  const { user_id } = req.params;
  res.json({ logs: logs[user_id] || [] });
});

// Start server
app.listen(PORT, () => {
  console.log(`JonGPT backend running on port ${PORT}`);
});
