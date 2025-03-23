import express from "express";
import mysql from "mysql2";
import admin from "firebase-admin";
import dotenv from "dotenv";
import { readFileSync } from "fs";
import path from "path";

// Function to load environment variables from .env file
function loadEnvVars(filePath) {
  try {
    const envFile = readFileSync(filePath, 'utf-8');
    const envVars = {};
    envFile.split('\n').forEach(line => {
      const [key, value] = line.split('=').map(part => part.trim());
      if (key && value) {
        process.env[key] = value;
      }
    });
    console.log('Environment variables loaded successfully.');
  } catch (error) {
    console.error('Error loading environment variables:', error);
  }
}

// Load environment variables from .env file
const envPath = path.resolve("../Patient-Clinician-Portal/backend/.env");
console.log("Resolved .env path:", envPath);
loadEnvVars(envPath);
console.log("DB_HOST:", process.env.DB_HOST);
console.log("DB_USER:", process.env.DB_USER);
console.log("DB_PASSWORD:", process.env.DB_PASSWORD);console.log("DB_NAME:", process.env.DB_NAME);

// Read the Firebase Admin JSON file
const serviceAccount = JSON.parse(
  readFileSync(new URL("../firebase-admin.json", import.meta.url))
);

// Initialize Firebase Admin
admin.initializeApp({
  credential: admin.credential.cert(serviceAccount),
  databaseURL: "https://your-project-id.firebaseio.com",
});

const db = admin.firestore();

// MySQL connection
const connection = mysql.createConnection({
    host: process.env.DB_HOST,
    user: process.env.DB_USER,
    password: process.env.DB_PASSWORD, // Use DB_PASSWORD instead of DB_PASS to match your .env file
    database: process.env.DB_NAME
  });

connection.connect((err) => {
  if (err) {
    console.error("❌ MySQL Connection Error:", err);
    return;
  }
  console.log("✅ Connected to MySQL!");
});

// Function to sync queries from Firebase to MySQL
const syncQueries = async () => {
  try {
    const snapshot = await db.collection("queries").get();

    snapshot.forEach((doc) => {
      const data = doc.data();
      const query = `
        INSERT INTO queries (conversation_id, patient_id, question, image_url, created_at)
        VALUES (?, ?, ?, ?, ?)
        ON DUPLICATE KEY UPDATE question = ?, image_url = ?, created_at = ?
      `;

      connection.query(
        query,
        [
          data.conversation_id,
          data.patient_id,
          data.question,
          data.image_url || null,
          new Date(data.timestamp),
          data.question,
          data.image_url || null,
          new Date(data.timestamp),
        ],
        (err) => {
          if (err) console.error("❌ MySQL Insert Error:", err);
        }
      );
    });

    console.log("✅ Queries synced successfully!");
  } catch (error) {
    console.error("❌ Firebase Fetch Error:", error);
  }
};

// Check MySQL connection before running sync
const startSync = () => {
  if (connection && connection.state === 'connected') {
    // Run sync every 5 seconds
    setInterval(syncQueries, 5000);
  } else {
    console.log("MySQL not connected, retrying in 5 seconds...");
    setTimeout(startSync, 5000); // Retry connection
  }
};

// Start Express server
const app = express();
app.listen(3000, () => {
  console.log("🚀 Sync server running on port 3000");
  startSync(); // Start sync only after the Express server is running
});

// Test connection function (using the already imported mysql module)
function testDbConnection() {
  const testConnection = mysql.createConnection({
    host: process.env.DB_HOST,
    user: process.env.DB_USER,
    password: process.env.DB_PASSWORD,
    database: process.env.DB_NAME
  });

  testConnection.connect((err) => {
    if (err) {
      console.error("Connection failed:", err);
      return;
    }
    console.log("Successfully connected to MySQL!");
    testConnection.end();
  });
}

// Uncomment this line to run the test connection
// testDbConnection();