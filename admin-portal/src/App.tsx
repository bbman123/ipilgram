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
import FlightsPage from "./pages/FlightsPage";
import FlightNewPage from "./pages/FlightNewPage";
import FlightDetailPage from "./pages/FlightDetailPage";
import FlightEditPage from "./pages/FlightEditPage";
import AccommodationsPage from "./pages/AccommodationsPage";
import AccommodationNewPage from "./pages/AccommodationNewPage";
import AccommodationDetailPage from "./pages/AccommodationDetailPage";
import AccommodationEditPage from "./pages/AccommodationEditPage";
import TransportsPage from "./pages/TransportsPage";
import TransportNewPage from "./pages/TransportNewPage";
import TransportDetailPage from "./pages/TransportDetailPage";
import TransportEditPage from "./pages/TransportEditPage";
import PackagesPage from "./pages/PackagesPage";
import PackageNewPage from "./pages/PackageNewPage";
import PackageDetailPage from "./pages/PackageDetailPage";
import PackageEditPage from "./pages/PackageEditPage";
import AnnouncementsPage from "./pages/AnnouncementsPage";
import AnnouncementNewPage from "./pages/AnnouncementNewPage";
import AnnouncementDetailPage from "./pages/AnnouncementDetailPage";
import AnnouncementEditPage from "./pages/AnnouncementEditPage";
import PreferencesPage from "./pages/PreferencesPage";
import PreferenceEditPage from "./pages/PreferenceEditPage";
import NotificationsPage from "./pages/NotificationsPage";

function NotFound() {
  return (
    <div className="flex flex-col items-center justify-center py-20">
      <div className="text-6xl font-bold text-gray-300 mb-4">404</div>
      <h1 className="text-xl font-semibold text-gray-900 mb-2">Page Not Found</h1>
      <p className="text-gray-500 mb-6">The page you are looking for does not exist.</p>
      <a href="/" className="text-emerald-600 hover:text-emerald-700 font-medium text-sm">Back to Dashboard</a>
    </div>
  );
}

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
            <Route path="flights" element={<FlightsPage />} />
            <Route path="flights/new" element={<FlightNewPage />} />
            <Route path="flights/:id" element={<FlightDetailPage />} />
            <Route path="flights/:id/edit" element={<FlightEditPage />} />
            <Route path="accommodations" element={<AccommodationsPage />} />
            <Route path="accommodations/new" element={<AccommodationNewPage />} />
            <Route path="accommodations/:id" element={<AccommodationDetailPage />} />
            <Route path="accommodations/:id/edit" element={<AccommodationEditPage />} />
            <Route path="transports" element={<TransportsPage />} />
            <Route path="transports/new" element={<TransportNewPage />} />
            <Route path="transports/:id" element={<TransportDetailPage />} />
            <Route path="transports/:id/edit" element={<TransportEditPage />} />
            <Route path="packages" element={<PackagesPage />} />
            <Route path="packages/new" element={<PackageNewPage />} />
            <Route path="packages/:id" element={<PackageDetailPage />} />
            <Route path="packages/:id/edit" element={<PackageEditPage />} />
            <Route path="announcements" element={<AnnouncementsPage />} />
            <Route path="announcements/new" element={<AnnouncementNewPage />} />
            <Route path="announcements/:id" element={<AnnouncementDetailPage />} />
            <Route path="announcements/:id/edit" element={<AnnouncementEditPage />} />
            <Route path="settings" element={<PreferencesPage />} />
            <Route path="settings/new" element={<PreferenceEditPage />} />
            <Route path="settings/:id" element={<PreferenceEditPage />} />
            <Route path="notifications" element={<NotificationsPage />} />
            <Route path="*" element={<NotFound />} />
          </Route>
        </Routes>
      </BrowserRouter>
    </AuthProvider>
  );
}

export default App;
