import { useState } from 'react';
import { Routes, Route } from 'react-router-dom';
import Login from '../pages/Login/Login';
import Welcome from '../pages/Login/Welcome';
import { AuthProvider } from '../auth/AuthProvider';
import ProtectedRoute from '../components/shared/ProtectedRoute';

function App() {
  return (
    <>
      <AuthProvider>
        <div className="App">
          <Routes>
            <Route path="/" element = {<Login />}/>

            <Route element={<ProtectedRoute/>}>
              <Route path="/welcome" element = {<Welcome />}/>
            </Route>
            
          </Routes>
        </div>
      </AuthProvider>
    </>
  )
};

export default App;
