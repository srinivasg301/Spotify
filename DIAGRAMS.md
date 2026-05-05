# 📊 Spotify Backend - Flow Diagrams

## 1. Application Request Flow

```mermaid
graph TD
    A["Client/Browser"] -->|HTTP Request| B["FastAPI Server"]
    B -->|1. Route Matching| C["Router Layer"]
    C -->|2. Check Auth Header| D["Dependencies Layer"]
    D -->|x-user-role| E{Is Admin?}
    E -->|No| F["403 Forbidden"]
    E -->|Yes| G["Service Layer"]
    
    G -->|3. Business Logic| H["Artist/Song Service"]
    H -->|Query Data| I["Database Session"]
    I -->|SQLAlchemy ORM| J["PostgreSQL Database"]
    
    J -->|Records| I
    I -->|Model Objects| H
    H -->|Processed Data| K["Schema Validation"]
    K -->|Pydantic Validation| L["Response Model"]
    L -->|JSON Response| M["FastAPI Response"]
    
    M -->|HTTP 200/201| N["Client Receives Data"]
    F -->|HTTP 403| N
    
    style A fill:#e1f5ff
    style B fill:#fff3e0
    style C fill:#f3e5f5
    style D fill:#f3e5f5
    style G fill:#e8f5e9
    style J fill:#fce4ec
    style N fill:#e1f5ff
```

---

## 2. Application Architecture Layers

```mermaid
graph TB
    subgraph "Presentation Layer"
        A["Swagger UI<br/>http://localhost:8000/docs"]
        B["Client Apps<br/>Web/Mobile"]
    end
    
    subgraph "API Layer"
        C["FastAPI<br/>app.main:app"]
    end
    
    subgraph "Router Layer"
        D["Artist Router<br/>POST/GET/PUT/DELETE"]
        E["Song Router<br/>POST/GET/PUT/DELETE"]
        F["Admin Router<br/>GET /admin/songs"]
    end
    
    subgraph "Middleware/Dependencies"
        G["get_user_context<br/>reads x-user-role"]
        H["require_admin<br/>checks role"]
    end
    
    subgraph "Service Layer"
        I["Artist Service<br/>create_artist, get_artists"]
        J["Song Service<br/>create_song, get_songs"]
    end
    
    subgraph "Data Layer"
        K["SQLAlchemy ORM<br/>Models"]
        L["Database Session<br/>Connection Pool"]
    end
    
    subgraph "Database"
        M["PostgreSQL<br/>artists table"]
        N["PostgreSQL<br/>songs table"]
    end
    
    A --> C
    B --> C
    C --> D
    C --> E
    C --> F
    
    D --> G
    E --> G
    F --> H
    
    G --> I
    G --> J
    H --> I
    H --> J
    
    I --> K
    J --> K
    
    K --> L
    
    L --> M
    L --> N
    
    style A fill:#64b5f6
    style B fill:#64b5f6
    style C fill:#fff176
    style D fill:#a5d6a7
    style E fill:#a5d6a7
    style F fill:#a5d6a7
    style G fill:#ffcc80
    style H fill:#ffcc80
    style I fill:#ce93d8
    style J fill:#ce93d8
    style K fill:#ef9a9a
    style L fill:#ef9a9a
    style M fill:#80deea
    style N fill:#80deea
```

---

## 3. Database Schema Relationship

```mermaid
erDiagram
    ARTIST ||--o{ SONG : creates
    
    ARTIST {
        int id PK
        string name UK "unique, indexed"
    }
    
    SONG {
        int id PK
        string title
        int artist_id FK
        string album
        int duration
        string thumbnail_url
    }
```

---

## 4. Complete Request Sequence: Create Song (Admin)

