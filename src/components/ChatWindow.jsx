import { useState, useEffect, useRef } from 'react';
import { useParams } from 'react-router-dom';
import TextField from '@mui/material/TextField';
import Button from '@mui/material/Button';
import Paper from '@mui/material/Paper';
import Typography from '@mui/material/Typography';
import SendIcon from '@mui/icons-material/Send';

const ChatWindow = () => {
  const { userId } = useParams();
  const [messages, setMessages] = useState([]);
  const [newMessage, setNewMessage] = useState('');
  const messagesEndRef = useRef(null);
  
  // Simulated data - in a real app, this would come from an API
  useEffect(() => {
    const sampleMessages = [
      {
        id: 1,
        sender: 'patient',
        text: 'I have been experiencing headaches for the past week.',
        timestamp: new Date('2023-11-30T09:41:00'),
        status: 'sent'
      },
      {
        id: 2,
        sender: 'ai',
        text: 'Based on your symptoms, this could be due to stress or dehydration. Try drinking more water and getting adequate rest.',
        timestamp: new Date('2023-11-30T09:42:00'),
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

  const handleSendMessage = (e) => {
    e.preventDefault();
    
    if (newMessage.trim() === '') return;
    
    const newMsg = {
      id: Date.now(),
      sender: 'patient',
      text: newMessage,
      timestamp: new Date(),
      status: 'sent'
    };
    
    setMessages([...messages, newMsg]);
    
    // Simulate AI response
    setTimeout(() => {
      const aiResponse = {
        id: Date.now() + 1,
        sender: 'ai',
        text: 'This is an AI-generated response that needs verification.',
        timestamp: new Date(),
        status: 'unverified'
      };
      
      setMessages(prev => [...prev, aiResponse]);
    }, 1000);
    
    setNewMessage('');
  };

  const handleVerify = (id) => {
    setMessages(messages.map(msg => 
      msg.id === id ? { ...msg, status: 'verified' } : msg
    ));
  };

  return (
    <Paper elevation={3} sx={{ height: '70vh', display: 'flex', flexDirection: 'column' }}>
      <div style={{ padding: 16, borderBottom: '1px solid #e0e0e0' }}>
        <Typography variant="h6">Chat</Typography>
      </div>
      
      <div style={{ flex: 1, overflow: 'auto', padding: 16 }}>
        {messages.map((message) => (
          <div 
            key={message.id} 
            style={{
              display: 'flex',
              justifyContent: message.sender === 'patient' ? 'flex-end' : 'flex-start',
              marginBottom: 16
            }}
          >
            <div 
              style={{
                background: message.sender === 'patient' ? '#1976d2' : 
                          message.status === 'unverified' ? '#f5f5f5' : '#e3f2fd',
                color: message.sender === 'patient' ? 'white' : 'black',
                padding: '8px 16px',
                borderRadius: 16,
                maxWidth: '70%',
                position: 'relative'
              }}
            >
              <Typography variant="body1">{message.text}</Typography>
              <Typography variant="caption" sx={{ opacity: 0.7 }}>
                {message.timestamp.toLocaleTimeString()}
              </Typography>
              
              {message.sender === 'ai' && message.status === 'unverified' && (
                <Button 
                  size="small" 
                  variant="contained" 
                  color="success"
                  onClick={() => handleVerify(message.id)}
                  sx={{ mt: 1 }}
                >
                  Verify
                </Button>
              )}
            </div>
          </div>
        ))}
        <div ref={messagesEndRef} />
      </div>
      
      <form onSubmit={handleSendMessage} style={{ display: 'flex', padding: 16, borderTop: '1px solid #e0e0e0' }}>
        <TextField
          fullWidth
          placeholder="Type a message..."
          value={newMessage}
          onChange={(e) => setNewMessage(e.target.value)}
          variant="outlined"
          sx={{ mr: 1 }}
        />
        <Button 
          type="submit" 
          variant="contained" 
          color="primary" 
          disabled={!newMessage.trim()}
        >
          <SendIcon />
        </Button>
      </form>
    </Paper>
  );
};

export default ChatWindow;
