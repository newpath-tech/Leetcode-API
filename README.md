# 🌌 LEETCODE REALTIME NEXUS API
> **Next-Generation Asynchronous Telemetry & Live Contest Pipeline for LeetCode**

[![Render Status](https://img.shields.io/badge/Render-Live%20Endpoint-00E5FF?style=for-the-badge&logo=render&logoColor=white)](https://leetcode-api-3g9n.onrender.com/neal_wu/contest)
[![Python Version](https://img.shields.io/badge/Python-3.10%2B-FFD700?style=for-the-badge&logo=python&logoColor=black)](https://python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.100%2B-00C7B7?style=for-the-badge&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com)
[![GraphQL Engine](https://img.shields.io/badge/Data%20Engine-GraphQL-E10098?style=for-the-badge&logo=graphql&logoColor=white)](https://graphql.org)

---

## ⚡ ARCHITECTURAL OVERVIEW

Traditional LeetCode profile integrations suffer from a **5 to 6-day telemetry latency** while official contest ratings, global ranks, and badges settle. 

**LeetCode Realtime Nexus** bypasses this delay entirely. By executing real-time GraphQL queries against user submission logs and cross-referencing problem-slug clusters against active contest problem sets, this API captures **unsettled, live contest submissions in real time**.

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
│     (Settled Data)        │                         │    (Unsettled Telemetry)  │
└─────────────┬─────────────┘                         └─────────────┬─────────────┘
│                                                     │
└──────────────────────────┬──────────────────────────┘
│
▼
┌───────────────────────────────┐
│   Unified JSON Response Payload│
└───────────────────────────────┘


---

## 🛰️ LIVE DEMO & ENDPOINTS

| Environment | Base Route |
| :--- | :--- |
| **Production (Render)** | `https://leetcode-api-3g9n.onrender.com/{username}/contest` |
| **Swagger UI Interactive Docs** | `https://leetcode-api-3g9n.onrender.com/docs` |

### 🔍 Quick Test (cURL)


curl -X GET "[https://leetcode-api-3g9n.onrender.com/neal_wu/contest](https://leetcode-api-3g9n.onrender.com/neal_wu/contest)" \
     -H "accept: application/json"
✨ KEY FEATURES
🛸 Zero-Latency Unsettled Contest Tracking: Immediately detects live Weekly/Biweekly contest activity before LeetCode updates official contest graphs.

🎯 Algorithmic Problem Filtering: Cross-references recentAcSubmissionList with official contest question lists (contest(titleSlug: ...)) to remove non-contest practice problems.

📊 Unified Telemetry: Delivers global rank, rating, total problems solved, and contest participation counts in a single payload.

🛡️ Fail-Safe Processing: Gracefully falls back to settled history if no live contest activity is detected.

💎 JSON RESPONSE SPECIFICATION
JSON
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
🚀 LOCAL DEVELOPMENT SETUP
1. Repository Setup
Bash
git clone [https://github.com/newpath-tech/leetcode-api.git](https://github.com/newpath-tech/leetcode-api.git)
cd leetcode-api
2. Environment Configuration
Bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
3. Server Initialization
Bash
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
Navigate to http://localhost:8000/docs to view the interactive API console.

🛠️ TECH STACK
           [FastAPI Engine]  ────  [Uvicorn Server]
                  │
                  ▼
         [LeetCode GraphQL API]
                  │
                  ▼
         [Render Cloud Platform]
👥 CREATORS & CONTRIBUTORS
Created By
Gokul S — GitHub ID: newpath-tech

Contributors
Nithya Shree P — Core Contributor

Yukith Prakash R — Core Contributor