```mermaid
sequenceDiagram
    participant Client
    participant FastAPI
    participant Router
    participant Dependency
    participant Service
    participant Database
    
    Client->>FastAPI: POST /songs<br/>body: {title, artist_id, ...}<br/>header: x-user-role: admin
    
    FastAPI->>Router: Route to song_router
    Router->>Dependency: get_user_context()
    Dependency->>Dependency: Read x-user-role header
    Dependency-->>Router: UserContext {role: admin}
    
    Router->>Dependency: require_admin()
    Dependency->>Dependency: Check if role == "admin"
    Dependency-->>Router: Authorized ✓
    
    Router->>Service: create_song(db, SongCreate)
    Service->>Service: Validate input
    Service->>Database: INSERT into songs table
    Database->>Database: Save to PostgreSQL
    Database-->>Service: Song object with id=1
    
    Service-->>Router: Song model
    Router->>Router: Serialize with jsonable_encoder
    Router->>Router: Build response dict
    Router-->>FastAPI: {success: true, data: {...}, message: "Song created"}
    
    FastAPI->>Client: HTTP 201<br/>JSON response
    Client->>Client: Display success message
```

---

## 5. Authorization Flow

```mermaid
flowchart TD
    A["Client Request"] --> B["Check x-user-role header"]
    B --> C{Is header present?}
    
    C -->|No| D["role = 'user'"]
    C -->|Yes| E["role = header value"]
    
    D --> F["UserContext created"]
    E --> F
    
    F --> G{Is endpoint admin-only?}
    
    G -->|No| H["Allow access"]
    G -->|Yes| I{require_admin check}
    
    I -->|role == 'admin'| H
    I -->|role != 'admin'| J["Raise HTTPException 403"]
    
    H --> K["Execute endpoint"]
    K --> L["Return 200/201 response"]
    
    J --> M["Return 403 Forbidden<br/>Admin access required"]
    
    L --> N["Client receives data"]
    M --> O["Client receives error"]
    
    style A fill:#e3f2fd
    style H fill:#c8e6c9
    style K fill:#fff9c4
    style L fill:#c8e6c9
    style J fill:#ffccbc
    style M fill:#ffccbc
    style N fill:#c8e6c9
    style O fill:#ffccbc
```

---

## 6. Admin Request Flow Diagram

```mermaid
graph TD
    A["🔐 Admin Client"] -->|HTTP Request<br/>header: x-user-role: admin| B["FastAPI Server"]
    B -->|Route Matching| C["Admin Check"]
    C -->|require_admin()| D{Is Admin?}
    
    D -->|Yes ✓| E["Service Layer"]
    D -->|No ✗| F["❌ HTTP 403<br/>Admin access required"]
    
    E -->|Full Access| E1["✅ Create Artist"]
    E -->|Full Access| E2["✅ Update Artist"]
    E -->|Full Access| E3["✅ Delete Artist"]
    E -->|Full Access| E4["✅ Create Song"]
    E -->|Full Access| E5["✅ Update Song"]
    E -->|Full Access| E6["✅ Delete Song"]
    E -->|Full Access| E7["✅ View Admin Dashboard"]
    
    E1 -->|Modify DB| DB[(PostgreSQL<br/>artists table)]
    E2 -->|Modify DB| DB
    E3 -->|Modify DB| DB
    E4 -->|Modify DB| DB2[(PostgreSQL<br/>songs table)]
    E5 -->|Modify DB| DB2
    E6 -->|Modify DB| DB2
    E7 -->|Read DB| DB
    E7 -->|Read DB| DB2
    
    DB -->|Success| RESP["✅ HTTP 200/201<br/>Changes Applied"]
    DB2 -->|Success| RESP
    
    RESP -->|Response| A
    F -->|Response| A
    
    style A fill:#d32f2f,color:#fff
    style B fill:#1565c0,color:#fff
    style C fill:#0277bd,color:#fff
    style D fill:#00796b,color:#fff
    style E1 fill:#2e7d32,color:#fff
    style E2 fill:#2e7d32,color:#fff
    style E3 fill:#c62828,color:#fff
    style E4 fill:#2e7d32,color:#fff
    style E5 fill:#2e7d32,color:#fff
    style E6 fill:#c62828,color:#fff
    style E7 fill:#1976d2,color:#fff
    style F fill:#c62828,color:#fff
    style DB fill:#1565c0,color:#fff
    style RESP fill:#2e7d32,color:#fff
```

