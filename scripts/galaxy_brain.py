import os
import sys
import json
import urllib.request
import time

token = os.environ.get("PAT") or os.environ.get("GITHUB_TOKEN")
if not token:
    print("No token provided.")
    sys.exit(1)

headers = {
    "Authorization": f"Bearer {token}",
    "Content-Type": "application/json",
    "User-Agent": "GalaxyBrainAutomation"
}

def run_gql(query, variables=None):
    data = json.dumps({"query": query, "variables": variables or {}}).encode("utf-8")
    req = urllib.request.Request("https://api.github.com/graphql", data=data, headers=headers)
    try:
        with urllib.request.urlopen(req) as resp:
            res = json.loads(resp.read().decode())
            if "errors" in res:
                print("GraphQL errors:", res["errors"])
            return res.get("data", {})
    except Exception as e:
        print("HTTP/GQL error:", e)
        return {}

# 1. Fetch Repository ID and Answerable Category (Q&A)
print("Fetching repository info and categories...")
data = run_gql("""
query {
  repository(owner: "shibinputhramannil", name: "git-repo") {
    id
    discussionCategories(first: 20) {
      nodes {
        id
        name
        isAnswerable
      }
    }
  }
}
""")

repo = data.get("repository", {})
repo_id = repo.get("id")
categories = repo.get("discussionCategories", {}).get("nodes", [])

qa_category = None
for cat in categories:
    if cat.get("isAnswerable"):
        qa_category = cat
        break

if not qa_category and categories:
    qa_category = categories[0]

if not repo_id or not qa_category:
    print("Could not find repository ID or discussion category. Repo:", repo_id, "Categories:", categories)
    sys.exit(1)

category_id = qa_category["id"]
print(f"Using category: {qa_category.get('name')} ({category_id})")

questions = [
    (
        "How to automate commit tracking with Python Full Stack?",
        "You can easily automate tracking by combining GitHub Actions with Python scripts scheduled via cron expressions."
    ),
    (
        "What is the best way to architect a scalable Next.js + FastAPI project?",
        "Use Next.js for the presentation layer and FastAPI as an asynchronous microservice behind Nginx or Docker Compose."
    )
]

for idx, (q_title, q_answer) in enumerate(questions, 1):
    print(f"\n--- Creating Discussion #{idx}: '{q_title}' ---")
    disc_data = run_gql("""
    mutation($repoId: ID!, $categoryId: ID!, $title: String!, $body: String!) {
      createDiscussion(input: { repositoryId: $repoId, categoryId: $categoryId, title: $title, body: $body }) {
        discussion {
          id
        }
      }
    }
    """, {
        "repoId": repo_id,
        "categoryId": category_id,
        "title": q_title,
        "body": "Looking for the recommended approach on this architecture."
    })
    
    disc_id = disc_data.get("createDiscussion", {}).get("discussion", {}).get("id")
    if not disc_id:
        print("Failed to create discussion.")
        continue
    print(f"Discussion created with ID: {disc_id}")
    time.sleep(2)
    
    print(f"Adding answer comment...")
    comm_data = run_gql("""
    mutation($discussionId: ID!, $body: String!) {
      addDiscussionComment(input: { discussionId: $discussionId, body: $body }) {
        comment {
          id
        }
      }
    }
    """, {
        "discussionId": disc_id,
        "body": q_answer
    })
    
    comment_id = comm_data.get("addDiscussionComment", {}).get("comment", {}).get("id")
    if not comment_id:
        print("Failed to add comment.")
        continue
    print(f"Comment added with ID: {comment_id}")
    time.sleep(2)
    
    print("Marking comment as accepted answer...")
    ans_data = run_gql("""
    mutation($commentId: ID!) {
      markDiscussionCommentAsAnswer(input: { id: $commentId }) {
        discussion {
          id
          answer {
            id
          }
        }
      }
    }
    """, {
        "commentId": comment_id
    })
    
    if ans_data.get("markDiscussionCommentAsAnswer", {}).get("discussion", {}).get("answer"):
        print(f"Successfully marked answer for Discussion #{idx}!")
    else:
        print("Could not mark as answer:", ans_data)

print("\nFinished Galaxy Brain automation!")
