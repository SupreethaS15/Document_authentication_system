# Document_authentication_system
Overview:
  The Legal Document System is a user-friendly application designed to manage legal documents and evidences efficiently. It provides functionalities for user authentication, document uploading, evidence uploading, evidence packing based on urgency, and more.

Features:
  User Authentication: 
    Secure login and signup system.
  Document Management:
    Upload, view, search, download, and delete documents.
  Evidence Management: 
    Upload evidence with urgency levels, pack evidences based on urgency, and display evidence pack details.
  Secure Hashing:
    Documents are hashed using SHA-256 for integrity checks.
  
Usage:
  User Authentication
  Login: 
    Enter your username and password to log in.
  Signup:
    Create a new account by providing a unique username and password.
  
Document Management:
  Upload Document:
    Select a file to upload. The document is hashed and stored securely.
  Search Documents:
    Enter keywords to search for documents.
  View Document:
    View document details, including file name, path, hash, and owner. You can also open the document.
  Download Document:
    Save a copy of the document to your local system.
  Delete Document:
    Delete a document that you own.
  
Evidence Management:
  Upload Evidence: Select a file and enter its urgency level (1-10). Evidences are packed based on urgency.
  View Evidence Pack Details: Displays details of evidence packs sorted by urgency.
  B+ Tree Implementation
  The application uses a simple B+ Tree implementation to manage document keys, providing efficient insertion, deletion, and retrieval operations.
