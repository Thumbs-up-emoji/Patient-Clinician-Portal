import { useState } from 'react';
import Grid from '@mui/material/Grid2';
import { 
  Container, Paper, Typography, Tabs, Tab, List, 
  ListItem, ListItemText, ListItemAvatar, Avatar, 
  Divider, Badge, Box
} from '@mui/material';
import NotificationsIcon from '@mui/icons-material/Notifications';
import VerifiedIcon from '@mui/icons-material/Verified';
import WarningIcon from '@mui/icons-material/Warning';
import Navbar from '../components/Navbar';
import ChatWindow from '../components/ChatWindow';
import { useAuth } from '../context/AuthContext';

const ClinicianDashboard = () => {
  const { currentUser } = useAuth();
  const [tabValue, setTabValue] = useState(0);
  const [selectedPatient, setSelectedPatient] = useState(null);
  
  // Sample data - in a real app, this would come from your backend
  const patients = [
    { id: 'p1', name: 'John Doe', condition: 'Hypertension', unread: 2, lastMessage: "I've been feeling dizzy lately" },
    { id: 'p2', name: 'Jane Smith', condition: 'Diabetes', unread: 0, lastMessage: 'My blood sugar readings are stable' },
    { id: 'p3', name: 'Robert Johnson', condition: 'Asthma', unread: 1, lastMessage: 'Need a new inhaler prescription' }
  ];
  
  const pendingReviews = [
    { 
      id: 'r1', 
      patientName: 'John Doe', 
      patientId: 'p1',
      query: 'Is it normal to feel dizzy after taking my medication?', 
      aiResponse: 'Dizziness can be a side effect of many blood pressure medications. If it persists, you should consult your doctor.',
      time: '2h ago' 
    },
    { 
      id: 'r2', 
      patientName: 'Alice Williams', 
      patientId: 'p4',
      query: 'My blood pressure readings have been fluctuating. Should I be concerned?', 
      aiResponse: 'Some fluctuation in blood pressure is normal. However, consistent high readings may require attention.',
      time: '5h ago' 
    }
  ];

  const handleTabChange = (event, newValue) => {
    setTabValue(newValue);
    setSelectedPatient(null); // Clear selected patient when switching tabs
  };

  const handleSelectPatient = (patient) => {
    setSelectedPatient(patient);
  };

  const handleSelectReview = (review) => {
    // Find the patient associated with this review
    const patient = patients.find(p => p.id === review.patientId) || {
      id: review.patientId,
      name: review.patientName,
      condition: 'Unknown',
      unread: 0
    };
    
    setSelectedPatient(patient);
  };

  return (
    <>
      <Navbar />
      <Container maxWidth="xl" sx={{ mt: 4, mb: 4 }}>
        <Typography variant="h4" gutterBottom>
          Clinician Dashboard
        </Typography>
        <Typography variant="subtitle1" color="textSecondary" gutterBottom>
          Welcome, Dr. {currentUser?.displayName?.split(' ')[0] || 'User'}
        </Typography>
        
        <Grid container spacing={3}>
          <Grid item xs={12} md={4} lg={3}>
            <Paper sx={{ p: 2, height: '100%' }}>
              <Tabs value={tabValue} onChange={handleTabChange} sx={{ mb: 2 }}>
                <Tab label="Patients" />
                <Tab 
                  label={
                    <Badge badgeContent={pendingReviews.length} color="error">
                      Pending Reviews
                    </Badge>
                  } 
                />
              </Tabs>
              
              {tabValue === 0 ? (
                <List sx={{ height: '70vh', overflow: 'auto' }}>
                  {patients.map((patient) => (
                    <Box key={patient.id}>
                      <ListItem 
                        button 
                        selected={selectedPatient?.id === patient.id}
                        onClick={() => handleSelectPatient(patient)}
                      >
                        <ListItemAvatar>
                          <Badge badgeContent={patient.unread} color="error" invisible={patient.unread === 0}>
                            <Avatar>{patient.name.charAt(0)}</Avatar>
                          </Badge>
                        </ListItemAvatar>
                        <ListItemText 
                          primary={patient.name} 
                          secondary={
                            <>
                              <Typography variant="body2" component="span">
                                {patient.condition}
                              </Typography>
                              <Typography variant="body2" component="div" noWrap>
                                {patient.lastMessage}
                              </Typography>
                            </>
                          } 
                        />
                      </ListItem>
                      <Divider component="li" />
                    </Box>
                  ))}
                </List>
              ) : (
                <List sx={{ height: '70vh', overflow: 'auto' }}>
                  {pendingReviews.map((review) => (
                    <Box key={review.id}>
                      <ListItem 
                        button
                        onClick={() => handleSelectReview(review)}
                      >
                        <ListItemAvatar>
                          <Avatar sx={{ bgcolor: 'warning.main' }}>
                            <WarningIcon />
                          </Avatar>
                        </ListItemAvatar>
                        <ListItemText 
                          primary={review.patientName} 
                          secondary={
                            <>
                              <Typography variant="body2" noWrap>
                                {review.query}
                              </Typography>
                              <Typography variant="caption" color="textSecondary">
                                {review.time}
                              </Typography>
                            </>
                          } 
                        />
                      </ListItem>
                      <Divider component="li" />
                    </Box>
                  ))}
                </List>
              )}
            </Paper>
          </Grid>
          
          <Grid item xs={12} md={8} lg={9}>
            {selectedPatient ? (
              <ChatWindow 
                recipientId={selectedPatient.id}
                recipientName={selectedPatient.name}
                isClinician={true}
              />
            ) : (
              <Paper 
                sx={{ 
                  p: 4, 
                  textAlign: 'center', 
                  height: '70vh', 
                  display: 'flex', 
                  flexDirection: 'column', 
                  justifyContent: 'center',
                  alignItems: 'center'
                }}
              >
                <Box sx={{ mb: 2 }}>
                  {tabValue === 0 ? (
                    <NotificationsIcon sx={{ fontSize: 60, color: 'primary.main' }} />
                  ) : (
                    <VerifiedIcon sx={{ fontSize: 60, color: 'success.main' }} />
                  )}
                </Box>
                <Typography variant="h5" gutterBottom>
                  {tabValue === 0 
                    ? "Select a patient to view their conversation" 
                    : "Select a message to review AI-generated response"}
                </Typography>
                <Typography variant="body1" color="textSecondary">
                  {tabValue === 0 
                    ? "You can communicate with patients and review their medical queries" 
                    : "Review and verify AI-generated responses before they're sent to patients"}
                </Typography>
              </Paper>
            )}
          </Grid>
        </Grid>
      </Container>
    </>
  );
};

export default ClinicianDashboard;