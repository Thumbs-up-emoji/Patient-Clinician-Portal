// In your App.jsx
import { Routes, Route } from 'react-router-dom';
import { HashRouter as Router } from 'react-router-dom';
import Login from './pages/Login'
import PatientDashboard from './pages/PatientDashboard'
import ClinicianDashboard from './pages/ClinicianDashboard'
import Chat from './pages/Chat'
import Profile from './pages/Profile'
import Navbar from './components/Navbar'

function App() {
  return (
    <>
      <Navbar />
      <Routes>
        <Route path="/" element={<Login />} />
        <Route path="/login" element={<Login />} />
        <Route path="/patient-dashboard" element={<PatientDashboard />} />
        <Route path="/clinician-dashboard" element={<ClinicianDashboard />} />
        <Route path="/chat" element={<Chat />} />
        <Route path="/profile" element={<Profile />} />
      </Routes>
    </>
  )
}


export default App

