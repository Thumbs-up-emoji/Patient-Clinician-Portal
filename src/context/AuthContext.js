import { createContext, useContext } from 'react';

// Create the context with default values
export const AuthContext = createContext({
  currentUser: null,
  logout: () => {}
});

// Create a custom hook to use the context
export function useAuth() {
  return useContext(AuthContext);
}

// Don't create AuthProvider as a context - it should be a component
// The AuthProvider component should be defined in a separate file
