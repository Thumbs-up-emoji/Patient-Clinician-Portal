import { initializeApp } from 'firebase/app';
import { getAuth, GoogleAuthProvider } from 'firebase/auth';

const firebaseConfig = {
    apiKey: "AIzaSyDtUcnpqyzpcad799fFIZUVGo0PpPKieGU",
    authDomain: "health-connect-portal.firebaseapp.com",
    projectId: "health-connect-portal",
    storageBucket: "health-connect-portal.firebasestorage.app",
    messagingSenderId: "213307759050",
    appId: "1:213307759050:web:06c50034e3b5ae37a6d733",
    measurementId: "G-6J0DF0LVYH"
  };

const app = initializeApp(firebaseConfig);
const auth = getAuth(app);
const googleProvider = new GoogleAuthProvider();

export { auth, googleProvider };