---

## 7. User Request Flow Diagram

```mermaid
graph TD
    A["👤 User Client"] -->|HTTP Request<br/>header: x-user-role: user| B["FastAPI Server"]
    B -->|Route Matching| C["Check Endpoint Type"]
    
    C -->|Read-Only| D1["✅ GET /artists"]
    C -->|Read-Only| D2["✅ GET /songs"]
    C -->|Read-Only| D3["✅ Search"]
    C -->|Read-Only| D4["✅ Stream"]
    
    C -->|Write Operation| E{Is Admin-Only?}
    E -->|Yes| F["❌ HTTP 403<br/>Admin access required"]
    E -->|No| G["✅ Execute endpoint"]
    
    D1 -->|Read DB| DB[(PostgreSQL<br/>Query)]
    D2 -->|Read DB| DB
    D3 -->|Read DB| DB
    D4 -->|Read DB| DB
    G -->|Read DB| DB
    
    DB -->|Return Data| RESP["✅ HTTP 200<br/>Data Retrieved"]
    RESP -->|Response| A
    
    F -->|Response| A
    
    style A fill:#2e7d32,color:#fff
    style C fill:#00796b,color:#fff
    style D1 fill:#1565c0,color:#fff
    style D2 fill:#1565c0,color:#fff
    style D3 fill:#0277bd,color:#fff
    style D4 fill:#0277bd,color:#fff
    style E fill:#f57f17,color:#fff
    style G fill:#2e7d32,color:#fff
    style F fill:#c62828,color:#fff
    style DB fill:#1565c0,color:#fff
    style RESP fill:#2e7d32,color:#fff
```

---

## 8. Admin Complete Workflow

```mermaid
graph TB
    subgraph "Admin Actions"
        A1["Create Artist"]
        A2["Update Artist"]
        A3["Delete Artist"]
        S1["Create Song"]
        S2["Update Song"]
        S3["Delete Song"]
    end
    
    subgraph "Database Operations"
        DB1["INSERT INTO artists"]
        DB2["UPDATE artists"]
        DB3["DELETE FROM artists"]
        DB4["INSERT INTO songs"]
        DB5["UPDATE songs"]
        DB6["DELETE FROM songs"]
    end
    
    subgraph "Response"
        R1["Success Response<br/>HTTP 201"]
        R2["Success Response<br/>HTTP 200"]
        R3["Success Response<br/>HTTP 204"]
    end
    
    A1 --> DB1
    A2 --> DB2
    A3 --> DB3
    S1 --> DB4
    S2 --> DB5
    S3 --> DB6
    
    DB1 --> R1
    DB4 --> R1
    
    DB2 --> R2
    DB5 --> R2
    
    DB3 --> R3
    DB6 --> R3
    
    style A1 fill:#d32f2f,color:#fff
    style A2 fill:#d32f2f,color:#fff
    style A3 fill:#b71c1c,color:#fff
    style S1 fill:#d32f2f,color:#fff
    style S2 fill:#d32f2f,color:#fff
    style S3 fill:#b71c1c,color:#fff
    
    style DB1 fill:#1565c0,color:#fff
    style DB2 fill:#1565c0,color:#fff
    style DB3 fill:#01579b,color:#fff
    style DB4 fill:#1565c0,color:#fff
    style DB5 fill:#1565c0,color:#fff
    style DB6 fill:#01579b,color:#fff
    
    style R1 fill:#2e7d32,color:#fff
    style R2 fill:#2e7d32,color:#fff
    style R3 fill:#2e7d32,color:#fff
```

---

## 9. User Complete Workflow

