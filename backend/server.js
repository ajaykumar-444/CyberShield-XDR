import express from "express";
import cors from "cors";
import dotenv from "dotenv";
import axios from "axios";

dotenv.config();

const app = express();

app.use(cors());
app.use(express.json());



// 🤖 GEMINI CHAT ROUTE
app.post("/chat", async (req, res) => {
    const userMessage = req.body.message;

    try {
        const response = await axios.post(
            `https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key=${process.env.GEMINI_API_KEY}`,
            {
                contents: [
                    {
                        parts: [
                            {
                                text: userMessage
                            }
                        ]
                    }
                ]
            }
        );

        const reply =
            response.data.candidates?.[0]?.content?.parts?.[0]?.text ||
            "No response from AI";

        res.json({ reply });

    } catch (error) {
        console.log(error.response?.data || error.message);

        res.status(500).json({
            error: "Gemini API error"
        });
    }
});

app.listen(5000, () => {
    console.log("Server running on http://127.0.0.1:5000");
});