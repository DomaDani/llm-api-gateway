import { Routes, Route, Navigate } from 'react-router-dom';
import Sidebar from '../components/blocks/Sidebar';
import { AuthProvider } from '../api/auth/AuthProvider';
import ProtectedRoute from '../components/shared/ProtectedRoute';
import RequirePermissions from '../components/shared/RequirePermissions';

import Login from '../pages/Login/Login';
import Home from '../pages/Home/Home'
import GlobalSettings from '../pages/Global/GlobalSettings';
import ProjectSetings from '../pages/Project/ProjectSettings';
import ApiKeys from '../pages/Keys/ApiKeys';
import Usage from '../pages/Usage/Usage';
import Profile from '../pages/Profile/Profile';

/**
 * The main application component that sets up routing and authentication context for the dashboard.
 * @returns {JSX.Element} The rendered application component.
 */
function App() {
  return (
    <AuthProvider>
      <div className="App">
        <Routes>
          <Route path="/" element={<Login />} />

          <Route element={<ProtectedRoute />}>
            <Route path="/home" element={<Sidebar><Home /></Sidebar>} />

            <Route path="/global"  element={
              <RequirePermissions requirements={(u) => u?.is_admin}>
                <Sidebar><GlobalSettings /></Sidebar>
              </RequirePermissions>
              } />
            <Route path="/project"  element={
              <RequirePermissions requirements={(u, p) => p && (u?.is_admin || u?.is_project_manager)}>
                <Sidebar><ProjectSetings /></Sidebar>
              </RequirePermissions>
            } />
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
