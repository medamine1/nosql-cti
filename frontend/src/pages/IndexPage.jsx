import React, { useEffect } from "react";
import { Button, Container, Typography, Box, Card, CardContent } from "@mui/material";
import { useNavigate } from "react-router-dom";
import { useAuth } from "../auth/AuthContext";

export default function IndexPage() {
  const navigate = useNavigate();
  const { user } = useAuth();

  useEffect(() => {
    if (user) {
      navigate("/predict");
    }
  }, [user, navigate]);

  return (
    <Container maxWidth="sm" sx={{ mt: 8, display: 'flex', flexDirection: 'column', alignItems: 'center' }}>
      <Card sx={{ minWidth: 350, boxShadow: 3, borderRadius: 3, bgcolor: '#fff', p: 2 }}>
        <CardContent>
          <Typography variant="h3" gutterBottom align="center" color="primary">
            CTI IDS
          </Typography>
          <Typography variant="body1" sx={{ mb: 4 }} align="center">
            Welcome to the Cyber Threat Intelligence Intrusion Detection System. Register or connect to start predicting threats from your network data.
          </Typography>
          <Box sx={{ display: "flex", justifyContent: "center", gap: 2 }}>
            <Button variant="contained" color="primary" onClick={() => navigate("/register")}>Register</Button>
            <Button variant="outlined" color="primary" onClick={() => navigate("/login")}>Connect</Button>
          </Box>
        </CardContent>
      </Card>
    </Container>
  );
}
