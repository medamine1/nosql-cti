import React from "react";
import { Routes, Route, Navigate, Link as RouterLink } from "react-router-dom";
import IndexPage from "./pages/IndexPage";
import RegisterPage from "./pages/RegisterPage";
import LoginPage from "./pages/LoginPage";
import PredictPage from "./pages/PredictPage";
import { AuthProvider, useAuth } from "./auth/AuthContext";
import AppBar from "@mui/material/AppBar";
import Toolbar from "@mui/material/Toolbar";
import Typography from "@mui/material/Typography";
import Button from "@mui/material/Button";
import Container from "@mui/material/Container";
import Box from "@mui/material/Box";

function PrivateRoute({ children }) {
  const { token } = useAuth();
  return token ? children : <Navigate to="/login" />;
}

function MyAppBar() {
  const { user, logout } = useAuth();
  return (
    <AppBar position="static" color="primary">
      <Toolbar>
        <Typography
          variant="h6"
          component={RouterLink}
          to="/"
          sx={{
            flexGrow: 1,
            color: "inherit",
            textDecoration: "none",
          }}
        >
          Binary IDS Dashboard
        </Typography>
        {user ? (
          <>
            <Button
              color="inherit"
              component={RouterLink}
              to="/predict"
            >
              Predict
            </Button>
            <Button color="inherit" onClick={logout}>
              Logout
            </Button>
          </>
        ) : (
          <>
            <Button
              color="inherit"
              component={RouterLink}
              to="/login"
            >
              Login
            </Button>
            <Button
              color="inherit"
              component={RouterLink}
              to="/register"
            >
              Register
            </Button>
          </>
        )}
      </Toolbar>
    </AppBar>
  );
}

export default function App() {
  return (
    <AuthProvider>
      <MyAppBar />
      <Box
        sx={{
          bgcolor: "#f5f6fa",
          minHeight: "100vh",
          py: 4,
        }}
      >
        <Container maxWidth="md">
          <Routes>
            <Route path="/" element={<IndexPage />} />
            <Route path="/register" element={<RegisterPage />} />
            <Route path="/login" element={<LoginPage />} />
            <Route
              path="/predict"
              element={
                <PrivateRoute>
                  <PredictPage />
                </PrivateRoute>
              }
            />
            <Route path="*" element={<Navigate to="/" />} />
          </Routes>
        </Container>
      </Box>
    </AuthProvider>
  );
}
