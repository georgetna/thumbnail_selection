import streamlit as st
import os
import sqlite3
from PIL import Image, ImageDraw, ImageFont
from modules.database import create_connection
from modules.authentication import (
    register_user,
    login_user,
    reset_password,
)


def main():
    # Connect to the database
    conn = create_connection("app.db")
    st.title("Thumbnail Selector")

    # Initialize session state variables
    if "logged_in" not in st.session_state:
        st.session_state.logged_in = False
    if "user_id" not in st.session_state:
        st.session_state.user_id = None

    # Define the menu
    menu = ["Home", "Login", "Register", "Reset Password", "View Thumbnails with Votes"]

    # Determine the default menu choice based on login status
    if st.session_state.logged_in:
        default_index = 0  # "Home"
    else:
        default_index = 1  # "Login"

    # Create the selectbox without a conflicting key
    choice = st.sidebar.selectbox("Menu", menu, index=default_index)

    # Handle navigation
    if st.session_state.logged_in and choice in ["Login", "Register"]:
        choice = "Home"

    if choice == "Home":
        if st.session_state.logged_in:
            thumbnail_selection(conn)
        else:
            st.warning("Please log in to continue.")
    elif choice == "Login":
        if st.session_state.logged_in:
            st.warning("You are already logged in.")
            st.rerun()
        else:
            login(conn)
    elif choice == "Register":
        if st.session_state.logged_in:
            st.warning("You are already logged in.")
            st.rerun()
        else:
            register(conn)
    elif choice == "Reset Password":
        reset_password_screen(conn)
    elif choice == "View Thumbnails with Votes":
        if st.session_state.logged_in:
            view_thumbnails_with_votes(conn)
        else:
            st.warning("Please log in to continue.")


def login(conn):
    st.subheader("Login")

    username = st.text_input("Username", key="login_username")
    password = st.text_input("Password", type="password", key="login_password")

    if st.button("Login"):
        user = login_user(conn, username, password)

        if user:
            st.success(f"Logged in as {username}")
            st.session_state.logged_in = True
            st.session_state.user_id = user[0]
            st.rerun()
        else:
            st.error("Incorrect username or password")


def register(conn):
    st.subheader("Register")

    username = st.text_input("Username", key="register_username")
    email = st.text_input("Email", key="register_email")
    password = st.text_input("Password", type="password", key="register_password")
    confirm_password = st.text_input(
        "Confirm Password", type="password", key="register_confirm_password"
    )

    if st.button("Register"):
        if password == confirm_password:
            success = register_user(conn, username, email, password)
            if success:
                st.success("Registration successful")
                st.session_state.logged_in = True
                # Retrieve user ID
                c = conn.cursor()
                c.execute("SELECT user_id FROM users WHERE username = ?", (username,))
                st.session_state.user_id = c.fetchone()[0]
                st.rerun()
            else:
                st.error("Username or email already exists")
        else:
            st.error("Passwords do not match")


def reset_password_screen(conn):
    st.subheader("Reset Password")

    email = st.text_input("Enter your registered email")

    if st.button("Reset Password"):
        success = reset_password(conn, email)
        if success:
            st.success(
                "Password reset successfully! Check your email for the new password."
            )
        else:
            st.error("Email not found.")


# def thumbnail_selection(conn):
#     st.subheader("Select the Best Thumbnail")

#     c = conn.cursor()
#     user_id = st.session_state.user_id

#     # Get the count of thumbnails selected by the user
#     c.execute("SELECT COUNT(*) FROM votes WHERE user_id = ?", (user_id,))
#     thumbnails_selected = c.fetchone()[0]
#     st.sidebar.write(f"Thumbnails Selected: {thumbnails_selected}")

#     # Check if video and tag are already stored in session_state
#     if "current_video" not in st.session_state or "current_tag" not in st.session_state:
#         # Query to find a video-tag combination the user hasn't seen
#         c.execute(
#             """
#             SELECT v.video_id, v.title, t.tag_id, t.tag_name
#             FROM videos v
#             JOIN videotags vt ON v.video_id = vt.video_id
#             JOIN tags t ON vt.tag_id = t.tag_id
#             WHERE NOT EXISTS (
#                 SELECT 1 FROM votes vo
#                 WHERE vo.user_id = ? AND vo.video_id = v.video_id AND vo.tag_id = t.tag_id
#             )
#             ORDER BY RANDOM()
#             LIMIT 1
#         """,
#             (user_id,),
#         )

#         result = c.fetchone()

