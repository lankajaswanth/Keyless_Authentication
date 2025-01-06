# Passwordless Face Authentication System

This repository contains the implementation and documentation for the Passwordless Face Authentication System. The project was developed as part of the ITE4001 - Network and Information Security course under the guidance of Prof. Aswani Kumar Cherukuri.

## 📌 Project Objective
The aim of this project is to design a secure authentication system where users can log in without passwords. Instead, a facial recognition system verifies the user’s identity. This approach improves security while eliminating the issues with password-based systems.

## 🚀 Technologies Used
- **Language:** Python
- **Face Recognition:** OpenCV and face_recognition library
- **Encryption:** AES (Advanced Encryption Standard)
- **Frontend:** HTML, CSS, Bootstrap, JavaScript
- **Database:** PostgreSQL
- **Backend:** Flask

## 📊 System Components
### ✅ User Features:
- Enter username for authentication
- Real-time face recognition for access
- Passwordless login

### ✅ Admin Features:
- Admin can add new users and upload their images
- Manage and update user information
- Encrypted storage of user data

### ✅ Security Measures:
- AES encryption for image encodings
- Secure PostgreSQL database integration

## 📈 Workflow:
1. **User Login:** The user enters the username, and the system captures a real-time image for face recognition.
2. **Face Matching:** The captured face is compared with encrypted face encodings stored in the database.
3. **Admin Management:** The admin can add, view, and manage user accounts and face data securely.

## 📦 Requirements:
Ensure the following dependencies are installed:
```bash
pip install face_recognition flask opencv-python cryptography psycopg2
```

## 🧪 How to Run the Project
1. **Clone the Repository:**
   ```bash
   git clone <your-repo-link>
   ```
2. **Navigate to Project Directory:**
   ```bash
   cd Passwordless-Face-Auth
   ```
3. **Run the Flask Server:**
   ```bash
   python app.py
   ```
4. **Open Web Browser:** Access the system at `http://localhost:5000`

## 📊 Results
- **Face Matching Accuracy:** Achieved over 99% accuracy for face recognition
- **Security:** AES encryption implemented for secure storage


## 📧 Contact Information
- **Contributors:**
   - Lanka Jaswanth 
   - Perumalla Sasank 
   - B K Anirudh 
   - Somaplli Yeswin

