import { useContext } from 'react';
import { Navigate } from 'react-router-dom';
import { AuthContext } from '../context/AuthContext';

const PrivateRoute = ({ children, role }) => {
  const { currentUser } = useContext(AuthContext);
  
  if (!currentUser) {
    return <Navigate to="/login" />;
  }
  
  // If role is specified, check if user has that role
  // In a real app, you'd check user roles from your database
  if (role && !currentUser.email.includes(role)) {
    return <Navigate to="/login" />;
  }
  
  return children;
};

export default PrivateRoute;
