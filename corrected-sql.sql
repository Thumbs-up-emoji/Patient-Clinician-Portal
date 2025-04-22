-- First, make sure we're using the right database
USE patient_portal;

-- 1. Insert Users (10 patients, 5 clinicians, 2 admins)
INSERT INTO users (email, name, role, google_id) VALUES
-- Patients
('patient1@example.com', 'John Smith', 'patient', 'google_id_p1'),
('patient2@example.com', 'Emily Johnson', 'patient', 'google_id_p2'),
('patient3@example.com', 'Michael Brown', 'patient', 'google_id_p3'),
('patient4@example.com', 'Sarah Davis', 'patient', 'google_id_p4'),
('patient5@example.com', 'Robert Wilson', 'patient', 'google_id_p5'),
('patient6@example.com', 'Jennifer Lee', 'patient', 'google_id_p6'),
('patient7@example.com', 'David Martinez', 'patient', 'google_id_p7'),
('patient8@example.com', 'Lisa Anderson', 'patient', 'google_id_p8'),
('patient9@example.com', 'James Taylor', 'patient', 'google_id_p9'),
('patient10@example.com', 'Sophia Garcia', 'patient', 'google_id_p10'),

-- Clinicians
('doctor1@example.com', 'Dr. Olivia Williams', 'clinician', 'google_id_d1'),
('doctor2@example.com', 'Dr. William Jones', 'clinician', 'google_id_d2'),
('doctor3@example.com', 'Dr. Emma Rodriguez', 'clinician', 'google_id_d3'),
('nurse1@example.com', 'Nurse Daniel White', 'clinician', 'google_id_n1'),
('nurse2@example.com', 'Nurse Maria Thompson', 'clinician', 'google_id_n2'),

-- Admins
('admin1@example.com', 'Admin Alex Johnson', 'admin', 'google_id_a1'),
('admin2@example.com', 'Admin Samantha Clark', 'admin', 'google_id_a2');

-- 2. Insert Conversations (multiple conversations for some patients)
INSERT INTO conversations (patient_id) VALUES
(1), -- John Smith's first conversation
(1), -- John Smith's second conversation
(2), -- Emily Johnson's conversation
(3), -- Michael Brown's conversation
(4), -- Sarah Davis's conversation
(5), -- Robert Wilson's first conversation
(5), -- Robert Wilson's second conversation
(6), -- Jennifer Lee's conversation
(8), -- Lisa Anderson's conversation
(9), -- James Taylor's conversation
(10); -- Sophia Garcia's conversation

-- 3. Insert Queries
-- To make sure we have the correct IDs for later reference, let's use a more controlled approach
SET @conv1 = 1;  -- John's first conversation
SET @conv2 = 2;  -- John's second conversation 
SET @conv3 = 3;  -- Emily's conversation
SET @conv4 = 4;  -- Michael's conversation
SET @conv5 = 5;  -- Sarah's conversation
SET @conv6 = 6;  -- Robert's first conversation
SET @conv7 = 7;  -- Robert's second conversation
SET @conv8 = 8;  -- Jennifer's conversation
SET @conv9 = 9;  -- Lisa's conversation
SET @conv10 = 10; -- James's conversation
SET @conv11 = 11; -- Sophia's conversation

-- Insert queries and store the IDs
INSERT INTO queries (conversation_id, patient_id, question, image_url) VALUES
-- John's queries in conversation 1
(@conv1, 1, 'I have been experiencing headaches for the past week. Could this be related to my blood pressure medication?', NULL);
SET @query1 = LAST_INSERT_ID();

INSERT INTO queries (conversation_id, patient_id, question, image_url) VALUES
(@conv1, 1, 'The headaches are mainly in the morning. Should I adjust when I take my medication?', NULL);
SET @query2 = LAST_INSERT_ID();

-- John's queries in conversation 2
INSERT INTO queries (conversation_id, patient_id, question, image_url) VALUES
(@conv2, 1, 'I noticed a rash on my arm after starting the new antibiotic.', 'https://picsum.photos/800/600?random=1');
SET @query3 = LAST_INSERT_ID();

-- Emily's queries
INSERT INTO queries (conversation_id, patient_id, question, image_url) VALUES
(@conv3, 2, 'My allergy symptoms seem worse this year. Can I increase my antihistamine dosage?', NULL);
SET @query4 = LAST_INSERT_ID();

-- Michael's queries
INSERT INTO queries (conversation_id, patient_id, question, image_url) VALUES
(@conv4, 3, 'I have been having trouble sleeping. What non-medication approaches would you recommend?', NULL);
SET @query5 = LAST_INSERT_ID();

