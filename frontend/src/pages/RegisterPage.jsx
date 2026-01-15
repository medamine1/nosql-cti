import React, { useState } from "react";
import { Button, TextField, Container, Typography, Box, Alert, Card, CardContent } from "@mui/material";
import { useNavigate } from "react-router-dom";
import axios from "axios";

export default function RegisterPage() {
  const [form, setForm] = useState({ username: "", email: "", password: "" });
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);
  const navigate = useNavigate();

  const handleChange = (e) => {
    setForm({ ...form, [e.target.name]: e.target.value });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError("");
    try {
      await axios.post("/api/auth/register", form);
      navigate("/login");
    } catch (err) {
      setError(err.response?.data?.detail || "Registration failed");
    } finally {
      setLoading(false);
    }
  };

  return (
    <Container maxWidth="xs" sx={{ mt: 8, display: 'flex', flexDirection: 'column', alignItems: 'center' }}>
      <Card sx={{ width: 1, boxShadow: 3, borderRadius: 3, bgcolor: '#fff', p: 2 }}>
        <CardContent>
          <Typography variant="h4" gutterBottom align="center" color="primary">Register</Typography>
          <Box component="form" onSubmit={handleSubmit}>
            <TextField label="Username" name="username" value={form.username} onChange={handleChange} fullWidth margin="normal" required />
            <TextField label="Email" name="email" value={form.email} onChange={handleChange} fullWidth margin="normal" required type="email" />
            <TextField label="Password" name="password" value={form.password} onChange={handleChange} fullWidth margin="normal" required type="password" />
            {error && <Alert severity="error" sx={{ mt: 2 }}>{error}</Alert>}
            <Button type="submit" variant="contained" color="primary" fullWidth sx={{ mt: 2 }} disabled={loading}>
              Register
            </Button>
          </Box>
        </CardContent>
      </Card>
    </Container>
  );
}
