import express from "express";
import path from "path";
import fs from "fs";
import bodyParser from "body-parser";
import { Configuration, OpenAIApi } from "openai";
import dotenv from "dotenv";

dotenv.config();

const app = express();
const PORT = process.env.PORT || 3000;

// Middleware
app.use(bodyParser.json());

// Serve openapi.json automatically
app.use("/openapi.json", express.static(path.join(process.cwd(), "openapi.json")));

// Logging directory
const logDir = path.join(process.cwd(), "logs");
if (!fs.existsSync(logDir)) fs.mkdirSync(logDir);

// OpenAI setup
const configuration = new Configuration({ apiKey: process.env.OPENAI_API_KEY });
const openai = new OpenAIApi(configuration);

// Ask endpoint
app.post("/ask", async (req, res) => {
  const { question, user_id } = req.body;
  if (!question) return res.status(400).json({ error: "No question provided." });

  try {
    const response = await openai.createChatCompletion({
      model: "gpt-4",
      messages: [{ role: "user", content: question }]
    });

    const answer = response.data.choices[0].message.content;

    // Log the Q&A
    const timestamp = new Date().toISOString();
    const logEntry = `${timestamp} | User: ${user_id || "anon"} | Q: ${question} | A: ${answer}\n`;
    fs.appendFileSync(path.join(logDir, "qa.log"), logEntry);

    res.json({ answer });
  } catch (err) {
    console.error(err);
    res.status(500).json({ error: "Error generating response." });
  }
});

// Health check
app.get("/", (req, res) => res.send("JonGPT backend is running"));

// Start server
app.listen(PORT, () => console.log(`JonGPT backend running on port ${PORT}`));
