import { useState, useRef, useEffect } from 'react';
import { 
  Container, Box, Paper, Typography, IconButton, 
  TextField, InputAdornment, Avatar, Button,
  Divider, AppBar, Toolbar
} from '@mui/material';
import ArrowBackIcon from '@mui/icons-material/ArrowBack';
import SearchIcon from '@mui/icons-material/Search';
import MenuIcon from '@mui/icons-material/Menu';
import SendIcon from '@mui/icons-material/Send';
import MicIcon from '@mui/icons-material/Mic';
import AttachFileIcon from '@mui/icons-material/AttachFile';
import CheckCircleIcon from '@mui/icons-material/CheckCircle';
import { useParams, useNavigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';

const Chat = () => {
  const { userId } = useParams();
  const { currentUser } = useAuth();
  const [message, setMessage] = useState('');
  const [messages, setMessages] = useState([]);
  const [recipient, _setRecipient] = useState({ name: 'Athalia Putri' });
  const navigate = useNavigate();
  const messagesEndRef = useRef(null);
  const isClinician = currentUser?.role === 'clinician';
  
  // Sample data - in a real app, this would come from your backend
  useEffect(() => {
    // Simulate loading messages
    const sampleMessages = [
      {
        id: 'm1',
        sender: 'user',
        content: 'Lorem ipsum dolor sit amet consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.',
        timestamp: new Date('2023-11-30T09:41:00'),
        status: 'sent'
      },
      {
        id: 'm2',
        sender: 'ai',
        content: 'Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.',
        timestamp: new Date('2023-11-30T09:42:00'),
        status: 'unverified'
      },
      {
        id: 'm3',
        sender: 'user',
        content: 'Lorem ipsum dolor sit amet consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.',
        timestamp: new Date('2023-11-30T09:43:00'),
        status: 'sent'
      },
      {
        id: 'm4',
        sender: 'ai',
        content: 'Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.',
        timestamp: new Date('2023-11-30T09:44:00'),
        status: 'unverified'
      }
    ];
    
    setMessages(sampleMessages);
  }, [userId]);

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  const handleSendMessage = () => {
    if (!message.trim()) return;
    
    const newMessage = {
      id: `m${Date.now()}`,
      sender: 'user',
      content: message,
      timestamp: new Date(),
      status: 'sent'
    };
    
    setMessages([...messages, newMessage]);
    setMessage('');
    
    // Simulate AI response
    setTimeout(() => {
      const aiResponse = {
        id: `m${Date.now() + 1}`,
        sender: 'ai',
        content: 'Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.',
        timestamp: new Date(),
        status: 'unverified'
      };
      
      setMessages(prev => [...prev, aiResponse]);
    }, 1000);
  };

  const handleVerify = (messageId) => {
    setMessages(messages.map(msg => 
      msg.id === messageId ? { ...msg, status: 'verified' } : msg
    ));
  };

  const handleEdit = (messageId) => {
    // In a real app, you would implement editing functionality
    console.log('Editing message:', messageId);
  };

  const formatTime = (date) => {
    return date.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
  };

  const formatDate = (date) => {
    return date.toLocaleDateString([], { month: 'short', day: 'numeric', year: 'numeric' });
  };

  return (
    <Box sx={{ display: 'flex', flexDirection: 'column', height: '100vh', bgcolor: '#f5f5f5' }}>
      <AppBar position="static" color="transparent" elevation={0} sx={{ borderBottom: '1px solid #e0e0e0' }}>
        <Toolbar>
          <IconButton edge="start" color="inherit" onClick={() => navigate(-1)}>
            <ArrowBackIcon />
          </IconButton>
          <Typography variant="subtitle1" sx={{ ml: 1, flexGrow: 1 }}>
            {recipient.name}
          </Typography>
          <IconButton color="inherit">
            <SearchIcon />
          </IconButton>
          <IconButton edge="end" color="inherit">
            <MenuIcon />
          </IconButton>
        </Toolbar>
      </AppBar>
      
      <Box sx={{ flex: 1, overflowY: 'auto', p: 2 }}>
        {messages.map((msg, index) => {
          const isFirstMessageOfDay = index === 0 || 
            formatDate(msg.timestamp) !== formatDate(messages[index - 1].timestamp);
          
          return (
            <Box key={msg.id}>
              {isFirstMessageOfDay && (
                <Typography 
                  variant="caption" 
                  align="center" 
                  display="block" 
                  sx={{ my: 2, color: 'text.secondary' }}
                >
                  {formatDate(msg.timestamp)} {formatTime(msg.timestamp)}
                </Typography>
              )}
              
              <Box 
                sx={{ 
                  display: 'flex', 
                  justifyContent: msg.sender === 'user' ? 'flex-end' : 'flex-start',
                  mb: 2 
                }}
              >
                <Box 
                  sx={{ 
                    maxWidth: '70%',
                    p: 2,
                    borderRadius: 2,
                    bgcolor: msg.sender === 'user' ? '#1976d2' : '#f0f0f0',
                    color: msg.sender === 'user' ? 'white' : 'text.primary',
                    ...(msg.sender === 'user' 
                      ? { borderBottomRightRadius: 0 } 
                      : { borderBottomLeftRadius: 0 })
                  }}
                >
                  <Typography variant="body1">
                    {msg.content}
                  </Typography>
                </Box>
              </Box>
              
              {msg.sender === 'ai' && (
                <Box 
                  sx={{ 
                    display: 'flex', 
                    justifyContent: 'flex-start',
                    mb: 2,
                    ml: 2
                  }}
                >
                  {msg.status === 'verified' ? (
                    <CheckCircleIcon color="success" sx={{ mr: 1 }} />
                  ) : isClinician && (
                    <Box sx={{ display: 'flex', gap: 1 }}>
                      <Button 
                        variant="contained" 
                        size="small" 
                        sx={{ bgcolor: '#000', color: '#fff', borderRadius: 4 }}
                        onClick={() => handleEdit(msg.id)}
                      >
                        Edit
                      </Button>
                      <Button 
                        variant="contained" 
                        size="small" 
                        sx={{ bgcolor: '#000', color: '#fff', borderRadius: 4 }}
                        onClick={() => handleVerify(msg.id)}
                      >
                        Verify
                      </Button>
                    </Box>
                  )}
                </Box>
              )}
            </Box>
          );
        })}
        <div ref={messagesEndRef} />
      </Box>
      
      <Box sx={{ p: 2, bgcolor: 'white', borderTop: '1px solid #e0e0e0' }}>
        <TextField
          fullWidth
          placeholder="Message..."
          value={message}
          onChange={(e) => setMessage(e.target.value)}
          variant="outlined"
          size="small"
          sx={{ 
            '& .MuiOutlinedInput-root': {
              borderRadius: 4,
            }
          }}
          InputProps={{
            endAdornment: (
              <InputAdornment position="end">
                <IconButton>
                  <MicIcon />
                </IconButton>
                <IconButton>
                  <AttachFileIcon />
                </IconButton>
              </InputAdornment>
            ),
          }}
          onKeyPress={(e) => {
            if (e.key === 'Enter') {
              handleSendMessage();
            }
          }}
        />
      </Box>
    </Box>
  );
};

export default Chat;
