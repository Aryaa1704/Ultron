export default function SettingsPage() {
  return (
    <section className="rounded-xl border border-neon/20 bg-surface p-6">
      <h2 className="text-2xl font-semibold text-neonSoft">Settings</h2>
      <div className="mt-5 space-y-4">
        <div>
          <label className="mb-1 block text-sm text-slate-300">Model Provider</label>
          <input
            type="text"
            readOnly
            value="Anthropic Claude"
            className="w-full rounded-lg border border-neon/20 bg-jet px-3 py-2 text-sm text-slate-200"
          />
        </div>
        <div>
          <label className="mb-1 block text-sm text-slate-300">Vector Store</label>
          <input
            type="text"
            readOnly
            value="ChromaDB"
            className="w-full rounded-lg border border-neon/20 bg-jet px-3 py-2 text-sm text-slate-200"
          />
        </div>
      </div>
    </section>
  );
}
