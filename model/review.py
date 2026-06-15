# Owned By Mohammed
# Optional Review model for rental history and ratings.

from datetime import datetime
from auth.database import get_connection


class Review:
    @staticmethod
    def create(reviewer_email, reviewee_email, booking_id, rating, comment):
        connection = get_connection()
        cursor = connection.cursor()
        cursor.execute("""
            INSERT INTO reviews (reviewer_email, reviewee_email, booking_id, rating, comment, created_at)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (
            reviewer_email,
            reviewee_email,
            booking_id,
            int(rating),
            comment,
            datetime.now().isoformat(timespec="seconds")
        ))
        connection.commit()
        review_id = cursor.lastrowid
        connection.close()
        return review_id
