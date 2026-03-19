# tweet_generatora_agent

# 🚀 AI Tweet Generator & Optimizer (LangGraph + Groq)

This project is an **AI-powered Tweet Generation and Optimization system** built using **LangGraph, LangChain, and Groq (LLM)**.

It automatically:
1. Generates a tweet  
2. Evaluates it (approval/rejection)  
3. Improves it iteratively  
4. Stops when approved or max iterations reached  

---

## 🧠 How It Works

The workflow follows a loop:

```
Generate Tweet → Evaluate → Improve → Evaluate → ... → End
```

### 🔄 Flow Breakdown

- **tweet_gen** → Generates a tweet  
- **tweet_approval** → Reviews the tweet  
- **tweet_optimizer** → Improves based on feedback  
- **Router** → Decides whether to stop or continue  

---

## 🛠️ Tech Stack

- **LangChain**
- **LangGraph**
- **Groq LLM (llama-3.3-70b-versatile)**
- **Pydantic**
- **Python**

---

## 📂 Project Structure

```
.
├── main.py
├── .env
├── README.md
```

---

## ⚙️ Setup Instructions

### 1️⃣ Clone the Repository

```bash
git clone <your-repo-url>
cd <repo-folder>
```

---

### 2️⃣ Install Dependencies

```bash
pip install langchain langgraph langchain-groq python-dotenv
```

---

### 3️⃣ Add Environment Variables

Create a `.env` file:

```
GROQ_API_KEY=your_api_key_here
```

---

### 4️⃣ Run the Project

```bash
python main.py
```

---

## 🧩 Core Components

### 📌 State Definition

```python
class Tweet():
    tweet: str
    topic: str
    tone: str
    response: Literal['APPROVED','REJECTED']
    feedback: list[str]
    iteration: int
    maximum_iteration: int
```

---

### ✍️ Tweet Generator

- Uses LLM to generate tweet based on:
  - Topic
  - Tone

---

### ✅ Tweet Approval System

Evaluates tweet on:
- Length (< 280 chars)
- Relevance to topic
- Tone consistency

Returns:
- `APPROVED` or `REJECTED`
- Feedback list

---

### 🔧 Tweet Optimizer

- Improves tweet using feedback
- Increases iteration count
- Stops at max iterations

---

### 🔀 Routing Logic

```python
if APPROVED → END
elif max iterations reached → END
else → OPTIMIZE
```

---

## 📊 Example Input

```python
initial_state = {
    'topic': 'DeepLearning',
    'tone': 'funny',
    'iteration': 0,
    'maximum_iteration': 5
}
```

---

## 📈 Example Output

```
Final Tweet: Deep learning be like: "I don’t know what I’m doing, but it works 🤖🔥"
Total Iterations: 2
Feedback: ['Make it more engaging', 'Add humor']
```

---

## 💡 Key Features

✔️ Automated tweet improvement loop  
✔️ Structured output using Pydantic  
✔️ Conditional graph execution  
✔️ Clean modular design  
✔️ Scalable for other content types  

---

## 🔮 Future Improvements

- Add hashtags generator  
- Multi-language tweet support  
- UI dashboard (Streamlit/React)  
- Real-time Twitter posting integration  
- Engagement score prediction  

---

## 🤝 Contributing

Feel free to fork and improve the project!

---

## ⭐ If You Like This Project

Give it a ⭐ on GitHub — it helps a lot!