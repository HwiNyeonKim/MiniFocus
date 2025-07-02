import { AuthProvider, useAuth } from "./contexts/AuthContext";
import Home from "./components/Home";
import Login from "./components/Login";

function AppContent() {
  const { user, loading, login } = useAuth();

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="text-xl">Loading...</div>
      </div>
    );
  }

  if (!user) {
    return <Login onLoginSuccess={login} />;
  }

  return <Home />;
}

function App() {
  return (
    <AuthProvider>
      <AppContent />
    </AuthProvider>
  );
}

export default App;
