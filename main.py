import requests
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="LeetCode Realtime Contest API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

LEETCODE_GRAPHQL_URL = "https://leetcode.com/graphql"

# 1. Main User Query
USER_DATA_QUERY = """
query getLeetCodeUserData($username: String!) {
  matchedUser(username: $username) {
    username
    submitStatsGlobal {
      acSubmissionNum {
        difficulty
        count
      }
    }
  }
  userContestRanking(username: $username) {
    rating
    globalRanking
    attendedContestsCount
  }
  userContestRankingHistory(username: $username) {
    attended
    rating
    ranking
    problemsSolved
    contest {
      title
      startTime
    }
  }
  recentAcSubmissionList(username: $username, limit: 20) {
    id
    title
    titleSlug
    timestamp
  }
}
"""

# 2. Query to fetch official problems for a given contest slug
CONTEST_PROBLEMS_QUERY = """
query getContestDetails($titleSlug: String!) {
  contest(titleSlug: $titleSlug) {
    title
    startTime
    duration
    questions {
      title
      titleSlug
    }
  }
}
"""


def get_contest_questions(contest_slug: str, headers: dict) -> list:
    """Fetch official problem titles for a given contest slug."""
    payload = {
        "query": CONTEST_PROBLEMS_QUERY,
        "variables": {"titleSlug": contest_slug},
    }
    try:
        res = requests.post(
            LEETCODE_GRAPHQL_URL, json=payload, headers=headers, timeout=5
        )
        if res.status_code == 200:
            questions = (
                res.json()
                .get("data", {})
                .get("contest", {})
                .get("questions", [])
            )
            return [q.get("title") for q in questions if q.get("title")]
    except Exception:
        pass
    return []


@app.get("/{username}/contest")
def get_leetcode_contest_data(username: str):
    headers = {
        "Content-Type": "application/json",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
        "Referer": f"https://leetcode.com/{username}/",
    }

    # Fetch User Data
    try:
        response = requests.post(
            LEETCODE_GRAPHQL_URL,
            json={"query": USER_DATA_QUERY, "variables": {"username": username}},
            headers=headers,
            timeout=10,
        )
        if response.status_code != 200:
            raise HTTPException(
                status_code=500, detail="LeetCode service unavailable"
            )

        data = response.json().get("data", {})
    except Exception:
        raise HTTPException(
            status_code=500, detail="Failed to connect to LeetCode"
        )

    matched_user = data.get("matchedUser")
    if not matched_user:
        raise HTTPException(status_code=404, detail="User not found")

    # Extract General Stats
    total_solved = 0
    ac_submissions = matched_user.get("submitStatsGlobal", {}).get(
        "acSubmissionNum", []
    )
    for stat in ac_submissions:
        if stat.get("difficulty") == "All":
            total_solved = stat.get("count", 0)
            break

    contest_ranking = data.get("userContestRanking") or {}
    current_rating = round(contest_ranking.get("rating", 0))
    global_rank = contest_ranking.get("globalRanking", 0)
    total_attended = contest_ranking.get("attendedContestsCount", 0)

    weekly_contests = []
    biweekly_contests = []
    processed_titles = set()

    # Verify latest contest activity against official question titles
    # Example slug format for recent/live contests
    latest_weekly_slug = "weekly-contest-520"
    official_weekly_questions = get_contest_questions(latest_weekly_slug, headers)

    recent_submissions = data.get("recentAcSubmissionList") or []
    recent_titles = [sub["title"] for sub in recent_submissions]

    # Filter recent submissions against official question list
    matched_contest_problems = [
        title for title in recent_titles if title in official_weekly_questions
    ]

    # Prepend unrated live contest data if recent activity matches
    if matched_contest_problems:
        live_contest_obj = {
            "attended": True,
            "rating": current_rating,
            "ranking": "Pending (Rating calculation in progress)",
            "problemsSolved": len(matched_contest_problems),
            "contest": {
                "title": "Weekly Contest 520",
                "startTime": recent_submissions[0]["timestamp"],
            },
            "status": "Live / Unsettled",
            "solvedProblemTitles": matched_contest_problems,
        }
        weekly_contests.append(live_contest_obj)
        processed_titles.add("weekly contest 520")

    # Fill remaining slots with official contest history
    history = data.get("userContestRankingHistory") or []
    for contest_entry in reversed(history):
        if not contest_entry.get("attended"):
            continue

        c_info = contest_entry.get("contest", {})
        title = c_info.get("title", "")
        title_lower = title.lower()

        if title_lower in processed_titles:
            continue

        contest_obj = {
            "attended": True,
            "rating": round(contest_entry.get("rating", 0)),
            "ranking": contest_entry.get("ranking", 0),
            "problemsSolved": contest_entry.get("problemsSolved", 0),
            "contest": {"title": title, "startTime": c_info.get("startTime")},
            "status": "Official / Settled",
        }

        if "weekly" in title_lower and len(weekly_contests) < 2:
            weekly_contests.append(contest_obj)
            processed_titles.add(title_lower)
        elif "biweekly" in title_lower and len(biweekly_contests) < 2:
            biweekly_contests.append(contest_obj)
            processed_titles.add(title_lower)

        if len(weekly_contests) >= 2 and len(biweekly_contests) >= 2:
            break

    return {
        "totalProblemsSolved": total_solved,
        "totalPlatformContestsAttend": total_attended,
        "contestRating": current_rating,
        "contestGlobalRanking": global_rank,
        "recentWeeklyContests": weekly_contests[:2],
        "recentBiweeklyContests": biweekly_contests[:2],
    }