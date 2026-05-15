import { Link, NavLink, useNavigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import { Activity, AlertTriangle, BarChart3, BrainCircuit, FileDown, FlaskConical, Lightbulb, LineChart, LogOut, UploadCloud, Zap } from 'lucide-react';
export default function Layout({ children }) {
  const { user, logout } = useAuth(); const navigate = useNavigate();
  const nav = [['/dashboard', BarChart3, 'Energy Dashboard'], ['/upload', UploadCloud, 'Upload Data'], ['/forecast', LineChart, 'Forecast AI'], ['/optimization', Lightbulb, 'Optimization'], ['/simulation', FlaskConical, 'Simulation'], ['/reports', FileDown, 'Reports']];
  return <div className="min-h-screen bg-[radial-gradient(circle_at_top_left,#facc15_0,#ef4444_28%,#1d4ed8_64%,#06111f_100%)] text-white">
    <aside className="fixed left-0 top-0 h-full w-76 p-5 hidden md:block">
      <div className="glass-dark rounded-[2rem] h-full p-5 shadow-2xl border border-yellow-300/30">
        <Link to="/dashboard" className="flex gap-3 items-center text-2xl font-black"><span className="grid place-items-center bg-yellow-300 text-red-700 rounded-2xl p-2"><Zap /></span> EnergyAI Grid</Link>
        <p className="text-sm text-yellow-100 mt-2">Forecasting • anomalies • savings • optimization</p>
        <div className="mt-8 space-y-3">{nav.map(([to, Icon, label]) => <NavLink key={to} to={to} className={({isActive})=>`flex items-center gap-3 px-4 py-3 rounded-2xl transition ${isActive?'bg-yellow-300 text-blue-950 font-black shadow-xl':'hover:bg-white/15 text-white'}`}><Icon size={20}/>{label}</NavLink>)}</div>
        <div className="absolute bottom-8 left-10 right-10"><p className="text-sm text-white/75 mb-3">Signed in: {user?.name}</p><button onClick={()=>{logout();navigate('/login')}} className="w-full flex gap-2 items-center justify-center bg-red-500 hover:bg-red-400 py-3 rounded-2xl font-bold"><LogOut size={18}/> Logout</button></div>
      </div>
    </aside>
    <main className="md:ml-80 p-5 md:p-8">{children}</main>
  </div>
}