INSERT INTO queries (conversation_id, patient_id, question, image_url) VALUES
(@conv4, 3, 'I tried the breathing exercises but still had insomnia. Would melatonin help?', NULL);
SET @query6 = LAST_INSERT_ID();

-- Sarah's queries
INSERT INTO queries (conversation_id, patient_id, question, image_url) VALUES
(@conv5, 4, 'My blood sugar readings have been fluctuating a lot this week.', 'https://picsum.photos/800/600?random=2');
SET @query7 = LAST_INSERT_ID();

-- Robert's queries in conversation 1
INSERT INTO queries (conversation_id, patient_id, question, image_url) VALUES
(@conv6, 5, 'I have a follow-up question about my recent lab results. My cholesterol is still high.', NULL);
SET @query8 = LAST_INSERT_ID();

-- Robert's queries in conversation 2
INSERT INTO queries (conversation_id, patient_id, question, image_url) VALUES
(@conv7, 5, 'I''m experiencing side effects from the statin medication. Can we discuss alternatives?', NULL);
SET @query9 = LAST_INSERT_ID();

-- Jennifer's queries
INSERT INTO queries (conversation_id, patient_id, question, image_url) VALUES
(@conv8, 6, 'My child has a fever of 101°F. When should I be concerned?', NULL);
SET @query10 = LAST_INSERT_ID();

-- Lisa's queries
INSERT INTO queries (conversation_id, patient_id, question, image_url) VALUES
(@conv9, 8, 'I need to reschedule my upcoming appointment on the 15th.', NULL);
SET @query11 = LAST_INSERT_ID();

-- James's queries
INSERT INTO queries (conversation_id, patient_id, question, image_url) VALUES
(@conv10, 9, 'The physical therapy exercises are causing more pain in my knee.', 'https://picsum.photos/800/600?random=3');
SET @query12 = LAST_INSERT_ID();

-- Sophia's queries
INSERT INTO queries (conversation_id, patient_id, question, image_url) VALUES
(@conv11, 10, 'I''m having an allergic reaction to something, but I''m not sure what. My face is swollen.', 'https://picsum.photos/800/600?random=4');
SET @query13 = LAST_INSERT_ID();

-- 4. Insert Responses - Now using the variables to ensure foreign key references are correct
INSERT INTO responses (query_id, ai_response, clinician_response, clinician_id, status, reviewed_at) 
VALUES (@query1, 'Headaches can be a side effect of some blood pressure medications. It would be good to discuss this with your healthcare provider who can evaluate if your medication needs adjustment.', 
'Yes, headaches can be a side effect of your lisinopril. Let\'s try adjusting the dosage. Please monitor your blood pressure daily and we can review at your appointment next week.', 
1, 'reviewed', '2023-09-05 14:30:00');

INSERT INTO responses (query_id, ai_response, clinician_response, clinician_id, status, reviewed_at)
VALUES (@query2, 'Morning headaches could be related to the timing of your medication. Some blood pressure medications can cause changes in pressure as they wear off or peak. Your doctor might suggest taking your medication at a different time of day.',
'Try taking your medication in the evening instead of morning for the next three days and let me know if that helps with the morning headaches.',
1, 'reviewed', '2023-09-05 15:45:00');

INSERT INTO responses (query_id, ai_response, clinician_response, clinician_id, status, reviewed_at)
VALUES (@query3, 'A rash can be a sign of an allergic reaction to an antibiotic. This should be evaluated promptly. Please contact your healthcare provider and consider stopping the antibiotic if advised to do so.',
'This appears to be an allergic reaction to the amoxicillin. Please stop taking it immediately and switch to the alternative antibiotic I\'ve just prescribed. If the rash worsens or you develop any breathing difficulties, please go to the emergency room.',
2, 'reviewed', '2023-09-10 09:15:00');

INSERT INTO responses (query_id, ai_response, clinician_response, clinician_id, status, reviewed_at)
VALUES (@query4, 'Increasing antihistamine dosage should only be done under medical guidance. Some antihistamines have maximum recommended daily doses that shouldn\'t be exceeded.',
'Your current cetirizine dose is already at the maximum recommended level. Let\'s add a nasal corticosteroid spray to help with the nasal symptoms. If that doesn\'t provide relief, we may need to consider allergy testing.',
3, 'reviewed', '2023-09-12 11:20:00');

INSERT INTO responses (query_id, ai_response, clinician_response, clinician_id, status, reviewed_at)
VALUES (@query5, 'Non-medication approaches for insomnia include maintaining a regular sleep schedule, creating a relaxing bedtime routine, limiting screen time before bed, avoiding caffeine and alcohol near bedtime, and ensuring your bedroom is dark, quiet, and cool. Relaxation techniques like deep breathing, meditation, or progressive muscle relaxation can also help.',
NULL, NULL, 'unreviewed', NULL);

