"""
SentimentIQ - Brand Controller
"""

from typing import List
from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from models.user import User
from schemas.brand import BrandCreate, BrandUpdate, Brand
from services.brand_service import BrandService


class BrandController:
    """Controller for brand operations"""

    @staticmethod
    async def get_brand(session: AsyncSession, brand_id: int) -> Brand:
        """Get a brand by ID"""
        brand = await BrandService.get_brand_by_id(session, brand_id)
        if not brand:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Brand not found"
            )
        return Brand.model_validate(brand)

    @staticmethod
    async def get_brands(session: AsyncSession, skip: int = 0, limit: int = 100) -> List[Brand]:
        """Get all brands"""
        brands = await BrandService.get_brands(session, skip, limit)
        return [Brand.model_validate(brand) for brand in brands]

    @staticmethod
    async def create_brand(session: AsyncSession, brand_data: BrandCreate, current_user: User) -> Brand:
        """Create a new brand"""
        # Only superusers can create brands
        if not current_user.is_superuser:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Only administrators can create brands"
            )

        brand = await BrandService.create_brand(session, brand_data)
        return Brand.model_validate(brand)

    @staticmethod
    async def update_brand(session: AsyncSession, brand_id: int, brand_data: BrandUpdate, current_user: User) -> Brand:
        """Update an existing brand"""
        # Only superusers can update brands
        if not current_user.is_superuser:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Only administrators can update brands"
            )

        brand = await BrandService.update_brand(session, brand_id, brand_data)
        if not brand:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Brand not found"
            )
        return Brand.model_validate(brand)

    @staticmethod
    async def delete_brand(session: AsyncSession, brand_id: int, current_user: User) -> dict:
        """Delete a brand"""
        # Only superusers can delete brands
        if not current_user.is_superuser:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Only administrators can delete brands"
            )

        deleted = await BrandService.delete_brand(session, brand_id)
        if not deleted:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Brand not found"
            )
        return {"message": "Brand deleted successfully"}