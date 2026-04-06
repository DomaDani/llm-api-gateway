import { Routes, Route, Navigate } from 'react-router-dom';
import Sidebar from '../components/blocks/Sidebar';
import Home from '../pages/Home/Home'

function App() {
  return (
    <Routes>
      <Route path="/" element={<Navigate to="/home" replace />} />
      <Route path="/home" element={<Sidebar><Home /></Sidebar>} />
      <Route path="/global"  element={<Sidebar></Sidebar>} />
      <Route path="/project"  element={<Sidebar></Sidebar>} />
      <Route path="/keys"   element={<Sidebar></Sidebar>} />
      <Route path="/statistics"   element={<Sidebar></Sidebar>} />
      <Route path="/usage"   element={<Sidebar></Sidebar>} />
      <Route path="/profile"   element={<Sidebar></Sidebar>} />
    </Routes>

  )
};

/*

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

*/

export default App;
