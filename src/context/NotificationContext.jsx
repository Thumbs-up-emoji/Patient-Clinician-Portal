// src/context/NotificationProvider.jsx
import { useState, useEffect } from 'react';
import { useAuth } from './AuthContext';
import { createContext } from 'react';

const NotificationContext = createContext({
  notifications: [],
  unreadCount: 0,
  markAsRead: () => {},
  markAllAsRead: () => {}
});

export default NotificationContext;

export function NotificationProvider({ children }) {
  const { currentUser } = useAuth();
  const [notifications, setNotifications] = useState([]);
  const [unreadCount, setUnreadCount] = useState(0);

  // In a real app, you would fetch notifications from Firebase
  useEffect(() => {
    if (currentUser) {
      // Mock notifications for now
      const mockNotifications = [
        {
          id: '1',
          title: 'New message',
          message: 'Dr. Smith has responded to your query',
          read: false,
          timestamp: new Date().toISOString(),
        },
        {
          id: '2',
          title: 'Verification needed',
          message: 'There are responses waiting for your verification',
          read: true,
          timestamp: new Date(Date.now() - 86400000).toISOString(), // 1 day ago
        },
      ];
      
      setNotifications(mockNotifications);
      setUnreadCount(mockNotifications.filter(n => !n.read).length);
    }
  }, [currentUser]);

  const markAsRead = (notificationId) => {
    setNotifications(prev => 
      prev.map(notif => 
        notif.id === notificationId 
          ? { ...notif, read: true } 
          : notif
      )
    );
    setUnreadCount(prev => Math.max(0, prev - 1));
  };

  const markAllAsRead = () => {
    setNotifications(prev => 
      prev.map(notif => ({ ...notif, read: true }))
    );
    setUnreadCount(0);
  };

  const value = {
    notifications,
    unreadCount,
    markAsRead,
    markAllAsRead,
  };

  return (
    <NotificationContext.Provider value={value}>
      {children}
    </NotificationContext.Provider>
  );
}
