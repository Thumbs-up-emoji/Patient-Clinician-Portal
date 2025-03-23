import { useState } from 'react';
import { 
  Typography, Button, TextField, Grid, Avatar, 
  Divider, Chip, List, ListItem, ListItemText 
} from '@mui/material';
import CloudUploadIcon from '@mui/icons-material/CloudUpload';
import EditIcon from '@mui/icons-material/Edit';
import SaveIcon from '@mui/icons-material/Save';

const PatientProfile = ({ patientData }) => {
  const [editing, setEditing] = useState(false);
  const [profile, setProfile] = useState(patientData || {
    name: '',
    email: '',
    phone: '',
    dateOfBirth: '',
    allergies: [],
    medications: []
  });

  const handleChange = (e) => {
    const { name, value } = e.target;
    setProfile({
      ...profile,
      [name]: value
    });
  };

  const handleSave = () => {
    // In a real app, you would save this to your backend
    console.log('Saving profile:', profile);
    setEditing(false);
  };

  const handleFileUpload = (e) => {
    const file = e.target.files[0];
    if (file) {
      // In a real app, you would upload this file to storage
      console.log('Uploading file:', file.name);
    }
  };

  return (
    <div>
      <div style={{ display: 'flex', alignItems: 'center', marginBottom: 20 }}>
        <Avatar 
          src={patientData?.photoUrl} 
          sx={{ width: 80, height: 80, marginRight: 2 }}
        >
          {profile.name.charAt(0)}
        </Avatar>
        <div>
          <Typography variant="h5">{profile.name}</Typography>
          <Typography variant="body2" color="textSecondary">
            Patient ID: {patientData?.id || 'N/A'}
          </Typography>
        </div>
        <Button 
          variant="outlined" 
          startIcon={editing ? <SaveIcon /> : <EditIcon />}
          onClick={editing ? handleSave : () => setEditing(true)}
          sx={{ marginLeft: 'auto' }}
        >
          {editing ? 'Save Profile' : 'Edit Profile'}
        </Button>
      </div>

      <Divider sx={{ my: 2 }} />

      <Grid container spacing={3}>
        <Grid item xs={12} md={6}>
          <Typography variant="h6" gutterBottom>Personal Information</Typography>
          
          <TextField
            fullWidth
            label="Full Name"
            name="name"
            value={profile.name}
            onChange={handleChange}
            disabled={!editing}
            margin="normal"
          />
          
          <TextField
            fullWidth
            label="Email"
            name="email"
            value={profile.email}
            onChange={handleChange}
            disabled={!editing}
            margin="normal"
          />
          
          <TextField
            fullWidth
            label="Phone Number"
            name="phone"
            value={profile.phone}
            onChange={handleChange}
            disabled={!editing}
            margin="normal"
          />
          
          <TextField
            fullWidth
            label="Date of Birth"
            name="dateOfBirth"
            type="date"
            value={profile.dateOfBirth}
            onChange={handleChange}
            disabled={!editing}
            margin="normal"
            InputLabelProps={{ shrink: true }}
          />
        </Grid>

        <Grid item xs={12} md={6}>
          <Typography variant="h6" gutterBottom>Medical Information</Typography>
          
          <Typography variant="subtitle1" gutterBottom>Allergies</Typography>
          <div style={{ display: 'flex', flexWrap: 'wrap', gap: 8, marginBottom: 16 }}>
            {profile.allergies.map((allergy, index) => (
              <Chip key={index} label={allergy} />
            ))}
            {editing && (
              <TextField
                label="Add Allergy"
                size="small"
                onKeyPress={(e) => {
                  if (e.key === 'Enter' && e.target.value) {
                    setProfile({
                      ...profile,
                      allergies: [...profile.allergies, e.target.value]
                    });
                    e.target.value = '';
                  }
                }}
              />
            )}
          </div>
          
          <Typography variant="subtitle1" gutterBottom>Medications</Typography>
          <List>
            {profile.medications.map((med, index) => (
              <ListItem key={index} disablePadding>
                <ListItemText 
                  primary={med.name} 
                  secondary={`${med.dosage} - ${med.frequency}`} 
                />
              </ListItem>
            ))}
          </List>
          
          <Typography variant="subtitle1" gutterBottom>Medical Records</Typography>
          <Button
            variant="contained"
            component="label"
            startIcon={<CloudUploadIcon />}
            sx={{ mt: 1 }}
          >
            Upload Document
            <input
              type="file"
              hidden
              onChange={handleFileUpload}
            />
          </Button>
        </Grid>
      </Grid>
    </div>
  );
};

export default PatientProfile;
