import React, { useState, useEffect } from "react";
import {
  Button,
  Container,
  Typography,
  Box,
  Alert,
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableRow,
  Paper,
  Card,
  CardContent,
  IconButton,
  Collapse,
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  CircularProgress,
  List,
  ListItem,
  ListItemText,
} from "@mui/material";
import HistoryIcon from "@mui/icons-material/History";
import axios from "axios";
import { useAuth } from "../auth/AuthContext";

export default function PredictPage() {
  const { token } = useAuth();

  const [file, setFile] = useState(null);
  const [results, setResults] = useState([]);
  const [history, setHistory] = useState([]);
  const [indicators, setIndicators] = useState({});
  const [expandedIncident, setExpandedIncident] = useState(null);
  const [showHistory, setShowHistory] = useState(false);
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);
  const [indicatorDialogOpen, setIndicatorDialogOpen] = useState(false);
  const [indicatorIncidentId, setIndicatorIncidentId] = useState(null);
  const [indicatorLoading, setIndicatorLoading] = useState(false);
  const [indicatorError, setIndicatorError] = useState("");
  const [detailsDialogOpen, setDetailsDialogOpen] = useState(false);
  const [detailsIncident, setDetailsIncident] = useState(null);

  // Fetch history from API
  const fetchHistory = () => {
    if (!token) return;
    axios
      .get("/api/incidents/me", {
        headers: { Authorization: `Bearer ${token}` },
      })
      .then(res => setHistory(res.data))
      .catch(() => {});
  };

  useEffect(() => {
    fetchHistory();
    // eslint-disable-next-line
  }, [token]);

  /* =========================
     FILE HANDLERS
  ========================= */
  const handleFileChange = (e) => {
    setFile(e.target.files[0]);
  };

  const handleUpload = async () => {
    if (!file) return;

    setError("");
    setLoading(true);
    setResults([]);

    try {
      const text = await file.text();
      const rows = csvToJsonRows(text);
      const newResults = [];

      for (const row of rows) {
        const res = await axios.post(
          "/api/predict",
          { rows: [row] },
          { headers: { Authorization: `Bearer ${token}` } }
        );
        newResults.push({ ...row, ...res.data });
      }

      setResults(newResults);
      fetchHistory(); // Always refresh history from backend after prediction
    } catch (err) {
      setError(err.response?.data?.detail || "Prediction failed");
    } finally {
      setLoading(false);
    }
  };

  /* =========================
     INDICATORS
  ========================= */
  const fetchIndicators = async (incidentId) => {
    if (expandedIncident === incidentId) {
      setExpandedIncident(null);
      return;
    }

    if (indicators[incidentId]) {
      setExpandedIncident(incidentId);
      return;
    }

    try {
      const res = await axios.get(`/api/indicators/me/${incidentId}`, {
        headers: { Authorization: `Bearer ${token}` },
      });

      setIndicators(prev => ({
        ...prev,
        [incidentId]: res.data,
      }));

      setExpandedIncident(incidentId);
    } catch (err) {
      console.error("Failed to fetch indicators");
    }
  };

  // Helper: find incident ID in history by created_at (for new predictions)
  function getIncidentIdByCreatedAt(createdAt) {
    if (!createdAt) return null;
    const match = history.find((h) => h.created_at === createdAt);
    return match ? match.id : null;
  }

  // Open indicator dialog for a given incidentId (fetch if needed)
  const handleOpenIndicators = async (incidentId) => {
    setIndicatorError("");
    if (!incidentId) {
      setIndicatorError("Incident not found in history.");
      setIndicatorDialogOpen(true);
      return;
    }
    if (indicators[incidentId]) {
      setIndicatorIncidentId(incidentId);
      setIndicatorDialogOpen(true);
      return;
    }
    setIndicatorLoading(true);
    setIndicatorIncidentId(incidentId);
    setIndicatorDialogOpen(true);
    try {
      const res = await axios.get(`/api/indicators/me/${incidentId}`, {
        headers: { Authorization: `Bearer ${token}` },
      });
      setIndicators((prev) => ({ ...prev, [incidentId]: res.data }));
    } catch (err) {
      setIndicatorError("Failed to fetch indicators");
    } finally {
      setIndicatorLoading(false);
    }
  };

  // Fetch and show details for a given incident id
  const handleShowDetails = async (incidentIdOrRow) => {
    // If passed a row with _id, treat as full doc (history); else, fetch by id (results)
    if (typeof incidentIdOrRow === "object" && incidentIdOrRow._id) {
      setDetailsIncident(incidentIdOrRow);
      setDetailsDialogOpen(true);
    } else if (typeof incidentIdOrRow === "string") {
      setDetailsIncident(null);
      setDetailsDialogOpen(true);
      try {
        const res = await axios.get(`/api/incident/${incidentIdOrRow}`, {
          headers: { Authorization: `Bearer ${token}` },
        });
        setDetailsIncident(res.data);
      } catch {
        setDetailsIncident({ error: "Could not fetch incident details." });
      }
    }
  };

  /* =========================
     CSV PARSER
  ========================= */
  function csvToJsonRows(csv) {
    const [header, ...lines] = csv.trim().split(/\r?\n/);
    const keys = header.split(",").map(k => k.trim());

    return lines.map(line => {
      const values = line.split(",");
      const obj = {};
      keys.forEach((k, i) => {
        obj[k] = isNaN(values[i]) ? values[i] : Number(values[i]);
      });
      return obj;
    });
  }

  // Compute the starting index for new predictions
  const lastPredictionNumber = history.length;

  /* =========================
     RENDER
  ========================= */
  return (
    <Container maxWidth="md" sx={{ mt: 8, display: 'flex', flexDirection: 'column', alignItems: 'center' }}>
      <Card sx={{ width: 1, boxShadow: 3, borderRadius: 3, bgcolor: '#fff', p: 2 }}>
        <CardContent>
          <Typography variant="h4" gutterBottom align="center" color="primary">Prediction</Typography>
          <Box sx={{ mb: 2, display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
            <input type="file" accept=".csv" onChange={handleFileChange} />
            <Button variant="contained" color="primary" onClick={handleUpload} sx={{ ml: 2 }} disabled={loading || !file}>
              Predict
            </Button>
            <IconButton color="primary" sx={{ ml: 2 }} onClick={() => setShowHistory((v) => !v)}>
              <HistoryIcon />
            </IconButton>
            <Typography variant="body2" sx={{ ml: 1 }}>History</Typography>
          </Box>
          {error && <Alert severity="error" sx={{ mb: 2 }}>{error}</Alert>}
          {results.length > 0 && (
            <Paper sx={{ mt: 2 }}>
              <Typography variant="h6" sx={{ p: 2 }}>Results</Typography>
              <Table size="small">
                <TableHead>
                  <TableRow>
                    <TableCell>#</TableCell>
                    <TableCell>Label</TableCell>
                    <TableCell>Indicator</TableCell>
                    <TableCell>Details</TableCell>
                  </TableRow>
                </TableHead>
                <TableBody>
                  {results.map((row, i) => (
                    <TableRow key={i}>
                      <TableCell>{lastPredictionNumber + i + 1}</TableCell>
                      <TableCell>{row.verdict || row.label}</TableCell>
                      <TableCell>
                        {(row.verdict || row.label) === 'blocked' ? (
                          <Button
                            variant="outlined"
                            color="error"
                            size="small"
                            onClick={() => {
                              handleOpenIndicators(row.incident_id);
                            }}
                          >
                            Indicators
                          </Button>
                        ) : (
                          <Typography variant="body2" color="text.secondary">-</Typography>
                        )}
                      </TableCell>
                      <TableCell>
                        <Button
                          variant="outlined"
                          size="small"
                          onClick={() => handleShowDetails(row.incident_id)}
                        >
                          Details
                        </Button>
                      </TableCell>
                    </TableRow>
                  ))}
                </TableBody>
              </Table>
            </Paper>
          )}

          {/* HISTORY */}
          <Collapse in={showHistory}>
            {history.length > 0 && (
              <Box sx={{ mt: 4, overflowX: 'auto' }}>
                <Paper>
                  <Typography variant="h6" sx={{ p: 2 }}>Your Prediction History</Typography>
                  <Box sx={{ width: 'max-content', minWidth: '100%' }}>
                    <Table size="small">
                      <TableHead>
                        <TableRow>
                          <TableCell>ID</TableCell>
                          <TableCell>Label</TableCell>
                          <TableCell>Indicator</TableCell>
                          <TableCell>Details</TableCell>
                        </TableRow>
                      </TableHead>
                      <TableBody>
                        {history.map((row, i) => (
                          <TableRow key={i}>
                            <TableCell>{row._id}</TableCell>
                            <TableCell>{row.label}</TableCell>
                            <TableCell>
                              {row.label === 'blocked' ? (
                                <Button
                                  variant="outlined"
                                  color="error"
                                  size="small"
                                  onClick={() => handleOpenIndicators(row._id)}
                                >
                                  Indicators
                                </Button>
                              ) : (
                                <Typography variant="body2" color="text.secondary">-</Typography>
                              )}
                            </TableCell>
                            <TableCell>
                              <Button
                                variant="outlined"
                                size="small"
                                onClick={() => handleShowDetails(row)}
                              >
                                Details
                              </Button>
                            </TableCell>
                          </TableRow>
                        ))}
                      </TableBody>
                    </Table>
                  </Box>
                </Paper>
              </Box>
            )}
          </Collapse>

          {/* INDICATOR DIALOG */}
          <Dialog open={indicatorDialogOpen} onClose={() => setIndicatorDialogOpen(false)} maxWidth="sm" fullWidth>
            <DialogTitle>Indicators</DialogTitle>
            <DialogContent>
              {indicatorLoading ? (
                <Typography>Loading...</Typography>
              ) : indicatorError ? (
                <Alert severity="error">{indicatorError}</Alert>
              ) : indicatorIncidentId && indicators[indicatorIncidentId] ? (
                <Box>
                  {Array.isArray(indicators[indicatorIncidentId]) && indicators[indicatorIncidentId].length > 0 ? (
                    <Table size="small">
                      <TableHead>
                        <TableRow>
                          <TableCell>Feature</TableCell>
                          <TableCell>Importance</TableCell>
                        </TableRow>
                      </TableHead>
                      <TableBody>
                        {indicators[indicatorIncidentId].map((ind, idx) => {
                          // Defensive: handle both [feature, importance] and {feature, importance}
                          let feature, importance;
                          if (Array.isArray(ind)) {
                            feature = ind[0];
                            importance = ind[1];
                          } else if (typeof ind === 'object' && ind !== null) {
                            feature = ind.feature || ind[0];
                            importance = ind.importance || ind[1];
                          } else {
                            feature = '';
                            importance = ind;
                          }
                          return (
                            <TableRow key={idx}>
                              <TableCell>{feature}</TableCell>
                              <TableCell>{importance}</TableCell>
                            </TableRow>
                          );
                        })}
                      </TableBody>
                    </Table>
                  ) : (
                    <Typography>No indicators found.</Typography>
                  )}
                </Box>
              ) : (
                <Typography>No data.</Typography>
              )}
            </DialogContent>
            <DialogActions>
              <Button onClick={() => setIndicatorDialogOpen(false)}>Close</Button>
            </DialogActions>
          </Dialog>

          {/* DETAILS DIALOG */}
          <Dialog open={detailsDialogOpen} onClose={() => setDetailsDialogOpen(false)} maxWidth="sm" fullWidth>
            <DialogTitle>Incident Details</DialogTitle>
            <DialogContent>
              {detailsIncident ? (
                <List dense>
                  {Object.entries(detailsIncident).map(([key, value]) => (
                    <ListItem key={key}>
                      <ListItemText
                        primary={key}
                        secondary={typeof value === 'object' ? JSON.stringify(value) : String(value)}
                      />
                    </ListItem>
                  ))}
                </List>
              ) : (
                <Typography>Loading...</Typography>
              )}
            </DialogContent>
            <DialogActions>
              <Button onClick={() => setDetailsDialogOpen(false)}>Close</Button>
            </DialogActions>
          </Dialog>
        </CardContent>
      </Card>
    </Container>
  );
}
