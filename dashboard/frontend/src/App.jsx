import { useState } from 'react';
import { Routes, Route } from 'react-router-dom';
import './App.css';
import Login from './pages/Login';
import Welcome from './pages/Welcome';
import { AuthProvider } from './auth/AuthProvider';
import ProtectedRoute from './components/ProtectedRoute';

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
