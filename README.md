 # 🌌 LEETCODE REALTIME NEXUS API

 > **Next-Generation Asynchronous Telemetry & Live Contest Pipeline for LeetCode**

 \
 [](<https://python.org>)\
 [](<https://fastapi.tiangolo.com>)\
 [](<https://graphql.org>)

---

 ## ⚡ ARCHITECTURAL OVERVIEW

 Traditional LeetCode profile integrations can experience a **5 to 6-day telemetry latency** while official contest ratings, global rankings, and related statistics settle.

 **LeetCode Realtime Nexus** is designed to reduce this delay by executing real-time GraphQL queries against user submission data and cross-referencing problem slugs with active contest problem sets.

 This allows the API to identify **potentially unsettled contest activity** before official contest statistics are fully reflected in the user's profile.

```
                       ┌───────────────────────────────┐
                       │      Client API Request       │
                       └───────────────┬───────────────┘
                                       │
                                       ▼
                       ┌───────────────────────────────┐
                       │   FastAPI Microservice Engine │
                       └───────────────┬───────────────┘
                                       │
            ┌──────────────────────────┴──────────────────────────┐
            ▼                                                     ▼
┌───────────────────────────┐                         ┌───────────────────────────┐
│ Official Ranking History  │                         │  Live Submission Cluster  │
│       (Settled Data)      │                         │   (Unsettled Telemetry)   │
└─────────────┬─────────────┘                         └─────────────┬─────────────┘
              │                                                     │
              └──────────────────────────┬──────────────────────────┘
                                         │
                                         ▼
                         ┌───────────────────────────────┐
                         │   Contest Correlation Engine │
                         └───────────────┬───────────────┘
                                         │
                                         ▼
                         ┌───────────────────────────────┐
                         │   Unified JSON Response      │
                         │           Payload            │
                         └───────────────────────────────┘
```

---

 ## 🛰️ LIVE DEMO & ENDPOINTS

 | Environment | Base Route |
| --- | --- |
| **Production (Render)** | `https://leetcode-api-3g9n.onrender.com/{username}/contest` |
| **Swagger UI Interactive Docs** | `https://leetcode-api-3g9n.onrender.com/docs` |

### 🔍 Quick Test (cURL)

```
curl -X GET "https://leetcode-api-3g9n.onrender.com/neal_wu/contest" \
     -H "accept: application/json"
```

---

 ## ✨ KEY FEATURES

 ### 🛸 Zero-Latency Unsettled Contest Tracking

 Detects recent Weekly/Biweekly contest activity using available submission telemetry before official contest statistics are fully settled.

 ### 🎯 Algorithmic Problem Filtering

 Cross-references `recentAcSubmissionList` with official contest question lists obtained through GraphQL contest queries such as `contest(titleSlug: ...)`.

 This helps distinguish contest-related submissions from ordinary practice activity.

 ### 📊 Unified Telemetry

 Delivers important profile and contest information through a single JSON payload, including:

 - Global ranking
- Contest rating
- Total problems solved
- Contest participation count
- Weekly contest history
- Biweekly contest history
- Solved contest problem titles
- Contest settlement status

 ### 🛡️ Fail-Safe Processing

 If no live contest activity is detected, the system gracefully falls back to available settled contest history.

---

 ## 🧠 REALTIME DETECTION PIPELINE

```
                    ┌─────────────────────────┐
                    │      User Username       │
                    └────────────┬────────────┘
                                 │
                                 ▼
                    ┌─────────────────────────┐
                    │      GraphQL Queries    │
                    └────────────┬────────────┘
                                 │
                ┌────────────────┴────────────────┐
                │                                 │
                ▼                                 ▼
     ┌──────────────────────┐          ┌────────────────────────┐
     │ Official Contest     │          │ Recent Accepted        │
     │ History              │          │ Submissions            │
     └──────────┬───────────┘          └────────────┬───────────┘
                │                                   │
                │                                   ▼
                │                         ┌────────────────────┐
                │                         │ Extract Problem    │
                │                         │ Slugs / Titles     │
                │                         └─────────┬──────────┘
                │                                   │
                └────────────────┬──────────────────┘
                                 │
                                 ▼
                    ┌─────────────────────────┐
                    │ Contest Problem Matching│
                    └────────────┬────────────┘
                                 │
                       ┌─────────┴─────────┐
                       │                   │
                       ▼                   ▼
                Contest Match        No Contest Match
                       │                   │
                       ▼                   ▼
                Live Activity        Practice Activity
                       │
                       ▼
              ┌─────────────────────┐
              │ Unified JSON Output │
              └─────────────────────┘
```

---

 ## 💎 JSON RESPONSE SPECIFICATION

```
{
  "totalProblemsSolved": 2450,
  "totalPlatformContestsAttend": 112,
  "contestRating": 3280,
  "contestGlobalRanking": 3,

  "recentWeeklyContests": [
    {
      "attended": true,
      "rating": 3280,
      "ranking": "Pending (Rating calculation in progress)",
      "problemsSolved": 3,

      "contest": {
        "title": "Weekly Contest 520",
        "startTime": 1789872508
      },

      "status": "Live / Unsettled",

      "solvedProblemTitles": [
        "Maximum Pulse Value After One Subarray Rotation",
        "Number of Intersecting Interval Pairs II",
        "Reverse Degree of a String"
      ]
    },

    {
      "attended": true,
      "rating": 3280,
      "ranking": 1,
      "problemsSolved": 4,

      "contest": {
        "title": "Weekly Contest 519",
        "startTime": 1789266600
      },

      "status": "Official / Settled"
    }
  ],

  "recentBiweeklyContests": [
    {
      "attended": true,
      "rating": 3270,
      "ranking": 2,
      "problemsSolved": 4,

      "contest": {
        "title": "Biweekly Contest 191",
        "startTime": 1789223400
      },

      "status": "Official / Settled"
    }
  ]
}
```

---

 ## 📦 RESPONSE FIELD OVERVIEW

 | Field | Description |
| --- | --- |
| `totalProblemsSolved` | Total number of problems solved |
| `totalPlatformContestsAttend` | Total number of contests attended |
| `contestRating` | Current available contest rating |
| `contestGlobalRanking` | Current available global ranking |
| `recentWeeklyContests` | Recent Weekly Contest telemetry |
| `recentBiweeklyContests` | Recent Biweekly Contest telemetry |
| `attended` | Whether the user attended the contest |
| `rating` | Contest rating associated with the record |
| `ranking` | Official ranking or pending status |
| `problemsSolved` | Number of detected solved contest problems |
| `contest.title` | Contest name |
| `contest.startTime` | Contest start time as Unix timestamp |
| `status` | `Live / Unsettled` or `Official / Settled` |
| `solvedProblemTitles` | Contest problems detected from recent submissions |

---

 ## 🚀 LOCAL DEVELOPMENT SETUP

 ### 1\. Repository Setup

```
git clone https://github.com/newpath-tech/leetcode-api.git
cd leetcode-api
```

 ### 2\. Environment Configuration

 #### Linux / macOS

```
python -m venv venv
source venv/bin/activate
```

 #### Windows

```
python -m venv venv
venv\Scripts\activate
```

 ### 3\. Install Dependencies

```
pip install -r requirements.txt
```

 ### 4\. Server Initialization

```
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

 ### 5\. Open Interactive API Documentation

```
http://localhost:8000/docs
```

---

 ## 🛠️ TECH STACK

```
             ┌───────────────────────┐
             │    FastAPI Engine     │
             └───────────┬───────────┘
                         │
                         ▼
             ┌───────────────────────┐
             │    Uvicorn Server     │
             └───────────┬───────────┘
                         │
                         ▼
             ┌───────────────────────┐
             │   GraphQL Data Layer  │
             └───────────┬───────────┘
                         │
                         ▼
             ┌───────────────────────┐
             │  LeetCode Data APIs   │
             └───────────┬───────────┘
                         │
                         ▼
             ┌───────────────────────┐
             │   Render Cloud Host   │
             └───────────────────────┘
```

 ### Core Technologies

 - 🐍 Python 3.10+
- ⚡ FastAPI
- 🚀 Uvicorn
- 🧬 GraphQL
- ☁️ Render
- 📦 JSON
- 🌐 HTTP API

---

 ## 🔗 API REQUEST FLOW

```
Client
  │
  │ GET /{username}/contest
  ▼
FastAPI
  │
  ▼
GraphQL Queries
  │
  ├───────────────┐
  │               │
  ▼               ▼
Settled Data   Recent Submissions
  │               │
  │               ▼
  │          Problem Filtering
  │               │
  │               ▼
  │       Contest Correlation
  │               │
  └───────┬───────┘
          │
          ▼
    Unified Payload
          │
          ▼
        JSON
```

---

 ## 🌐 PRODUCTION EXAMPLE

 ### Request

```
GET /neal_wu/contest
```

 ### Production URL

```
https://leetcode-api-3g9n.onrender.com/neal_wu/contest
```

 ### Swagger Documentation

```
https://leetcode-api-3g9n.onrender.com/docs
```

---

 ## 📊 CONTEST DATA STATES

```
                    CONTEST DATA
                         │
             ┌───────────┴───────────┐
             │                       │
             ▼                       ▼
       LIVE / UNSETTLED       OFFICIAL / SETTLED
             │                       │
             ▼                       ▼
     Recent Submission        Official Contest
        Telemetry                  History
             │                       │
             ▼                       ▼
     Rating Pending           Rating Available
     Ranking Pending          Ranking Available
             │                       │
             └───────────┬───────────┘
                         │
                         ▼
                 Unified API Output
```

---

 ## 🎯 USE CASES

 LeetCode Realtime Nexus can be integrated into:

 - 📊 Competitive programming dashboards
- 🏆 Contest tracking applications
- 📈 Developer analytics platforms
- 🤖 Discord bots
- 🤖 Telegram bots
- 🌐 Personal developer portfolios
- 📱 Coding profile applications
- 📡 Live contest monitoring tools
- 🔥 Competitive programming communities

---

 ## 🧪 EXAMPLE INTEGRATION

```
                  LEETCODE USER
                        │
                        ▼
              ┌───────────────────┐
              │  REALTIME NEXUS    │
              │       API          │
              └─────────┬─────────┘
                        │
          ┌─────────────┼─────────────┐
          │             │             │
          ▼             ▼             ▼
       Rating        Ranking       Problems
          │             │             │
          └─────────────┼─────────────┘
                        │
                        ▼
              Contest Dashboard
```

---

 ## 🛡️ DATA PROCESSING PHILOSOPHY

```
        RAW LEETCODE TELEMETRY
                  │
                  ▼
             ┌─────────┐
             │ OBSERVE │
             └────┬────┘
                  │
                  ▼
             ┌─────────┐
             │ FILTER  │
             └────┬────┘
                  │
                  ▼
             ┌─────────┐
             │  MATCH  │
             └────┬────┘
                  │
                  ▼
             ┌─────────┐
             │CORRELATE│
             └────┬────┘
                  │
                  ▼
             ┌─────────┐
             │ PROCESS │
             └────┬────┘
                  │
                  ▼
           UNIFIED JSON DATA
```

 > **Observe → Filter → Match → Correlate → Process → Respond**

---

 ## ☁️ DEPLOYMENT ARCHITECTURE

```
                     GitHub Repository
                            │
                            │ Push
                            ▼
                    ┌───────────────┐
                    │     Render    │
                    │    Platform   │
                    └───────┬───────┘
                            │
                            ▼
                    ┌───────────────┐
                    │ Python Runtime│
                    └───────┬───────┘
                            │
                            ▼
                    ┌───────────────┐
                    │    Uvicorn    │
                    └───────┬───────┘
                            │
                            ▼
                    ┌───────────────┐
                    │    FastAPI    │
                    └───────┬───────┘
                            │
                            ▼
                    ┌───────────────┐
                    │   GraphQL     │
                    └───────┬───────┘
                            │
                            ▼
                       JSON API
```

---

 ## 🤝 CONTRIBUTING

 Contributions, improvements, bug reports, and feature ideas are welcome.

```
Fork Repository
      │
      ▼
Clone Repository
      │
      ▼
Create Feature Branch
      │
      ▼
Make Changes
      │
      ▼
Test Locally
      │
      ▼
Commit Changes
      │
      ▼
Push Branch
      │
      ▼
Open Pull Request
```

 ### Example

```
git checkout -b feature/your-feature

git add .

git commit -m "Add your feature"

git push origin feature/your-feature
```

---

 ## 🐛 ISSUES & FEATURE REQUESTS

 Found a bug or have an idea?

 Contributions are welcome in the form of:

 - 🐛 Bug fixes
- ⚡ Performance improvements
- 🧠 Contest detection improvements
- 🔍 Better problem filtering
- 📊 New telemetry fields
- 🧪 Automated tests
- 📚 Documentation improvements
- 💡 New API features

---

 # 👥 CREATORS & CONTRIBUTORS

 ## 🚀 Created By

 ### **Gokul S**

 **GitHub ID:** `newpath-tech`

---

 ## 🤝 Core Contributors

 ### **Nithya Shree P**

 **Role:** Core Contributor

 ### **Yukith Prakash R**

 **Role:** Core Contributor

---

 ## 🌌 PROJECT

```
╔══════════════════════════════════════════════════════════╗
║                                                          ║
║              🌌 LEETCODE REALTIME NEXUS                 ║
║                                                          ║
║       Next-Generation Contest Telemetry API             ║
║                                                          ║
║        ⚡ FastAPI  •  🧬 GraphQL  •  🐍 Python          ║
║                                                          ║
║              📡 REALTIME CONTEST DATA                   ║
║                                                          ║
╚══════════════════════════════════════════════════════════╝
```

 > **Built to bridge the gap between live contest activity and settled LeetCode statistics.**

---

 ## ⭐ SUPPORT THE PROJECT

 If you find this project useful:

 - ⭐ Star the repository
- 🍴 Fork the repository
- 🐛 Report bugs
- 💡 Suggest features
- 🤝 Contribute
- 📢 Share the project

---
### 🌌 LEETCODE REALTIME NEXUS API

 **Realtime Contest Telemetry • GraphQL • FastAPI • Python**

 `Built with ⚡ for Competitive Programming`