#         if result:
#             video_id, video_title, tag_id, tag_name = result
#             # Store in session_state
#             st.session_state["current_video"] = {
#                 "video_id": video_id,
#                 "video_title": video_title,
#             }
#             st.session_state["current_tag"] = {"tag_id": tag_id, "tag_name": tag_name}
#         else:
#             st.info("You have completed all available video-tag combinations.")
#             return  # Exit the function since there's nothing to display

#     else:
#         # Retrieve from session_state
#         video_id = st.session_state["current_video"]["video_id"]
#         video_title = st.session_state["current_video"]["video_title"]
#         tag_id = st.session_state["current_tag"]["tag_id"]
#         tag_name = st.session_state["current_tag"]["tag_name"]

#     st.write(f"**Video Title:** {video_title}")
#     st.write(f"**Keyword:** {tag_name}")

#     # Load thumbnails for the selected video, limit to 10
#     c.execute(
#         "SELECT thumbnail_id, thumbnail_path FROM thumbnails WHERE video_id = ? LIMIT 10",
#         (video_id,),
#     )
#     thumbnails_data = c.fetchall()
#     thumbnails = [(data[0], data[1]) for data in thumbnails_data]

#     if thumbnails:
#         # Display thumbnails in a grid
#         num_columns = 3  # Adjust the number of columns as needed
#         cols = st.columns(num_columns)

#         # Initialize selected_thumbnail_id
#         selected_thumbnail_id = None

#         for idx, (thumbnail_id, thumbnail_path) in enumerate(thumbnails):
#             image = Image.open(thumbnail_path)
#             col = cols[idx % num_columns]
#             with col:
#                 # Make thumbnails bigger
#                 st.image(image, use_column_width=True)
#                 # Use a button to select the thumbnail
#                 if st.button("Select", key=f"select_{thumbnail_id}_{tag_id}"):
#                     selected_thumbnail_id = thumbnail_id
#                     # Save the selection to the database
#                     c.execute(
#                         "INSERT INTO votes (user_id, video_id, thumbnail_id, tag_id) VALUES (?, ?, ?, ?)",
#                         (user_id, video_id, selected_thumbnail_id, tag_id),
#                     )
#                     conn.commit()
#                     st.success("Selection saved!")
#                     # Reset the selected thumbnail and current video/tag
#                     st.session_state.pop("current_video", None)
#                     st.session_state.pop("current_tag", None)
#                     # Rerun to load the next video-tag combination
#                     st.rerun()
#                 # No need to indicate selection since we move on immediately

#     else:
#         st.warning("No thumbnails available for this video.")
#         if st.button("Skip"):
#             # Reset current video/tag and load a new one
#             st.session_state.pop("current_video", None)
#             st.session_state.pop("current_tag", None)
#             st.rerun()


