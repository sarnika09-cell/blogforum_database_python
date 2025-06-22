# Blog/Forum Database Project

A simple command-line application built with Python and SQLite for managing blog posts and comments.

## Features

* User management (view existing users)
* Post management (view all posts, add new posts)
* Comment management (view comments for specific posts)
* Data persistence using SQLite database.
* Interactive command-line interface.

## Technologies Used

* **Python 3:** For the application logic and database interaction.
* **SQLite:** A lightweight, file-based relational database.
* **SQL:** For database definition (DDL) and data manipulation (DML).
* **DB Browser for SQLite:** Used for initial database setup and exploration.
* **Git & GitHub:** For version control and project hosting.

## Setup and Running

1.  **Clone the repository:**
    ```bash
    git clone [https://github.com/sarnika09-cell/blogforum_database_python.git](https://github.com/sarnika09-cell/blogforum_database_python.git)
    ```
2.  **Navigate to the project directory:**
    ```bash
    cd blogforum_database_python
    ```
3.  **Ensure you have Python 3 installed.**
4.  **If the `blog_forum.db` file is not present after cloning (sometimes `.db` files are ignored by default or for size reasons), you might need to create it.** (For this project, it *is* committed, so this step is less likely, but good to know for future projects). If you re-create it, use the `CREATE TABLE` statements from our earlier steps in DB Browser for SQLite.
5.  **Run the application:**
    ```bash
    python3 database_ops.py
    ```
    Follow the on-screen menu prompts.

## Database Schema

(Optional: You can include a simple text representation of your table schemas here)

**Users Table:**
- `user_id` (PK)
- `username`
- `email`
- `password`
- `created_at`

**Posts Table:**
- `post_id` (PK)
- `user_id` (FK to Users)
- `title`
- `content`
- `created_at`

**Comments Table:**
- `comment_id` (PK)
- `post_id` (FK to Posts)
- `user_id` (FK to Users)
- `comment_text`
- `created_at`

## Future Enhancements

* Add features for editing and deleting posts/comments from the CLI.
* Implement user authentication (login/logout).
* Add categories/tags for posts.
* Expand to a web-based application using Flask or Django.
