from typing import Dict, Any, Tuple, Type, Optional, List, TypedDict

from django.conf import settings
from django.db.models.query import QuerySet
from django.db import models


# TODO records_per_pageはsettingsから取得

class Pagination(TypedDict):
    result_list: List[Any]
    has_next: bool

class PaginationHandlerMixin():

    def get_current_pagination(
        self, 
        model_class: Type[models.Model],
        query: Dict[str, Any],
        records_per_page: int,
        order: Optional[Tuple[str]]
    ) -> Pagination:
        

        result_query = model_class.objects.filter(**query)

        if order:
            result_query = result_query.order_by(*order)

        result_list = list(result_query)[:records_per_page+1]

        return {
            'result_list': result_list[:records_per_page],
            'has_next': self._exists_next(result_list, records_per_page),
        }

    def _exists_next(self, records: List[Any], records_per_page: int) -> bool:

        return len(records) > records_per_page