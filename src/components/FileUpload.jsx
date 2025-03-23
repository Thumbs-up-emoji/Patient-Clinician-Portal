// src/components/FileUpload.jsx
import { useState } from 'react';
import { 
  Box, 
  Button, 
  Typography, 
  LinearProgress, 
  Paper, 
  List, 
  ListItem, 
  ListItemIcon, 
  ListItemText, 
  IconButton 
} from '@mui/material';
import CloudUploadIcon from '@mui/icons-material/CloudUpload';
import InsertDriveFileIcon from '@mui/icons-material/InsertDriveFile';
import DeleteIcon from '@mui/icons-material/Delete';

export default function FileUpload() {
  const [files, setFiles] = useState([]);
  const [uploading, setUploading] = useState(false);
  const [uploadProgress, setUploadProgress] = useState({});

  const handleFileChange = (event) => {
    const newFiles = Array.from(event.target.files);
    setFiles(prev => [...prev, ...newFiles]);
  };

  const handleRemoveFile = (index) => {
    setFiles(prev => prev.filter((_, i) => i !== index));
  };

  const handleUpload = async () => {
    setUploading(true);
    
    // Mock upload progress
    const totalFiles = files.length;
    for (let i = 0; i < totalFiles; i++) {
      const _file = files[i];
      
      // Simulate upload progress
      for (let progress = 0; progress <= 100; progress += 10) {
        setUploadProgress(prev => ({
          ...prev,
          [i]: progress
        }));
        await new Promise(resolve => setTimeout(resolve, 200));
      }
    }
    
    // In a real app, you would upload to Firebase Storage here
    
    setUploading(false);
    setFiles([]);
    setUploadProgress({});
  };

  return (
    <Box sx={{ mt: 3 }}>
      <Paper elevation={3} sx={{ p: 3 }}>
        <Typography variant="h6" gutterBottom>
          Upload Medical Records
        </Typography>
        
        <Box 
          sx={{ 
            border: '2px dashed #ccc', 
            borderRadius: 2, 
            p: 3, 
            textAlign: 'center',
            mb: 3,
            backgroundColor: '#f8f8f8'
          }}
        >
          <input
            accept="image/*,.pdf,.doc,.docx"
            style={{ display: 'none' }}
            id="file-upload"
            multiple
            type="file"
            onChange={handleFileChange}
          />
          <label htmlFor="file-upload">
            <Button
              variant="contained"
              component="span"
              startIcon={<CloudUploadIcon />}
            >
              Select Files
            </Button>
          </label>
          <Typography variant="body2" sx={{ mt: 1 }}>
            Supported formats: PDF, DOC, DOCX, JPG, PNG
          </Typography>
        </Box>
        
        {files.length > 0 && (
          <>
            <List>
              {files.map((file, index) => (
                <ListItem
                  key={index}
                  secondaryAction={
                    <IconButton 
                      edge="end" 
                      aria-label="delete"
                      onClick={() => handleRemoveFile(index)}
                      disabled={uploading}
                    >
                      <DeleteIcon />
                    </IconButton>
                  }
                >
                  <ListItemIcon>
                    <InsertDriveFileIcon />
                  </ListItemIcon>
                  <ListItemText 
                    primary={file.name} 
                    secondary={`${(file.size / 1024).toFixed(2)} KB`} 
                  />
                  {uploading && uploadProgress[index] !== undefined && (
                    <Box sx={{ width: '100%', ml: 2, mr: 2 }}>
                      <LinearProgress 
                        variant="determinate" 
                        value={uploadProgress[index]} 
                      />
                    </Box>
                  )}
                </ListItem>
              ))}
            </List>
            
            <Button
              variant="contained"
              color="primary"
              onClick={handleUpload}
              disabled={uploading}
              sx={{ mt: 2 }}
            >
              {uploading ? 'Uploading...' : 'Upload Files'}
            </Button>
          </>
        )}
      </Paper>
    </Box>
  );
}
