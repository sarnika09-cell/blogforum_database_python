import sqlite3
import os

# --- Configuration ---
# IMPORTANT: This path should be correct based on your previous successful run.
# It assumes database_ops.py is in the same 'FirstDatabase' folder as blog_forum.db.
database_file = 'blog_forum.db' 

# --- Connection Function ---
def get_db_connection():
    conn = None
    try:
        conn = sqlite3.connect(database_file)
        conn.row_factory = sqlite3.Row # This makes rows behave like dictionaries
        return conn
    except sqlite3.Error as e:
        print(f"Error connecting to database: {e}")
        if not os.path.exists(database_file):
            print(f"'{database_file}' not found. Make sure the path is correct or the file exists.")
        return None

# --- Database Operation Functions ---

def view_all_users(cursor):
    """Fetches and prints all users from the Users table."""
    try:
        cursor.execute("SELECT user_id, username, email FROM Users;")
        users = cursor.fetchall()
        if users:
            print("\n--- All Users ---")
            for user in users:
                print(f"ID: {user['user_id']}, Username: {user['username']}, Email: {user['email']}")
        else:
            print("No users found.")
    except sqlite3.Error as e:
        print(f"Error viewing users: {e}")

def view_all_posts_with_authors(cursor):
    """Fetches and prints all posts with their author's username."""
    try:
        cursor.execute("""
            SELECT P.post_id, P.title, P.content, U.username AS author_username, P.created_at
            FROM Posts AS P
            JOIN Users AS U ON P.user_id = U.user_id
            ORDER BY P.created_at DESC;
        """)
        posts = cursor.fetchall()
        if posts:
            print("\n--- All Posts ---")
            for post in posts:
                print(f"Post ID: {post['post_id']}")
                print(f"Title: {post['title']}")
                print(f"Content: {post['content']}")
                print(f"Author: {post['author_username']}")
                print(f"Posted On: {post['created_at']}")
                print("---")
        else:
            print("No posts found.")
    except sqlite3.Error as e:
        print(f"Error viewing posts: {e}")

def add_new_post(conn, cursor):
    """Prompts user for post details and adds a new post to the database."""
    print("\n--- Add New Post ---")
    title = input("Enter post title: ")
    content = input("Enter post content: ")
    
    # Show available users to help pick an author
    view_all_users(cursor) 
    while True:
        try:
            user_id_str = input("Enter author User ID from the list above: ")
            user_id = int(user_id_str)
            # Basic check if user_id exists
            cursor.execute("SELECT 1 FROM Users WHERE user_id = ?", (user_id,))
            if cursor.fetchone():
                break # Valid user ID
            else:
                print("User ID does not exist. Please enter a valid ID.")
        except ValueError:
            print("Invalid input. Please enter a number for User ID.")
        except sqlite3.Error as e:
            print(f"Database error checking user ID: {e}")
            return # Exit function if serious error

    try:
        cursor.execute("INSERT INTO Posts (user_id, title, content) VALUES (?, ?, ?);",
                       (user_id, title, content))
        conn.commit() # Save changes
        print(f"Post '{title}' added successfully!")
    except sqlite3.Error as e:
        print(f"Error adding post: {e}")
        conn.rollback() # Rollback changes if an error occurs

def view_comments_for_post(cursor):
    """Prompts for a post ID and displays its comments."""
    print("\n--- View Comments for a Post ---")
    # First, list posts to help user choose
    view_all_posts_with_authors(cursor) 
    
    while True:
        try:
            post_id_str = input("Enter the Post ID to view comments for: ")
            post_id = int(post_id_str)
            # Check if post exists
            cursor.execute("SELECT 1 FROM Posts WHERE post_id = ?", (post_id,))
            if cursor.fetchone():
                break # Valid post ID
            else:
                print("Post ID does not exist. Please enter a valid ID.")
        except ValueError:
            print("Invalid input. Please enter a number for Post ID.")
        except sqlite3.Error as e:
            print(f"Database error checking post ID: {e}")
            return # Exit function if serious error

    try:
        cursor.execute("""
            SELECT C.comment_text, U.username AS comment_author, C.created_at
            FROM Comments AS C
            JOIN Users AS U ON C.user_id = U.user_id
            WHERE C.post_id = ?
            ORDER BY C.created_at;
        """, (post_id,))
        comments = cursor.fetchall()
        if comments:
            print(f"\n--- Comments for Post ID {post_id} ---")
            for comment in comments:
                print(f"  Comment: {comment['comment_text']}")
                print(f"  Author: {comment['comment_author']}")
                print(f"  On: {comment['created_at']}")
                print("  ---")
        else:
            print(f"No comments found for Post ID {post_id}.")
    except sqlite3.Error as e:
        print(f"Error viewing comments: {e}")

# --- Main Application Loop ---
def main_menu():
    conn = get_db_connection()
    if conn:
        cursor = conn.cursor()
        while True:
            print("\n===== Blog/Forum Application =====")
            print("1. View All Users")
            print("2. View All Posts")
            print("3. Add New Post")
            print("4. View Comments for a Post")
            print("5. Exit")
            print("==================================")
            
            choice = input("Enter your choice (1-5): ")

            if choice == '1':
                view_all_users(cursor)
            elif choice == '2':
                view_all_posts_with_authors(cursor)
            elif choice == '3':
                add_new_post(conn, cursor)
            elif choice == '4':
                view_comments_for_post(cursor)
            elif choice == '5':
                print("Exiting application. Goodbye!")
                break
            else:
                print("Invalid choice. Please enter a number between 1 and 5.")
        
        conn.close() # Close connection when loop breaks
    else:
        print("Application could not start due to database connection error.")

if __name__ == "__main__":
    main_menu()