```mermaid
graph TB
    subgraph "User Actions"
        B1["Browse Artists"]
        B2["Browse Songs"]
        S1["Search Artists"]
        S2["Search Songs"]
        ST["Stream Song"]
    end
    
    subgraph "Database Queries"
        Q1["SELECT * FROM artists"]
        Q2["SELECT * FROM songs"]
        Q3["SELECT FROM artists WHERE name ILIKE"]
        Q4["SELECT FROM songs WHERE title ILIKE"]
        Q5["SELECT FROM songs WHERE id=?"]
    end
    
    subgraph "Response"
        R1["Return Artist List<br/>HTTP 200"]
        R2["Return Song List<br/>HTTP 200"]
        R3["Return Search Results<br/>HTTP 200"]
        R4["Return Stream URL<br/>HTTP 200"]
    end
    
    B1 --> Q1
    B2 --> Q2
    S1 --> Q3
    S2 --> Q4
    ST --> Q5
    
    Q1 --> R1
    Q2 --> R2
    Q3 --> R3
    Q4 --> R3
    Q5 --> R4
    
    style B1 fill:#2e7d32,color:#fff
    style B2 fill:#2e7d32,color:#fff
    style S1 fill:#0277bd,color:#fff
    style S2 fill:#0277bd,color:#fff
    style ST fill:#0277bd,color:#fff
    
    style Q1 fill:#1565c0,color:#fff
    style Q2 fill:#1565c0,color:#fff
    style Q3 fill:#1565c0,color:#fff
    style Q4 fill:#1565c0,color:#fff
    style Q5 fill:#1565c0,color:#fff
    
    style R1 fill:#2e7d32,color:#fff
    style R2 fill:#2e7d32,color:#fff
    style R3 fill:#2e7d32,color:#fff
    style R4 fill:#2e7d32,color:#fff
```

---

## 📌 How to View These Diagrams

