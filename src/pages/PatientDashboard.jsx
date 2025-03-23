import { useState } from 'react';
import { 
  Container, Box, Paper, Typography, Tabs, Tab, 
  TextField, InputAdornment, List, ListItem, 
  ListItemText, ListItemAvatar, Avatar, Divider,
  Button
} from '@mui/material';
import SearchIcon from '@mui/icons-material/Search';
import VerifiedIcon from '@mui/icons-material/Verified';
import Navbar from '../components/Navbar';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';

const PatientDashboard = () => {
  const { currentUser } = useAuth();
  const [tabValue, setTabValue] = useState(0);
  const [searchQuery, setSearchQuery] = useState('');
  const [medicalQuestion, setMedicalQuestion] = useState('');
  const navigate = useNavigate();
  
  // Sample data - in a real app, this would come from your backend
  <Typography variant="subtitle1" sx={{ mb: 2 }}>
  Welcome, {currentUser?.displayName || 'Patient'}
</Typography>
  const verifiedQueries = [
    { id: 'q1', title: 'Hairfall Problem', avatar: '/avatar1.jpg', status: 'verified' },
    { id: 'q2', title: 'Acne Problem', avatar: '/avatar2.jpg', status: 'verified' },
  ];
  
  const unverifiedQueries = [
    { id: 'q3', title: 'Dark Circles problem', avatar: '/avatar3.jpg', status: 'reviewed' },
    { id: 'q4', title: 'Drinking milk while having cough advice', avatar: null, initials: 'RD', status: 'to-review' },
    { id: 'q5', title: 'Sleeping problem', avatar: '/avatar4.jpg', status: 'reviewed' },
  ];

  const handleTabChange = (event, newValue) => {
    setTabValue(newValue);
  };

  const handleSearch = (event) => {
    setSearchQuery(event.target.value);
  };

  const handleQuestionChange = (event) => {
    setMedicalQuestion(event.target.value);
  };

  const handleSubmitQuestion = () => {
    if (medicalQuestion.trim()) {
      console.log('Submitting question:', medicalQuestion);
      // In a real app, you would send this to your backend
      setMedicalQuestion('');
      // Optionally navigate to the chat with an AI or doctor
      // navigate('/chat/ai');
    }
  };

  const handleQueryClick = (queryId) => {
    navigate(`/chat/${queryId}`);
  };

  const filteredQueries = tabValue === 0 
    ? verifiedQueries.filter(q => q.title.toLowerCase().includes(searchQuery.toLowerCase()))
    : unverifiedQueries.filter(q => q.title.toLowerCase().includes(searchQuery.toLowerCase()));

  return (
    <Box sx={{ display: 'flex', flexDirection: 'column', height: '100vh', bgcolor: '#f5f5f5' }}>
      <Navbar />
      <Container maxWidth="sm" sx={{ flex: 1, display: 'flex', flexDirection: 'column', py: 2 }}>
        <Paper elevation={1} sx={{ mb: 2, borderRadius: 2, overflow: 'hidden' }}>
          <Box sx={{ p: 2, borderBottom: '1px solid #e0e0e0' }}>
            <Typography variant="h6" align="center" sx={{ fontWeight: 500 }}>
              {tabValue === 0 
                ? "Trusted AI Support, Verified by Experts." 
                : "Your Expertise, Elevated with AI Support."}
            </Typography>
          </Box>
          
          <Tabs 
            value={tabValue} 
            onChange={handleTabChange}
            variant="fullWidth"
            sx={{ borderBottom: '1px solid #e0e0e0' }}
          >
            <Tab label="Verified" />
            <Tab label={tabValue === 0 ? "Not Verified" : "To Review"} />
          </Tabs>
          
          <Box sx={{ p: 2 }}>
            <TextField
              fullWidth
              placeholder="Search"
              value={searchQuery}
              onChange={handleSearch}
              variant="outlined"
              size="small"
              sx={{ 
                mb: 2,
                bgcolor: '#f5f5f5',
                borderRadius: 1,
                '& .MuiOutlinedInput-root': {
                  borderRadius: 8,
                }
              }}
              InputProps={{
                startAdornment: (
                  <InputAdornment position="start">
                    <SearchIcon color="action" />
                  </InputAdornment>
                ),
              }}
            />
            
            <List sx={{ mb: 2 }}>
              {filteredQueries.map((query) => (
                <Box key={query.id}>
                  <ListItem 
                    button 
                    onClick={() => handleQueryClick(query.id)}
                    sx={{ py: 1 }}
                  >
                    <ListItemAvatar>
                      {query.avatar ? (
                        <Avatar src={query.avatar} />
                      ) : (
                        <Avatar sx={{ bgcolor: '#2196f3' }}>
                          {query.initials}
                        </Avatar>
                      )}
                    </ListItemAvatar>
                    <ListItemText primary={query.title} />
                    {query.status === 'verified' && (
                      <VerifiedIcon color="primary" fontSize="small" />
                    )}
                  </ListItem>
                  <Divider component="li" />
                </Box>
              ))}
              
              {filteredQueries.length > 0 && (
                <Typography 
                  variant="body2" 
                  align="right" 
                  sx={{ mt: 1, color: '#2196f3', cursor: 'pointer' }}
                >
                  Tap to See more
                </Typography>
              )}
            </List>
            
            <TextField
              fullWidth
              placeholder="Ask a Medical Question"
              value={medicalQuestion}
              onChange={handleQuestionChange}
              variant="outlined"
              size="small"
              sx={{ 
                mb: 2,
                bgcolor: '#f0f0f0',
                borderRadius: 1,
                '& .MuiOutlinedInput-root': {
                  borderRadius: 1,
                }
              }}
            />
            
            <Button
              fullWidth
              variant="contained"
              color="primary"
              onClick={handleSubmitQuestion}
              disabled={!medicalQuestion.trim()}
              sx={{ borderRadius: 1 }}
            >
              Submit Question
            </Button>
          </Box>
        </Paper>
      </Container>
    </Box>
  );
};

export default PatientDashboard;
