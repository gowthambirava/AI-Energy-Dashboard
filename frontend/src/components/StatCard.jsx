export default function StatCard({ title, value, icon, color='from-yellow-300 via-red-400 to-blue-500' }) {
  return <div className={`rounded-[2rem] p-6 shadow-2xl bg-gradient-to-br ${color} border border-white/30`}><div className="text-4xl mb-3">{icon}</div><p className="text-white/85 text-sm font-semibold">{title}</p><h2 className="text-3xl font-black mt-1">{value}</h2></div>
}
