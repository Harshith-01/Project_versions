import React, { useState, useEffect } from 'react';
import axios from 'axios';
import {
  Container, CssBaseline, Box, Typography, TextField, Button, CircularProgress,
  Paper, Grid, Link, Chip, Stack, Tooltip, keyframes, Stepper, Step, StepLabel
} from '@mui/material';
import { createTheme, ThemeProvider, styled } from '@mui/material/styles';
import UploadFileIcon from '@mui/icons-material/UploadFile';
import DownloadIcon from '@mui/icons-material/Download';
import ScienceIcon from '@mui/icons-material/Science';
import DescriptionIcon from '@mui/icons-material/Description';
import WebIcon from '@mui/icons-material/Web';

// --- Animations ---
const fadeIn = keyframes`
  from { opacity: 0; transform: translateY(20px); }
  to { opacity: 1; transform: translateY(0); }
`;

const pulse = keyframes`
  0% { box-shadow: 0 0 0 0 rgba(22, 163, 74, 0.7); }
  70% { box-shadow: 0 0 0 10px rgba(22, 163, 74, 0); }
  100% { box-shadow: 0 0 0 0 rgba(22, 163, 74, 0); }
`;

// --- Professional Light Theme ---
const theme = createTheme({
  palette: {
    mode: 'light',
    primary: { main: '#16a34a' }, // A professional, calming green
    secondary: { main: '#475569' },
    background: {
      default: '#f8fafc', // Off-white for a soft feel
      paper: '#ffffff',
    },
    text: {
      primary: '#1e293b',
      secondary: '#64748b',
    },
  },
  typography: {
    fontFamily: '"Inter", "Roboto", "Helvetica", "Arial", sans-serif',
    h2: { fontWeight: 700, color: '#0f172a' },
    h5: { fontWeight: 600, color: '#334155' },
    body1: { color: '#475569' },
  },
  components: {
    MuiPaper: {
      styleOverrides: {
        root: {
          borderRadius: '16px',
          boxShadow: '0 4px 12px rgba(0,0,0,0.05)',
          transition: 'transform 0.3s ease-in-out, box-shadow 0.3s ease-in-out',
          '&:hover': {
            transform: 'translateY(-4px)',
            boxShadow: '0 8px 24px rgba(0,0,0,0.08)',
          }
        }
      }
    },
    MuiButton: {
      styleOverrides: {
        root: {
          borderRadius: '8px',
          textTransform: 'none',
          fontWeight: 600,
          padding: '10px 20px',
        },
        containedPrimary: {
          color: 'white',
        }
      },
    },
    MuiTextField: {
      styleOverrides: {
        root: {
          '& .MuiOutlinedInput-root': {
            borderRadius: '8px',
          },
        },
      },
    },
  },
});

// --- Custom Stepper Styling ---
const ColorlibStepIconRoot = styled('div')(
  ({ theme, ownerState }) => ({
    backgroundColor: theme.palette.mode === 'dark' ? theme.palette.grey[700] : '#ccc',
    zIndex: 1,
    color: '#fff',
    width: 40,
    height: 40,
    display: 'flex',
    borderRadius: '50%',
    justifyContent: 'center',
    alignItems: 'center',
    ...(ownerState.active && {
      backgroundColor: theme.palette.primary.main,
      boxShadow: '0 4px 10px 0 rgba(0,0,0,.25)',
    }),
    ...(ownerState.completed && {
      backgroundColor: theme.palette.primary.main,
    }),
  }),
);

function ColorlibStepIcon(props) {
  const { active, completed, className } = props;
  const icons = {
    1: <UploadFileIcon />,
    2: <WebIcon />,
    3: <DownloadIcon />,
  };
  return (
    <ColorlibStepIconRoot ownerState={{ completed, active }} className={className}>
      {icons[String(props.icon)]}
    </ColorlibStepIconRoot>
  );
}

const API_BASE_URL = 'http://localhost:8000';

