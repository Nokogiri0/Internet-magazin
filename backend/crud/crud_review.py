from backend.db.base import CRUDBase
from backend.core.config import settings
from backend.models.products import Review


class CRUDReview(CRUDBase):
    def has_review(self, user_id: int, product_id: int):
        return self.db.query(Review).filter(Review.user_id == user_id and Review.product_id == product_id).first()

    def create_review(self, user_id: int, product_id: int, description: str, rating: int):
        review = Review(user_id=user_id, product_id=product_id,
                        description=description, rating=rating)
        return self.create(review)

    def get_review_by_id(self, review_id: int) -> Review:
        return self.get(model=Review, id=review_id)

    def delete_review(self, review: Review):
        self.delete(review)

    def edit_review(self, review: Review, description: str, rating: int):
        review.description = description
        review.rating = rating
        return self.update(review)

    def get_reviews_by_user_id(self, user_id: int, page: int, page_size: int = settings.REVIEWS_PER_PAGE):
        end = page * page_size
        return self.db.query(Review).filter(Review.user_id == user_id).slice(end-page_size, end).all()

    def get_last_product_reviews(self, product_id: int, page: int, page_size: int = settings.REVIEWS_PER_PAGE):
        end = page * page_size
        return self.db.query(Review).filter(Review.product_id == product_id).order_by(Review.time_created.desc()).slice(end-page_size, end).all()
