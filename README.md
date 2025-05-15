# 🎬 InVideo ChatBot YouTube Chrome Extension

A powerful Chrome extension that allows users to **ask questions about any YouTube video** and get instant, intelligent answers — even without watching the video. This project combines the power of **LangChain**, **Gemini 1.5 Flash**, **FAISS**, and **YouTubeTranscriptAPI** to create a fully functional Retrieval-Augmented Generation (RAG)-based chatbot that works directly from the browser.

---

## ✨ Key Features

- 🧠 Asks intelligent questions about YouTube videos using LLMs
- 🗣️ Supports **English and Hindi** video transcripts (Hindi is automatically translated)
- 🔎 Uses **LangChain** + **FAISS** for retrieval and similarity search
- 🤖 Powered by **Gemini 1.5 Flash** (via Google Generative AI)
- 📄 Summarizes, explains, or answers based on actual transcript content
- 🌐 Seamless Chrome Extension UI for direct interaction

---

## 📁 Project Structure

```bash

InVideo-AI/
│
├── extension_server/            # Backend Flask server
│   ├── server.py                # Main backend logic
│   ├── requirements.txt         # Python dependencies
│   └── .env                     # Environment variables (add manually)
│
├── extension/                   # Chrome extension code
│   ├── manifest.json
│   ├── popup.html
│   ├── popup.js
│   └── ...                      # Additional static assets (CSS, icons, etc.)
```
---

## 🧑‍💻 Setup Instructions

### 🧪 1. Clone the Repository

```bash
git clone https://github.com/shashu777/InVideo-AI.git
cd InVideo-AI
````

---

### ⚙️ 2. Set Up the Backend (Flask Server)

> ⚠️ Note: Due to **YouTubeTranscriptAPI** being blocked on cloud deployments (e.g. Render, Railway), the server **must be run locally**. This is because YouTube blocks scraping-based requests unless proxies are used — and proxies are costly. So we use local execution instead.

#### 📂 Navigate to the `extension_server` folder:

```bash
cd extension_server
```

#### 🧬 Create a Python virtual environment:

```bash
python -m venv venv
```

#### 🔛 Activate the virtual environment:

**On Windows (CMD):**

```bash
venv\Scripts\activate
```

**On macOS/Linux or Git Bash:**

```bash
./venv/Scripts/activate
```

#### 📦 Install required Python packages:

```bash
pip install -r requirements.txt
```

#### 🔐 Create a `.env` file in the `extension_server` directory:

Add your Google API key:

```
GOOGLE_API_KEY=your_google_api_key_here
```

#### ▶️ Start the Flask server:

```bash
python server.py
```

Once it runs, it should start on `http://127.0.0.1:5000/`

---

### 🌐 3. Set Up the Chrome Extension

1. Open Chrome and go to `chrome://extensions/`
2. Enable **Developer mode** (toggle at top-right)
3. Click **Load unpacked**
4. Select the `extension` folder from this project

You're now ready to use the extension!

---

## 🧠 How It Works – Technical Flow

1. User opens a YouTube video and interacts with the Chrome extension.
2. The extension extracts the video ID and sends it with the user query to the Flask backend (`/query/<flag>`).
3. Backend:

   * Uses `YouTubeTranscriptAPI` to fetch captions (if available).
   * If transcript is in Hindi, detects it using `langdetect` and translates to English using `googletrans`.
   * Transcript is saved to `translated_text.txt`.
4. Text is split into overlapping chunks using `LangChain`’s `RecursiveCharacterTextSplitter`.
5. Chunks are converted to embeddings using `GoogleGenerativeAIEmbeddings`.
6. These are stored in a **FAISS vector store** and used to retrieve the most relevant content.
7. The query and relevant context are passed to **Gemini 1.5 Flash** via LangChain.
8. Gemini responds with a natural language answer, which is shown in the Chrome extension.

---

## 📌 Use Cases

* 📚 Summarize long YouTube tutorials without watching them
* 🔍 Find key points in podcasts or lectures
* 🗣️ Understand Hindi-language videos (translated and processed automatically)
* 🤔 Ask anything about a video and get context-aware answers

---

## ❗ Known Limitations

* Requires **local backend server** due to scraping restriction by YouTubeTranscriptAPI
* Proxy support is not enabled to keep cost minimal
* Only works with videos that have **captions (English or Hindi)**

---

## 🎥 Demo Video

▶️ [Watch the demo video on Google Drive](https://drive.google.com/drive/folders/1cXGxqS9txqP-nIo1LMmpSMVMf0FCBXMG?usp=sharing)


---

## 🖼️ Sample Screenshot

Here is a preview of the extension in action:

![YouTube InVideo Chatbot Screenshot](./assets/screenshot.png)

---

## 📝 Sample Interaction

> **Video ID:** `abc123xyz`
> **Question:** "What is the main topic discussed in this video?"

✅ Chatbot responds:
*"This video discusses the basics of supervised learning, including classification and regression models."*

---

## 🔒 Environment Variables

You need to provide your **Google Generative AI API Key**:

Create `.env` inside `extension_server` and add:

```
GOOGLE_API_KEY='your_google_api_key'
```

---

## 🧾 Requirements (already in `requirements.txt`)

```txt
Flask
flask-cors
googletrans==4.0.0-rc1
langdetect
langchain
langchain_google_genai
langchain_community
python-dotenv
youtube-transcript-api
```

---

## 🤝 Contributions

Pull requests and feedback are welcome! If you encounter bugs or have ideas, please open an issue or submit a PR.

---

## 🔖 Tags

\#LangChain #Gemini #RAG #FAISS #ChromeExtension #YouTube #LLM #AIProject #SmartChatbot #Python #Flask #GoogleGenAI

