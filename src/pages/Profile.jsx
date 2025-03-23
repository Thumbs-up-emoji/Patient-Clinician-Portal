// src/pages/Profile.jsx
import { useState } from 'react';
import { Box, Typography, Avatar, Button, Paper, Grid, TextField, Alert } from '@mui/material';
import { useAuth } from '../context/AuthContext';
import UploadIcon from '@mui/icons-material/Upload';
import FileUpload from '../components/FileUpload';

export default function Profile() {
  const { user, logout } = useAuth();
  const [file, setFile] = useState(null);
  const [success, setSuccess] = useState(false);
  
  const handleFileChange = (e) => {
    if (e.target.files[0]) {
      setFile(e.target.files[0]);
    }
  };
  
  const handleUpload = () => {
    // Mock implementation - in a real app, this would connect to Firebase Storage
    setTimeout(() => {
      setSuccess(true);
      setFile(null);
      setTimeout(() => setSuccess(false), 3000);
    }, 1000);
  };
  
  return (
    <Box sx={{ p: 2, maxWidth: 600, mx: 'auto' }}>
      <Paper elevation={3} sx={{ p: 3, mb: 3, textAlign: 'center' }}>
        <Avatar 
          src={user?.photoURL} 
          sx={{ width: 80, height: 80, mx: 'auto', mb: 2 }}
        />
        <Typography variant="h5" gutterBottom>Profile</Typography>
        
        <Grid container spacing={2} sx={{ mt: 2, textAlign: 'left' }}>
          <Grid item xs={12}>
            <Typography variant="body1">
              <strong>Name:</strong> {user?.displayName || 'John Doe'}
            </Typography>
          </Grid>
          <Grid item xs={12}>
            <Typography variant="body1">
              <strong>Email ID:</strong> {user?.email || 'johndoe@gmail.com'}
            </Typography>
          </Grid>
        </Grid>
        
        <Button 
          variant="outlined" 
          color="error" 
          sx={{ mt: 4 }}
          onClick={logout}
          startIcon={<Box component="span" sx={{ transform: 'rotate(180deg)' }}>➔</Box>}
        >
          Log out
        </Button>
      </Paper>
      
      <Paper elevation={3} sx={{ p: 3 }}>
        <Typography variant="h6" gutterBottom>Medical Information</Typography>
        
        {success && (
          <Alert severity="success" sx={{ mb: 2 }}>
            Medical information uploaded successfully!
          </Alert>
        )}
        
        <Button
          variant="contained"
          component="label"
          startIcon={<UploadIcon />}
          fullWidth
          sx={{ mt: 2 }}
        >
          Upload Medical Information
          <input
            type="file"
            hidden
            onChange={handleFileChange}
          />
        </Button>
        
        {file && (
          <Box sx={{ mt: 2 }}>
            <Typography variant="body2">{file.name}</Typography>
            <Button 
              variant="contained" 
              color="primary"
              size="small"
              onClick={handleUpload}
              sx={{ mt: 1 }}
            >
              Confirm Upload
            </Button>
          </Box>
        )}
      </Paper>
      <FileUpload/>

    </Box>
  );
}
