import { BrowserRouter, Routes, Route } from "react-router-dom";
import { AuthProvider } from "./contexts/AuthContext";
import ProtectedRoute from "./components/ProtectedRoute";
import Layout from "./components/Layout";
import LoginPage from "./pages/LoginPage";
import DashboardPage from "./pages/DashboardPage";
import PilgrimsPage from "./pages/PilgrimsPage";
import PilgrimNewPage from "./pages/PilgrimNewPage";
import PilgrimDetailPage from "./pages/PilgrimDetailPage";
import PilgrimEditPage from "./pages/PilgrimEditPage";

function App() {
  return (
    <AuthProvider>
      <BrowserRouter>
        <Routes>
          <Route path="/login" element={<LoginPage />} />
          <Route
            element={
              <ProtectedRoute>
                <Layout />
              </ProtectedRoute>
            }
          >
            <Route index element={<DashboardPage />} />
            <Route path="pilgrims" element={<PilgrimsPage />} />
            <Route path="pilgrims/new" element={<PilgrimNewPage />} />
            <Route path="pilgrims/:id" element={<PilgrimDetailPage />} />
            <Route path="pilgrims/:id/edit" element={<PilgrimEditPage />} />
          </Route>
        </Routes>
      </BrowserRouter>
    </AuthProvider>
  );
}

export default App;