function App() {
  const [diseaseName, setDiseaseName] = useState('');
  const [url, setUrl] = useState('');
  const [selectedFile, setSelectedFile] = useState(null);
  const [status, setStatus] = useState('Welcome! Please follow the steps below to generate your dataset.');
  const [isLoading, setIsLoading] = useState(false);
  const [processedFileId, setProcessedFileId] = useState(null);
  const [activeStep, setActiveStep] = useState(0);

  useEffect(() => {
    if (selectedFile && diseaseName && url) {
      setActiveStep(2);
    } else if (selectedFile) {
      setActiveStep(1);
    } else {
      setActiveStep(0);
    }
  }, [selectedFile, diseaseName, url]);

  const handleFileSelect = (event) => {
    const file = event.target.files[0];
    if (file && file.type === "text/csv") {
      setSelectedFile(file);
      setProcessedFileId(null);
      setStatus(`Base file selected: ${file.name}. Please provide the disease context.`);
    } else {
      setSelectedFile(null);
      setStatus("Invalid file. Please select a valid .csv file.");
    }
  };

  const handleProcess = async () => {
    if (!selectedFile || !diseaseName || !url) {
      setStatus('Error: You must complete all steps before processing.');
      return;
    }
    setIsLoading(true);
    setProcessedFileId(null);
    setStatus('Processing... This may take a moment.');

    const formData = new FormData();
    formData.append('file', selectedFile);
    formData.append('disease_name', diseaseName);
    formData.append('url', url);

    try {
      const response = await axios.post(`${API_BASE_URL}/process`, formData, {
        headers: { 'Content-Type': 'multipart/form-data' },
      });
      setProcessedFileId(response.data.file_id);
      setStatus(`✅ Success: ${response.data.message}`);
      setActiveStep(3); // Mark final step as complete
    } catch (error) {
      setStatus(`❌ Error: ${error.response?.data?.detail || error.message}`);
    }
    setIsLoading(false);
  };

  const handleDownload = () => {
    if (!processedFileId) return;
    window.open(`${API_BASE_URL}/download/${processedFileId}`, '_blank');
  };

  const handleDownloadTemplate = () => {
    window.open(`${API_BASE_URL}/template`, '_blank');
  };

  const steps = ['Upload Base File', 'Provide Context', 'Generate & Download'];

  return (
    <ThemeProvider theme={theme}>
      <CssBaseline />
      <Box sx={{ minHeight: '100vh', backgroundColor: 'background.default', p: { xs: 2, sm: 4 } }}>
        <Container maxWidth="lg">
          <Box sx={{ my: 4, textAlign: 'center', animation: `${fadeIn} 0.5s ease-out` }}>
            <Typography variant="h2" component="h1" gutterBottom>
              MedData Synthesizer
            </Typography>
            <Typography variant="h6" color="text.secondary">
              Turn medical articles into structured clinical datasets with AI.
            </Typography>
          </Box>

          <Paper sx={{ p: { xs: 2, sm: 4 }, mb: 4, animation: `${fadeIn} 0.7s ease-out 0.2s`, animationFillMode: 'backwards' }}>
            <Stepper activeStep={activeStep} alternativeLabel sx={{ mb: 4 }}>
              {steps.map((label) => (
                <Step key={label}>
                  <StepLabel StepIconComponent={ColorlibStepIcon}>{label}</StepLabel>
                </Step>
              ))}
            </Stepper>

            <Grid container spacing={4} alignItems="center">
              {/* --- Step 1: File Upload --- */}
              <Grid item xs={12} md={4}>
                <Typography variant="h5" gutterBottom>Step 1: Base File</Typography>
                <Typography variant="body1" sx={{ mb: 2 }}>
                  Select a CSV to append data to, or download a template to start fresh.
                </Typography>
                <Stack spacing={2}>
                  <Button variant="contained" component="label" startIcon={<UploadFileIcon />}>
                    Select CSV File
                    <input type="file" hidden accept=".csv" onChange={handleFileSelect} />
                  </Button>
                  <Button variant="outlined" onClick={handleDownloadTemplate} startIcon={<DescriptionIcon />}>
                    Download Template
                  </Button>
                  {selectedFile && <Chip label={selectedFile.name} onDelete={() => { setSelectedFile(null); setProcessedFileId(null); }} />}
                </Stack>
              </Grid>

              {/* --- Step 2: Context --- */}
              <Grid item xs={12} md={8}>
                <Typography variant="h5" gutterBottom>Step 2: Context</Typography>
                <Typography variant="body1" sx={{ mb: 2 }}>
                  Provide the name of the disease and a trusted medical source URL.
                </Typography>
                <Stack spacing={2}>
                  <TextField fullWidth required label="Disease Name" variant="outlined" value={diseaseName} onChange={(e) => setDiseaseName(e.target.value)} disabled={isLoading} />
                  <TextField fullWidth required label="Medical Source URL" variant="outlined" value={url} onChange={(e) => setUrl(e.target.value)} disabled={isLoading} />
                </Stack>
              </Grid>
            </Grid>
          </Paper>

          {/* --- Step 3: Generate & Download --- */}
          <Paper sx={{ p: { xs: 2, sm: 4 }, mb: 4, textAlign: 'center', animation: `${fadeIn} 0.9s ease-out 0.4s`, animationFillMode: 'backwards' }}>
            <Typography variant="h5" gutterBottom>Step 3: Generate & Download</Typography>
            <Typography variant="body1" sx={{ mb: 2 }}>
              Once all fields are complete, you can process the data and download the result.
            </Typography>
            <Stack direction={{ xs: 'column', sm: 'row' }} spacing={2} justifyContent="center">
              <Button
                variant="contained"
                size="large"
                onClick={handleProcess}
                disabled={isLoading || !selectedFile || !diseaseName || !url}
                startIcon={isLoading ? <CircularProgress size={20} color="inherit" /> : null}
                sx={{ animation: (!isLoading && selectedFile && diseaseName && url) ? `${pulse} 2s infinite` : 'none' }}
              >
                {isLoading ? 'Processing...' : 'Process & Append Data'}
              </Button>
              <Button
                variant="outlined"
                size="large"
                onClick={handleDownload}
                disabled={isLoading || !processedFileId}
                startIcon={<DownloadIcon />}
              >
                Download Result
              </Button>
            </Stack>
          </Paper>

          {/* --- Status Log --- */}
          <Paper sx={{ p: 2, animation: `${fadeIn} 1.1s ease-out 0.6s`, animationFillMode: 'backwards' }}>
            <Typography variant="h6" gutterBottom>Status Log</Typography>
            <Box sx={{ p: 2, backgroundColor: '#eef2f6', color: '#334155', borderRadius: '8px', minHeight: 80, fontFamily: 'monospace', whiteSpace: 'pre-wrap' }}>
              {status}
            </Box>
          </Paper>
        </Container>
      </Box>
    </ThemeProvider>
  );
}

export default App;