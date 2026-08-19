export default function DashboardPage() {
  const cards = [
    { title: "Active Agents", value: "5", description: "Email, Calendar, Research, Browser, Job" },
    { title: "Memory Layers", value: "2", description: "PostgreSQL + ChromaDB" },
    { title: "Queue Status", value: "Ready", description: "Celery connected to Redis" }
  ];

  return (
    <section>
      <h2 className="mb-6 text-2xl font-semibold text-neonSoft">System Dashboard</h2>
      <div className="grid gap-4 md:grid-cols-3">
        {cards.map((card) => (
          <article key={card.title} className="rounded-xl border border-neon/20 bg-surface p-5">
            <p className="text-sm uppercase tracking-wide text-slate-400">{card.title}</p>
            <p className="mt-2 text-3xl font-bold text-neon">{card.value}</p>
            <p className="mt-3 text-sm text-slate-300">{card.description}</p>
          </article>
        ))}
      </div>
    </section>
  );
}
