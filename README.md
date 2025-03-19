# Patient-Clinician-Portal
 
Problem Statement:


Patient-Clinician Portal for Connected Care and Healthy Aging


Project Description:-
Admins will manage clinician data and oversee smooth functioning.
Doctors/Clinicians will log in based on notifications received on their email/WhatsApp to review AI responses to patient queries.
Patients can upload their medical data, and ask questions receiving immediate responses from the AI, which will subsequently be verified by a clinician.


Key Features:-
Google Login: Simple and secure authentication, leading the user to their personalised dashboard.
AI-Generated Responses: Automatically generated responses to patient queries using an AI model such as Mistral, distinctly marked as 'unreviewed' until approved by a clinician.
Doctor Review and Editing: Doctors can review and modify AI responses to ensure accuracy.
Marked Responses: Responses will indicate whether they have been reviewed and approved by a doctor.
Notification System: Patients receive timely updates on their query status via email and WhatsApp, and clinicians will be notified when there are responses to be reviewed.
Response History: Both patients and doctors can access previous interactions for reference. Patients can also upload personal details such as medical reports, for more accurate responses from the AI and the clinicians.
Accessibility Features: Speech input and text-to-speech output for individuals with disabilities, along with a clean, minimalistic UI to enhance usability. These features are designed from the outset to be integral to the system's architecture.
Multi-Device Compatibility: Responsive design to support desktop, tablet, and mobile users.


Technology Stack:-
Frontend: ReactJS for building an interactive, user-friendly UI with responsive design principles.
Accessibility: Text-to-speech and speech-to-text features will be added through libraries like react-text-to-speech.
Backend: Python (Flask/Django) for handling APIs and server logic.
Database: MySQL to store patient inquiries, responses, and other user data.
Authentication: Google OAuth 2.0 to enable secure login and role management.
Communication: Libraries like smtplib and pywhatkit to be used to send notifications when required.


Implementation Strategy:-
Accessibility is integrated as a core principle from the outset to ensure inclusivity. Speech input, text-to-speech output, and a clean, minimalistic UI are prioritized throughout the development process to accommodate users with disabilities and those with limited technical literacy.
Milestones:
Core Feature Implementation - Fundamental aspects of the project such as Google OAuth, a basic dashboard for both clinicians and patients, the AI model integration, and a review page for clinicians to review AI responses.

Accessibility, Notifications, and more - Incorporate speech input and TTS features for accessibility. Implement notifications via email and/or WhatsApp. Explore further improvements/optimisations feasible within the available time (For example - options to target requests to specific clinicians, options regarding notifications, etc.).

Testing and Deployment - Thorough cross-platform testing of core functionalities, followed by addressing of bugs in order of priority. 
Subsequently, we proceed with deployment via a cloud platform such as AWS, followed by further testing and optimisation where appropriate.