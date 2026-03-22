# Art Gallery Management System (DBMS Project)

## Overview
The Art Gallery Management System is a database-driven web application designed to manage artworks, artists, customers, and exhibitions efficiently. It replaces traditional manual systems such as registers and spreadsheets with a structured and secure digital solution.

This project integrates database design, backend development, and frontend rendering to simulate a real-world gallery management system.

---

## Key Features
- Role-Based Access Control (Admin, Curator, Customer)
- Artwork Reservation and Waitlist System
- Artwork and Artist Management
- Real-time Dashboard and Reports
- CRUD Operations (Create, Read, Update, Delete)
- Provenance Tracking (Ownership History)

---

## Problem Statement
Traditional gallery systems lack structured data management, secure access control, and reservation mechanisms. They are inefficient in tracking artworks, customers, and exhibitions.

This system addresses these issues using a normalized relational database with a web-based interface.

---

## System Architecture
Frontend (HTML, CSS, Jinja Templates)  
Backend (Python Flask)  
Database (MySQL)

---

## Database Design

### Tables

**Artist_art**
- Artist_ID (Primary Key)
- Name
- Birthplace
- Age
- Style

**Artwork_art**
- Artwork_ID (Primary Key)
- Title
- Year
- Type
- Price
- Artist_ID (Foreign Key)

**Customer**
- Customer_ID (Primary Key)
- Name
- Email
- Password
- Role

**Reservation**
- Reservation_ID (Primary Key)
- Artwork_ID (Foreign Key)
- Customer_ID (Foreign Key)
- Status
- Date

---

## Tech Stack

**Backend**
Python, Flask  

**Frontend**
HTML, CSS, Jinja Templates  

**Database**
MySQL  

**Tools**
VS Code, MySQL Connector  

---

## Implementation Details
- Designed a normalized relational database schema  
- Developed Flask routes for CRUD operations and authentication  
- Integrated frontend using Jinja templates  
- Implemented reservation and waitlist logic  
- Ensured data integrity using constraints and validation  

---

## Results
- Successful integration of Flask and MySQL  
- CRUD operations tested and validated  
- Role-based authentication implemented  
- Reservation and waitlist features working correctly  
- Real-time updates displayed on dashboard  

---

## Applications
- Art galleries for managing artworks and exhibitions  
- Museums for tracking artwork ownership  
- Online art marketplaces  
- Academic DBMS and web development projects  

---

## Future Scope
- Integration of online payment and auction features  
- Support for artwork image uploads  
- Mobile-friendly interface with REST APIs  
- Expansion of user roles and permissions  

---

## References
- Flask Documentation  
- MySQL Workbench Documentation  
- W3Schools Tutorials  
- RBAC Model by Sandhu et al. (1996)  

---

## Conclusion
The Art Gallery Management System provides an efficient, secure, and scalable solution for managing gallery operations. It demonstrates practical implementation of database concepts combined with web technologies.
