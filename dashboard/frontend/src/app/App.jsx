import { Routes, Route, Navigate } from 'react-router-dom';
import Sidebar from '../components/blocks/Sidebar';
import { AuthProvider } from '../auth/AuthProvider';
import ProtectedRoute from '../components/shared/ProtectedRoute';

import Login from '../pages/Login/Login';
import Home from '../pages/Home/Home'
import GlobalSettings from '../pages/Global/GlobalSettings';
import ProjectSetings from '../pages/Project/ProjectSettings';
import ApiKeys from '../pages/Keys/ApiKeys';
import Usage from '../pages/Usage/Usage';
import Profile from '../pages/Profile/Profile';

function App() {
  return (
    <AuthProvider>
      <div className="App">
        <Routes>
          <Route path="/" element={<Login />} />

          <Route element={<ProtectedRoute />}>
            <Route path="/home" element={<Sidebar><Home /></Sidebar>} />
            <Route path="/global"  element={<Sidebar><GlobalSettings /></Sidebar>} />
            <Route path="/project"  element={<Sidebar><ProjectSetings /></Sidebar>} />
            <Route path="/keys"   element={<Sidebar><ApiKeys /></Sidebar>} />
            {/* <Route path="/statistics"   element={<Sidebar></Sidebar>} /> */}
            <Route path="/usage"   element={<Sidebar><Usage /></Sidebar>} />
            <Route path="/profile"   element={<Sidebar><Profile /></Sidebar>} />
          </Route>

          <Route path="*" element={<Navigate to="/home" replace />} />
        </Routes>
      </div>
    </AuthProvider>
  )
};

export default App;