1. **GitHub:** If you push this to GitHub, Mermaid diagrams render automatically
2. **VS Code:** Install "Markdown Preview Mermaid Support" extension
3. **Online:** Copy any diagram code to [mermaid.live](https://mermaid.live)

## 10. Use Case Diagram - Admin Role

```mermaid
graph TB
    subgraph "Admin User"
        Admin["🔐 Admin User"]
    end
    
    subgraph "Artist Management"
        A1["View All Artists"]
        A2["Create Artist"]
        A3["Update Artist"]
        A4["Delete Artist"]
        A5["Search Artist"]
    end
    
    subgraph "Song Management"
        S1["View All Songs"]
        S2["Create Song"]
        S3["Update Song"]
        S4["Delete Song"]
        S5["Search Song"]
        S6["Stream Song"]
    end
    
    subgraph "Admin Dashboard"
        D1["View Admin Songs"]
        D2["Monitor All Activities"]
    end
    
    Admin --> A1
    Admin --> A2
    Admin --> A3
    Admin --> A4
    Admin --> A5
    Admin --> S1
    Admin --> S2
    Admin --> S3
    Admin --> S4
    Admin --> S5
    Admin --> S6
    Admin --> D1
    Admin --> D2
    
    style Admin fill:#d32f2f,color:#fff
    style A2 fill:#d32f2f,color:#fff
    style A3 fill:#d32f2f,color:#fff
    style A4 fill:#b71c1c,color:#fff
    style S2 fill:#d32f2f,color:#fff
    style S3 fill:#d32f2f,color:#fff
    style S4 fill:#b71c1c,color:#fff
    style D1 fill:#1565c0,color:#fff
    style D2 fill:#1565c0,color:#fff
```

---

## 11. Use Case Diagram - User Role

```mermaid
graph TB
    subgraph "Regular User"
        User["👤 User"]
    end
    
    subgraph "Browse Content"
        B1["View All Artists"]
        B2["View Artist Details"]
        B3["Search Artists"]
        B4["View Artist Songs"]
    end
    
    subgraph "Music Discovery"
        M1["View All Songs"]
        M2["View Song Details"]
        M3["Search Songs"]
        M4["Stream Song"]
    end
    
    User --> B1
    User --> B2
    User --> B3
    User --> B4
    User --> M1
    User --> M2
    User --> M3
    User --> M4
    
    style User fill:#2e7d32,color:#fff
    style B1 fill:#2e7d32,color:#fff
    style B2 fill:#2e7d32,color:#fff
    style B3 fill:#0277bd,color:#fff
    style B4 fill:#2e7d32,color:#fff
    style M1 fill:#2e7d32,color:#fff
    style M2 fill:#2e7d32,color:#fff
    style M3 fill:#0277bd,color:#fff
    style M4 fill:#2e7d32,color:#fff
```

---

## 12. Use Case Diagram - Combined (Admin & User)

```mermaid
graph TB
    subgraph "Actors"
        Admin["🔐 Admin User"]
        User["👤 Regular User"]
    end
    
    subgraph "Artist Operations"
        UC1["View All Artists"]
        UC2["Create Artist<br/>ADMIN ONLY"]
        UC3["Update Artist<br/>ADMIN ONLY"]
        UC4["Delete Artist<br/>ADMIN ONLY"]
        UC5["Search Artists"]
        UC6["Get Artist Songs"]
    end
    
    subgraph "Song Operations"
        UC7["View All Songs"]
        UC8["Create Song<br/>ADMIN ONLY"]
        UC9["Update Song<br/>ADMIN ONLY"]
        UC10["Delete Song<br/>ADMIN ONLY"]
        UC11["Search Songs"]
        UC12["Stream Song"]
    end
    
    subgraph "Admin Only"
        UC13["Admin Dashboard"]
    end
    
    Admin --> UC1
    Admin --> UC2
    Admin --> UC3
    Admin --> UC4
    Admin --> UC5
    Admin --> UC6
    Admin --> UC7
    Admin --> UC8
    Admin --> UC9
    Admin --> UC10
    Admin --> UC11
    Admin --> UC12
    Admin --> UC13
    
    User --> UC1
    User --> UC5
    User --> UC6
    User --> UC7
    User --> UC11
    User --> UC12
    
    style Admin fill:#ffccbc
    style User fill:#c8e6c9
    
    style UC1 fill:#fff9c4
    style UC5 fill:#fff9c4
    style UC6 fill:#fff9c4
    style UC7 fill:#fff9c4
    style UC11 fill:#fff9c4
    style UC12 fill:#fff9c4
    
    style UC2 fill:#ffab91
    style UC3 fill:#ffab91
    style UC4 fill:#ff8a65
    style UC8 fill:#ffab91
    style UC9 fill:#ffab91
    style UC10 fill:#ff8a65
    style UC13 fill:#ffab91
```

---

## 📊 Use Case Summary Table

| Feature | Admin | User |
|---------|-------|------|
| **View Artists** | ✅ | ✅ |
| **Search Artists** | ✅ | ✅ |
| **Create Artist** | ✅ ONLY | ❌ |
| **Update Artist** | ✅ ONLY | ❌ |
| **Delete Artist** | ✅ ONLY | ❌ |
| **View Songs** | ✅ | ✅ |
| **Search Songs** | ✅ | ✅ |
| **Stream Song** | ✅ | ✅ |
| **Create Song** | ✅ ONLY | ❌ |
| **Update Song** | ✅ ONLY | ❌ |
| **Delete Song** | ✅ ONLY | ❌ |
| **Admin Dashboard** | ✅ ONLY | ❌ |

---

## 🎯 What Each Diagram Shows

- **Diagram 1:** How data flows through the entire application
- **Diagram 2:** The layered architecture and component relationships
- **Diagram 3:** Database table relationships
- **Diagram 4:** Step-by-step flow of a create request
- **Diagram 5:** Authorization and role-checking logic
- **Diagram 6:** Admin complete request flow and all accessible endpoints
- **Diagram 7:** User complete request flow and read-only operations
- **Diagram 8:** Admin workflow with all create/update/delete operations
- **Diagram 9:** User workflow with browse/search/stream operations
- **Diagram 10:** Admin use cases and capabilities
- **Diagram 11:** User use cases and capabilities
- **Diagram 12:** Combined view showing differences between admin and user roles
- **Table:** Quick reference for role-based access control
