from fastapi import APIRouter

router = APIRouter(tags=["Products"]) # Etiqueta para la documentación

@router.get("/products")
async def get_products():
    return ["Product 1", "Product 2", "Product 3"]