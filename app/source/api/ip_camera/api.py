# from .api_settings import PREFIX, Paths
# from fastapi import APIRouter, Depends, status
# from services.lot import ILotService, get_lot_service
# from shared.core.schemas.marketplace.app.lot import *


# router = APIRouter(prefix=PREFIX, tags=["Lots", ])


# @router.put(
#     path=Paths.Create,
#     name="Create Lot",
#     responses={
#         status.HTTP_201_CREATED: {"model": response.CreateLot},
#         status.HTTP_503_SERVICE_UNAVAILABLE: {},
#     },
#     status_code=status.HTTP_201_CREATED,
# )
# async def create_lot(body: bodies.Create, 
#                      service: ILotService = Depends(get_lot_service)) -> response.CreateLot:
#     return await service.create(body)


# @router.get(
#     path=Paths.List,
#     name="List Lot",
#     responses={
#         status.HTTP_200_OK: {"model": response.ListLot}
#     },
#     status_code=status.HTTP_200_OK,
# )
# async def list_lot(query: query.List = Depends(), 
#                    service: ILotService = Depends(get_lot_service)) -> response.ListLot:
#     return await service.list(query)


# @router.get(
#     path=Paths.My,
#     name="Get bought lots",
#     responses={
#         status.HTTP_200_OK: {"model": response.MyBoughtLots}
#     },
#     status_code=status.HTTP_200_OK,
# )
# async def my_bought_lots(query: query.MyBoughtLots = Depends(), 
#                           service: ILotService = Depends(get_lot_service)) -> response.MyBoughtLots:
#     return await service.my_bought_lots(query)


# @router.get(
#     path=Paths.Read,
#     name="Read Lot",
#     responses={
#         status.HTTP_200_OK: {"model": response.ReadLot},
#         status.HTTP_404_NOT_FOUND: {},
#     },
#     status_code=status.HTTP_200_OK,
# )
# async def read_lot(path: path.Read = Depends(),
#                    query: query.Read = Depends(),
#                    service: ILotService = Depends(get_lot_service)) -> response.ReadLot:
#     return await service.read(path, query)


# @router.patch(
#     path=Paths.Update,
#     name="Update Lot",
#     responses={
#         status.HTTP_200_OK: {"model": response.UpdateLot},
#         status.HTTP_403_FORBIDDEN: {},
#         status.HTTP_404_NOT_FOUND: {},
#     },
#     status_code=status.HTTP_200_OK,
# )
# async def update_lot(body: bodies.Update,
#                      path: path.Update = Depends(), 
#                      query: query.Update = Depends(),
#                      service: ILotService = Depends(get_lot_service)) -> response.UpdateLot:
#     return await service.update(path, query, body)


# # @router.delete(
# #     path=Paths.Delete,
# #     name="Delete Lot",
# #     responses={
# #         status.HTTP_204_NO_CONTENT: {},
# #         status.HTTP_403_FORBIDDEN: {},
# #         status.HTTP_404_NOT_FOUND: {},
# #     },
# #     status_code=status.HTTP_204_NO_CONTENT,
# # )
# # async def delete_lot(path: path.Delete = Depends(), 
# #                      query: query.Delete = Depends(),
# #                      service: ILotService = Depends(get_lot_service)):
# #     return await service.delete(path, query)


# @router.post(
#     path=Paths.Buy,
#     name="Buy Lot",
#     responses={
#         status.HTTP_200_OK: {"model": response.BuyLot},
#         status.HTTP_400_BAD_REQUEST: {},
#         status.HTTP_404_NOT_FOUND: {},
#         status.HTTP_503_SERVICE_UNAVAILABLE: {},
#     },
#     status_code=status.HTTP_200_OK,
# )
# async def buy_lot(path: path.Buy = Depends(),
#                   query: query.Buy = Depends(), 
#                   service: ILotService = Depends(get_lot_service)) -> response.BuyLot:
#     return await service.buy(path, query)