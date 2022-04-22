# from drf_yasg.utils import no_body, swagger_auto_schema


# def generate_swagger_overrides(prep: str, obj: str,):
#   @swagger_auto_schema(
#     operation_description=f"create {prep} {obj}",
#     operation_summary=f'create {obj}'
#   )
#   def create(self, request, *args, **kwargs):
#     """create method docstring"""
#     return super().create(request, *args, **kwargs)
  
#   @swagger_auto_schema(
#   operation_description=f"list all {obj}s",
#   operation_summary=f'list {obj}s'
#   )
#   def list(self, request, *args, **kwargs):
#     """list method docstring"""
#     return super().list(request, *args, **kwargs)

#   @swagger_auto_schema(
#   operation_description=f"retrieve {prep} {obj}",
#   operation_summary=f'retrieve {obj}'
#   )
#   def retrieve(self, request, *args, **kwargs):
#     """retrieve method docstring"""
#     return super().retrieve(request, *args, **kwargs)

#   @swagger_auto_schema(
#   operation_description=f"update {prep} {obj}",
#   operation_summary=f'update {obj}'
#   )
#   def update(self, request, *args, **kwargs):
#     """update method docstring"""
#     return super().update(request, *args, **kwargs)

#   @swagger_auto_schema(
#   operation_description=f"partial_update {prep} {obj}",
#   operation_summary=f'partial_update {obj}'
#   )
#   def partial_update(self, request, *args, **kwargs):
#     """partial_update method docstring"""
#     return super().partial_update(request, *args, **kwargs)

#   @swagger_auto_schema(
#   operation_description=f"delete {prep} {obj}",
#   operation_summary=f'delete {obj}'
#   )
#   def destroy(self, request, *args, **kwargs):
#     """destroy method docstring"""
#     return super().destroy(request, *args, **kwargs)