INSERT INTO responses (query_id, ai_response, clinician_response, clinician_id, status, reviewed_at)
VALUES (@query6, 'Melatonin is a natural hormone that regulates sleep-wake cycles. It may help with insomnia for some people. It\'s generally considered safe for short-term use, but it\'s best to start with a low dose (0.5-1mg) and take it 1-2 hours before bedtime.',
'Melatonin may help, but let\'s first try to improve your sleep hygiene. Avoid screens 2 hours before bed, establish a consistent sleep schedule, and try the progressive muscle relaxation technique I\'ve linked in your patient portal. If these don\'t help after a week, you can try 1mg melatonin 30 minutes before bed.',
1, 'reviewed', '2023-09-15 16:40:00');

INSERT INTO responses (query_id, ai_response, clinician_response, clinician_id, status, reviewed_at)
VALUES (@query7, 'Fluctuations in blood sugar can be caused by changes in diet, activity level, stress, illness, or medication. It\'s important to maintain a consistent carbohydrate intake throughout the day and monitor patterns in your readings.',
'I notice your morning fasting levels are particularly high. Let\'s adjust your evening insulin dose from 10 to 12 units for the next three days and see if that helps stabilize your morning readings. Continue to log your carb intake alongside the readings.',
2, 'reviewed', '2023-09-18 10:10:00');

INSERT INTO responses (query_id, ai_response, clinician_response, clinician_id, status, reviewed_at)
VALUES (@query8, 'High cholesterol can be managed through a combination of diet, exercise, and sometimes medication. Focus on reducing saturated fats and increasing fiber intake. Regular physical activity can also help improve cholesterol levels.',
'Your LDL is still above our target. Let\'s increase your atorvastatin to 40mg daily and recheck in 8 weeks. Also, I\'d like you to consult with our dietitian for additional dietary strategies.',
3, 'reviewed', '2023-09-20 14:55:00');

INSERT INTO responses (query_id, ai_response, clinician_response, clinician_id, status, reviewed_at)
VALUES (@query9, 'Statins can cause side effects in some people, including muscle pain and digestive issues. There are alternative medications and approaches to managing cholesterol that your doctor can discuss with you.',
'I understand the muscle pain can be uncomfortable. Let\'s try switching you to rosuvastatin, which some patients tolerate better. Start with 10mg daily and we\'ll check your levels and symptoms in 6 weeks.',
2, 'reviewed', '2023-09-22 09:30:00');

INSERT INTO responses (query_id, ai_response, clinician_response, clinician_id, status, reviewed_at)
VALUES (@query10, 'For a child, a fever of 101°F is usually not concerning by itself. You should seek medical attention if the fever is over 102.2°F for children older than 3 months, if it persists for more than 2-3 days, or if your child shows signs of dehydration, unusual drowsiness, or a rash.',
'A fever of 101°F is usually the body\'s normal response to fighting an infection. Make sure your child stays hydrated and you can give children\'s acetaminophen for comfort. If the fever lasts more than 3 days, goes above 102.5°F, or if your child develops a rash, severe headache, stiff neck, or persistent vomiting, please call us immediately or go to the ER.',
4, 'reviewed', '2023-09-25 13:20:00');

INSERT INTO responses (query_id, ai_response, clinician_response, clinician_id, status, reviewed_at)
VALUES (@query11, 'I see that you need to reschedule your appointment. Our AI assistant cannot directly access or modify the scheduling system. A staff member will need to help you with this request.',
'I\'ve rescheduled your appointment to the 22nd at 2:30 PM. Please confirm if this works for you.',
5, 'reviewed', '2023-09-26 11:05:00');

INSERT INTO responses (query_id, ai_response, clinician_response, clinician_id, status, reviewed_at)
VALUES (@query12, 'Increased pain during physical therapy exercises could indicate that the exercises need modification. It\'s important to distinguish between therapeutic discomfort and harmful pain. Please contact your physical therapist or doctor to evaluate and potentially adjust your exercise program.',
'Based on the image, there\'s significant swelling that wasn\'t present at your last visit. Please pause the current exercises and switch to just the gentle range of motion exercises we started with. I\'ve asked our physical therapy department to call you today to reassess your program.',
1, 'reviewed', '2023-09-28 15:40:00');

INSERT INTO responses (query_id, ai_response, clinician_response, clinician_id, status, reviewed_at)
VALUES (@query13, 'Facial swelling can be a sign of a serious allergic reaction. If you\'re experiencing difficulty breathing, severe swelling, or other concerning symptoms, please seek emergency medical care immediately. For mild reactions, an antihistamine like diphenhydramine (Benadryl) may help reduce symptoms.',
NULL, NULL, 'unreviewed', NULL);
