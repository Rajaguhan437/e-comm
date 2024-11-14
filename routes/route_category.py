from fastapi import APIRouter, Depends, HTTPException, Body, Request
from sqlalchemy.orm import Session
from database.database import get_db
from auth.jwt_bearer import JWTBearer
from database.schema import detailsInfo, categoryDetails, subCategoryDetails, editCategoryDetails
from database.model import Details, Category, Sub_Category, User
from auth.jwt_handler import decodeJWT

router = APIRouter(
    prefix="/category",
    tags=["Category"],
    responses={404: {"description": "Not found"}},
)

@router.post(
    "/create/",
    description="Creating a New Category",
    dependencies=[Depends(JWTBearer())]
)
def Create_Category(
    category : categoryDetails ,
    request: Request,
    db: Session = Depends(get_db),
):
    try:
        token = request.headers.get("authorization")[7:]
        payload_dict = decodeJWT(token)

        user_id = payload_dict["user_id"]

        categoryDict = {
            "cat_name" : category.cat_name,
            "created_by": user_id,
            "cat_img": category.cat_img,
            }
        categoryCreate = Category(**categoryDict) 
        
        db.add(categoryCreate)
        db.commit()
        db.refresh(categoryCreate)

        return {"status_code":200, **categoryDict}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    

@router.get(
    "/read/",
    description="Read all items in Category",
    dependencies=[Depends(JWTBearer())]
)
def Read_Category(
    skip: int = 0, 
    limit: int = 100, 
    db: Session = Depends(get_db),
):
    try:
        catDetails = db.query(Category).offset(skip).limit(limit).all()
        return catDetails
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    

@router.put(
    "/edit",
    description="Editing the items in Category",
    dependencies=[Depends(JWTBearer())]
)
def Edit_Category(
    editDetails: editCategoryDetails,
    db: Session = Depends(get_db)
):

    if not data:
        raise HTTPException(
            status_code=400,
            detail="data not found"
        )
    
    if editDetails.cat_name:
        data.cat_name = editDetails.cat_name
    if editDetails.cat_img:
        data.cat_id = editDetails.cat_img
    if editDetails.is_active:
        data.is_active = editDetails.is_active
    
    data = db.query(Category).filter(Category.cat_name == editDetails.cat_name).update(
        {

        }
    )

    db.commit()
    db.refresh(data)