def thumbnail_selection(conn):
    st.subheader("Select the Best Thumbnail")

    c = conn.cursor()
    user_id = st.session_state.user_id

    # Get the count of thumbnails selected by the user
    c.execute("SELECT COUNT(*) FROM votes WHERE user_id = ?", (user_id,))
    thumbnails_selected = c.fetchone()[0]
    st.sidebar.write(f"Thumbnails Selected: {thumbnails_selected}")

    # Add a slider to select the number of thumbnails to show
    num_thumbnails = st.slider(
        "Number of Thumbnails to Display", min_value=3, max_value=50, value=10
    )

    # Check if video and tag are already stored in session_state
    if "current_video" not in st.session_state or "current_tag" not in st.session_state:
        # Query to find a video-tag combination the user hasn't seen
        c.execute(
            """
            SELECT v.video_id, v.title, t.tag_id, t.tag_name
            FROM videos v
            JOIN videotags vt ON v.video_id = vt.video_id
            JOIN tags t ON vt.tag_id = t.tag_id
            WHERE NOT EXISTS (
                SELECT 1 FROM votes vo
                WHERE vo.user_id = ? AND vo.video_id = v.video_id AND vo.tag_id = t.tag_id
            )
            ORDER BY RANDOM()
            LIMIT 1
        """,
            (user_id,),
        )

        result = c.fetchone()

        if result:
            video_id, video_title, tag_id, tag_name = result
            # Store in session_state
            st.session_state["current_video"] = {
                "video_id": video_id,
                "video_title": video_title,
            }
            st.session_state["current_tag"] = {"tag_id": tag_id, "tag_name": tag_name}
        else:
            st.info("You have completed all available video-tag combinations.")
            return  # Exit the function since there's nothing to display

    else:
        # Retrieve from session_state
        video_id = st.session_state["current_video"]["video_id"]
        video_title = st.session_state["current_video"]["video_title"]
        tag_id = st.session_state["current_tag"]["tag_id"]
        tag_name = st.session_state["current_tag"]["tag_name"]

    st.write(f"**Video Title:** {video_title}")
    st.write(f"**Keyword:** {tag_name}")

    # Load thumbnails for the selected video, limit based on slider value
    c.execute(
        "SELECT thumbnail_id, thumbnail_path FROM thumbnails WHERE video_id = ? LIMIT ?",
        (video_id, num_thumbnails),
    )
    thumbnails_data = c.fetchall()
    thumbnails = [(data[0], data[1]) for data in thumbnails_data]

    if thumbnails:
        # Display thumbnails in a grid
        num_columns = 3  # Adjust the number of columns as needed
        cols = st.columns(num_columns)

        # Initialize selected_thumbnail_id
        selected_thumbnail_id = None

        for idx, (thumbnail_id, thumbnail_path) in enumerate(thumbnails):
            image = Image.open(thumbnail_path)
            col = cols[idx % num_columns]
            with col:
                # Make thumbnails bigger
                st.image(image, use_column_width=True)
                # Use a button to select the thumbnail
                if st.button("Select", key=f"select_{thumbnail_id}_{tag_id}"):
                    selected_thumbnail_id = thumbnail_id
                    # Save the selection to the database
                    c.execute(
                        "INSERT INTO votes (user_id, video_id, thumbnail_id, tag_id) VALUES (?, ?, ?, ?)",
                        (user_id, video_id, selected_thumbnail_id, tag_id),
                    )
                    conn.commit()
                    st.success("Selection saved!")
                    # Reset the selected thumbnail and current video/tag
                    st.session_state.pop("current_video", None)
                    st.session_state.pop("current_tag", None)
                    # Rerun to load the next video-tag combination
                    st.rerun()
                # No need to indicate selection since we move on immediately

    else:
        st.warning("No thumbnails available for this video.")
        if st.button("Skip"):
            # Reset current video/tag and load a new one
            st.session_state.pop("current_video", None)
            st.session_state.pop("current_tag", None)
            st.rerun()


# New function to view thumbnails with votes
def view_thumbnails_with_votes(conn):
    st.subheader("View Thumbnails and Their Votes")

    c = conn.cursor()

    # Fetch all available videos
    c.execute("SELECT video_id, title FROM videos")
    videos = c.fetchall()

    # Select a video
    video_choice = st.selectbox("Select a Video", videos, format_func=lambda x: x[1])

    if video_choice:
        video_id = video_choice[0]

        # Fetch associated tags for the selected video
        c.execute(
            "SELECT t.tag_id, t.tag_name FROM tags t JOIN videotags vt ON t.tag_id = vt.tag_id WHERE vt.video_id = ?",
            (video_id,),
        )
        tags = c.fetchall()

        # Select a tag
        tag_choice = st.selectbox("Select a Tag", tags, format_func=lambda x: x[1])

        if tag_choice:
            tag_id = tag_choice[0]

            # Fetch top 5 thumbnails by number of votes
            c.execute(
                """
                SELECT th.thumbnail_path, COUNT(v.vote_id) as vote_count
                FROM thumbnails th
                LEFT JOIN votes v ON th.thumbnail_id = v.thumbnail_id
                WHERE th.video_id = ? AND v.tag_id = ?
                GROUP BY th.thumbnail_id
                ORDER BY vote_count DESC
                LIMIT 5
                """,
                (video_id, tag_id),
            )
            top_thumbnails = c.fetchall()

            # Display the top 5 thumbnails with the vote count overlaid
            if top_thumbnails:
                cols = st.columns(5)
                for idx, (thumbnail_path, vote_count) in enumerate(top_thumbnails):
                    image = Image.open(thumbnail_path)

                    # Overlay vote count on the image
                    image_with_votes = overlay_vote_count(image, vote_count)

                    # Display the image with votes overlaid
                    with cols[idx]:
                        st.image(image_with_votes, use_column_width=True)
                        st.write(f"Votes: {vote_count}")
            else:
                st.warning("No thumbnails found for the selected video and tag.")


def overlay_vote_count(image, vote_count):
    # Overlay the vote count on the image
    draw = ImageDraw.Draw(image)
    font = ImageFont.load_default()
    text = f"Votes: {vote_count}"
    text_size = draw.textsize(text, font)
    position = (image.width - text_size[0] - 10, 10)  # Top-right corner
    draw.text(position, text, fill="white", font=font)
    return image


if __name__ == "__main__":
    main()
