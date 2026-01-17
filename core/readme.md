┌─────────────────────────────────────────────┐
│  User calls: document_loader("report.pdf")  │
└──────────────────┬──────────────────────────┘
                   ↓
         ┌─────────────────┐
         │  File exists?   │
         └────┬────────┬───┘
              ↓        ↓
             Yes       No → Return []
              ↓
      ┌──────────────┐
      │ Get extension│
      │  ".pdf"      │
      └──────┬───────┘
             ↓
   ┌─────────────────────--┐
   │ Lookup in mapping     │
   │ ".pdf" → PyMuPDFLoader│
   └──────────┬──────────--┘
              ↓
     ┌────────────────┐
     │ Create loader  │
     │ Read the file  │
     └────────┬───────┘
              ↓
    ┌──────────────────┐
    │ Got documents?   │
    └─────┬────────┬───┘
          ↓        ↓
         Yes       No → Return []
          ↓
   ┌─────────────────┐
   │ Add metadata to │
   │ each document   │
   └────────┬────────┘
            ↓
   ┌────────────────┐
   │ Return docs!   │
   └────────────────┘
   document_loader.py