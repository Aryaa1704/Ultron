import { useState } from "react";

export default function ChatPage() {
  const [messages, setMessages] = useState([
    { role: "assistant", content: "JARVIS online. How can I assist you?" }
  ]);
  const [input, setInput] = useState("");

  const sendMessage = () => {
    if (!input.trim()) {
      return;
    }

    const userMessage = { role: "user", content: input.trim() };
    setMessages((prev) => [...prev, userMessage]);
    setInput("");
  };

  return (
    <section className="flex h-[70vh] flex-col rounded-xl border border-neon/20 bg-surface p-4">
      <h2 className="mb-4 text-xl font-semibold text-neonSoft">Agent Chat</h2>
      <div className="mb-4 flex-1 space-y-3 overflow-y-auto rounded-lg bg-jet p-4">
        {messages.map((msg, idx) => (
          <div
            key={`${msg.role}-${idx}`}
            className={`max-w-[85%] rounded-lg px-4 py-2 text-sm ${
              msg.role === "assistant"
                ? "bg-neon/15 text-slate-100"
                : "ml-auto bg-neon text-black"
            }`}
          >
            {msg.content}
          </div>
        ))}
      </div>
      <div className="flex gap-2">
        <input
          type="text"
          value={input}
          onChange={(event) => setInput(event.target.value)}
          placeholder="Ask JARVIS..."
          className="flex-1 rounded-lg border border-neon/30 bg-jet px-3 py-2 text-sm outline-none ring-neon focus:ring-2"
        />
        <button
          type="button"
          onClick={sendMessage}
          className="rounded-lg bg-neon px-4 py-2 text-sm font-semibold text-black hover:bg-neonSoft"
        >
          Send
        </button>
      </div>
    </section>
  );
}
